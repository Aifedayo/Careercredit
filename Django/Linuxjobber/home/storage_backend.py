from django.core.files.storage import FileSystemStorage


class MediaStorage(FileSystemStorage):
    location = '/mnt/media'
    file_overwrite = False