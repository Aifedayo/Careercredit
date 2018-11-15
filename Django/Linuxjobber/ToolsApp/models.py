from django.db import models

# Create your models here.

class Tool(models.Model):
    tool_name = models.CharField(max_length = 200)
    
    class Meta:
        verbose_name_plural = 'Tools'
    
    def __str__(self):
        return self.tool_name



class ToolTopic(models.Model):
    tool = models.ForeignKey(Tool, on_delete = models.CASCADE, related_name='tools_app_topics',related_query_name='tools_app_topic')
    topic_number = models.PositiveSmallIntegerField(default=0)
    topic =  models.CharField(max_length = 200)
    lab_name = models.CharField(max_length = 50)
    video = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Tool Topics'
    
    def __str__(self):
        return self.topic




class LabTask(models.Model):
    lab = models.ForeignKey(ToolTopic, on_delete = models.CASCADE, related_name='tools_app_tasks',related_query_name='tools_app_task')
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