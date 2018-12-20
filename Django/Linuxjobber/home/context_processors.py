from Courses.models import Course
from ToolsApp.models import Tool

def courses(request):
    return {
        'courses': Course.objects.all()
    }

def tools(request):
	return{
		'tools': Tool.objects.all()
	}