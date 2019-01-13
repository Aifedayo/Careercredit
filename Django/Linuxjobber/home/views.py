import stripe
import csv, io
import logging
import subprocess, json, os
import random, string
from smtplib import SMTPException
from urllib.parse import urlparse
from django.conf import settings
from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from datetime import timedelta

from .models import *
from Courses.models import Course
from ToolsApp.models import Tool
from users.models import CustomUser
from .forms import JobPlacementForm, JobApplicationForm, AWSCredUpload, InternshipForm, ResumeForm

fs = FileSystemStorage(location= settings.MEDIA_ROOT+'/uploads')
# stripe.api_key = settings.STRIPE_SECRET_KEY


#Error Logging Instances
'''Log database errors with the dbalogger instance. example dblogger.level_of_error()
Log non database errors with the standard_logger instance'''
standard_logger = logging.getLogger(__name__)
dbalogger = logging.getLogger('dba')



def get_courses():
    return Course.objects.all()

def get_tools():
    return Tool.objects.all()


#INDEX VIEW
def index(request):
    return render (request, 'home/index.html', {'courses' : get_courses(), 'tools' : get_tools(),})


def signup(request):
    if request.method == "POST":
        firstname = request.POST['fullname'].split()[0]
        lastname = request.POST['fullname'].split()[1] if len(request.POST['fullname'].split()) > 1 else request.POST['fullname'].split()[0]
        email = request.POST['email']
        password = request.POST['password']
        username = email.split('@')[0]

        if (firstname):
            user = CustomUser(username=username, email=email)
            user.set_password(password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            send_mail('Linuxjobber Free Account Creation', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + '\n Follow this link http://stage.linuxjobber.com/login to login to you account\n\n Thanks & Regards \n Linuxjobber', settings.EMAIL_HOST_USER, [email])
            return render(request, "home/registration/success.html", {'user': user})
        else:
            error = True
            return render(request, 'home/registration/signup.html', {'error':error})
    else:
        return render(request, 'home/registration/signup.html')       


def forgot_password(request):
    email = ''
    message = ''
    if request.method == "POST":
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            u = CustomUser.objects.get(email=email)
            u.pwd_reset_token = ''.join(random.choice(string.ascii_lowercase) for x in range(64))
            u.save()
            password_reset_link = 'reset_password/'+str(u.pwd_reset_token)
            send_mail('Linuxjobber Account Password Reset', 'Hello, \n' + 'You are receiving this email because we received a request to reset your password,\nignore this message if you did not initiate the request else click the link below to reset your password.\n'+'http://stage.linuxjobber.com/'+password_reset_link+'\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])

            return render(request, 'home/registration/forgot_password.html',{'message':'An email with password reset information has been sent to you. Check your email to proceede.'})
        else:
            return render(request, 'home/registration/forgot_password.html', {'message':'There is no account associated with this email'})
    else:
        return render(request, 'home/registration/forgot_password.html', {'message':message})

def reset_password(request, reset_token):
    message = ''
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            usr = CustomUser.objects.get(pwd_reset_token=reset_token)
            usr.pwd_reset_token = ''.join(random.choice(string.ascii_lowercase) for x in range(64))
            usr.set_password(request.POST['password1'])
            usr.save()
            message = "You have successfully changed your password."
            return render(request, 'home/registration/reset_password.html', {'message':message})
        else:
            message = "Passwords don't match"
            return render(request, 'home/registration/reset_password.html', {'message':message})
    else:
        return render(request, 'home/registration/reset_password.html', {'message':message})

def selfstudy(request):
    return render(request, 'home/selfstudy.html', {'courses' : get_courses(), 'tools' : get_tools()})


def faq(request):
    faqs = FAQ.objects.all()
    context ={
            'faqs': faqs,
                   
                }
    return render(request, 'home/faq.html', {'faqs': faqs,'courses' : get_courses(), 'tools' : get_tools()})

def gainexperience(request):
    return render(request, 'home/gainexperience.html', {'courses' : get_courses(), 'tools' : get_tools()})

def internships(request):
    if request.method == "POST":
        form = InternshipForm(request.POST, request.FILES)
        if form.is_valid():
            internform = form.save(commit=False)
            internform.save()
            messages.success(request, 'Thanks for applying for the internship which starts on the 14th of April, 2018. Please ensure you keep in touch with Linuxjobber latest updates on our various social media platform. Thanks')
            return render(request, 'home/internships.html', {'form': form, 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        form = InternshipForm()
    form = InternshipForm()
    return render(request, 'home/internships.html', {'form': form, 'courses' : get_courses(), 'tools' : get_tools()})

def resumeservice(request):
    return render(request, 'home/resumeservice.html', {'courses' : get_courses(), 'tools' : get_tools()})



@login_required
@csrf_exempt
def resumepay(request):
    form = ResumeForm()
    stripeset = StripePayment.objects.all()
    if request.method == "POST":
        stripe.api_key = stripeset[0].secretkey
        token = request.POST.get("stripeToken")
        try:
            charge = stripe.Charge.create(
                amount= 199 * 100,
                currency='usd',
                description='Resume services charge',
                source=token,
            )
            messages.success(request, 'Payment succesfully, please upload your resume')
            form = ResumeForm()
            return redirect("home:resumeupload")
        except stripe.error.CardError as ce:
            return False, ce
    else:
        pass
    return render(request, 'home/resumepay.html', {'courses' : get_courses(), 'tools' : get_tools()})

@login_required(login_url='/login')
def resumeupload(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resumeform = form.save(commit=False)
            resumeform.user = request.user
            resumeform.save()
            messages.success(request, 'Resume has been submitted succesfully, you will be contact by your mentor if more details are required')
            return render(request, 'home/resumeupload.html', {'form': form, 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        form = ResumeForm()
    form = ResumeForm()
    return render(request, 'home/resumeupload.html', {'form': form, 'courses' : get_courses(), 'tools' : get_tools()})



def aboutus(request):
    return render(request, 'home/aboutus.html', {'courses' : get_courses(), 'tools' : get_tools()})

 
def policies(request):
    return render(request, 'home/policies.html', {'courses' : get_courses(), 'tools' : get_tools()})
 

def jobs(request):
    return render(request, 'home/job.html', {'courses' : get_courses(), 'tools' : get_tools()})


def jobapplication(request):

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            jobform = form.save(commit=False)
            jobform.save()
            return render(request, 'home/job.html', {'courses' : get_courses(), 'tools' : get_tools()})
    else:
        form = JobApplicationForm()
    form = JobApplicationForm()
    return render(request, 'home/jobapplication.html', {'form': form,'courses' : get_courses(), 'tools' : get_tools()})


def resume(request):
    return render(request, 'home/resume.html', {'courses' : get_courses(), 'tools' : get_tools()})


def log_in(request):
    if request.method == "POST":
        user_name = request.POST['username']
        password = request.POST['password']
        if "@" in user_name:
            user_name = user_name.split('@')[0]
        user = authenticate(request, username = user_name, password = password)
        
        if user is not None:
            login(request, user)
            #check if user paid for work experience and has not filled the form
            try:
                weps = wepeoples.objects.get(user=request.user)
                if not weps.trainee_position:
                    return redirect("home:workexpform")
            except wepeoples.DoesNotExist:
                return redirect("Courses:userinterest")
            return redirect("Courses:userinterest")
        else:
            error_message = "yes"
            return render(request, "home/registration/login.html", {'error_message' : error_message})
    else:
        return render(request, "home/registration/login.html", {'courses' : get_courses(), 'tools' : get_tools()})


def log_out(request):
    logout(request)
    return redirect("home:login")



def linux_full_training(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email = email)
            subscriber.save()
            send_mail('Linuxjobber Newsletter', 'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render (request, 'home/linux_full_training.html', {'news_letter_message': 'You have successfully subscribed to our news letter!', 'courses' : get_courses(), 'tools' : get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render (request, 'home/linux_full_training.html', {'news_letter_message': 'Something went wrong please try again!', 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        return render(request, 'home/linux_full_training.html', {'news_letter_message': news_letter_message ,'courses' : get_courses(), 'tools' : get_tools()})


def aws_full_training(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email = email)
            subscriber.save()
            send_mail('Linuxjobber Newsletter', 'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render (request, 'home/aws_full_training.html', {'news_letter_message': 'You have successfully subscribed to our news letter!', 'courses' : get_courses(), 'tools' : get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render (request, 'home/aws_full_training.html', {'news_letter_message': 'Something went wrong please try again!', 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        return render(request, 'home/aws_full_training.html', {'news_letter_message': news_letter_message ,'courses' : get_courses(), 'tools' : get_tools()})


def oracledb_full_training(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email = email)
            subscriber.save()
            send_mail('Linuxjobber Newsletter', 'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render (request, 'home/oracledb_full_training.html', {'news_letter_message': 'You have successfully subscribed to our news letter!', 'courses' : get_courses(), 'tools' : get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render (request, 'home/oracledb_full_training.html', {'news_letter_message': 'Something went wrong please try again!', 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        return render(request, 'home/oracledb_full_training.html', {'news_letter_message': news_letter_message ,'courses' : get_courses(), 'tools' : get_tools()})


def linux_certification(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email = email)
            subscriber.save()
            send_mail('Linuxjobber Newsletter', 'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render (request, 'home/linux_certification.html', {'news_letter_message': 'You have successfully subscribed to our news letter!', 'courses' : get_courses(), 'tools' : get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render (request, 'home/linux_certification.html', {'news_letter_message': 'Something went wrong please try again!', 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        return render(request, 'home/linux_certification.html', {'news_letter_message': news_letter_message ,'courses' : get_courses(), 'tools' : get_tools()})

def aws_certification(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email = email)
            subscriber.save()
            send_mail('Linuxjobber Newsletter', 'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render (request, 'home/aws_certification.html', {'news_letter_message': 'You have successfully subscribed to our news letter!', 'courses' : get_courses(), 'tools' : get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render (request, 'home/aws_certification.html', {'news_letter_message': 'Something went wrong please try again!', 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        return render(request, 'home/aws_certification.html', {'news_letter_message': news_letter_message ,'courses' : get_courses(), 'tools' : get_tools()})

def oracledb_certification(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email = email)
            subscriber.save()
            send_mail('Linuxjobber Newsletter', 'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render (request, 'home/oracledb_certification.html', {'news_letter_message': 'You have successfully subscribed to our news letter!', 'courses' : get_courses(), 'tools' : get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render (request, 'home/oracledb_certification.html', {'news_letter_message': 'Something went wrong please try again!', 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        return render(request, 'home/oracledb_certification.html', {'news_letter_message': news_letter_message ,'courses' : get_courses(), 'tools' : get_tools()})





def workexperience(request):
    return render(request, 'home/workexperience.html')

@login_required
def workexpform(request):

    try:
        weps = wepeoples.objects.get(user=request.user)
        student = False
    except wepeoples.DoesNotExist:
        student = True


    if request.method == 'POST':
        trainee = request.POST['trainee_position']
        current = request.POST['current_position']
        state = request.POST['state']
        income = request.POST['income']
        relocate = request.POST['relocate']
        person = request.POST['type']


        if person == "Graduant" or person == "Student":
            graduation = request.POST['gdate']
        else:
            now = timezone.now()
            graduation = now + timedelta(days=120)
        
        try:
            weps = wepeoples.objects.get(user=request.user)
            weps.trainee_position = trainee
            weps.current_position = current
            weps.person_type = person
            weps.state = state
            weps.income = income
            weps.relocation = relocate
            weps.last_verification = None
            weps.Paystub = None
            weps.graduation_date = graduation
            weps.save()
        except wepeoples.DoesNotExist:
            weps = wepeoples.objects.create(user=request.user,trainee_position=trainee,
                current_position=current,person_type=person,state=state,income=income,
                relocation=relocate,last_verification=None,Paystub=None,graduation_date=graduation)
            weps.save()
        return redirect("home:workexprofile")
    else:
        return render(request, 'home/workexpform.html',{'student':student})

@login_required
def workexprofile(request):
    
    weps = wepeoples.objects.get(user=request.user)

    if not weps.trainee_position:
        return redirect("home:workexpform")

    if request.method == "POST":
        print(request.POST['type'])
        if request.POST['type'] == '1':
            last_verify = request.FILES['verify']
            weps.Paystub = last_verify
            weps.save(update_fields=["Paystub"])
            messages.success(request, 'Paystub uploaded successfully, Last verification would be updated as soon as Paystub is verified')
            return redirect("home:workexprofile")
        else:
            income = request.POST['income']
            weps.income = income
            weps.save(update_fields=['income'])
            messages.success(request, 'Total monthly income updated successfully')
            return redirect("home:workexprofile")

    return render(request, 'home/workexprofile.html',{'weps': weps})

def jobplacements(request):
    return render(request, 'home/jobplacements.html',{'courses' : get_courses(), 'tools' : get_tools()})


def get_application_grade(exp,certif,train,reloc):
    grade = 10
    if exp > 0: grade += 20
    if certif.lower() == 'yes': grade += 30
    if train.lower() == 'yes': grade += 30
    if reloc.lower() == 'yes': grade += 10
    return grade

@login_required
def apply(request,level):
    if request.method == "GET":
        return render(request, 'home/apply.html', {'level':level, 'courses': get_courses()})
    else:
        form = JobPlacementForm(request.POST)
        if form.is_valid():
            certificates = request.FILES.getlist('certificates')
            if certificates:
                for f in certificates:
                    fs.save(os.path.join('certs',request.user.username, f.name), f)
            lvl = 1 if level == 'snr' else 2
            education = form.cleaned_data['education']
            career = form.cleaned_data['career']
            resume = request.FILES['resume']
            experience = form.cleaned_data['experience']
            is_certified = form.cleaned_data['is_certified']
            training = form.cleaned_data['training']
            can_relocate = form.cleaned_data['can_relocate']
            awareness = form.cleaned_data['awareness1']
            if awareness == "Others":
                awareness = request.POST['awareness2']
            placement_grade = get_application_grade(experience,is_certified,
                                                    training,can_relocate)
            try:
                Jobplacement.objects.create(user=request.user,level=lvl,
                                            education = education,career = career, resume = resume, 
                                            placement_grade = placement_grade, experience = experience,
                                            is_certified = is_certified, training = training, can_relocate = can_relocate, awareness = awareness,
                                            )
                if placement_grade != 100:
                    context = {
                        'issue_lvl': 1,
                        'msg':'Sorry, you did not meet the job requirements',
                        'redirinfo':{
                            'txt':"Apply Now" if level == 'snr' else "Get Certificate",
                            'msg':'Click the Apply Now button below for placement to junior level role.' if level == 'snr' else "Click the Get Certificate button below to apply for our certification course.",
                            'url': reverse('home:apply', args=['jnr']) if level == 'snr' else reverse('home:selfstudy'),
                            },
                        'level':level,
                        }
                    return render(request,'home/failed_application.html',context)
                return render(request,'home/accepted.html')
            except Exception as error:
                print(error)
                context = {
                        'issue_lvl': 2,
                        'msg':'Sorry, you did not meet the job requirements',
                        }
                return render(request,'home/failed_application.html',context)


@login_required
def pay(request):
    PRICE = 399
    mode = "One Time"
    PAY_FOR = "Work Experience"
    DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${}".format(PRICE,PRICE)
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey
    if request.method == "POST":
        token = request.POST.get("stripeToken")
        try:
            charge = stripe.Charge.create(
                amount = PRICE * 100,
                currency = "usd",
                source = token,
                description = PAY_FOR
            )
        except stripe.error.CardError as ce:
            return False, ce
        else:
            try:
                UserPayment.objects.create(user=request.user, amount=PRICE,
                                            trans_id = charge.id, pay_for = charge.description,
                                            )
                _, created = wepeoples.objects.update_or_create(user=request.user,trainee_position=None,current_position=None,
                                                        person_type=None,state=None,income=None,relocation=None,
                                                        last_verification=None,Paystub=None,graduation_date=None)
                return render(request,'home/accepted.html')
            except Exception as error:
                print(error)
                return redirect("home:index")
    else:
        context = { "stripe_key": stripeset[0].publickey,
                   'price': PRICE,
                   'amount': str(PRICE)+'00',
                   'mode': mode,
                   'PAY_FOR': PAY_FOR,
                   'DISCLMR': DISCLMR}
        return render(request, 'home/pay.html', context)


def accepted(request):
    return render(request, 'home/accepted.html')

@csrf_exempt
def check_subscription_status(request):

    if request.method == "POST":
        event_json = json.loads(request.body)
        jsonObject = event_json

        subscription_id = jsonObject['data']['object']['subscription']
        customer_id = jsonObject['data']['object']['customer']
        amount = jsonObject['data']['object']['amount_paid'] / 100
        types = jsonObject['type']


        customersubscription = UserOrder.objects.get(order_id=customer_id, subscription= subscription_id)

        if types == 'customer.subscription.deleted' and customer_id:
            if customersubscription:
                customersubscription.status = "inactive/deleted"
                customersubscription.save()

                billing = BillingHistory(user=customersubscription.user, amount=amount, subscription_id=subscription_id, status="inactive/deleted")
                billing.save()

                user = CustomUser.objects.get(email=customersubscription.user.email)
                user.role = 6
                user.save()

        elif types == 'invoice.payment_failed' and customer_id:
            if customersubscription:
                customersubscription.status = "failed"
                customersubscription.save()

                billing = BillingHistory(user=customersubscription.user, amount=amount, subscription_id=subscription_id, status="Failed")
                billing.save()

                user = CustomUser.objects.get(email=customersubscription.user.email)
                user.role = 6
                user.save()

        elif types == 'invoice.payment_succeeded' and customer_id:
            if customersubscription:
                customersubscription.status = "success"
                customersubscription.save()

                billing = BillingHistory(user=customersubscription.user, amount=amount, subscription_id=subscription_id, status="success")
                billing.save()

                user = CustomUser.objects.get(email=customersubscription.user.email)
                user.role = 3
                user.save()

    return render(request, 'home/check_subscription.html')

@login_required
def monthly_subscription(request):
    email = request.user.email
    
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey
    plan_id = stripeset[0].planid

    if request.method == "POST":
        token = request.POST.get("stripeToken")
        plan = stripe.Plan.retrieve(plan_id)
        amount = plan.amount

        try:
            customer = stripe.Customer.create(
                source = token,
                email = request.user.email,
            )

            subscription = stripe.Subscription.create(
                customer = customer.id,
                plan = plan_id,
            )

            order = UserOrder(
                user = request.user,
                order_id = customer.id,
                subscription = subscription.id,
                status="pending",
                order_amount = int(amount)/100,
            )

            order.save()

            messages.success(request, 'Thanks for your sucbscription! Please allow 10-20 seconds for your account to be updated as we have to wait for confirmation from the credit card processor.')
            return redirect("home:monthly_subscription")
        except stripe.error.CardError as ce:
            return False, ce

    return render(request, 'home/monthly_subscription.html', {'email':email,'publickey':stripeset[0].publickey})

def group(request,pk):
    group_item = get_object_or_404(Groupclass,pk=pk)
    user = None
    if request.user.is_authenticated:
        print('user authenticated')
        user=CustomUser.objects.get(email=request.user)
    # try:
    #     user = CustomUser.objects.get(email=request.user)
    # except CustomUser.DoesNotExist:
    #     pass
    # finally:
    if request.method == "POST":
        email = request.POST['email']
        choice = request.POST['choice']

        # type_of_class = request.POST['name']
        # amount = request.POST['price']

        # request.session['email'] = email
        # request.session['amount'] = amount
        # request.session['class'] = type_of_class
        try:
            password = request.POST['password']
            user = CustomUser.objects.get(email=email)
            the_user = authenticate(email=email,password=password)

            if the_user:
                login(request,the_user)
            else:
                messages.error(request, 'Account found, invalid password entered.')

        except MultiValueDictKeyError:
            print('Error')

        except CustomUser.DoesNotExist:
            firstname = request.POST['fullname'].split()[0]
            lastname = request.POST['fullname'].split()[1] if len(request.POST['fullname'].split()) > 1 else request.POST['fullname'].split()[0]
            password = request.POST['password']
            username = email.split('@')[0]
            if (firstname):
                user = CustomUser.objects.create_user(username, email, password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                # send_mail('Linuxjobber Free Account Creation', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + '\n Follow this link http://35.167.153.1:8001/login to login to you account\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])

                groupreg = GroupClassRegister.objects.create(user= user, is_paid=0, amount=29, type_of_class = group_item.type_of_class)
                groupreg.save()

                new_user = authenticate(username=username,
                                    password=password,
                                    )
                login(request, new_user)

                if int(choice) == 1:
                    return redirect("home:monthly_subscription")

                return redirect("home:group_pay",pk=group_item.pk)

        if user:
            groupreg = GroupClassRegister.objects.create(user= user, is_paid = 0, amount=29, type_of_class = group_item.type_of_class)
            groupreg.save()
            login(request, user)
            if int(choice) == 1:
                return redirect("home:monthly_subscription")
            return redirect("home:group_pay",pk=group_item.pk)
    user_token=""
    if user:
        user_token,_=Token.objects.get_or_create(user=user)
    return render(request, 'home/group_class_item.html', {'group':group_item,'user':user,'GROUP_URL':settings.GROUP_CLASS_URL,'token':user_token})

@login_required
def group_pay(request,pk):
    # email = request.session['email']
    # amount = request.session['amount']
    # amount = int(amount) * 100
    # type_class = request.session['class']
    group_item=get_object_or_404(Groupclass,pk=pk)
    amount=group_item.price * 100
    stripeset = StripePayment.objects.all()
    # Stripe uses cent notation for amount 10 USD = 10 * 100
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey
    context = { "stripe_key": stripeset[0].publickey,
                   'amount': amount,
                'group':group_item,

                }
    if request.method == "POST":

       # stripe.api_key = "sk_test_FInuRlOzwpM1b3RIw5fwirtv"
        stripe.api_key = stripeset[0].secretkey
        token = request.POST.get("stripeToken")
        try:
            charge = stripe.Charge.create(
                amount= amount,
                currency='usd',
                description='Group Course Payment',
                source=token,
            )
            messages.success(request, 'You are registered in group class successfully.')
            _, created = GroupClassRegister.objects.update_or_create(
                user=request.user,
                is_paid=1,
                amount=29,
                type_of_class = group_item.type_of_class,
            )
            # After payment, add user to the group
            user=get_object_or_404(CustomUser,email=request.user.email)
            group_item.users.add(user)
            return redirect("home:group",pk=pk)
        except stripe.error.CardError as ce:
            return False, ce
    return render(request, 'home/group_pay.html', context)


def contact_us(request):
    error = ''
    success = ''
    if request.method == "POST":
        fname = request.POST['full_name']
        phone = request.POST['phonenumber']
        email = request.POST['email']
        subj = request.POST['subject']
        message = request.POST['message']
        try:
            contact_message = ContactMessages(full_name=fname, phone_no=phone, email=email, message_subject=subj, message=message)
            contact_message.save()
        except Exception as e:
            error = 'yes'
        else:
            success = 'yes'    
        return render(request, 'home/contact_us.html',{'error':error, 'success':success})
    else:
        return render(request, 'home/contact_us.html',{'error':error, 'success':success,'courses' : get_courses(), 'tools' : get_tools()})


def location(request):
    return render(request, 'home/location.html', {'courses' : get_courses(), 'tools' : get_tools()})


def account_settings(request):
    form = AWSCredUpload()
    if request.method == "POST":
        form = AWSCredUpload(request.POST, request.FILES)
        csv_file = request.FILES['document']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload csv files only')
            return render(request, 'home/account_settings.html', {'form': form, 'courses' : get_courses(), 'tools' : get_tools()})

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        username = ""
        access_key = ""
        secret_key = ""

        for column in csv.reader(io_string, delimiter=','):
            count = len(list(column))
            if count == 5:
                username = column[0]
                access_key = column[2]
                secret_key = column[3]
            elif count == 3:
                username = column[0]
                access_key = column[1]
                secret_key = column[2] 
            else:
                username = ""
                access_key = column[0]
                secret_key = column[1] 

        V_AWS_ACTION = 'verify';
        V_MACHINE_ID = 'verify';
        command = ['python3.6 '+settings.BASE_DIR+"/home/utils/s3_sample.py %s %s %s %s" %(access_key,secret_key,V_AWS_ACTION,V_MACHINE_ID) ]
        
        try:
            output = subprocess.check_output(command, shell=True )
            return_code = 0

            _, created = AwsCredential.objects.update_or_create(
                user = request.user,
                username = username,
                accesskey = access_key,
                secretkey = secret_key,
                )

            if form.is_valid():
                messages.success(request, 'AWS credentials have been uploaded successfully')
                return redirect("home:ec2dashboard")

        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output

        #types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"
            error3 = "OptInRequired"

            for out in output:
                if not sorted(out) == sorted(error1):
                    messages.error(request, 'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                    return render(request, 'home/account_settings.html', {'form': form,'courses' : get_courses(), 'tools' : get_tools() })
                elif not sorted(out) == sorted(error2):
                    messages.error(request, 'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                    return render(request, 'home/account_settings.html', {'form': form, 'courses' : get_courses(), 'tools' : get_tools()})
                elif not sorted(out) == sorted(error3):
                    messages.error(request, 'You are not subscribed to the AWS service, Please go to http://aws.amazon.com to subscribe.')
                    return render(request, 'home/account_settings.html', {'form': form,'courses' : get_courses(), 'tools' : get_tools() })

    else:
        try:
            check = AwsCredential.objects.get(user=request.user)
        except AwsCredential.DoesNotExist:
            check = None
        if check:
            return redirect("home:ec2dashboard")
            
        return render(request, 'home/account_settings.html', {'form':form,'courses' : get_courses(), 'tools' : get_tools() })


def ec2dashboard(request, command=None):
    form = AWSCredUpload()
    awscred = AwsCredential.objects.get(user = request.user)
       

    #Running instance
    running_machine = []
    RUNING_AWS_ACTION = 'instance_running';
    RUNING_MACHINE_ID = 'running';
    command = ['python3.6 '+ settings.BASE_DIR+"/home/utils/s3_sample.py %s %s %s %s" %(awscred.accesskey,awscred.secretkey,RUNING_AWS_ACTION,RUNING_MACHINE_ID) ]
        
    try:
        outputs = subprocess.check_output(command, shell=True )
        return_code = 0
        outputs = bytes(outputs)
        output = outputs.decode()
        
        output = output.split(",")

        for i in range(0,len(output)-1):
            out = output[i].split()
            running_machine.append(out)     

    except subprocess.CalledProcessError as grepexc:
        print("error code", grepexc.returncode, grepexc.output)
        return_code = grepexc.returncode
        output = grepexc.output

    #stopped Instance
    stopped_machine = []
    STOP_AWS_ACTION = 'instance_stopped';
    STOP_MACHINE_ID = 'stopped';
    

    command = ['python3.6 '+ settings.BASE_DIR+"/home/utils/s3_sample.py %s %s %s %s"  %(awscred.accesskey,awscred.secretkey,STOP_AWS_ACTION,STOP_MACHINE_ID) ]

    try:
        stopped_outputs = subprocess.check_output(command, shell=True )
        return_code = 0
        stopped_outputs = bytes(stopped_outputs)
        output = stopped_outputs.decode()
        
        output = output.split(",")

        for i in range(0,len(output)-1):
            out = output[i].split()
            stopped_machine.append(out)

    except subprocess.CalledProcessError as grepexc:
        print("error code", grepexc.returncode, grepexc.output)
        return_code = grepexc.returncode
        output = grepexc.output

    context={
            'form': form,
            'running_machine': running_machine,
            'stopped_machine': stopped_machine,
    }

     #Launch an instance
    if command and command == "launch":
        AWS_ACTION = 'launch_instance';
        MACHINE_ID = "new";
        command = ['python3.6 '+ settings.BASE_DIR+"/home/utils/s3_sample.py %s %s %s %s" %(awscred.accesskey,awscred.secretkey,AWS_ACTION,MACHINE_ID) ]
            
        try:
            output = subprocess.check_output(command, shell=True )
            return_code = 0
            messages.error(request, 'Machine is starting up, wait and click refresh in 2 minutes. Username is : sysadmin , Password is : 8iu7*IU& . We advice you to use this console for all your EC2 instances. If you have started other instances, please turn them all off now')
            return render(request, 'home/ec2dashboard.html', context)
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output

            #types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"
            error3 = "InstanceLimitExceeded"

            for out in output:
                if not sorted(out) == sorted(error1):
                    messages.error(request, 'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                    return render(request, 'home/ec2dashboard.html', context)
                elif not sorted(out) == sorted(error2):
                    messages.error(request, 'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                    return render(request, 'home/ec2dashboard.html', context)
                elif not sorted(out) == sorted(error3):
                    messages.error(request, 'Sorry, you can only launch one machine at a time')
                    return render(request, 'home/ec2dashboard.html', context)
                else:
                    messages.error(request, 'Unhandled exception has occurred. Please contact admin@linuxjobber.com')
                    return render(request, 'home/ec2dashboard.html', context)

    if request.method == "POST":
        form = AWSCredUpload(request.POST, request.FILES)
        csv_file = request.FILES['document']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload csv files only')
            return render(request, 'home/ec2dashboard.html', context)

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        username = ""
        access_key = ""
        secret_key = ""

        for column in csv.reader(io_string, delimiter=','):
            count = len(list(column))
            if count == 5:
                username = column[0]
                access_key = column[2]
                secret_key = column[3]
            elif count == 3:
                username = column[0]
                access_key = column[1]
                secret_key = column[2] 
            else:
                username = ""
                access_key = column[0]
                secret_key = column[1] 

        V_AWS_ACTION = 'verify';
        V_MACHINE_ID = 'verify';
        command = ['python3.6 '+ settings.BASE_DIR+"/home/utils/s3_sample.py %s %s %s %s" %(access_key,secret_key,V_AWS_ACTION,V_MACHINE_ID) ]
        
        try:
            output = subprocess.check_output(command, shell=True )
            return_code = 0
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output

        #types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"
            error3 = "OptInRequired"

            for out in output:
                if not sorted(out) == sorted(error1):
                    messages.error(request, 'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                    return render(request, 'home/ec2dashboard.html', context)
                elif not sorted(out) == sorted(error2):
                    messages.error(request, 'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                    return render(request, 'home/ec2dashboard.html', context)
                elif not sorted(out) == sorted(error3):
                    messages.error(request, 'You are not subscribed to the AWS service, Please go to http://aws.amazon.com to subscribe.')
                    return render(request, 'home/ec2dashboard.html', context)

            #return render(request,'courses/result.html',{'gradingerror':"There was an error encountered during grading",'coursetopic':topic})
        _, created = AwsCredential.objects.update_or_create(
                user = request.user,
                username = username,
                accesskey = access_key,
                secretkey = secret_key,
                )
        if form.is_valid():
            #form.save()
            messages.success(request, 'AWS credentials have been uploaded successfully')
            return render(request, 'home/ec2dashboard.html', context)
    
    return render(request, 'home/ec2dashboard.html', context)

def startmachine(request, machine_id):
    awscred = AwsCredential.objects.get(user = request.user)

    if machine_id:
        AWS_ACTION = 'start_instance';
        MACHINE_ID = machine_id;
        command = ['python3.6 '+ settings.BASE_DIR+"/home/utils/s3_sample.py %s %s %s %s" %(awscred.accesskey,awscred.secretkey,AWS_ACTION,MACHINE_ID) ]
            
        try:
            output = subprocess.check_output(command, shell=True )
            return_code = 0
            messages.success(request, 'Machine is starting up, wait and click refresh in 2 minutes. Username is : sysadmin , Password is : 8iu7*IU& . We advice you to use this console for all your EC2 instances. If you have started other instances, please turn them all off now')
            return redirect("home:ec2dashboard")
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output

            #types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"

            for out in output:
                if not sorted(out) == sorted(error1):
                    messages.error(request, 'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                    return redirect("home:ec2dashboard")
                elif not sorted(out) == sorted(error2):
                    messages.error(request, 'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                    return redirect("home:ec2dashboard")
                else:
                    messages.error(request, 'Unhandled exception has occurred. Please contact admin@linuxjobber.com')
                    return redirect("home:ec2dashboard")


def stopmachine(request, machine_id):
    awscred = AwsCredential.objects.get(user = request.user)
    if machine_id:
        AWS_ACTION = 'stop_instance';
        MACHINE_ID = machine_id;
        command = ['python3.6 '+ settings.BASE_DIR+"/home/utils/s3_sample.py %s %s %s %s" %(awscred.accesskey,awscred.secretkey,AWS_ACTION,MACHINE_ID) ]
            
        try:
            output = subprocess.check_output(command, shell=True )
            return_code = 0
            messages.success(request, 'Machine is shutting down, wait and click refresh in 2 minutes. Username is : sysadmin , Password is : 8iu7*IU& . We advice you to use this console for all your EC2 instances. If you have started other instances, please turn them all off now')
            return redirect("home:ec2dashboard")
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output

            #types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"

            for out in output:
                if not sorted(out) == sorted(error1):
                    messages.error(request, 'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                    return redirect("home:ec2dashboard")
                elif not sorted(out) == sorted(error2):
                    messages.error(request, 'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                    return redirect("home:ec2dashboard")
                else:
                    messages.error(request, 'Unhandled exception has occurred. Please contact admin@linuxjobber.com')
                    return redirect("home:ec2dashboard")


def order_list(request):
    return render(request, 'home/orderlist.html', {'order': UserOrder.objects.filter(user=request.user),'courses' : get_courses(), 'tools' : get_tools() })


def students_packages(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email = email)
            subscriber.save()
            send_mail('Linuxjobber Newsletter', 'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render (request, 'home/students_packages.html', {'news_letter_message': 'You have successfully subscribed to our news letter!', 'courses' : get_courses(), 'tools' : get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render (request, 'home/students_packages.html', {'news_letter_message': 'Something went wrong please try again!', 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        return render(request, 'home/students_packages.html', {'news_letter_message': news_letter_message ,'courses' : get_courses(), 'tools' : get_tools()})




def server_service(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email = email)
            subscriber.save()
            send_mail('Linuxjobber Newsletter', 'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render (request, 'home/server_service.html', {'news_letter_message': 'You have successfully subscribed to our news letter!', 'courses' : get_courses(), 'tools' : get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render (request, 'home/server_service.html', {'news_letter_message': 'Something went wrong please try again!', 'courses' : get_courses(), 'tools' : get_tools()})
    else:
        return render(request, 'home/server_service.html', {'news_letter_message': news_letter_message ,'courses' : get_courses(), 'tools' : get_tools()})



def live_help(request):
    return render(request, 'home/live_help.html', {'courses' : get_courses(), 'tools' : get_tools()} )

@login_required
def pay_live_help(request):
    PRICE = 399
    mode = "One Time"
    PAY_FOR = "Live Help"
    DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${}".format(PRICE,PRICE)
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey
    if request.method == "POST":
        token = request.POST.get("stripeToken")
        try:
            charge = stripe.Charge.create(
                amount = PRICE * 100,
                currency = "usd",
                source = token,
                description = PAY_FOR
            )
        except stripe.error.CardError as ce:
            return False, ce
        else:
            try:
                UserPayment.objects.create(user=request.user, amount=PRICE,
                                            trans_id = charge.id, pay_for = charge.description,
                                            )
                send_mail('Linuxjobber Live Help Subscription', 'Hello, you have successfuly subscribed for Live Help on Linuxjobber.\n\n Thanks & Regards \n Linuxjobber', settings.EMAIL_HOST_USER, [request.user.email])
                return render(request,'home/live_help_pay_success.html')
            except SMTPException as error:
                print(error)
                return render(request,'home/live_help_pay_success.html')
            except Exception as error:
                print(error)
                return redirect("home:index")
    else:
        context = { "stripe_key": stripeset[0].publickey,
                   'price': PRICE,
                   'amount': str(PRICE)+'00',
                   'mode': mode,
                   'PAY_FOR': PAY_FOR,
                   'DISCLMR': DISCLMR}
        return render(request, 'home/live_help_pay.html', context)


def in_person_training(request):
    return render(request, 'home/in_person_training.html', {'courses' : get_courses(), 'tools' : get_tools()})

@login_required
def tryfree(request, sub_plan):

    if sub_plan == 'standardPlan':
        PRICE = 29
        mode = "Monthly Subscription"
        PAY_FOR = "14 days free trial"
        DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time within 14 days for a full refund. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${}/Monthly".format(PRICE,PRICE)
        stripeset = StripePayment.objects.all()
        stripe.api_key = stripeset[0].secretkey
        if request.method == "POST":
            token = request.POST.get("stripeToken")
            try:
                charge = stripe.Charge.create(
                    amount = PRICE *100,
                    currency = "usd",
                    source = token,
                    description = sub_plan.lower()
                )
            except stripe.error.CardError as ce:
                return False, ce
            else:
                try:
                    UserPayment.objects.create(user=request.user, amount=PRICE,
                                                trans_id = charge.id, pay_for = charge.description,
                                                )
                    user = request.user
                    user.role = 3
                    user.save()
                    send_mail('Linuxjobber Standard Plan Subscription', 'Hello, you have successfuly subscribed for our Standard Plan package.\n\n Thanks & Regards \n Linuxjobber', settings.EMAIL_HOST_USER, [request.user.email])
                    return render(request,'home/standardPlan_pay_success.html')
                except SMTPException as error:
                    print(error)
                    return render(request,'home/standardPlan_pay_success.html')
                except Exception as error:
                    print(error)
                    return redirect("home:index")
        else:
            context = { "stripe_key": stripeset[0].publickey,
                       'price': PRICE,
                       'amount': str(PRICE)+'00',
                       'mode': mode,
                       'PAY_FOR': PAY_FOR,
                       'DISCLMR': DISCLMR,
                       'courses' : get_courses(),
                       'tools' : get_tools()}
            return render(request, 'home/standard_plan_pay.html', context)
    else:
        PRICE = 2499
        mode = "One Time Payment"
        PAY_FOR = "PREMIUM PLAN"
        DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time within 14 days for a full refund. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ONE TIME ${}".format(PRICE,PRICE)
        stripeset = StripePayment.objects.all()
        stripe.api_key = stripeset[0].secretkey
        if request.method == "POST":
            token = request.POST.get("stripeToken")
            try:
                charge = stripe.Charge.create(
                    amount = PRICE,
                    currency = "usd",
                    source = token,
                    description = sub_plan.lower()
                )
            except stripe.error.CardError as ce:
                return False, ce
            else:
                try:
                    UserPayment.objects.create(user=request.user, amount=PRICE,
                                                trans_id = charge.id, pay_for = charge.description,
                                                )
                    send_mail('Linuxjobber Premium Plan Subscription', 'Hello, you have successfuly subscribed for our Premium Plan package.\n\n Thanks & Regards \n Linuxjobber', settings.EMAIL_HOST_USER, [request.user.email])
                    return render(request,'home/premiumPlan_pay_success.html')
                except SMTPException as error:
                    print(error)
                    return render(request,'home/premiumPlan_pay_success.html')
                except Exception as error:
                    print(error)
                    return redirect("home:index")
        else:
            context = { "stripe_key": stripeset[0].publickey,
                       'price': PRICE,
                       'amount': str(PRICE)+'00',
                       'mode': mode,
                       'PAY_FOR': PAY_FOR,
                       'DISCLMR': DISCLMR,
                       'courses' : get_courses(),
                       'tools' : get_tools()}
            return render(request, 'home/premium_plan_pay.html', context)




@login_required
def rhcsa_order(request):

    orders = RHCSAOrder.objects.filter(user=request.user)
    orders_not_empty = RHCSAOrder.objects.filter(user=request.user).exists()

    return render(request, 'home/rhcsa_order.html', {  'orders_not_empty':orders_not_empty, 'orders':orders, 'courses' : get_courses(), 'tools' : get_tools()} )


def user_interest(request):

    return render(request, 'home/user_interest.html', {'courses' : get_courses(), 'tools' : get_tools()})

def upload_profile_pic(request):
    update_feedback = ''
    if request.method == 'POST' and request.FILES['profile_picture']:
        if request.FILES['profile_picture'].name.endswith('.png') or request.FILES['profile_picture'].name.endswith('.jpg'):
            picture = request.FILES['profile_picture']
            filename = FileSystemStorage().save(picture.name, picture)
            picture_url = FileSystemStorage().url(filename)
            current_user = request.user
            current_user.profile_img = picture_url
            current_user.save()
            update_feedback = 'Your profile update was successful'
            return render(request,'home/upload_profile_pic.html',{'update_feedback':update_feedback})
        else:
            update_feedback = 'This file format is not supported'
            return render(request,'home/upload_profile_pic.html',{'update_feedback':update_feedback})
    else:
        return render(request,'home/upload_profile_pic.html')

def group_list(request):

    return TemplateResponse(request,'home/groupclass_list.html',{'groups': Groupclass.objects.all()})

