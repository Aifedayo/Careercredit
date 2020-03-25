
from django.conf import settings
from django.template.response import TemplateResponse

from .models import GraduateCertificates
from .utils import generate_certificate_name

# Create your views here.


def get_certificate(request,certificate_id, type = None):
    context = {}
    try:
        certificate = GraduateCertificates.objects.get(certificate_id=certificate_id)
        certificate.generate_certificate()
        certificate.upload_to_s3()
        context['certificate'] = certificate
        certificate_name = generate_certificate_name(certificate)
        # certificate_name_png =  certificate_name + '.png'
        # certificate_name_pdf =  certificate_name + '.pdf'
        # context['image_url'] = certificate.convert_to_media_fqn("/certs/"+certificate_name_png)
        # context['pdf_url'] = certificate.convert_to_media_fqn("/certs/"+certificate_name_pdf)
        s3_path = f"http://{settings.AWS_S3_CUSTOM_DOMAIN}/media/certs/"
        context['image_url'] = f"{s3_path}{certificate_name}.png"
        context['pdf_url'] = f"{s3_path}{certificate_name}.pdf"

    except Exception as e:
        print(e)

    finally:
        return TemplateResponse(request,'certificates/preview_certificate.html',context)
