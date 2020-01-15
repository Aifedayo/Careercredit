from django.urls import path

app_name = 'certificates'
from . import views

urlpatterns = [
    path('preview/<slug:certificate_id>', views.get_certificate, name='download-certificate')
]
