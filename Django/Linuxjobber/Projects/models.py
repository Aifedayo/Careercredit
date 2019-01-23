from django.db import models

from users.models import CustomUser


class Project(models.Model):
    project_id = models.IntegerField(unique=True)
    project_title = models.CharField(max_length=100)
    project_description = models.CharField(max_length=500)
    project_image = models.TextField(max_length=500)
    project_bg_image = models.TextField(max_length=500)
    project_contents = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.project_title



class ProjectCourse(models.Model):
    course_id = models.IntegerField(unique=True)
    course_title = models.CharField(max_length=100)
    course_description = models.CharField(max_length=500)
    course_objective = models.CharField(max_length=100)
    course_content = models.CharField(max_length=500)
    course_duration = models.CharField(max_length=20)
    course_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    course_image = models.TextField(max_length=1000)


    class Meta:
        verbose_name_plural = 'Projects Course'

    def __str__(self):
        return self.course_title



class ProjectCourseTopic(models.Model):
    topic_id = models.IntegerField(unique=True)
    topic_title = models.CharField(max_length=200)
    topic_video = models.CharField(max_length=100)
    topic_course = models.ForeignKey(ProjectCourse,on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = 'Projects Course Topic'

    def __str__(self):
        return self.topic_title


class CourseLab(models.Model):
    lab_id = models.IntegerField(unique=True)
    lab_title = models.CharField(max_length=200)  
    lab_course = models.ForeignKey(ProjectCourse, on_delete=models.CASCADE)

    def __str__(self):
        return self.lab_title



class CourseLabTask(models.Model):
    task_id = models.IntegerField(unique=True)
    task = models.TextField()
    task_note = models.TextField()
    task_comment = models.TextField()
    task_lab = models.ForeignKey(CourseLab, on_delete=models.CASCADE)
    #lab_task_course = models.ForeignKey(ProjectCourse, on_delete=models.CASCADE)







'''
Not making use of this but for some reason i do not know, it just has to sit here so we dont have a migrations error.
'''
def content_file_name(instance, filename):
    return os.path.join('asset','img', filename.replace(" ", "_"))
