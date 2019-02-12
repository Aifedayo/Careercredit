from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import *

class NoteForm(forms.ModelForm):
	detail = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = CourseTopicNote
		fields = ['topic','detail'] 

class CourseTopicNoteAdmin(admin.ModelAdmin):
	form = NoteForm

admin.site.register(Project)
admin.site.register(ProjectCourse)
admin.site.register(LabTask)
# admin.site.register(CourseLab)
# admin.site.register(CourseLabTask)
admin.site.register(ProjectCourseTopic)
admin.site.register(CourseTopicNote, CourseTopicNoteAdmin)
admin.site.register(UsersLabTaskStatus)
admin.site.register(ProjectPermission)