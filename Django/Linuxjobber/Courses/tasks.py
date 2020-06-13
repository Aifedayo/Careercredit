from background_task.models import Task
from background_task import background
from .models import GradesReport
from datetime import timedelta

SEND_GRADE_REPORTS_TO_STUDENTS_N_INSTRUCTORS = 'send_grade_reports_to_students_n_instructors_label'

def clear_old_task(match_string):
   Task.objects.filter(task_params__contains=match_string).delete()

@background()
def send_lab_reports_out(param):
    try:
        GradesReport.send_lab_report()
    except:
        pass

def get_process(label):
    try:
        return Task.objects.get(task_params__contains=label)
    except:
        return None

def activate_service(label,background_function,task_repeat=0,schedule=21600 ):  #timedelta(minutes=1)):
    process = get_process(label)
    # print(process)
    if not process:
        clear_old_task(label)
        background_function(label,repeat=task_repeat,schedule=schedule)