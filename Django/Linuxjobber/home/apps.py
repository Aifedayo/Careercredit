from django.apps import AppConfig



class HomeConfig(AppConfig):
    name = 'home'
    app_label='home'

    def get_urls(self,urllist=None, depth=0, app="", store=None):
        from Linuxjobber.urls import urlpatterns
        import pickle
        if store is None:
            store = []
        if urllist is None:
            urllist = urlpatterns
        for entry in urllist:
            if hasattr(entry, 'app_name'):
                if entry.app_name is not None:
                    app = entry.app_name
            if hasattr(entry, 'name'):
                if entry.name is not None:
                    store.append("{}:{}".format(str(app), str(entry.name)))
            if hasattr(entry, 'url_patterns'):
                self.get_urls(entry.url_patterns, depth + 1, app, store)
        return sorted(store)

    def ready(self):
        from Linuxjobber.urls import urlpatterns
        import pickle
        with open('urls_tmp', 'wb') as url_tmp:
            print('Proxy URLS loading')
            # Remove admin routes
            items = [url for url in self.get_urls(urlpatterns) if not url.startswith('admin')]
            pickle.dump(items, url_tmp)

        # Background tasks are activated here

        from .background_tasks import activate_service,set_installment_upcoming_payment_notification_service,\
            UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL,OVERDUE_PAYMENT_NOTIFICATION_SERVICE_LABEL,\
            set_installment_overdue_payment_notification_service
        from background_task.models import Task
        from .utilities import set_payment_notification_schedule
        import calendar

        # Upcoming payments notification activation
        try:

            activate_service(
                label=UPCOMING_PAYMENT_NOTIFICATION_SERVICE_LABEL,
                background_function=set_installment_upcoming_payment_notification_service,
                task_repeat=Task.WEEKLY
            )
            # Overdue payments notification activation
            activate_service(
                label=OVERDUE_PAYMENT_NOTIFICATION_SERVICE_LABEL,
                background_function=set_installment_overdue_payment_notification_service,
                task_repeat=Task.WEEKLY
            )

            # Trigger the automatic inclusion of variables
            set_payment_notification_schedule(calendar.SUNDAY,0,0,on_load=True)
        except Exception as e:
            print(e)


