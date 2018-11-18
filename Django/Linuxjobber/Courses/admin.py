from django.contrib import admin

from .models import *

admin.site.register(Course)
admin.site.register(CourseTopic)
admin.site.register(LabTask)
admin.site.register(GradesReport)