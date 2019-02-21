from django.db import models

from users.models import CustomUser


LAB_SUBMISSION= (
        (0, 'none'),
        (1, 'submit by uploading document'),
        (2, 'submit by machine ID'),
        (3, 'submit from repo')
    )


class Project(models.Model):
    project_id = models.IntegerField(unique=True)
    project_title = models.CharField(max_length=100)
    project_description = models.CharField(max_length=500)
    project_image = models.ImageField(upload_to = 'project', null=True)
    project_contents = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ('project_id',)

    def __str__(self):
        return self.project_title



class ProjectCourse(models.Model):
    course_id = models.IntegerField()
    course_title = models.CharField(max_length=100)
    course_description = models.CharField(max_length=250)
    course_objective = models.CharField(max_length=100)
    course_content = models.CharField(max_length=250)
    course_duration = models.CharField(max_length=20)
    course_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    course_image = models.ImageField(upload_to = 'project', null=True)
    lab_submission_type = models.PositiveSmallIntegerField(default=1, choices=LAB_SUBMISSION)


    class Meta:
        unique_together = (('course_id','course_project'),)
        verbose_name_plural = 'Projects Course'

    def __str__(self):
        return self.course_title



class ProjectCourseTopic(models.Model):
    topic_id = models.IntegerField()
    topic_title = models.CharField(max_length=200)
    topic_video = models.CharField(max_length=100)
    topic_course = models.ForeignKey(ProjectCourse,on_delete=models.CASCADE)
    has_notes = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))
    has_labs = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))


    class Meta:
        unique_together = (('topic_id','topic_course'),)
        verbose_name_plural = 'Projects Course Topic'

    def __str__(self):
        return self.topic_title

class CourseTopicNote(models.Model):
    topic = models.ForeignKey(ProjectCourseTopic,on_delete=models.CASCADE)
    detail = models.TextField()

    def __str__(self):
        return self.topic.topic_title

class ProjectPermission(models.Model):
    course = models.ForeignKey(ProjectCourse,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE, limit_choices_to={'role': 4})
    permission = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))

    def __str__(self):
        return self.user.email

class CourseLab(models.Model):
    lab_id = models.IntegerField(unique=True)
    lab_title = models.CharField(max_length=200)
    lab_course = models.ForeignKey(ProjectCourse, on_delete=models.CASCADE)

    def __str__(self):
        return self.lab_title


class CourseLabTask(models.Model):
    task_id = models.IntegerField(unique=True)
    lab_task_no = models.IntegerField(default=1)
    task = models.TextField()
    task_note = models.TextField()
    task_comment = models.TextField()
    task_lab = models.ForeignKey(CourseLab, on_delete=models.CASCADE)
    #lab_task_course = models.ForeignKey(ProjectCourse, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_task



class UsersLabTaskStatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(CourseLabTask, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)



'''
Not making use of this but for some reason i do not know, it just has to sit here so we dont have a migrations error.
'''
def content_file_name(instance, filename):
    return os.path.join('asset','img', filename.replace(" ", "_"))
