from . import views
from django.urls import path, include

app_name = 'Projects'


urlpatterns = [
    path('', views.project_index, name='index'),
    path('projects/<slug:project_name>', views.project_courses, name='courses'),
    path('<slug:course_name>/course', views.project_course_topics, name='course_topics'),
    path('<slug:course_name>/labs', views.project_course_labs, name='course_labs'),
    path('<slug:lab_title>/lab_tasks', views.course_lab_tasks , name='lab_tasks'),

    ]