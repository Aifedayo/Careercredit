from decouple import config
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class MediaStorage(FileSystemStorage):
    location = '/mnt/media'
    file_overwrite = False

    def _save(self, name, content):
        filename = super()._save(name, content)
        if not settings.DEBUG:
            import subprocess
            import platform
            if platform.system().lower() != 'windows':
                try:
                    outs = subprocess.Popen(
                        ["sshpass", "-p", config('SSH_PASSWORD', ''), "ssh", "-o StrictHostKeyChecking=no",
                         "-o LogLevel=ERROR",
                         "-o UserKnownHostsFile=/dev/null", config('SSH_USER', '') + "@" + settings.SERVER_IP,
                         " [ -f /opt/scripts/s3_sync_media_files.sh ] && echo $?"], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE).communicate()
                except:
                    pass
        return filename