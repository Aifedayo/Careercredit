from django.contrib import admin

from .models import FAQ, Job, UserOrder, Document, MainModel, AwsCredential, Jobplacement, Groupclass, BillingHistory, GroupClassRegister

admin.site.register(FAQ)
admin.site.register(Job)
admin.site.register(UserOrder)
admin.site.register(Document)
admin.site.register(MainModel)
admin.site.register(AwsCredential)
admin.site.register(Jobplacement)
admin.site.register(Groupclass)
admin.site.register(GroupClassRegister)
admin.site.register(BillingHistory)