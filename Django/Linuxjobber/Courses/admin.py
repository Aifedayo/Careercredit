from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget


from .models import *

class CourseTopicAdmin(admin.ModelAdmin):
	search_fields = ('course__course_title','topic',)

class CoursePermissionAdmin(admin.ModelAdmin):
	search_fields = ('user__username','user__email',)
	list_display = ('user','course','permission')

class LabTaskAdmin(admin.ModelAdmin):
	search_fields = ('lab__topic',)

class NoteAdminForm(forms.ModelForm):
	Detail = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = Note
		fields = ['Topic','Detail'] 

class NoteAdmin(admin.ModelAdmin):
	form = NoteAdminForm

admin.site.register(Course)
admin.site.register(CourseTopic, CourseTopicAdmin)
admin.site.register(CourseDescription)
admin.site.register(CoursePermission, CoursePermissionAdmin)
admin.site.register(LabTask, LabTaskAdmin)
admin.site.register(GradesReport)
admin.site.register(Note, NoteAdmin)
admin.site.register(NoteComment)