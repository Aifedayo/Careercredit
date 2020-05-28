from background_task.models import Task
from background_task import background

@background()
def send_lab_reports( ):
    print('Hello world')

