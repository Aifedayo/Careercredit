from django.contrib import admin
from django import forms
from . import models
from django.core.mail import send_mail
from django.conf import settings
from .models import FAQ, Job, RHCSAOrder, FreeAccountClick, Campaign, Message, Unsubscriber, Internship, \
    InternshipDetail, MessageGroup, UserLocation, NewsLetterSubscribers, UserOrder, Document, MainModel, AwsCredential, \
    Jobplacement, Groupclass, BillingHistory, GroupClassRegister, StripePayment, UserPayment, wepeoples, wetask, werole, \
    wework, wetype, PartTimeJob, TryFreeRecord, FullTimePostion, PartTimePostion, Resume, CareerSwitchApplication

from datetime import timedelta
import datetime
import subprocess, os
from django.conf import settings

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
        # send task to user
        if obj.send_task == 1:
            task = wetask.objects.get(pk=form.cleaned_data['task'].id)
            template = """
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
    list_display = ['email', 'position','get_technology','interest']

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

