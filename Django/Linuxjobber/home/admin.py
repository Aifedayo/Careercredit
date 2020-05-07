from typing import List

#from background_task.models import CompletedTask
from django.contrib import admin, messages
from django import forms
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.core.files.uploadedfile import SimpleUploadedFile

from django.core.mail import send_mail
from django.utils import timezone
from .utilities import encrypt,decrypt

from .forms import  UpcomingScheduleForm
from .mail_service import LinuxjobberMassMailer, handle_campaign, LinuxjobberMailer
from .models import FAQ, Job, RHCSAOrder, FreeAccountClick, Campaign, Message, Unsubscriber, Internship, \
    InternshipDetail, MessageGroup, UserLocation, NewsLetterSubscribers, UserOrder, Document, MainModel, AwsCredential, \
    Jobplacement, Groupclass, PaymentHistory, GroupClassRegister, StripePayment, UserPayment, wepeoples, wetask, werole, \
    wework, wetype, PartTimeJob, TryFreeRecord, FullTimePostion, PartTimePostion, Resume, CareerSwitchApplication, \
    Certificates, EmailMessageType, EmailMessageLog, CompleteClass, \
    CompleteClassLearn, CompleteClassCertificate, WorkExperienceEligibility, WorkExperienceIsa, WorkExperiencePay, \
    SubPayment, InstallmentPlan, EmailGroup, EmailGroupMessageLog, WorkExperiencePriceWaiver, Variables, ItPartnership,\
     WorkExperiencePaystub, WorkexpFormStage, WeTraineeStatus, RecordWEChange

from datetime import timedelta
import datetime
import subprocess
from django.conf import settings


def get_send_task_mail_template(obj, task):
    return """
        Hello {firstname}

        You have been assigned a task for the {program} program.  

        Task assigned: {task}
        {objective}

        Further Description:
        {description}


        Do ensure you accomplish this task as it is a requirement to finish the work experience program.
        Always ensure you reach out to your tech lead when you are stuck.


        Warm Regards,
        Linuxjobber

        """.format(
            firstname=obj.we_people.user.first_name,
            program = task.types,
            objective = task.objective,
            task = task.task,
            description = task.description
        )

class weworkAdmin(admin.ModelAdmin):
    search_fields = ['we_people__user__email']
    raw_id_fields = ['task']
    list_filter = ('status',)
    list_display = ['we_people', 'weight', 'task', 'status', 'due', 'task_type']

    def task_type(self, obj):
        return obj.task.types

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "task":
            kwargs["queryset"] = wetask.objects.filter(is_active=1)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # check if start date is added already
        weprof = wepeoples.objects.get(user=obj.we_people.user)
        if not weprof.start_date:
            weprof.start_date = datetime.datetime.now()
            weprof.graduation_date = datetime.datetime.now() + timedelta(days=90)
            weprof.save(update_fields=["start_date", "graduation_date"])
        
        if not weprof.profile_picture:
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, 
                'Unable to create work for user as user profile image is not set yet'
            )
        else:
            # send task to user
            if obj.send_task == 1:
                task = wetask.objects.get(pk=form.cleaned_data['task'].id)
                template = get_send_task_mail_template(obj, task)
                mailer = LinuxjobberMailer(
                    subject="New Work Experience Task Assigned - Linuxjobber",
                    to_address=obj.we_people.user.email,
                    header_text="Linuxjobber",
                    type=None,
                    message=template
                )
                mailer.send_mail()
            super().save_model(request, obj, form, change)


class campaignAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.send_message == 1:
            outps = None
            outs = None
            Role = ""
            if obj.Target == 0:
                Role = "all_role6"
            elif obj.Target == 1:
                Role = "all_role4"
            elif obj.Target == 2:
                Role = "nigerian_internship"
            elif obj.Target == 3:
                Role = "part_time_fresh_grads"
            elif obj.Target == 4:
                Role = "marketing_internship"

            outps = subprocess.Popen(
                ["sshpass", "-p", settings.TOOLS_PASSWORD,
                 "ssh", "-o StrictHostKeyChecking=no",
                 "-o LogLevel=ERROR", "-o UserKnownHostsFile=/dev/null",
                 settings.TOOLS_USER + "@" + settings.SERVER_IP,
                 "cd " + settings.OLD_TOOLS_PATH + " && sudo bash scheduler.sh"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE).communicate()
            outs = subprocess.Popen(
                ["sshpass", "-p", settings.TOOLS_PASSWORD,
                 "ssh", "-o StrictHostKeyChecking=no",
                 "-o LogLevel=ERROR",
                 "-o UserKnownHostsFile=/dev/null",
                 settings.TOOLS_USER + "@" + settings.SERVER_IP,
                 "cd " + settings.NEW_TOOLS_PATH + " && sudo python composeMail.py", '1', Role,
                 str(obj.message.slug)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print(outps)
            print(outs)

        print(obj.message.slug)
        print(obj.send_message)
        print(obj.Target)

        super().save_model(request, obj, form, change)


class wetaskAdmin(admin.ModelAdmin):
    search_fields = ['types__types', 'task']
    list_display = ['task', 'weight', 'is_active', 'types', 'group']
    list_filter = ('types__types', 'is_active',)


class MessageAdmin(admin.ModelAdmin):
    search_fields = ['group']
    list_display = ['title', 'slug', 'group']
    list_filter = ('group',)


class FreeAccountClickAdmin(admin.ModelAdmin):
    list_display = ['email', 'filled_jobs', 'freeaccountclick', 'registered', 'visited_tryfree', 'paid', 'date_created']


class JobAdmin(admin.ModelAdmin):
    search_fields = ['email', 'position__job_title']
    list_display = ['email', 'position','get_technology','interest','application_date']

    def get_technology(self, obj):
        return obj.position.required_technology

    get_technology.short_description = 'Required Technology'
    get_technology.admin_order_field = 'position__required_technology'


class PartimeAdmin(admin.ModelAdmin):
    search_fields = ['email', 'position__job_title']
    list_display = ['email', 'position']

class CareerSwitchApplicationAdmin(admin.ModelAdmin):
    list_display = ['email','old_career','new_career']

def get_urls():
    urls = ['---']
    import pickle

    try:
        with open('urls_tmp', 'rb') as file:
            urls = pickle.load(file)
    except:
        return []
    return ((choice, choice) for choice in urls)





class CustomAdminFullTimeForm(forms.ModelForm):

    interested_page = forms.ChoiceField(choices=get_urls())
    not_interested_page= forms.ChoiceField(choices=get_urls())
    skilled_page = forms.ChoiceField(choices=get_urls())
    class Meta:
        model = FullTimePostion
        exclude = []

class FullTimeAdmin(admin.ModelAdmin):

    search_fields = ['interested','not_interested','skilled']
    form = CustomAdminFullTimeForm

class EmailMessageTypeAdmin(admin.ModelAdmin):
    list_display = ['type','is_default','header_format']


class EmailMessageLogAdmin(admin.ModelAdmin):
    list_display = ['subject','to_address','header_text','message_type','has_sent','group_log','timestamp']
    actions = ['resend_message','unsent']
    list_filter = ('has_sent','group_log')
    change_list_template = 'admin/emailmessage_log_changelist.html'


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('mail/delete', self.clean_mail, name= 'clean-mail-log'),
        ]  # type: List[path]
        return my_urls + urls

    def clean_mail(self,request):
        if request.method == "POST":
            message_count = 0
            amount_of_days = request.POST.get('amount_of_days',None)
            if amount_of_days:
                amount_of_days = int(amount_of_days)
                logs = EmailMessageLog.objects.filter(timestamp__lte=timezone.now() - timedelta(days=amount_of_days))
                message_count = logs.count()

                logs.delete()
                self.message_user(request,'{message_count} total messages from {days} days have been deleted'.format(
                    message_count = message_count,
                    days = amount_of_days,
                ),messages.SUCCESS)
            else:
                self.message_user(request,'Error, cannot use a value less than 1 ')
        return HttpResponseRedirect('../')

    def unsent(self, request, queryset):
        for message in queryset:
            message.set_as_fail('Custom ')


    def resend_message(self, request, queryset):
        mailer = LinuxjobberMassMailer(queryset,is_queryset = True)
        mailer.send()

        for message in mailer.messages:
            if message.message_obj.has_sent:
                self.message_user(request,"{} sent to {} successfully".format(
                    message.subject,
                    message.to
                ))
            else:
                self.message_user(request,"Failed to send email {} to {} [ERROR: {}] ".format(
                    message.subject,
                    message.message_obj.to_address,
                    message.message_obj.error_message
                ), level=messages.ERROR)

    resend_message.short_description = 'Send/Resend selected messages'
    unsent.short_description = 'Set selected messages as unsent'

class SubPaymentInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        total = 0
        installment_plan = None
        initial_set = []
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
                    if not form.cleaned_data['is_disabled']:
                        total+=form.cleaned_data['amount']
                    installment_plan = form.cleaned_data['installment']
                    initial_set.append(form.cleaned_data['is_initial'])
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        initial_count = initial_set.count(True)
        if count < 1:
            raise forms.ValidationError('You must have at least one sub payment')
        if initial_count == 0:
            raise forms.ValidationError('Please set an initial payment')
        if  initial_count > 1:
            raise forms.ValidationError('You can only set one payment as initial payment')
        if installment_plan:
            difference = installment_plan.total_amount - total
            if difference < 0:
                raise forms.ValidationError(' Sum of total sub payments is {} greater than the plan amount'.format(
                    abs(difference)
                ))
            elif difference > 0 :
                raise forms.ValidationError(' Sum of total sub payments is {} lesser than the plan amount'.format(
                    abs(difference))
                )

class SubPaymentInline(admin.TabularInline):
    model = SubPayment
    verbose_name = "Sub Payment"
    verbose_name_plural = "Sub Payments"
    extra = 0
    # radio_fields ={''}
    formset = SubPaymentInlineFormset





class CustomInstallmentAdminForm(forms.ModelForm):
    # status = forms.ChoiceField(choices=INSTALLMENT_PLAN_STATUS)
    class Meta:
        model = InstallmentPlan
        exclude = []
class CustomSubPaymentAdminForm(forms.ModelForm):
    # status = forms.ChoiceField(choices=INSTALLMENT_PLAN_STATUS)

    def clean(self):
        pass

    class Meta:
        model = SubPayment
        exclude = []




class InstallmentPlanAdmin(admin.ModelAdmin):
    list_display = ('user','description','total_amount','balance','total_installments','is_cancelled')
    list_filter = ('status','is_cancelled')
    search_fields = ('user__email','description')
    fieldsets = [
        ['General Information', {
            'fields': ['user', 'description', 'total_amount','is_cancelled']
        }],
    ]
    inlines =  (SubPaymentInline,)
    change_list_template = 'admin/installmentplan_changelist.html'

    raw_id_fields = ('user',)

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = ""


    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList


    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context['form'] = UpcomingScheduleForm(request.POST or None)
        try:
            from .utilities import context,convert_to_day,convert_to_time
            upcoming_day =  Variables.objects.get(key=context['upcoming_notification_day']).value
            upcoming_time =  Variables.objects.get(key=context['upcoming_notification_time']).value
            overdue_day =  Variables.objects.get(key=context['overdue_notification_day']).value
            overdue_time =  Variables.objects.get(key=context['overdue_notification_time']).value
            extra_context['form'] = UpcomingScheduleForm(request.POST or None)
            extra_context['upcoming_day'] = convert_to_day(upcoming_day)
            extra_context['upcoming_time'] = convert_to_time(upcoming_time)
            extra_context['overdue_day'] = convert_to_day(overdue_day)
            extra_context['overdue_time'] = convert_to_time(overdue_time)

        except:
            raise Exception


        return super(InstallmentPlanAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('set_upcoming', self.set_upcoming_schedule, name= 'set-upcoming-payment-notification'),
            path('ser_overdue', self.set_overdue_schedule, name= 'set-overdue-payment-notification'),
        ]  # type: List[path]
        return my_urls + urls

    def set_upcoming_schedule(self,request):
        if request.method == 'POST':
            form = UpcomingScheduleForm(request.POST or None)
            if form.is_valid():
                time = form.cleaned_data['time']
                day = int(form.cleaned_data['day'])
                # time = "{},{}".format(time.hour,time.minute)
                from .utilities import set_payment_notification_schedule
                try:
                    set_payment_notification_schedule(
                        day,
                        time.hour,
                        time.minute,
                        key = 'upcoming_notification',
                    )
                    self.message_user(request,'Upcoming Payment Notification Updated ',messages.SUCCESS)

                except Exception as e:
                    self.message_user(request,e,messages.ERROR)
                    return HttpResponseRedirect('./')
        return HttpResponseRedirect('./')

    def set_overdue_schedule(self,request):
        if request.method == 'POST':
            form = UpcomingScheduleForm(request.POST or None)
            if form.is_valid():
                time = form.cleaned_data['time']
                day = int(form.cleaned_data['day'])
                # time = "{},{}".format(time.hour,time.minute)
                from .utilities import set_payment_notification_schedule
                try:
                    set_payment_notification_schedule(
                        day,
                        time.hour,
                        time.minute,
                        key = 'overdue_notification',
                    )
                    self.message_user(request,'Overdue Payment Notification Updated ',messages.SUCCESS)

                except Exception as e:
                    self.message_user(request,e,messages.ERROR)
                    return HttpResponseRedirect('./')

            else:
                self.message_user(request,"Error",messages.ERROR)
        return HttpResponseRedirect('./')



    class Media:
        js = ('admin/js/bootstrap-formhelpers.min.js',)
    #
    # form = CustomInstallmentAdminForm
    #
    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     super().save_model(request, obj, form, change)
    #     all_subpayments = obj.subpayment_set.all()
    #     if all_subpayments:
    #         subpayments_total_amount = all_subpayments.aggregate(total_amount=Sum('amount'))
    #         difference = obj.total_amount - subpayments_total_amount['total_amount']
    #         if difference > 0:
    #             self.message_user(request, "Total amount of sub payments lesser than plan total amount for {}'s {}".format(
    #                 obj.user,obj.description),messages.WARNING)
    #
    #         elif difference < 0 :
    #             self.message_user(request, "Total amount of sub payments greater than plan total amount for {}'s {}".format(
    #                 obj.user,obj.description),messages.WARNING)
    #     else:
    #         self.message_user(request, "Please add at least one payment for {}'s {}".format(
    #                 obj.user,obj.description),messages.WARNING)

class EmailGroupForm(forms.ModelForm):
    class Meta:
        model = EmailGroup
        exclude =[]

    def clean(self):
        if self.cleaned_data:
            try:
                EmailGroup.run_query(None,self.cleaned_data['sql_query'],
                                     self.cleaned_data['where_clause'],
                                     self.cleaned_data['exclude_clause'])
            except Exception as e:
                raise forms.ValidationError('Error in query : {}'.format(e))




class EmailGroupAdmin(admin.ModelAdmin):
    list_display = ('name','description',)
    form = EmailGroupForm
    filter_horizontal = ('extra_members',)
    search_fields = ('name',)
    fieldsets = [
        ['Basic Information', {
            'fields': ['name', 'description']
        }],['Query Builder',{
            'fields' : ['sql_query',('where_clause','exclude_clause')]
        }],['Extra',{
            'fields' : ['extra_members']
        }],
    ]






class SendMessageAdmin(admin.ModelAdmin):
    """
        Maps to the email message log model, this is just to enable the filed to show send message in model admin
    """
    change_list_template = 'admin/emailgroup_changelist.html'
    list_display = ('message','group','get_mail_statistics')
    search_fields = ('message','group')
    list_filter = ('group',)

    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = 'Emails Sent Via Email Groups'


    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('mail/compose', self.compose_mail, name= 'mail-compose'),
            path('mail/activate', self.mail_activate, name= 'mail-activate'),
            path('mail/logs', self.mail_logs, name= 'mail-logs'),
            path('mail/status', self.check_mail_status, name= 'mail-status'),
        ]  # type: List[path]
        return my_urls + urls

    def has_add_permission(self, request, obj=None):
        return False

    def compose_mail(self,request,is_sent=False):
        context = {'groups': EmailGroup.objects.all(),'group_messages':Message.objects.all()}
        return TemplateResponse(request,'admin/compose_mail.html',context)

    def mail_logs(self,request):
        context = {'groups': EmailGroup.objects.all()}
        return TemplateResponse(request,'admin/list_group_mail.html',context)

    def mail_activate(self,request):
        context = {}
        if request.method == 'POST':
            email_group_id=request.POST.get('group',None)
            message=request.POST.get('message',None)
            is_instant=request.POST.get('is_instant',True)
            # Implementation for scheduled messages
            if is_instant:
                pass
            if email_group_id and message:
                try:
                    _message = Message.objects.get(id=message)
                    _email_group = EmailGroup.objects.get(id=email_group_id)

                    # Check for request duplication
                    try:
                        last = CompletedTask.objects.last()
                        import re
                        group_message_log_id = re.findall('\d+', last.task_params)[0]
                        group_message_log = EmailGroupMessageLog.objects.get(pk=group_message_log_id)
                        if group_message_log.message == _message and group_message_log.group == _email_group:
                            context['group'] = group_message_log
                            messages.error(
                                request,' Multiple request detected, details of original request are as follows')

                        else:
                            raise

                    except:
                        # Means duplicate found
                        created_group = EmailGroupMessageLog.objects.create(
                            group=_email_group,
                            message = _message,
                            created_by=request.user,
                            is_instant = is_instant
                        )
                        # members = created_group.group.get_members()
                        context['group'] = created_group
                        handle_campaign(group_id=created_group.id)
                    finally:
                        return TemplateResponse(request,'admin/mail_pocessing.html',context)
                except Exception as e:
                    print(e)
                    self.message_user(request,'Error in creating a message')
                    return HttpResponseRedirect('../')
            return TemplateResponse(request,'admin/mail_pocessing.html')
        else:
            self.message_user(request,'Cannot validate request, try again',messages.WARNING)
            return redirect('admin:index')

    def check_mail_status(self,request):
        if request.method == 'POST':
            group_id = request.POST.get('group_id',None)
            try:
                group = EmailGroupMessageLog.objects.get(pk=group_id)
                return JsonResponse(group.get_mail_statistics())
            except:
                return JsonResponse({})


class WorkExperienceIsaAdmin(admin.ModelAdmin):
    # Customiz the work experience ISA form 
    def save_model(self, request, obj, form, change):
        try:
            details =  WorkExperienceEligibility.objects.get(user=obj.user)
        
        except  WorkExperienceEligibility.DoesNotExist:
            details = None

        try: 
            det = WorkExperienceIsa.objects.get(user=obj.user)
        except WorkExperienceIsa.DoesNotExist:
            det = None

        html_template = get_template('home/workexpisapdf.html').render({'user':details})


        pdf_file = HTML(string=html_template).write_pdf( stylesheets=[CSS("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css")],presentational_hints=True)
        obj.pdf = SimpleUploadedFile('Work-Experience-ISA-'+ details.user.first_name +' '+details.user.last_name +'.pdf', pdf_file, content_type='application/pdf')

        super().save_model(request, obj, form, change)

class WorkExperienceEligibilityAdmin(admin.ModelAdmin):
    # Customize the work experience eligibity form on the admin panel
    list_display = ('user','first_name','state','SSN','ssn_last_four','is_encrypted')
    search_fields = ('first_name','user__email','last_name')
    change_form_template = 'admin/workexperienceeligibility_change_list.html'
    ordering = ('is_encrypted',)
    list_filter = ('is_encrypted',)

    class CustomChangeList(ChangeList):
        #Change list of the form
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = ''

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = ""
        return super(WorkExperienceEligibilityAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList


    def get_urls(self):
        # Invoke the urls attached
        urls = super().get_urls()
        my_urls = [
            path('ssn/handle', self.handle_encryption, name= 'transform-ssn'),
        ]  # type: List[path]
        return my_urls + urls



    def handle_encryption(self,request):
        # Take care of the encryption from the form
        if request.method == 'POST':
            if request.POST.get('action') == 'encrypt':
                self.encrypt_one(request)
            else:
                self.decrypt_one(request)
        return redirect('../')


    def encrypt_all(self,request):
        # Encrypt the details from the form
        if request.method == 'POST':

            from  .views import ADMIN_EMAIL
            log = []
            is_valid = False
            password = request.POST.get('password', None)
            try:
                for obj in WorkExperienceEligibility.objects.all():
                    if not obj.is_encrypted:
                        # Confirm if it is the same password used previously
                        if not is_valid:
                            try:
                                old = WorkExperienceEligibility.objects.filter(is_encrypted=True)
                                if old:
                                    random_test = old[0]
                                    if decrypt(random_test.SSN,password):
                                        is_valid = True
                                    else:
                                        raise
                                else:
                                    is_valid = True

                            except:
                                self.message_user(request, 'Records could not be updated, password doesnt match previously '
                                                           'used one', messages.ERROR)
                                return

                        obj.transform_ssn()

                        encrypted_data = encrypt(obj.SSN,password)
                        obj.SSN = encrypted_data
                        obj.is_encrypted = True
                        obj.save()
                        log.append(True)

                if True in log:
                    # Check if the log is true
                    self.message_user(request, 'Records updated', messages.SUCCESS)
                    new_mail_message = "SSN data has been encrypted by {}".format(request.user)
                    mailer = LinuxjobberMailer(
                        subject="SSN Encrypted",
                        to_address=ADMIN_EMAIL,
                        header_text="Linuxjobber Notifications",
                        type=None,
                        message=new_mail_message
                    )
                    mailer.send_mail()
                else:
                    self.message_user(request, 'All Records already updated', messages.SUCCESS)
            except:
                self.message_user(request, 'Records could not be updated', messages.ERROR)

    def encrypt_one(self,request):
        # Encrypt one of the SSN
        if request.method == 'POST':
            from  .views import ADMIN_EMAIL
            password = request.POST.get('password', None)
            object_id = request.POST.get('object_id', None)
            try:
                obj = WorkExperienceEligibility.objects.get(pk = object_id)
                if not obj.is_encrypted:
                    obj.transform_ssn()
                    encrypted_data = encrypt(obj.SSN, password)
                    obj.SSN = encrypted_data
                    obj.is_encrypted = True
                    obj.save()
                    self.message_user(request, 'Records updated', messages.SUCCESS)
                    new_mail_message = "SSN data for {} has been encrypted by {}".format(obj.user.email,request.user)
                    mailer = LinuxjobberMailer(
                        subject="SSN Encrypted",
                        to_address=ADMIN_EMAIL,
                        header_text="Linuxjobber Notifications",
                        type=None,
                        message=new_mail_message
                    )
                    mailer.send_mail()
                else:
                    self.message_user(request, 'All Records already updated', messages.SUCCESS)
            except:
                self.message_user(request, 'SSN cannot be encrypted', messages.ERROR)
    def decrypt_one(self,request):
        # Decrypt one SSN
        if request.method == 'POST':
            from .utilities import decrypt
            from .views import ADMIN_EMAIL
            password = request.POST.get('password', None)
            object_id = request.POST.get('object_id', None)
            decrypted_data = ""
            try:
                obj = WorkExperienceEligibility.objects.get(pk = object_id)
                if obj.is_encrypted:
                    if password:
                        decrypted_data = decrypt(obj.SSN, password)
                        if not decrypted_data:
                            raise
                        # obj.SSN = decrypted_data
                        # obj.is_encrypted = False
                        # obj.save()
                    new_mail_message = "SSN data for {} has been decrypted by {}".format(obj.user.email,request.user)
                    mailer = LinuxjobberMailer(
                        subject="SSN Decrypted",
                        to_address=ADMIN_EMAIL,
                        header_text="Linuxjobber Notifications",
                        type=None,
                        message=new_mail_message
                    )
                    mailer.send_mail()
                    self.message_user(request, 'Decrypted SSN is {}'.format(decrypted_data), messages.SUCCESS)
                else:
                    self.message_user(request, 'All Records already updated', messages.SUCCESS)
            except:
                new_mail_message = "SSN data was tried to be decrypted by {}".format(request.user)
                mailer = LinuxjobberMailer(
                    subject="SSN Decryption Failed",
                    to_address=ADMIN_EMAIL,
                    header_text="Linuxjobber Notifications",
                    type=None,
                    message=new_mail_message
                )
                mailer.send_mail()
                self.message_user(request, 'SSN cannot be decrypted, Invalid password', messages.ERROR)
    def decrypt_all(self,request):
        # Decrypt all the SSN
        if request.method == 'POST':
            from .utilities import decrypt
            from .views import ADMIN_EMAIL
            log = []
            try:
                for obj in WorkExperienceEligibility.objects.all():
                    if obj.is_encrypted:
                        obj.transform_ssn()
                        password = request.POST.get('password', None)
                        if password:
                            decrypted_data = decrypt(obj.SSN, password)
                            if not decrypted_data:
                                raise
                            obj.SSN = decrypted_data
                            obj.is_encrypted = False
                            obj.save()
                            log.append(True)

                if True in log:
                    new_mail_message = "SSN data has been decrypted by {}, ensure to encrypt back".format(request.user)
                    mailer = LinuxjobberMailer(
                        subject="SSN Decrypted",
                        to_address=ADMIN_EMAIL,
                        header_text="Linuxjobber Notifications",
                        type=None,
                        message=new_mail_message
                    )
                    mailer.send_mail()
                    self.message_user(request, 'Records updated', messages.SUCCESS)
                else:
                    self.message_user(request, 'All Records already updated', messages.SUCCESS)
            except:
                new_mail_message = "SSN data was tried to be decrypted by {}".format(request.user)
                mailer = LinuxjobberMailer(
                    subject="SSN Decryption Failed",
                    to_address=ADMIN_EMAIL,
                    header_text="Linuxjobber Notifications",
                    type=None,
                    message=new_mail_message
                )
                mailer.send_mail()
                self.message_user(request, 'Records could not be updated, Invalid password', messages.ERROR)
                
    def save_model(self, request, obj, form, change):
        # Save the form detail into the database
        if obj.generate_pdf == 1:
            try:
                details =  WorkExperienceEligibility.objects.get(user=obj.user)
                date = details.date_of_birth
                date = date.strftime('%m/%d/%Y')
                created = details.date_created
                created = created.strftime('%Y/%m/%d')
                ssn = details.SSN
                ssn = ssn[-4:]
                ssn = "•••••" + ssn
                print("grab")
                
            except  WorkExperienceEligibility.DoesNotExist:
                details = None
                date = None
                created = None
            #return render(request, 'home/workexpeligibilitypdf.html')
            html_template = get_template('home/workexpeligibilitypdf.html').render({'details':details,'date':date,'ssn':ssn,'created':created})


            pdf_file = HTML(string=html_template).write_pdf( stylesheets=[CSS("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css")],presentational_hints=True)
            obj.pdf = SimpleUploadedFile('Work-Experience-Eligibility-'+ details.user.first_name +' '+details.user.last_name +'.pdf', pdf_file, content_type='application/pdf')
            html_template1 = get_template('home/workexptermpdf.html').render({'user':details})


            pdf_file = HTML(string=html_template).write_pdf( stylesheets=[CSS("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css")],presentational_hints=True)
            obj.terms = SimpleUploadedFile('Work-Experience-Terms-'+ details.user.first_name +' '+details.user.last_name +'.pdf', pdf_file, content_type='application/pdf')

        super().save_model(request, obj, form, change)


class ItPartnershipAdmin(admin.ModelAdmin):
    list_display = ('full_name','company','email','idea_title','idea_detail')
    # list_display = ItPartnership._meta.get_fields()

admin.site.register(WorkExperienceIsa,WorkExperienceIsaAdmin)
admin.site.register(WorkExperienceEligibility,WorkExperienceEligibilityAdmin)
admin.site.register(WorkExperiencePay)
admin.site.register(WorkExperiencePaystub)
admin.site.register(WorkExperiencePriceWaiver)
admin.site.register(FAQ)
admin.site.register(Job, JobAdmin)
admin.site.register(UserOrder)
admin.site.register(Document)
admin.site.register(MainModel)
admin.site.register(AwsCredential)
admin.site.register(Jobplacement)
admin.site.register(Groupclass)
admin.site.register(GroupClassRegister)
admin.site.register(PaymentHistory)
admin.site.register(RHCSAOrder)
admin.site.register(Campaign, campaignAdmin)
admin.site.register(NewsLetterSubscribers)
admin.site.register(StripePayment)
admin.site.register(UserLocation)
admin.site.register(Internship)
admin.site.register(InternshipDetail)
admin.site.register(UserPayment)
admin.site.register(Unsubscriber)
admin.site.register(wepeoples)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageGroup)
admin.site.register(PartTimeJob, PartimeAdmin)
admin.site.register(FullTimePostion,FullTimeAdmin)
admin.site.register(PartTimePostion)
admin.site.register(wetask, wetaskAdmin)
admin.site.register(wework, weworkAdmin)
admin.site.register(wetype)
admin.site.register(FreeAccountClick, FreeAccountClickAdmin)
admin.site.register(werole)
admin.site.register(Resume)
admin.site.register(TryFreeRecord)
admin.site.register(CareerSwitchApplication, CareerSwitchApplicationAdmin)
admin.site.register(Certificates)
admin.site.register(CompleteClass)
admin.site.register(CompleteClassLearn)
admin.site.register(CompleteClassCertificate)
admin.site.register(EmailMessageType,EmailMessageTypeAdmin)
admin.site.register(EmailMessageLog,EmailMessageLogAdmin)
admin.site.register(InstallmentPlan, InstallmentPlanAdmin)
admin.site.register(EmailGroup, EmailGroupAdmin)
admin.site.register(EmailGroupMessageLog, SendMessageAdmin)
admin.site.register(ItPartnership, ItPartnershipAdmin)
admin.site.register(WorkexpFormStage)
admin.site.register(WeTraineeStatus)
admin.site.register(RecordWEChange)

class VariablesAdmin(admin.ModelAdmin):
    list_display = ('key','value')


admin.site.register(Variables,VariablesAdmin)


