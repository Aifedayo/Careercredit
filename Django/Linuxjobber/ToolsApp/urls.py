from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

app_name = 'ToolsApp'

urlpatterns = [
    path('', views.tools, name='tools'),
    path('<slug:tool_name>/topics/', login_required(views.ToolTopicsView.as_view()), name='topics'),
    path('<slug:tool_name>/topic/<int:lab_no>/', views.topicdetails, name='topic_details'),
    path('<slug:tool_name>/labs/<int:lab_no>/', login_required(views.LabDetailsView.as_view()), name='labs')
    ]