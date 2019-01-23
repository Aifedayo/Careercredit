from django.contrib import admin

from .models import *

admin.site.register(Project)
admin.site.register(ProjectCourse)
admin.site.register(CourseLab)
admin.site.register(CourseLabTask)
admin.site.register(ProjectCourseTopic)
admin.site.register(UsersLabTaskStatus)