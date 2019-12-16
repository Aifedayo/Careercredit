from typing import List

from background_task.models_completed import CompletedTask
from django.contrib import admin, messages
from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path

from django.core.mail import send_mail
from .mail_service import LinuxjobberMassMailer, handle_campaign
from .models import FAQ, Job, RHCSAOrder, FreeAccountClick, Campaign, Message, Unsubscriber, Internship, \
    InternshipDetail, MessageGroup, UserLocation, NewsLetterSubscribers, UserOrder, Document, MainModel, AwsCredential, \
    Jobplacement, Groupclass, BillingHistory, GroupClassRegister, StripePayment, UserPayment, wepeoples, wetask, werole, \
    wework, wetype, PartTimeJob, TryFreeRecord, FullTimePostion, PartTimePostion, Resume, CareerSwitchApplication, \
    Certificates, EmailMessageType, EmailMessageLog, CompleteClass, \
    CompleteClassLearn, CompleteClassCertificate, WorkExperienceEligibility, WorkExperienceIsa, WorkExperiencePay, \
    SubPayment, InstallmentPlan, EmailGroup, EmailGroupMessageLog

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
                send_mail('New Work Experience Task Assigned - Linuxjobber', template, settings.EMAIL_HOST_USER, [obj.we_people.user.email])

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
    list_filter = ('has_sent',)


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

    raw_id_fields = ('user',)
    # form = CustomInstallmentAdminForm

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



    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('mail/compose', self.compose_mail, name= 'mail-compose'),
            path('mail/activate', self.mail_activate, name= 'mail-activate'),
            path('mail/logs', self.mail_logs, name= 'mail-logs'),
            path('mail/status', self.check_mail_status, name= 'mail-status'),
        ]  # type: List[path]
        return my_urls + urls

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
                        # Means duplicate fount
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

admin.site.register(WorkExperienceIsa)
admin.site.register(WorkExperienceEligibility)
admin.site.register(WorkExperiencePay)
admin.site.register(FAQ)
admin.site.register(Job, JobAdmin)
admin.site.register(UserOrder)
admin.site.register(Document)
admin.site.register(MainModel)
admin.site.register(AwsCredential)
admin.site.register(Jobplacement)
admin.site.register(Groupclass)
admin.site.register(GroupClassRegister)
admin.site.register(BillingHistory)
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



