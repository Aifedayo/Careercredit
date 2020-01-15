from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import GraduateCertificates
from home.utilities import initiate_file_download
# Create your views here.
def get_certificate(request,certificate_id):
    try:
        certificate = GraduateCertificates.objects.get(certificate_id=certificate_id)
        return initiate_file_download(certificate.generate_certificate())
    except:
        return HttpResponse( 'Certificate Not Found')



