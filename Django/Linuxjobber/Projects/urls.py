from . import views
from django.urls import path, include

app_name = 'Projects'


urlpatterns = [
    path('', views.project_index, name='index'),
    path('<int:project_id>/course', views.project_courses, name='courses'),
    path('course/<int:course_id>/topics/<int:topic_id>', views.project_course_topics, name='course_topics'),
    path('<slug:course_name>/labs', views.project_course_labs, name='course_labs'),
    path('course/<int:course_id>/topics/<int:topic_id>/notes', views.project_course_notes, name='course_note'),
    # path('<slug:lab_title>/lab_tasks', views.course_lab_tasks , name='lab_tasks'),
    path('projects/<slug:project_name>', views.project_courses, name='courses'),
    path('<slug:course_name>', views.project_course_topics, name='course_topics'),
    path('<slug:course_name>/labs', views.project_course_labs, name='course_labs'),
    path('<slug:topic_id>/lab_tasks', views.lab_task, name='lab_tasks'),

    ]