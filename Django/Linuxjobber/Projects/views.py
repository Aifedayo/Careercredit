from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Courses.models import Course
from ToolsApp.models import Tool

from .models import *



def get_courses():
    return Course.objects.all()

def get_tools():
    return Tool.objects.all()


#INDEX VIEW
def index(request):
    return render(request, 'projects/index.html', {'project_grps': ProjectGroup.objects.all(), 'courses' : get_courses(), 'tools' : get_tools()})

def listgrpcourses(request, grp_nm):
    context = {'group' : ProjectGroup.objects.get(group_name = grp_nm),
               'courses' : get_courses(),
               'tools' : get_tools(),
               }
    return render(request, 'projects/projectlist.html', context)

@login_required
def coursetopics(request, grp_nm, course_name,tp_id = None):
    course_topics = ProjectCourse.objects.get(course_name = course_name, projectgroup__group_name = grp_nm).topics.all()
    context = {
        'mtopic':ProjectTopic.objects.get(pk = tp_id) if tp_id is not None else course_topics.first(),
        'course_topics': course_topics,
        'courses' : get_courses(),
        'tools' : get_tools(),
        }
    return render(request, 'projects/coursetopics.html', context)

# @login_required
def topicnotes(request,grp_nm, course_name, tp_id):
    topicNotes = ProjectNoteGroup.objects.get(topic_id = tp_id, course__course_name = course_name).notes
    comments = ProjectNoteGroup.objects.get(topic_id = tp_id, course__course_name = course_name).comments
    context = {
        'topic_notes' : topicNotes,
        'comments': comments,
        'courses' : get_courses(),
        'tools' : get_tools(),
        'mtopic': ProjectTopic.objects.get(pk=tp_id),
        }
    return render(request, 'projects/topicnotes.html', context)
    


