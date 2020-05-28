from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'Courses'

    def ready(self):

        # Upcoming payments notification activation
        # from .tasks import send_lab_reports
        from background_task.models import Task
        try:
            pass
            # send_lab_reports(schedule= 120)
        except Exception as e:
            print(e)
