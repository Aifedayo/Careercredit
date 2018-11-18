from . import views
from django.urls import path, include

app_name = 'Projects'

grp_patterns = [
    path('', views.listgrpcourses , name='listgrpcourses'),
    path('<slug:course_name>/', views.coursetopics, name='coursetopics'),
    path('<slug:course_name>/<int:tp_id>', views.coursetopics, name='coursetopics2'),
    path('<slug:course_name>/notes/<int:tp_id>', views.topicnotes, name='topicnotes'),
    ]

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:grp_nm>/', include(grp_patterns)),
   
#     path('<slug:course_name>/labs/<int:lab_no>/', login_required(views.LabDetailsView.as_view()), name='labs')
    ]