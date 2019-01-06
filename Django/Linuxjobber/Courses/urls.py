from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

app_name = "Courses"

urlpatterns = [
    path('', views.courses,name='courses'),
    path('<slug:course_name>/topics/', login_required(views.CourseTopicsView.as_view()), name='topics'),
    path('<slug:course_name>/topic/<int:lab_no>/', views.topicdetails, name='topic_details'),
    path('<slug:course_name>/notes/<int:lab_no>/', views.TopicNote, name='Note'),
    path('<slug:course_name>/labs/<int:lab_no>/', login_required(views.LabDetailsView.as_view()), name='labs'),
    path('userinterest', views.userinterest, name='userinterest'),
    path('description/<slug:course_name>', views.description, name='description'),
    path('signup', views.signup, name='signup'),
    path('success', views.success, name='success'),
    path('videostat/<int:topic>', views.videostat, name='videostat'),
    path('store_lab_result', views.store_lab_result, name='store_lab_result'),
    path('<slug:course_name>/lab/<int:lab_no>/result', views.linux_result, name='linux_result'),
    path('update/<int:lab_no>', views.linux_result_update, name='linux_result_update'),
    path('topic_stat/<int:lab_no>', views.topic_stat, name='topic_stat'),
    path('task_update/<int:lab_no>/<int:task_no>/', views.task_update, name='task_update'),
    ]