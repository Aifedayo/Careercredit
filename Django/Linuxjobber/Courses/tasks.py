from background_task.models import Task
from background_task import background
from .models import GradesReport

@background()
def send_lab_reports( ):
    try:
        GradesReport.send_lab_report()
    except:
        pass

