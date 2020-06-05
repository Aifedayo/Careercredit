from django.contrib import admin
from .models import DjangoStudent, ChatMessage, ChatRoom, ChatUpload, Course, AttendanceLog

# Register your models here.
admin.site.register(Course)
admin.site.register(DjangoStudent)
admin.site.register(ChatMessage)
admin.site.register(ChatRoom)
admin.site.register(ChatUpload)



