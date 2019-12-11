from django.contrib import admin, messages
from django import forms
from django.db.models import Sum
from django.shortcuts import redirect

from . import models
from django.core.mail import send_mail
from django.conf import settings
from .models import FAQ, Job, RHCSAOrder, FreeAccountClick, Campaign, Message, Unsubscriber, Internship, \
    InternshipDetail, MessageGroup, UserLocation, NewsLetterSubscribers, UserOrder, Document, MainModel, AwsCredential, \
    Jobplacement, Groupclass, BillingHistory, GroupClassRegister, StripePayment, UserPayment, wepeoples, wetask, werole, \
    wework, wetype, PartTimeJob, TryFreeRecord, FullTimePostion, PartTimePostion, Resume, CareerSwitchApplication, \
    Certificates, EmailMessageType, EmailMessageLog,CompleteClass,\
    CompleteClassLearn, CompleteClassCertificate, workexpeligibility, workexpisa, workexppay, SubPayment, InstallmentPlan, INSTALLMENT_PLAN_STATUS


from datetime import timedelta
import datetime
import subprocess, os
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
    list_display = ['subject','to_address','header_text','message_type','has_sent','timestamp']
    actions = ['resend_message',]

    def resend_message(self, request, queryset):
        for message in queryset:
            message.send_mail()
            if message.has_sent:
                self.message_user(request,"{} sent to {} successfully".format(
                    message.subject,
                    message.to_address
                ))
            else:
                self.message_user(request,"Failed to send email {} to {} [ERROR: {}] ".format(
                    message.subject,
                    message.to_address,
                    message.error_message
                ), level=messages.ERROR)

    resend_message.short_description = 'Resend Message'

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
    list_display = ('user','description','total_amount','balance','total_installments')
    list_filter = ('status',)
    search_fields = ('user__email','description')
    fieldsets = [
        ['General Information', {
            'fields': ['user', 'description', 'total_amount']
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





admin.site.register(workexpisa)
admin.site.register(workexpeligibility)
admin.site.register(workexppay)
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
admin.site.register(EmailMessageLog)
admin.site.register(InstallmentPlan, InstallmentPlanAdmin)


