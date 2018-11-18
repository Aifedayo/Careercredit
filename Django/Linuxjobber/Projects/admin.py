from django.contrib import admin

from .models import *

admin.site.register(ProjectGroup)
admin.site.register(ProjectCourse)
admin.site.register(ProjectTopic)
admin.site.register(ProjectNoteGroup)
admin.site.register(ProjectNote)
admin.site.register(ProjectNComment)