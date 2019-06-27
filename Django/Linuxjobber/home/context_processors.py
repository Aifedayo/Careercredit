from Courses.models import Course
from ToolsApp.models import Tool
from home.models import wepeoples
from Projects.models import Project, ProjectCourse

def courses(request):
    return {
        'courses': Course.objects.all()
    }

def tools(request):
	return{
		'tools': Project.objects.filter(show_on_navigation=1),
		'procourse': ProjectCourse.objects.all()
	}


def workexperience(request):
	if request.user.is_authenticated:
		try:
			workexp = wepeoples.objects.get(user=request.user)
			workex = True
		except wepeoples.DoesNotExist:
			workex = False

		
		return{
			'workexp': workex
		}
	else:
		workex = False

		return{
			'workexp': workex
		}