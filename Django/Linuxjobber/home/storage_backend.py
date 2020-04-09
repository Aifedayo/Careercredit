from decouple import config
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'media'

class S3UploadStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'uploads'

class MediaStorage(FileSystemStorage):
    location = '/mnt/media'
    file_overwrite = False

    def _save(self, name, content):
        filename = super()._save(name, content)
        if True:
            import subprocess
            import platform
            if platform.system().lower() != 'windows':
                print('file saved')
                # outs = subprocess.Popen(
                #     ["sshpass", "-p", config('SSH_PASSWORD', ''), "ssh", "-o StrictHostKeyChecking=no",
                #      "-o LogLevel=ERROR",
                #      "-o UserKnownHostsFile=/dev/null", config('SSH_USER', '') + "@" + settings.SERVER_IP,
                #      " [ -f /opt/scripts/echo.sh "+config('AWS_STORAGE_BUCKET_NAME','test')+"] && echo $?"], stdin=subprocess.PIPE,
                #     stdout=subprocess.PIPE,
                #     stderr=subprocess.PIPE).communicate()
                #
                # subprocess.Popen(
                #     [
                #     "aws",
                #     's3',
                #     'sync',
                #     '/mnt/media/',
                #     's3://{}/media/'.format(config('AWS_STORAGE_BUCKET_NAME','test'))
                #     ]
                # )

        return filename