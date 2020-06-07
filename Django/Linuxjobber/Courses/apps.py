from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'Courses'

    def ready(self):

        # Upcoming payments notification activation
        from .tasks import send_lab_reports_out, activate_service, SEND_GRADE_REPORTS_TO_STUDENTS_N_INSTRUCTORS
        from background_task.models import Task
        from datetime import timedelta
        try:
            activate_service(
                label=SEND_GRADE_REPORTS_TO_STUDENTS_N_INSTRUCTORS,
                background_function=send_lab_reports,
                task_repeat=Task.DAILY
            )

        except Exception as e:
            print(e)
