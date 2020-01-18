import datetime

from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
# Create your tests here.
from django.utils import timezone
from home.models import InstallmentPlan, SubPayment



def insert_installment_data(request,breached=None):
    if not settings.DEBUG:
        return Http404('Not found')
    try:
        installment = InstallmentPlan.objects.create(
            user = request.user,
            total_amount = 1000,
            description= 'Test Installment Plan'
        )
        if breached:
            installment.total_amount = 1500
            installment.save()
            i=SubPayment.objects.create(
                installment = installment,
                amount = 500,
                due_in = 5,
                is_initial=True,
                description = 'Initial Payment',
            )

            SubPayment.objects.create(
                installment = installment,
                amount = 500,
                due_in = 5,
                description = 'Initial Payment',
            )
            SubPayment.objects.create(
                installment = installment,
                amount = 500,
                due_in = 5,

                description = 'Initial Payment',
            )
            i.approve_payment()
            i.paid_on = timezone.now() - datetime.timedelta(weeks=10)
            i.save()
        else:
            SubPayment.objects.create(
                installment = installment,
                amount = 500,
                due_in = 5,
                is_initial=True,
                description = 'Initial Payment'
            )
            SubPayment.objects.create(
                installment = installment,
                amount = 500,
                due_in = 5,
                description='Next Installment Payment'
            )
        return HttpResponse('Success')
    except  Exception as e:
        return HttpResponse(e)

def delete_installment_record(request):
    if not settings.DEBUG:
        return Http404('Not found')
    plans = request.user.installmentplan_set.all() #InstallmentPlan.objects.filter(user=request.user)
    for plan in plans:
        plan.subpayment_set.all().delete()
        plan.delete()
    return HttpResponse('Deleted')


def check_file(request):
    from django.utils.encoding import smart_str

    response = HttpResponse(content_type='application/force-download')  # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('test.pdf')

    response['X-Sendfile'] = smart_str('test.pdf')
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
