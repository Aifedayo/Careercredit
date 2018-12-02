import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import CustomUser
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/media/uploads')

LAB_SUBMISSION= (
        (1, 'submit by uploading document'),
        (2, 'submit by machine ID'),
        (3, 'submit from repo')
    )

class Course(models.Model):
    course_title = models.CharField(max_length = 200)
    lab_submission_type = models.PositiveSmallIntegerField(default=1, choices=LAB_SUBMISSION)
    
    class Meta:
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return self.course_title

class CoursePermission(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE, limit_choices_to={'role': 4})
    permission = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))

    def __str__(self):
        return self.user.email



class CourseTopic(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name='topics',related_query_name='topic')
    topic_number = models.PositiveSmallIntegerField(default=0)
    topic =  models.CharField(max_length = 200)
    lab_name = models.CharField(max_length = 50)
    video = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Course Topics'
    
    def __str__(self):
        return self.topic

class Note(models.Model):
    Topic = models.OneToOneField(CourseTopic, on_delete = models.CASCADE)
    Detail = models.TextField()

    def __str__(self):
        return self.Topic.topic


class NoteComment(models.Model):
    User = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    Note = models.ForeignKey(Note, on_delete = models.CASCADE)
    Comment = models.CharField(max_length = 200)

    def __str__(self):
        return self.Comment


class CourseDescription(models.Model):
    course = models.OneToOneField(Course, on_delete = models.CASCADE)
    course_detail = models.TextField()
    why_course = models.TextField()
    opportunity = models.TextField()
    prerequisite = models.TextField()
    course_duration = models.PositiveSmallIntegerField()
    study_plan = models.TextField()
    salary = models.IntegerField(default=0)
    salary_source = models.CharField(max_length = 200)
    syllabus_content = models.TextField()
    syllabus_topic = models.TextField()
    certificate = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.course.course_title 


class LabTask(models.Model):
    lab = models.ForeignKey(CourseTopic, on_delete = models.CASCADE, related_name='tasks',related_query_name='task')
    task_number = models.PositiveSmallIntegerField()
    comment = models.TextField()
    note = models.TextField(null = True, blank = True)
    task = models.TextField()
    xpected = models.TextField(default="Nil")
    hint = models.TextField(null = True, blank = True)
    instruction = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Lab Tasks'
        ordering = ('lab_id', 'task_number')
        
    def __str__(self):
        return self.task
    
    
class GradesReport(models.Model):
    date = models.DateTimeField(default=timezone.now, null=False)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    course_topic = models.ForeignKey(CourseTopic, on_delete = models.CASCADE, related_name='grades',related_query_name='grade')
    score = models.PositiveSmallIntegerField(default=0)
    grade = models.CharField(default='not graded', max_length=20)
    
    class Meta:
        verbose_name_plural = 'Grades Reports'
    
    def __str__(self):
        return self.grade, self.date, self.score


def content_file_name(instance, filename):
    ext = ''
    if instance.course_topic.topic_number == 4:
        ext = 'py'
    elif instance.course_topic.topic_number > 4 and instance.course_topic.topic_number < 7 :
        ext = 'sql'
    else:
        if filename.endswith('.zip'):
            ext = 'zip'
        elif filename.endswith('tar'):
            ext = 'tar'
        else:
            ext = 'gz'
    filename = "%s_%s.%s" % (instance.user.username, instance.course_topic.topic_number, ext)
    return os.path.join('uploads', filename)


class Document(models.Model):
    course_topic = models.ForeignKey(CourseTopic, on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    document = models.FileField(upload_to = content_file_name )
    uploaded_at = models.DateTimeField(auto_now_add = True)


class MainModel(models.Model):
    title = models.CharField(max_length = 42)
    document = models.ForeignKey(Document, on_delete = models.CASCADE)

