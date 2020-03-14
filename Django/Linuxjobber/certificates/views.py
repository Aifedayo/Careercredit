
from django.template.response import TemplateResponse

from .models import GraduateCertificates
# Create your views here.

from  .utils import generate_certificate_name

def get_certificate(request,certificate_id, type = None):
    context = {}
    try:
        certificate = GraduateCertificates.objects.get(certificate_id=certificate_id)
        certificate.generate_certificate()
        context['certificate'] = certificate
        certificate_name = generate_certificate_name(certificate)
        certificate_name_png =  certificate_name + '.png'
        certificate_name_pdf =  certificate_name + '.pdf'
        context['image_url'] = certificate.convert_to_media_fqn("/media/certs/"+certificate_name_png)
        context['pdf_url'] = certificate.convert_to_media_fqn("/media/certs/"+certificate_name_pdf)


    except Exception as e:
        print(e)

    finally:
        return TemplateResponse(request,'certificates/preview_certificate.html',context)

