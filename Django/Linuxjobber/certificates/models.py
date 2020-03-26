from io import BytesIO
import os
import boto3
import botocore
from django.db import models

# Create your models here.
from django.template.loader import get_template
from django.utils import html
from users.models import CustomUser
from home.utilities import get_variable
from django.conf import settings
from home.mail_service import LinuxjobberMailer
from .utils import generate_certificate_name
from weasyprint import CSS

from xhtml2pdf import pisa


def render_to_pdf(source, result):
    pisaStatus = pisa.CreatePDF(
            source,                # the HTML to convert
            dest=result)           # file handle to recieve result
    return pisaStatus.err

class CertificateType(models.Model):
    name = models.CharField(max_length=200)
    instructor_name = models.CharField(max_length=200)
    instructor_signature = models.ImageField()
    instructor_role = models.CharField(max_length=200, null=True)
    logo = models.ImageField()

    def __str__(self):
        return self.name


class GraduateCertificates(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    certificate_type = models.ForeignKey(CertificateType, on_delete=models.CASCADE)
    certificate_id = models.CharField(max_length=10, null=True, blank=True)
    alternate_graduate_image = models.ImageField(
        upload_to='certs/', null=True, blank=True
    )
    graduation_date = models.DateField()
    alternate_email = models.EmailField(null=True, blank=True)
    alternate_full_name = models.CharField(max_length=255, null=True, blank=True)
    is_draft = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    @staticmethod
    def generate_certificate_number():
        is_unique = False

        def randomStringDigits(stringLength=6):
            import string
            import random
            """Generate a random string of letters and digits """
            lettersAndDigits = string.ascii_letters + string.digits
            return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

        # Length can be set in variables model in the admin page CERTIFICATE_ID_LENGTH
        id_length = get_variable('CERTIFICATE_ID_LENGTH', 6)

        while not is_unique:
            generated_id = randomStringDigits(id_length)
            if generated_id not in GraduateCertificates.objects.values_list('certificate_id'):
                is_unique = True
                return generated_id

    def get_email(self):
        if self.user:
            return self.user.email
        else:
            return self.alternate_email

    def get_fullname(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return self.alternate_full_name

    def get_instructor_logo(self):
        if settings.DEBUG:
            return self.certificate_type.instructor_role.url
        return self.certificate_type.instructor_role.url

    def get_graduate_image(self):
        if self.user:
            return self.user.profile_img
        return self.alternate_graduate_image.url

    def convert_to_fqn(self, url):

        return "{}{}".format(
                settings.ENV_URL.rstrip('/'),
                url
            )

    def convert_to_media_fqn(self,url):
        if settings.DEBUG:
            return "{}{}".format(
                settings.ENV_URL.rstrip('/'),
                url
            )
        return url


    def generate_certificate(self):
        try:

            template = get_template('certificates/certificate_format.html')
            images = self.get_logo_and_signature_from_s3()
            certificate_logo = images['logo']
            instructor_signature = images['instructor_signature']
            graduate_image= images['alternate_graduate_image']
            context={
                'certificate_logo': certificate_logo,
                'env_url': settings.ENV_URL.rstrip('/'),
                'static_url': settings.STATIC_URL,
                'certificate_name': self.certificate_type.name,
                'instructor_signature': instructor_signature,
                'instructor_name': self.certificate_type.instructor_name,
                'instructor_role': self.certificate_type.instructor_role,
                'graduate_name': self.get_fullname(),
                'certificate_id': self.certificate_id,
                'issue_date': self.graduation_date,
                'graduate_image': graduate_image,
            }
            formatted_file = template.render(context)
            filename_pdf = "/mnt/media/" + generate_certificate_name(self) + ".pdf"
            filename_html = filename_pdf.replace('pdf', 'html')
            filename_png = filename_pdf.replace('pdf', 'png')

            with open(filename_html, 'w') as certificate_file:
                certificate_file.write(formatted_file)

            from weasyprint import HTML, CSS
            html_file = HTML(filename_html)
            css = CSS(string='@page { size: A3; width: 40cm; align: center; margin-left: 2cm; margin-right: 0 }')
            import os
            if filename_pdf not in os.listdir('/mnt/media'):
                html_file.write_pdf(
                  filename_pdf, stylesheets=[css]
                )
                html_file.write_png(
                  filename_png, stylesheets=[css]
                )
            return True
        except Exception as e:
            print(e)
            return False



        # is_success = False
        # with open(filename_pdf, 'wb') as certificate_file:
        #     is_success=render_to_pdf(formatted_file,certificate_file)
        # if is_success:
        #     return filename_pdf
        # return None

    def get_logo_and_signature_from_s3(self):
        files = [
            self.certificate_type.logo,
            self.certificate_type.instructor_signature,
            self.alternate_graduate_image
        ]

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        location = settings.AWS_LOCATION

        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.S3DIRECT_REGION
        )

        s3 = session.resource('s3')

        for f in files:
            try:
                s3.Bucket(bucket).download_file(
                    f'{location}/{str(f)}',f'/mnt/media/{str(f)}'
                )
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise

        return {
            'logo':str(files[0]),
            'instructor_signature':str(files[1]),
            'alternate_graduate_image':str(files[2])
        }

    def upload_to_s3(self):
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.S3DIRECT_REGION
        )
        s3 = session.resource('s3')
        bucket = str(settings.AWS_STORAGE_BUCKET_NAME)
        filename = generate_certificate_name(self)
               
        for ext in ['pdf','png']:
            s3.Bucket(bucket).upload_file(
                f"/mnt/media/{filename}.{ext}", 
                f"media/certs/{filename}.{ext}",
                ExtraArgs={'ACL':settings.AWS_DEFAULT_ACL}
            )

    def set_as_sent(self):
        self.is_sent = True
        self.save()

    def mail_certificate(self):

        mail_message = """
        Congratulations {fullname},

        You have successfully completed {certificate} and earned a certificate.

        You can download your certificate from here

        {env_url}/certificates/preview/{certificate_id}

        Best Regards
        Admin.

        """.format(
            fullname=self.get_fullname(),
            certificate_id=self.certificate_id,
            env_url=settings.ENV_URL.rstrip('/'),
            certificate=self.certificate_type
        )
        mailer = LinuxjobberMailer(
            subject="Congratulations! Certificate Issued to you",
            to_address=self.get_email(),
            header_text="Linuxjobber",
            type=None,
            message=mail_message
        )
        mailer.send_mail()

    def save(self, *args, **kwargs):
        """
        Generates a certificate id to be used
        :param args:
        :param kwargs:
        :return:
        """
        if not self.pk:
            self.certificate_id = GraduateCertificates.generate_certificate_number()

        super(type(self), self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Issue Certificate'
        verbose_name_plural = 'Issue Certificates'
