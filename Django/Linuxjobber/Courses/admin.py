from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget


from .models import *

class CourseTopicAdmin(admin.ModelAdmin):
	search_fields = ('course__course_title','topic',)
	list_display = ('topic','course')

class CoursePermissionAdmin(admin.ModelAdmin):
	search_fields = ('user__username','user__email',)
	list_display = ('user','course','permission','expiry_date')

class LabTaskAdmin(admin.ModelAdmin):
	search_fields = ('lab__topic',)

class NoteAdminForm(forms.ModelForm):
	Detail = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = Note
		fields = ['Topic','Detail'] 

class NoteAdmin(admin.ModelAdmin):
	form = NoteAdminForm

class UserInterestAdmin(admin.ModelAdmin):
	list_display = ('user', 'course')

class UserCourseStatAdmin(admin.ModelAdmin):
	list_display = ('user', 'course', 'visit')

class GradesReportAdmin(admin.ModelAdmin):
	list_display = ('user','course_topic','grade')

class LabTaskAdmin(admin.ModelAdmin):
	list_display = ('task', 'lab')

class TopicStatAdmin(admin.ModelAdmin):
	list_display = ('user','topic','last_watched')
	search_fields = ('user__email',)

class CourseSectionAdmin(admin.ModelAdmin):
	list_display = ('course', 'name')

admin.site.register(Course)
admin.site.register(CourseTopic, CourseTopicAdmin)
admin.site.register(CourseDescription)
admin.site.register(CoursePermission, CoursePermissionAdmin)
admin.site.register(LabTask, LabTaskAdmin)
admin.site.register(GradesReport, GradesReportAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(NoteComment)
admin.site.register(TopicStat,TopicStatAdmin)
admin.site.register(UserInterest,UserInterestAdmin)
admin.site.register(UserCourseStat,UserCourseStatAdmin)
admin.site.register(CourseSection,CourseSectionAdmin)