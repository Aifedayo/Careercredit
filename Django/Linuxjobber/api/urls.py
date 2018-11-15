from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.ListCourses.as_view()),
	path('<int:pk>/', views.DetailCourse.as_view()),
	path('users/', views.ListUser.as_view()),
	path('users/<int:pk>/', views.DetailUser.as_view()),
	path('rest-auth/', include('rest_auth.urls')),
	path('authed-user/<str:tkn>/', views.token_owner),
]