from django.contrib import admin

from .models import FAQ, Job, RHCSAOrder, Internship, Location, NewsLetterSubscribers, UserOrder, Document, MainModel, AwsCredential, Jobplacement, Groupclass, BillingHistory, GroupClassRegister, StripePayment, UserPayment, wepeoples, PartTimeJob, FullTimePostion, PartTimePostion


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
admin.site.register(RHCSAOrder)
admin.site.register(NewsLetterSubscribers)
admin.site.register(StripePayment)
admin.site.register(Location)
admin.site.register(Internship)
admin.site.register(UserPayment)
admin.site.register(wepeoples)
admin.site.register(PartTimeJob)
admin.site.register(FullTimePostion)
admin.site.register(PartTimePostion)