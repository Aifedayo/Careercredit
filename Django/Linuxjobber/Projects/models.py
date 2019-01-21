import os
from django.db import models
# from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import CustomUser
# from django.core.files.storage import FileSystemStorage
# 
# 
# fs = FileSystemStorage(location= settings.BASE_DIR)


def content_file_name(instance, filename):
    return os.path.join('asset','img', filename.replace(" ", "_"))

# def get_model_for_instance(instance):
#     return instance._meta.model

class ProjectGroup(models.Model):
    group_name = models.CharField( max_length=100)
    description = models.TextField()
    background_image = models.ImageField(upload_to = content_file_name )
    icon = models.ImageField(upload_to = content_file_name )
    color = models.CharField(max_length=70)
  
    class Meta:
        verbose_name_plural = 'Project Groups'
     
    def __str__(self):
        return self.group_name
 
 
class ProjectCourse(models.Model):
    course_name = models.CharField( max_length=100)
    projectgroup = models.ForeignKey(ProjectGroup, on_delete = models.CASCADE, related_name='courses',related_query_name='course')
    background_image = models.ImageField(upload_to = content_file_name )
    description = models.TextField()
     
    class Meta:
        verbose_name_plural = 'Project Courses'
     
    def __str__(self):
        return self.course_name
 
 
class ProjectTopic(models.Model):
    title = models.CharField(max_length = 80)
    topic_no = models.PositiveSmallIntegerField()
    project_course = models.ForeignKey(ProjectCourse, on_delete = models.CASCADE, related_name='topics',related_query_name='topic')
    video = models.TextField()
     
    class Meta:
        verbose_name_plural = 'Project Topics'
        ordering = ('id', 'topic_no')
     
    def __str__(self):
        return self.title
 
 
class ProjectNoteGroup(models.Model):
    title = models.CharField(max_length = 80)
    topic = models.ForeignKey(ProjectTopic, on_delete = models.CASCADE, related_name='notegroups',related_query_name='notegroup')
    course = models.ForeignKey(ProjectCourse, on_delete = models.CASCADE, related_name='notegroups',related_query_name='notegroup')
    view_count = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now, null=False)
     
    class Meta:
        verbose_name_plural = 'Project Note Groups'
     
    def __str__(self):
        return self.title
    
    
class ProjectNote(models.Model):
    ngroup = models.ForeignKey(ProjectNoteGroup, on_delete = models.CASCADE, related_name='notes',related_query_name='note')
    n_number = models.PositiveSmallIntegerField()
    info = models.TextField()
    extra = models.TextField()
    todo = models.TextField()
    created = models.DateTimeField(default=timezone.now, null=False)
     
    class Meta:
        verbose_name_plural = 'Project Notes'
        ordering = ('id','n_number')
     
    def __str__(self):
        return 'note number {}'.format(self.n_number)
 
 
class ProjectNComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    project_ng = models.ForeignKey(ProjectNoteGroup, on_delete = models.CASCADE, related_name='comments',related_query_name='comment')
    comment = models.TextField()
    status = models.CharField(max_length = 80)
    created = models.DateTimeField(default=timezone.now, null=False)
     
    class Meta:
        verbose_name_plural = 'Project Note Comments'
     
    def __str__(self):
        return self.comment
    
    