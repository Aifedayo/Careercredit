from django.urls import path
from rest_framework.authtoken import views as auth
from . import views

urlpatterns = [

    path('login',views.login),
    path('group',views.groups),
    # path('group',views.GroupUsers.as_view()),
    path('groups',views.GroupUsers.as_view()),
    path('group/<int:pk>/group_users',views.GroupUsers.as_view()),
    path('api-token-auth/',auth.obtain_auth_token)
]