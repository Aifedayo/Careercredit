from django.urls import path
from rest_framework.authtoken import views as auth
from . import views

urlpatterns = [
    path('login',views.login),
    path('upload',views.MyUploadView.as_view()),
    path('groups',views.UserGroups.as_view()),
    path('user/',views.UserView.as_view()),
    path('user/upload',views.UserView.as_view()),
    path('user/<int:user_id>',views.UserView.as_view()),
    path('group/<int:group_id>',views.GroupCourseDetail.as_view()),
    path('group/<int:group_id>/detail',views.GroupDetail.as_view()),
    path('group/<int:group_id>/users',views.GroupMembers.as_view()),
    path('group/<int:group_id>/users2',views.GroupUsers.as_view()),
    path('group/<int:group_id>/userlog/',views.UserAttendance.as_view()),
    path('group/<int:group_id>/userlog/<int:user_id>',views.UserAttendance.as_view()),
    path('confirm_key',views.confirm_api),
    path('api-token-auth',auth.obtain_auth_token)
]