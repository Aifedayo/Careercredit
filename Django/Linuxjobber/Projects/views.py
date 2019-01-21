from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Courses.models import Course
from ToolsApp.models import Tool
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import *



def get_courses():
    return Course.objects.all()

def get_tools():
    return Tool.objects.all()

def project_index(request):
    context = {
        'projects': Project.objects.all(),
        'courses': get_courses(),
        'tools': get_tools()
    }
    return render(request, 'projects/index.html', context)



def project_courses(request, project_name):
    project = Project.objects.get(project_title=project_name)
    context = {
        'project_courses': project.projectcourse_set.all(),
        'project_title': project.project_title,
        'project_description': project.project_description,
        'courses': get_courses(),
        'tools': get_tools(),
    }

    return render(request, 'projects/project_courses.html', context)


@login_required
def project_course_topics(request, course_name):
    course = ProjectCourse.objects.get(course_title=course_name.replace("_", " "))
    context = {
        'course_topics': course.projectcoursetopic_set.all(),
        'course_title': course.course_title,
        'course_description': course.course_description,
        'project_title': course.course_project.project_title,
        'courses': get_courses(),
        'tools': get_tools(),

    }

    if request.user.role == 4:
        if course.course_project.project_id != request.user.allowed_project:
            return render(request, 'projects/project_access_denied.html') #you are not allowed to view this page
        else:
            contx = {
                'course_topics': course.projectcoursetopic_set.all(),
                'course_title': course.course_title,
                'course_description': course.course_description,
                'project_title': course.course_project.project_title,
                'courses': get_courses(),
                'tools': get_tools(),
            }
            return render(request, 'projects/project_course_topics.html', contx)
    elif request.user.role == 3:
        return render(request, 'projects/project_course_topics.html', context)
    else:
        return redirect("home:tryfree",'standardPlan')



@login_required
def project_course_labs(request, course_name):
    course = ProjectCourse.objects.get(course_title=course_name.replace("_", " ")) 

    context = {
        'course_labs': course.courselab_set.all(),
        'course_title': course.course_title,
        'course_description': course.course_description,
        'courses': get_courses(),
        'tools': get_tools(),
    }

    if request.user.role == 4:
        if course.course_project.project_id != request.user.allowed_project:
            return render(request, 'projects/project_access_denied.html') #you are not allowed to view this page
        else:
            contx = {
                'course_labs': course.courselab_set.all(),
                'course_title': course.course_title,
                'course_description': course.course_description,
                'courses': get_courses(),
                'tools': get_tools(),
            }
            return render(request, 'projects/project_course_labs.html', contx)
    elif request.user.role == 3:
        return render(request, 'projects/project_course_labs.html', context)
    else:
        return redirect("home:tryfree",'standardPlan')


@login_required
def course_lab_tasks(request, lab_title):
    lab = CourseLab.objects.get(lab_title=lab_title.replace("_", " ")) 

    context = {
        'lab_tasks': lab.courselabtask_set.all(),
        'courses': get_courses(),
        'tools': get_tools(),
    }


    return render(request, 'projects/course_lab_tasks.html', context)