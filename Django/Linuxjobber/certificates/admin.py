import base64
from typing import List, Any

from django.contrib import admin, messages

# Register your models here.
from django.contrib.admin.views.main import ChangeList
from django.core.files.images import get_image_dimensions
from django.contrib import admin
from django.http import HttpResponseRedirect, FileResponse, HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import path

from .models import GraduateCertificates, CertificateType
from django import forms


class GraduateCertificateForm(forms.ModelForm):
    class Meta:
        model = GraduateCertificates
        exclude = []

    def clean(self):

        user = self.cleaned_data.get('user')
        alternate_email = self.cleaned_data.get('alternate_email')
        alternate_full_name = self.cleaned_data.get('alternate_full_name')
        alternate_graduate_image = self.cleaned_data.get('alternate_graduate_image')

        if not user and not alternate_full_name:
            raise forms.ValidationError("Supply either an alternate student name or select an existing user")

        if not user and not alternate_graduate_image:
            raise forms.ValidationError(
                "Supply either an alternate graduate image name or update user profile with image")

        if not user and not alternate_email:
            raise forms.ValidationError("Supply either an alternate graduate email or select an existing user")

        if alternate_graduate_image:
            w, h = get_image_dimensions(alternate_graduate_image)
            if w > 180 and h > 192:
                raise forms.ValidationError("The image too large. It's supposed to be atmost 180 X 192 pixels")


class CertificateTypeForm(forms.ModelForm):
    class Meta:
        model = CertificateType
        exclude = []

    def clean_logo(self):
        picture = self.cleaned_data.get("logo")
        if not picture:
            raise forms.ValidationError("No image!")
        else:
            width, height = get_image_dimensions(picture)
            if width > 180 and height > 192:
                raise forms.ValidationError("The image too large. It's supposed to be atmost 180 X 192 pixels")

        return picture


@admin.register(GraduateCertificates)
class GraduateCertificateAdmin(admin.ModelAdmin):
    form = GraduateCertificateForm
    # fields = ('certificate_id',('user','alternate_email'),('alternate_fullname','alternate_image'),'certificate_type','graduation_date',)
    fieldsets = [
        ['Certificate Information', {
            'fields': ['certificate_id', 'certificate_type', 'graduation_date']
        }],
        ['Graduate Information', {
            'fields': ['user']
        }],
        ['Alternate Graduate Information', {
            'fields': ['alternate_full_name', 'alternate_email', 'alternate_graduate_image']
        }],
    ]

    list_display = ('certificate_id', 'user', 'alternate_email', 'certificate_type', 'graduation_date','is_sent')
    readonly_fields = ['certificate_id']
    search_fields = ('alternate_email', 'user__email')
    change_form_template = 'admin/certificate_change.html'
    ordering = ('graduation_date',)
    list_filter = ('is_sent',)
    raw_id_fields = ('user',)

    # def save_model(self, request, obj, form, change):
    #     image = request.FILES.get('alternate_graduate_image',None)
    #     if image:
    #         image_string = base64.b64encode(image.read())
    #         print(image_string.decode())

    #     super().save_model(request, obj, form, change)


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('certificate/handle/<slug:certificate_id>', self.handle_action, name='handle-certificate'),
        ]  # type: List[path]
        return my_urls + urls



    class CustomChangeList(ChangeList):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title = 'Issue Certificate '

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = ""
        return super(GraduateCertificateAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def handle_action(self, request, certificate_id):
        try:
            certificate = GraduateCertificates.objects.get(certificate_id=certificate_id)
        except:
            return Http404(request,'Not found')
        if request.POST.get('action', None) == 'send_mail':
            certificate.mail_certificate()
            certificate.set_as_sent()
            self.message_user(request, 'Certificate sent to user', messages.SUCCESS)
            return redirect('./')
        else:
            return self.preview_certificate(request, certificate)

    def get_changelist(self, request, **kwargs):
        return self.CustomChangeList

    def mail_certificate(self, request, queryset):
        if request.method == 'POST':
            queryset.mail_certificate()
            queryset.set_as_sent()
            self.message_user(request, 'Certificate sent to user', messages.SUCCESS)
        return redirect('./')

    def preview_certificate(self, request, queryset):
        if request.method == 'POST':
            certificate = queryset.generate_certificate()
            from home.utilities import initiate_file_download
            return initiate_file_download(certificate)

        return redirect('./')


admin.site.register(CertificateType)
