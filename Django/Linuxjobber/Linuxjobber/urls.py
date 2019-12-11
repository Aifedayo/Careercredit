"""Linuxjobber URL Configuration

"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import log_in

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
#     path('api/v1/', include('api.urls')), # This is the route to the very first version of Linuxjobber-GroupClass API
    path('courses/', include("Courses.urls")),
    path('projects/', include("Projects.urls")),
    path('tools/', include("ToolsApp.urls")),
    path('classroom/', include("classroom.urls")),
    path('accounts/login/', log_in, name="login" ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sso_api/', include('sso_api.urls')),
]

urlpatterns += staticfiles_urlpatterns()

admin.site.site_header = "Dashboard"
admin.site.site_title = "Linuxjobber Admin Portal"
admin.site.index_title = "Welcome to Linuxjobber Admin Portal"

from home.views import handler_404, handler_500, handler_401
#handler404 = handler_404
#handler500 = handler_500
# handler401 = handler_401



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
