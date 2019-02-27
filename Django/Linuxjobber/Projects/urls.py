from . import views
from django.urls import path, include

app_name = 'Projects'


urlpatterns = [
    path('', views.project_index, name='index'),
    path('<int:project_id>/course', views.project_courses, name='courses'),
    path('course/<int:course_id>/topics/<int:topic_id>', views.project_course_topics, name='course_topics'),
    # path('<int:course_id>/labs', views.project_course_labs, name='course_labs'),
    path('course/<int:course_id>/topics/<int:topic_id>/notes', views.project_course_notes, name='course_note'),
    path('<int:topic_id>/task', views.course_tasks, name='topic_tasks'),
    ]