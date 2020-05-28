from background_task import background
from background_task.models import Task
from django.utils import timezone

from home.models import InstallmentPlan

from background_task.models import Task

UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL = 'upcoming_payment_notification_service'
OVERDUE_PAYMENT_NOTIFICATION_SERVICE_LABEL = 'overdue_payment_notification_service'


def clear_old_task(match_string):
   Task.objects.filter(task_params__contains=match_string).delete()




@background()
def set_installment_upcoming_payment_notification_service(param):

    """
    The time of the week the notification should be sent is saved Variables model as

    UPCOMING_NOTIFICATION_SERVICE_DELIVERY_DAY = [ Sunday| Monday| Tuesday...]
    UPCOMING_NOTIFICATION_SERVICE_DELIVERY_TIME = [ 00:00| 01:00| 02:00...]

    :param param:
    :return:
    """

    # Update the status before sending notification
    try:
        InstallmentPlan.send_all_users_notification_on_upcoming_payments()
    except:
        pass

@background()
def set_installment_overdue_payment_notification_service(param):

    """
    The time of the week the notification should be sent is saved Variables model as

    OVERDUE_NOTIFICATION_DELIVERY_DAY = [ Sunday| Monday| Tuesday...]
    OVERDUE_NOTIFICATION_DELIVERY_TIME = [ 00:00| 01:00| 02:00...]

    :param param:
    :return:
    """

    # Update the status before sending notification
    try:
        InstallmentPlan.send_all_users_notification_on_overdue_payments()
    except:
        pass








# def get_upcoming_payment_notification_service_process():
# #     try:
# #         return Task.objects.get(task_params__contains=UPCOMING_PAYMENT_LABEL)
# #     except:
# #         return None

def get_process(label):
    try:
        return Task.objects.get(task_params__contains=label)
    except:
        return None


# def activate_upcoming_payment_notification_service_process():
#     try:
#         task = get_upcoming_payment_notification_service_process()
#
#     except Task.DoesNotExist:
#         clear_old_task(UPCOMING_PAYMENT_LABEL)
#         set_installment_upcoming_payment_notification_service(UPCOMING_PAYMENT_LABEL,repeat=Task.WEEKLY)

def activate_service(label,background_function,task_repeat=0,schedule=86400):
    process = get_process(label)
    if not process:
        clear_old_task(label)
        background_function(label,repeat=task_repeat,schedule=schedule)






