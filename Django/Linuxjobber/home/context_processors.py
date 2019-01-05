from Courses.models import Course
from ToolsApp.models import Tool
from home.models import wepeoples

def courses(request):
    return {
        'courses': Course.objects.all()
    }

def tools(request):
	return{
		'tools': Tool.objects.all()
	}

def workexperience(request):
	try:
		workexp = wepeoples.objects.get(user=request.user)
		workex = True
	except wepeoples.DoesNotExist:
		workex = False

	
	return{
		'workexp': workex
	}