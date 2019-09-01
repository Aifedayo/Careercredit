import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from users.models import CustomUser

from Courses.models import Course


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    response = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class FullTimePostion(models.Model):
    job_title = models.CharField(max_length=200)
    requirement = models.CharField(max_length=200)
    responsibility = models.TextField()
    weight = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return '%s' % self.job_title


class PartTimePostion(models.Model):
    job_title = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.job_title


class Job(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    position = models.ForeignKey(FullTimePostion, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume', null=True)
    cv_link = models.CharField(max_length=200, null=True)

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
    users = models.ManyToManyField(CustomUser, blank=True, null=True)
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
    message = models.TextField()
    slug = models.SlugField(max_length=40)
    group = models.ForeignKey(MessageGroup, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


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
    task = models.CharField(max_length=50, null=True)
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
    created = models.DateTimeField(default=timezone.now, null=False)
    send_task = models.IntegerField(default=0, choices=((0, 'No'), (1, 'Yes')))
    due = models.DateTimeField(default=timezone.now, null=True)

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
    old_career =  models.CharField(max_length=255)
    new_career = models.ForeignKey(FullTimePostion, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume', null=True)
    cv_link = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.fullname
