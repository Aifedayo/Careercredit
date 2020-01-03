from django.utils import timezone

from .background_tasks import get_process, UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL,\
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


def set_payment_notification_schedule(notification_day,notification_time,on_load = False,key=None):
    key_auto_created = False
    if key is None:
        key = 'upcoming_notification'
        key_auto_created = True
    day_variable, created = Variables.objects.get_or_create(key=context['{}_day'.format(key)])
    day_variable.value = notification_day
    time_variable, created = Variables.objects.get_or_create(key=context['{}_time'.format(key)])
    time_variable.value = notification_time
    notification_service = get_process(
        label=UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL if key == 'upcoming_notification' else
        OVERDUE_PAYMENT_NOTIFICATION_SERVICE_LABEL
    )

    if notification_service:
        new_day = next_weekday(notification_day)
        hour, minute = notification_time.split(',')
        new_day = new_day.replace(hour=int(hour), minute=int(minute))
        notification_service.run_at = new_day

        # If service doesnt exist, or variable is being updated it creates it
        if not on_load or created:
            notification_service.save()
            time_variable.save()
            day_variable.save()

    # Auto sets the value for overdue payment at once
    if key_auto_created:
        set_payment_notification_schedule(
            notification_day,notification_time,on_load=True,key='overdue_notification'
        )

if __name__ == '__main__':
    pass
