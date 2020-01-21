import datetime
import enum

from background_task.models import CompletedTask
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, Q
from django.db import connection, models

from Courses.models import Course
from django.utils import timezone
from users.models import CustomUser

from datetime import date


def due_time():
    return timezone.now() + timezone.timedelta(days=6)


class FAQ(models.Model):
    question = models.CharField(max_length=2000)
    response = models.CharField(max_length=5000)
    is_wefaq = models.BooleanField(default=False)
    is_fifty_percent_faq = models.BooleanField(default=False)

    @classmethod
    def wefaq_is_visible_for(cls, user, weps):
        if user.is_authenticated:
            wep = weps.objects.filter(user=user)
            if wep.exists():
                if wep[0].wework_set.all().count() > 20:
                    return True
        return False

    class Meta:
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class FullTimePostion(models.Model):
    job_title = models.CharField(max_length=200)
    requirement = models.CharField(max_length=500)
    responsibility = models.TextField()
    required_technology = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True)
    weight = models.IntegerField(unique=True, null=True)
    interested_page = models.CharField(max_length=500, default="home:userinterest")
    not_interested_page = models.CharField(max_length=500, default="home:jobfeed")
    skilled_page = models.CharField(max_length=500, default="home:workexperience")

    def __str__(self):
        return '%s' % self.job_title


class PartTimePostion(models.Model):
    job_title = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.job_title


class CompleteClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default="-")
    slug = models.CharField(max_length=200)
    rating_point = models.IntegerField(default=5)
    rating_total = models.CharField(default="2673", max_length=200)
    description = models.TextField()
    about = models.TextField()
    prerequisite = models.TextField()
    fee = models.CharField(max_length=200, default="1,225.00")
    pay_url = models.CharField(max_length=200)
    show_on_footer = models.IntegerField(default=1, choices=((0, 'No'), (1, 'Yes')))
    due_date = models.DateTimeField(default=timezone.now)

    @property
    def is_past_due(self):
        return date.today() > self.due_date

    def __str__(self):
        return self.title


class CompleteClassLearn(models.Model):
    description = models.TextField()
    weight = models.IntegerField()
    completeclass = models.ForeignKey(CompleteClass, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('weight', 'completeclass'),)


class CompleteClassCertificate(models.Model):
    url_of_image = models.TextField()
    weight = models.IntegerField()
    completeclass = models.ForeignKey(CompleteClass, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('weight', 'completeclass'),)

    def __str__(self):
        return self.completeclass.title


class Job(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    position = models.ForeignKey(FullTimePostion, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume', null=True)
    cv_link = models.CharField(max_length=200, null=True)
    interest = models.CharField(max_length=200, null=True, blank=True, default="")
    application_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.fullname


class PartTimeJob(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    cv = models.FileField(upload_to='resume', null=True)
    cv_link = models.CharField(max_length=200, null=True)
    position = models.ForeignKey(PartTimePostion, on_delete=models.CASCADE)
    high_salary = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    application_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


def content_file_name(instance, filename):
    return os.path.join('uploads', 'resumes', instance.user.username + '_' + filename)


class Jobplacement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1)
    education = models.CharField(max_length=70)
    career = models.CharField(max_length=100)
    resume = models.FileField(upload_to=content_file_name)
    placement_grade = models.PositiveSmallIntegerField(default=0)
    experience = models.IntegerField(default=0)
    is_certified = models.CharField(max_length=50)
    training = models.CharField(max_length=50)
    can_relocate = models.CharField(max_length=50)
    awareness = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name_plural = 'Jobplacement Applications'

    def __str__(self):
        return self.user.email


class UserPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments',
                             related_query_name='payment')
    amount = models.IntegerField(default=0)
    trans_id = models.CharField(max_length=100)
    pay_for = models.CharField(max_length=100)
    paid_at = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name_plural = 'User Payments'

    def __str__(self):
        return self.user.username + ' ' + self.pay_for + '_' + self.trans_id


class Groupclass(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    price = models.IntegerField(default=0)
    class_meet = models.CharField(max_length=50)
    type_of_class = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now, null=False)
    video_required = models.BooleanField(default=False)
    users = models.ManyToManyField(CustomUser, blank=True)
    description = models.TextField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


# To-do Unmap this model
class GroupClassRegister(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_paid = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    type_of_class = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.user.email


class StripePayment(models.Model):
    secretkey = models.TextField()
    publickey = models.TextField()
    planid = models.TextField()

    def __str__(self):
        return self.secretkey


class BillingHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    subscription_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.user.email


class ContactMessages(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_no = models.CharField(max_length=20)
    message_subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'ContactMessages'

    def __str__(self):
        return self.subject


class Document(models.Model):
    document = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class MainModel(models.Model):
    title = models.CharField(max_length=42)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class AwsCredential(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    accesskey = models.CharField(max_length=200)
    secretkey = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.user.username


class Internship(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    Address = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    experience = models.CharField(max_length=50)
    course = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resume')
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Resume(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume')

    def __str__(self):
        return self.user.username


class TryFreeRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    paid_date = models.DateTimeField(default=timezone.now, null=False)
    webhook_response = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.username


class UserOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=50)
    order_amount = models.IntegerField(default=0)
    subscription = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    paid_date = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name_plural = "User Orders"

    def __str__(self):
        return self.user.email


class RHCSAOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    membership_plan = models.CharField(max_length=20)
    order_amount = models.IntegerField(default=0)
    transaction_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "RHCSA Orders"

    def __str__(self):
        return self.transaction_id


class MessageGroup(models.Model):
    group = models.CharField(max_length=250)

    def __str__(self):
        return self.group


class Message(models.Model):
    title = models.CharField(max_length=250)
    sender_name = models.CharField(max_length=255, null=True)
    message = models.TextField()
    slug = models.SlugField(max_length=40)
    group = models.ForeignKey(MessageGroup, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.slug


TARGETS = (
    (0, 'all role 6'),
    (1, 'all role 4'),
    (2, 'Nigerian Interns'),
    (3, 'Parttime Fresh Graduate'),
    (4, 'Marketing Internship'),
)


class Campaign(models.Model):
    message = models.ForeignKey(Message, default=1, on_delete=models.CASCADE)
    Target = models.PositiveSmallIntegerField(default=1, choices=TARGETS)
    send_message = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.message.title


class NewsLetterSubscribers(models.Model):
    email = models.EmailField(max_length=200)


class Unsubscriber(models.Model):
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.email


class UserLocation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ipaddress = models.CharField(max_length=50)
    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=20, blank=True)
    longtitude = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.user.email


class FreeAccountClick(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    filled_jobs = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    tryfreeclick = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    freeaccountclick = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    from_what_page = models.CharField(max_length=100, blank=True)
    registered = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    visited_tryfree = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    paid = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    date_created = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.email


class wetype(models.Model):
    types = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.types


class werole(models.Model):
    roles = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.roles


class WorkExperiencePay(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    includes_job_placement = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.email


WORKEXPERIENCE_OPTIONS = (
    (0, 'A citizen of the united states'),
    (1, 'A non national citizen of the united states'),
    (2, 'A lawful permanent resident'),
    (3, 'An alien authorized to work'),
)


class WorkExperienceEligibility(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    middle_initial = models.CharField(max_length=200, null=True)
    middle_name = models.CharField(max_length=200, null=True)
    address = models.TextField()
    apt_number = models.TextField()
    city = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateTimeField(default=timezone.now, null=True)
    SSN = models.TextField()
    ssn_last_four = models.CharField(max_length=255,null=True,default='',blank=True)
    ssn_first_five = models.CharField(max_length=255,null=True,default='',blank=True)
    is_encrypted = models.BooleanField(default=False)
    employee_address = models.TextField()
    employee_email = models.TextField()
    employee_phone = models.CharField(max_length=50, null=True)
    expiry_date = models.DateTimeField(default=timezone.now, null=True)
    preparer_or_translator = models.BooleanField(default=False)
    i_am_a = models.IntegerField(default=0, choices=WORKEXPERIENCE_OPTIONS)
    Alien_reg_num = models.TextField(null=True)
    form_19_num = models.TextField(null=True)
    foreign_pass_num = models.TextField(null=True)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.email

    def transform_ssn(self):
        if not self.SSN:
            # self.ssn_first_five = self.SSN[:5]
            self.SSN = self.ssn_first_five.__str__() + self.ssn_last_four.__str__()
        self.ssn_last_four = self.SSN[5:]

    def save(self, *args, **kwargs):
        from .mail_service import LinuxjobberMailer
        from .views import ADMIN_EMAIL
        new_mail_message = """
A new SSN has been added to the database, go to https://linuxjobber.com/admin to encrypt
                            """

        if not self.pk:
            mailer = LinuxjobberMailer(
                subject="SSN Added",
                to_address=ADMIN_EMAIL,
                header_text="Linuxjobber Notifications",
                type=None,
                message=new_mail_message
            )
            mailer.send_mail()

        if self.SSN and not self.is_encrypted:
            self.transform_ssn()

        # elif not self.is_encrypted and self.pk:
        #     new_mail_message = "SSN data has been decrypted, ensure to encrypt back"
        #     mailer = LinuxjobberMailer(
        #         subject="SSN Decrypted",
        #         to_address=ADMIN_EMAIL,
        #         header_text="Linuxjobber Notifications",
        #         type=None,

        #         message=new_mail_message
        #     )
        #     mailer.send_mail()
        #
        # elif self.is_encrypted and self.pk:
        #     new_mail_message = "SSN data has been encrypted back, ensure to encrypt back"
        #     mailer = LinuxjobberMailer(
        #         subject="SSN Encrypted",
        #         to_address=ADMIN_EMAIL,
        #         header_text="Linuxjobber Notifications",
        #         type=None,
        #         message=new_mail_message
        #     )
        #     mailer.send_mail()
        super(type(self), self).save(*args, **kwargs)





class WorkExperienceIsa(models.Model):
    email = models.TextField(default='')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    current_annual_income = models.TextField(null=True)
    monthly_house_payment = models.TextField(null=True)
    highest_level_education = models.TextField(null=True)
    employment_status = models.TextField(null=True)
    estimated_date_of_program_completion = models.DateTimeField(default=timezone.now, null=True)
    is_signed_isa = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class WorkExperiencePriceWaiver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    price = models.CharField(max_length=200, default="0")
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class wepeoples(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='resume', null=True)
    person = models.ForeignKey(werole, on_delete=models.CASCADE, null=True)
    current_position = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    income = models.CharField(max_length=20, null=True)
    relocation = models.CharField(max_length=5, null=True)
    Paystub = models.ImageField(upload_to='resume', null=True)
    last_verification = models.DateTimeField(default=timezone.now, null=True)
    start_date = models.DateTimeField(default=timezone.now, null=True)
    graduation_date = models.DateTimeField(default=timezone.now, null=True)
    types = models.ForeignKey(wetype, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.email


class wetask(models.Model):
    weight = models.IntegerField(null=True)
    task = models.CharField(max_length=500, null=True)
    objective = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now, null=False)
    is_active = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    types = models.ForeignKey(wetype, on_delete=models.CASCADE)
    group = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('types', 'weight'),)
        ordering = (('types', 'weight'))

    def __str__(self):
        return self.task


class wework(models.Model):
    weight = models.IntegerField(null=True)
    we_people = models.ForeignKey(wepeoples, on_delete=models.CASCADE)
    task = models.ForeignKey(wetask, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, choices=((0, 'Pending'), (1, 'Done')))
    created = models.DateTimeField(default=timezone.now, null=True)
    send_task = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    due = models.DateTimeField(default=due_time)

    class Meta:
        unique_together = (('we_people', 'weight'),)
        ordering = (('we_people', 'weight'))

    def __str__(self):
        return self.we_people.user.email


class GroupClassLog(models.Model):
    group = models.ForeignKey(Groupclass, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now=True)

    def get_log(group_id):
        data = {}
        from datetime import datetime, timedelta
        current_day = datetime.now().strftime('%A')
        range = None
        if current_day == "Monday":
            range = datetime.now() - timedelta(days=5)
        else:
            range = datetime.now() - timedelta(days=3)
        list = GroupClassLog.objects.filter(group=group_id, last_login__gte=range).order_by('-last_login')
        for i in list:
            data.setdefault(i.last_login.strftime('%D'), [])
            data[i.last_login.strftime('%D')].append({'username': i.user.username, 'id': i.user.id})
        return data


class InternshipDetail(models.Model):
    date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return str(self.date.date())


class CareerSwitchApplication(models.Model):
    """
        Author  : Azeem Animashaun
        Career Switch Page enables us to capture information of people who need to switch jobs
    """
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    old_career = models.CharField(max_length=255)
    new_career = models.ForeignKey(FullTimePostion, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume', null=True)
    cv_link = models.CharField(max_length=200, null=True)
    application_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.fullname


class Certificates(models.Model):
    graduate_id = models.CharField(max_length=200, unique=True)
    graduate_name = models.CharField(max_length=250)
    graduate_email = models.CharField(max_length=200)
    graduation_date = models.CharField(max_length=200)
    technology_learnt = models.CharField(max_length=200)
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.graduate_name


class EmailMessageType(models.Model):
    """
    Defines the type of message format

    header_format: {} from Linuxjobber
    """
    type = models.CharField(max_length=255)
    is_default = models.BooleanField()
    header_format = models.CharField(max_length=255, default="", null=True)

    def save(self, *args, **kwargs):
        """
        Sets default message format to be used
        :param args:
        :param kwargs:
        :return:
        """
        if self.is_default:
            type_list = type(self).objects.filter(is_default=True)
            if self.pk:
                type_list.exclude(self)
            type_list.update(is_default=False)
        super(type(self), self).save(*args, **kwargs)

    def __str__(self):
        return "{} - [{}]".format(
            self.type,
            self.header_format
        )


class EmailMessageLog(models.Model):
    header_text = models.CharField(max_length=255, default="Linuxjobber")
    message_type = models.ForeignKey(EmailMessageType, on_delete=models.CASCADE, null=True)
    to_address = models.CharField(max_length=255, default="", blank=True)
    subject = models.CharField(max_length=500, default="", blank=True)
    content = models.TextField(default="", blank=True)
    has_sent = models.BooleanField(default=False)
    group_log = models.ForeignKey('EmailGroupMessageLog', null=True, blank=True, on_delete=models.CASCADE)
    error_message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return "{} - [{}]".format(
            self.subject,
            self.to_address
        )

    def set_as_sent(self):
        self.has_sent = True
        self.error_message = ""
        self.save()

    def set_as_fail(self, error=""):
        self.error_message = error
        self.has_sent = False
        self.save()

    def format_mail(self):
        if self.message_type:
            header_format = self.message_type.header_format
        else:
            try:
                if not self.header_text:
                    self.message_type = EmailMessageType.objects.get(is_default=True)
                    header_format = EmailMessageType.objects.get(is_default=True).header_format
                else:
                    self.message_type = EmailMessageType.objects.get(type='custom')
                    header_format = self.message_type.header_format
            except Exception as e:
                print(e)
                header_format = "{}"
        self.header_text = header_format.format(self.header_text)

    def send_mail(self):
        self.format_mail()
        from .mail_service import send_mail_with_client
        try:
            send_mail_with_client(self)
            self.set_as_sent()
        except Exception as error:
            self.set_as_fail(error.__str__())

    def save(self, *args, **kwargs):
        """
        Sets paid_on date
        :param args:
        :param kwargs:
        :return:
        """
        self.format_mail()
        super(type(self), self).save(*args, **kwargs)


class SubPayment(models.Model):
    amount = models.FloatField()
    description = models.CharField(max_length=255, null=True)
    installment = models.ForeignKey("InstallmentPlan", on_delete=models.CASCADE, null=True)
    due_in = models.IntegerField(default=1, )
    is_initial = models.BooleanField(default=False, )
    is_paid = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    paid_on = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return "{description} at {amount} ".format(
            amount=self.amount,
            description=self.description
        )

    def set_as_paid(self):
        self.is_paid = True
        # self.paid_on = timezone.now()
        self.save()

    def approve_payment(self):
        self.set_as_paid()
        # self.installment.set_payment_status()

    def get_previously_completed_payment(self):
        return

    def get_initial_payment(self):
        return self.installment.subpayment_set.get(is_initial=True)

    def get_initial_payment_amount(self):
        return self.get_initial_payment().amount

    def initial_has_been_paid(self) -> bool:
        return self.get_initial_payment().is_paid

    def calculate_due_date(self):
        return self.get_initial_payment().paid_on + datetime.timedelta(weeks=self.due_in)

    def calculate_due_date_pretty(self):
        if self.is_initial:
            return 'Due now'

    def get_paid_date(self):
        if self.is_paid:
            return humanize.naturalday(self.paid_on)
        else:
            return None

    def payment_overdue(self) -> bool:
        if self.initial_has_been_paid():
            return timezone.now() > self.calculate_due_date()
        else:
            return False

    def get_due_date(self):
        if self.initial_has_been_paid():
            return self.calculate_due_date()
        else:
            if self.is_initial:
                return timezone.now()
            return "Waiting to be activated".format(
                number_of_weeks=self.due_in
            )

    def get_due_date_pretty(self):
        if self.initial_has_been_paid():
            return humanize.naturaltime(self.calculate_due_date())
        else:
            if self.is_initial:
                return timezone.now()
            return "Waiting to be activated".format(
                number_of_weeks=self.due_in
            )

    def get_balance_after_payment(self):
        all_payments = self.installment.get_paid_subpayments()
        if all_payments:
            amount = all_payments.filter(paid_on__lte=self.paid_on).aggregate(sum=Sum('amount'))
            return self.installment.total_amount - amount['sum']
        else:
            return self.installment.total_amount

    def save(self, *args, **kwargs):
        """
        Sets paid_on date
        :param args:
        :param kwargs:
        :return:
        """
        if self.is_paid and not self.paid_on:
            self.paid_on = timezone.now()
        elif self.paid_on:
            pass
        else:
            self.paid_on = None
        super(type(self), self).save(*args, **kwargs)
        self.installment.set_payment_status()


INSTALLMENT_PLAN_STATUS = (
    ('is_unpaid', 'Unpaid'),
    ('is_pending', 'Pending'),
    ('is_settled', 'Settled'),
    ('is_cancelled', 'Cancelled'),
    ('is_breached', 'Breached')
)


class PlanStatus(enum.Enum):
    is_unpaid = 'is_unpaid'
    is_pending = "is_pending"
    is_settled = 'is_settled'
    is_breached = 'is_breached'
    is_cancelled = 'is_cancelled'


class BulkData:
    def __init__(self, subject, header_text, message, email):
        self.subject = subject
        self.header_text = header_text
        self.message = message
        self.email = email


class InstallmentPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True)
    total_amount = models.FloatField()
    is_cancelled = models.BooleanField(default=False)
    status = models.CharField(editable=False, max_length=15, default=PlanStatus.is_unpaid.value)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.subpayment_set.count() < 0:
            raise ValidationError('Please put at least one payment')

    def __str__(self):
        return "{description} in ({installment_count}) installments for {user}  ".format(
            installment_count=self.subpayment_set.count(),
            description=self.description,
            user=self.user.get_full_name()
        )

    def get_total_amount_paid(self):
        if self.get_balance() != self.total_amount:
            return self.total_amount - self.get_balance()
        else:
            return 0

    def get_paid_subpayments(self):
        return self.subpayment_set.filter(is_paid=True).order_by('-paid_on')

    def get_balance(self):
        if not self.subpayment_set.all():
            return 'No payment plan exists'
        all_paid_subpayments = self.subpayment_set.filter(is_paid=True)
        if all_paid_subpayments:
            total_amount_paid = all_paid_subpayments.aggregate(total_amount=Sum('amount'))
            total_amount_paid = total_amount_paid['total_amount']
            return self.total_amount - total_amount_paid
        else:
            return self.total_amount

    def total_installments(self):
        return self.subpayment_set.filter(is_disabled=False).count()

    def get_initial_payment_amount(self):
        return self.subpayment_set.get(is_initial=True, is_disabled=False).amount

    def get_next_due_payment(self):
        all_subpayments = self.subpayment_set.all()
        initial_payment = all_subpayments.get(is_initial=True, is_disabled=False)

        if initial_payment.is_paid:
            # Removes all paid installments
            left_over = all_subpayments.exclude(is_paid=True)
            next_payment = left_over.order_by('due_in').first()
            return next_payment
        return initial_payment

    def get_next_due_payment_id(self):

        if self.get_next_due_payment():
            return self.get_next_due_payment().pk
        return None

    def get_upcoming_payments(self):
        all_upcoming = SubPayment.objects.filter(is_paid=False).order_by('due_in')
        return all_upcoming

    balance = property(get_balance)
    total_installments.short_description = 'Total Installments'
    get_balance.short_description = 'Balance Left'

    def set_payment_status(self):
        if self.is_cancelled:
            self.status = PlanStatus.is_cancelled.value
            self.save()
            return

        if self.get_balance() == 0:
            self.status = PlanStatus.is_settled.value
            self.save()

        elif self.get_balance() < self.total_amount:
            self.status = PlanStatus.is_pending.value
            self.save()

            # Set status appropriately
            next_payment = self.get_next_due_payment()
            if next_payment.payment_overdue():
                self.status = PlanStatus.is_breached.value
                self.save()

        else:
            self.status = PlanStatus.is_unpaid.value
            self.save()

    @staticmethod
    def get_upcoming_plans():
        InstallmentPlan.refresh_all_plan_status()
        return InstallmentPlan.objects.filter(~Q(status=PlanStatus.is_settled.value)) \
               | InstallmentPlan.objects.filter(~Q(status=PlanStatus.is_cancelled.value))

    @staticmethod
    def get_overdue_plans():
        InstallmentPlan.refresh_all_plan_status()
        return InstallmentPlan.objects.filter(status=PlanStatus.is_breached.value)

    @staticmethod
    def refresh_all_plan_status():
        for plan in InstallmentPlan.objects.all():
            print('Setting ', plan)
            plan.set_payment_status()
            print('Plan status:', plan.status)
        return True

    @staticmethod
    def send_all_users_notification_on_upcoming_payments():
        plans = InstallmentPlan.get_upcoming_plans()
        message_template = """
Hello {name}

This is a notification for an upcoming payment for {plan_name}

Details are as follows
Plan - {plan_name}.
Amount Due - ${amount}
Payment Due Date - {payment_date} ({payment_date_pretty})

Kindly go to https://linuxjobber.com/installments to make payment.
"""
        bulk_data = []
        for plan in plans:
            bulk_data.append(
                BulkData(
                    subject='Upcoming Installment Payment',
                    header_text='Linuxjobber Installments',
                    email=plan.user.email,
                    message=message_template.format(
                        payment_date=plan.get_next_due_payment().get_due_date().strftime('%d-%m-%Y'),
                        payment_date_pretty=plan.get_next_due_payment().get_due_date_pretty(),
                        amount=plan.get_next_due_payment().amount,
                        plan_name=plan.description,
                        name=plan.user.first_name
                    )
                )
            )

        from .mail_service import handle_bulk_mail
        if bulk_data:
            handle_bulk_mail(bulk_data)
            return
        print('No payment found')

    @staticmethod
    def send_all_users_notification_on_overdue_payments():
        plans = InstallmentPlan.get_overdue_plans()
        message_template = """
Hello {name}

You have an installment payment for {plan_name} that is overdue. 

Details are as follows
Plan - {plan_name}.
Amount Due - ${amount}
Payment Due Date - {payment_date} ({payment_date_pretty})

Kindly go to https://linuxjobber.com/installments to make payment now.
"""
        bulk_data = []
        for plan in plans:
            bulk_data.append(
                BulkData(
                    subject='Installment Payment Overdue',
                    header_text='Linuxjobber Installments',
                    email=plan.user.email,
                    message=message_template.format(
                        payment_date=plan.get_next_due_payment().get_due_date().strftime('%d-%m-%Y'),
                        payment_date_pretty=plan.get_next_due_payment().get_due_date_pretty(),
                        amount=plan.get_next_due_payment().amount,
                        plan_name=plan.description,
                        name=plan.user.first_name
                    )
                )
            )
        from .mail_service import handle_bulk_mail
        if bulk_data:
            handle_bulk_mail(bulk_data)
            return
        print('No payment found')


class EmailGroup(models.Model):
    name = models.CharField(max_length=255, )
    description = models.CharField(max_length=255, )
    # members_by_role = models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True)
    sql_query = models.TextField(null=True)
    where_clause = models.TextField(null=True, blank=True)
    exclude_clause = models.TextField(null=True, blank=True)
    extra_members = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.name + "".format(self.description)

    def run_query(self, *args):
        if args:
            with connection.cursor() as cursor:
                cursor.execute("{} {} {}".format(args[0],
                                                 args[1] if args[1] else "",
                                                 args[2] if args[2] else ""
                                                 ).strip('""'))
                row = cursor.fetchall()
            return row

        if self.sql_query:
            with connection.cursor() as cursor:
                cursor.execute("{} {} {}".format(self.sql_query,
                                                 self.where_clause if self.where_clause else "",
                                                 self.exclude_clause if self.exclude_clause else ""
                                                 ).strip('""'))
                row = cursor.fetchall()
                from functools import reduce
                import operator
                if row:
                    row = reduce(operator.concat, row)
                else:
                    row = []
                return row
        else:
            return []

    def members_count(self):
        # return self.get_members_by_role().count() + self.extra_members.all().count()
        # extra_members = self.extra_members.all().count()
        # members_from_query = self.run_query()
        return len(self.get_members_emails())

    def get_members(self):
        members = self.run_query()
        total_members = CustomUser.objects.filter(email__in=members) | self.extra_members.all()
        return total_members

    def get_members_emails(self):
        # Values are made distinct in here
        return set(self.get_members().values_list('email', flat=True))


class EmailGroupMessageLog(models.Model):
    group = models.ForeignKey(EmailGroup, on_delete=models.DO_NOTHING)
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_instant = models.BooleanField(default=True)
    delivery_time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)

    def schedule_mail(self):
        pass

    def __str__(self):
        return self.group.name + "({})".format(self.message.slug)

    def get_failed_messages(self):
        return self.emailmessagelog_set.filter(has_sent=False)

    def handle_failed_messages(self):
        pass

    def get_mail_statistics(self):
        failed_flag = False
        # try:
        #     CompletedTask.objects.get(task_params__contains=self.pk)
        #     self.is_completed=True
        #
        #     self.save()
        # except:
        #     pass
        if not self.get_failed_messages():
            self.is_completed = True
            self.save()

        context = {
            'has_completed': self.is_completed,
            'sent': self.emailmessagelog_set.filter(has_sent=True).count(),
            'pending': self.emailmessagelog_set.filter(has_sent=False).count(),
            'failed': self.emailmessagelog_set.filter(has_sent=False).count(),
            'total': self.emailmessagelog_set.count()
        }
        return context

    def set_as_completed(self):
        self.is_completed = True
        self.save()

    class Meta:
        verbose_name = "Send Message"
        verbose_name_plural = "Send Message"


class Variables(models.Model):
    key = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Variables'
        verbose_name_plural = 'Variables'

    # def save(self, *args, **kwargs):
        """
        Checks for duplicates and rewrites old value
        :param args:
        :param kwargs:
        :return:

     """
        # # changes to upper_case by default
        # self.key = str(self.key.upper())
        # try:
        #     old = Variables.objects.get(key=self.key)
        #     old.value = self.value
        #     if not kwargs.get('halt',None):
        #         old.save(halt=True)
        # except Variables.DoesNotExist:
        #     super(type(self), self).save(*args, **kwargs)

class ItPartnership(models.Model):
    full_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    email = models.CharField(max_length=200,unique=True)
    idea_title = models.CharField(max_length=500)
    idea_detail = models.TextField()

    def __str__(self):
        return self.full_name