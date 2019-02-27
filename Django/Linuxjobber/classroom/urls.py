from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.permissions import IsAuthenticatedOrReadOnly

app_name = "classroom"

def_router = DefaultRouter()
def_router.register('djangostudent', views.DjangoStudentViewSet)




urlpatterns = [
    path('', views.classroom_index, name='index'),
    path('<int:course_id>/course', views.course_topics, name='courses'),
    url(r'djangostudent-api/', include(def_router.urls)),
    url(r'api-token-auth/', obtain_jwt_token),
]