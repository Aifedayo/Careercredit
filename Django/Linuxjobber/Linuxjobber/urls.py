"""Linuxjobber URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
#     path('api/v1/', include('api.urls')), # This is the route to the very first version of Linuxjobber-GroupClass API
    path('courses/', include("Courses.urls")),
    path('projects/', include("Projects.urls")),
    path('tools/', include("ToolsApp.urls")),
    path('classroom/', include("classroom.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sso_api/', include('sso_api.urls')),


]

urlpatterns += staticfiles_urlpatterns()

from home.views import handler_404, handler_500, handler_401
handler404 = handler_404
handler500 = handler_500
handler401 = handler_401


#
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
