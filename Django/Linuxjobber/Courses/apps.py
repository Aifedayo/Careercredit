from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'Courses'

    def ready(self):

        # Upcoming payments notification activation
        from .tasks import send_lab_reports
        from background_task.models import Task
        from datetime import timedelta
        try:
            send_lab_reports(schedule= timedelta(hours=12))

        except Exception as e:
            print(e)
