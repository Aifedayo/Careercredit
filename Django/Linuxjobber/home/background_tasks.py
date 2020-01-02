from background_task import background
from background_task.models import Task

from home.models import InstallmentPlan

from background_task.models import Task

UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL = 'upcoming_payment_notification_service'


def clear_old_task(match_string):
   Task.objects.filter(task_params__contains=match_string).delete()


@background()
def set_installment_upcoming_payment_notification_service(param):
    # Update the status before sending notification
    InstallmentPlan.refresh_all_plan_status()





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

def activate_service(label,background_funtion,task_repeat=0):
    try:
        process = get_process(label)
    except Task.DoesNotExist:
        clear_old_task(label)
        background_funtion(label,repeat=task_repeat)







