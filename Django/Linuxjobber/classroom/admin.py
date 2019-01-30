from django.contrib import admin
from .models import DjangoStudent, ChatMessage, ChatRoom, ChatUpload

# Register your models here.
admin.site.register(DjangoStudent)
admin.site.register(ChatMessage)
admin.site.register(ChatRoom)
admin.site.register(ChatUpload)


