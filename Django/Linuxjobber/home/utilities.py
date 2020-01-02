from django.utils import timezone

from .background_tasks import get_process, UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL
from .models import Variables
import calendar
import datetime

context = {
    'upcoming_notification_day': 'UPCOMING_NOTIFICATION_SERVICE_DELIVERY_DAY',
    'upcoming_notification_time': 'UPCOMING_NOTIFICATION_SERVICE_DELIVERY_TIME',
}


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


def set_upcoming_payment_notification_schedule(notification_day, notification_time):
    day_variable, created = Variables.objects.get_or_create(key=context['upcoming_notification_day'])
    day_variable.value = notification_day
    day_variable.save()
    time_variable, created = Variables.objects.get_or_create(key=context['upcoming_notification_time'])
    time_variable.value = notification_day
    time_variable.save()
    notification_service = get_process(
        label=UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL
    )
    if notification_service:
        new_day = next_weekday(notification_day)
        hour, minute = notification_time.split(',')
        new_day = new_day.replace(hour=int(hour), minute=int(minute))
        notification_service.run_at = new_day
        notification_service.save()


if __name__ == '__main__':
    pass
