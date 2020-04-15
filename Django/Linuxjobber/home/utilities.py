from django.http import HttpResponse
from django.utils import timezone

from .background_tasks import get_process, UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL, \
    OVERDUE_PAYMENT_NOTIFICATION_SERVICE_LABEL
from .models import Variables
import calendar
import datetime

context = {
    'upcoming_notification_day': 'UPCOMING_NOTIFICATION_DELIVERY_DAY',
    'upcoming_notification_time': 'UPCOMING_NOTIFICATION_DELIVERY_TIME',
    'overdue_notification_day': 'OVERDUE_NOTIFICATION_DELIVERY_DAY',
    'overdue_notification_time': 'OVERDUE_NOTIFICATION_DELIVERY_TIME',
}


def convert_to_day(day: int):
    if day:
        return calendar.day_name[int(day)]

    return 'Invalid'


def convert_to_time(time):
    hour, minute = time.split(',')
    return "{}:{}".format(hour, minute)


def next_weekday(weekday):
    now = timezone.now()
    days_ahead = weekday - now.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7
    elif days_ahead == 0:
        days_ahead = 0
    return now + datetime.timedelta(days_ahead)


def get_upcoming_payment_notification_day():
    try:
        return Variables.objects.get(key=context['notification_day']).value
    except Variables.DoesNotExist:
        return calendar.SUNDAY


def set_payment_notification_schedule(notification_day, notification_hour, notification_minute, on_load=False,
                                      key=None):
    key_auto_created = False
    if key is None:
        key = 'upcoming_notification'
        key_auto_created = True
    day_variable, created = Variables.objects.get_or_create(key=context['{}_day'.format(key)])
    day_variable.value = notification_day
    time_variable, created = Variables.objects.get_or_create(key=context['{}_time'.format(key)])
    time_variable.value = "{},{}".format(notification_hour, notification_minute)
    notification_service = get_process(
        label=UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL if key == 'upcoming_notification' else
        OVERDUE_PAYMENT_NOTIFICATION_SERVICE_LABEL
    )

    if notification_service:
        new_day = next_weekday(notification_day)

        new_day = new_day.replace(hour=int(notification_hour), minute=int(notification_minute))
        notification_service.run_at = new_day

        # If service doesnt exist, or variable is being updated it creates/updates it
        if not on_load or created:
            notification_service.save()
            time_variable.save()
            day_variable.save()

    # Auto sets the value for overdue payment at once
    if key_auto_created:
        set_payment_notification_schedule(
            notification_day, notification_hour, notification_minute, on_load=True, key='overdue_notification'
        )


import base64
# from Crypto.Cipher import AES
# from Crypto import Random
# from Crypto.Protocol.KDF import PBKDF2

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def get_private_key(password):
    salt = bytes(password,'utf8')
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key


def encrypt(raw, password):
    raw=str(raw)
    private_key = get_private_key(password)
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    data = base64.b64encode(iv + cipher.encrypt(raw))
    return data.decode('utf-8')


def decrypt(enc, password):
    enc = str(enc)
    private_key = get_private_key(password)
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(enc[16:]))
    return  data.decode('utf-8')


def get_variable(variable_name,default=None):
    try:
        return Variables.objects.get(key=variable_name)
    except:
        return default


def initiate_file_download(filename):
    from django.utils.encoding import smart_str
    response = HttpResponse(
        content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)

    response['X-Sendfile'] = smart_str(filename)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response


if __name__ == '__main__':
    pass
