from django.shortcuts import render, get_object_or_404
from .models import Tool, ToolTopic
from django.views import generic
from django.contrib.auth.decorators import login_required
from Courses.models import Course

# Create your views here.


def get_courses():
    return Course.objects.all()

def get_tools():
    return Tool.objects.all()


def tools(request):
    tools = Tool.objects.all()
    context ={
            'tools': tools    
            }
    return render(request, 'toolsapp/tools.html', context)


class ToolTopicsView(generic.ListView):
    template_name = 'toolsapp/topics.html'
 
    def get_queryset(self):
        return ToolTopic.objects.filter(tool__tool_name = self.kwargs.get('tool_name').replace("_", " "))
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tool'] = Tool.objects.get(tool_name = self.kwargs.get('tool_name').replace("_", " "))
        context['tools'] = get_tools()
        context['courses'] = get_courses()
        return context


@login_required
def topicdetails(request, tool_name, lab_no):
    context ={
            'topic': ToolTopic.objects.get(tool__tool_name = tool_name.replace("_"," "),topic_number = lab_no),
            'next_vid' : ToolTopic.objects.filter(tool__tool_name = tool_name.replace("_", " ")),
            'courses' : get_courses(),
            'tools' : get_tools(),
            }
    return render(request, 'toolsapp/topic_detail.html', context)




class LabDetailsView(generic.DetailView):
    template_name = 'toolsapp/tasks.html'
    
    def get_object(self):
        return get_object_or_404(ToolTopic, tool__tool_name = self.kwargs.get('tool_name').replace("_", " "),topic_number = self.kwargs.get('lab_no'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tools'] = get_tools()
        context['courses'] = get_courses()
        #context['form'] = get_gradingform(context['coursetopic'], self.request.user)
        return context