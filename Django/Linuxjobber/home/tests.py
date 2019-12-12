from django.conf import settings
from django.http import HttpResponse, Http404
# Create your tests here.
from home.models import InstallmentPlan, SubPayment



def insert_installment_data(request):
    if not settings.DEBUG:
        return Http404('Not found')
    try:
        installment = InstallmentPlan.objects.create(
            user = request.user,
            total_amount = 1000,
            description= 'Test Installment Plan'
        )
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
    except:
        return HttpResponse('Failed')

def delete_installment_record(request):
    if not settings.DEBUG:
        return Http404('Not found')
    plans = request.user.installmentplan_set.all() #InstallmentPlan.objects.filter(user=request.user)
    for plan in plans:
        plan.subpayment_set.all().delete()
        plan.delete()
    return HttpResponse('Deleted')
