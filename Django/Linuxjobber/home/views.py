import stripe
import csv, io
import logging
import subprocess, json
import random, string
import pytz
import requests
import os


from smtplib import SMTPException
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib import messages
# from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from rest_framework.authtoken.models import Token
from datetime import timedelta
from weasyprint import HTML, CSS
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import *
from users.models import *
from Courses.models import Course, CoursePermission, UserInterest, CourseTopic
from ToolsApp.models import Tool
from users.models import CustomUser
from .forms import JobPlacementForm, JobApplicationForm, AWSCredUpload, InternshipForm, \
    ResumeForm, PartimeApplicationForm, WeForm, UnsubscribeForm, ItPartnershipForm
from datetime import datetime
from .mail_service import LinuxjobberMailer, handle_failed_campaign

fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/uploads')
# stripe.api_key = settings.STRIPE_SECRET_KEY



# Error Logging Instances
'''Log database errors with the dbalogger instance. example dblogger.level_of_error()
Log non database errors with the standard_logger instance'''
standard_logger = logging.getLogger(__name__)
dbalogger = logging.getLogger('dba')
utc = pytz.UTC

ADMIN_EMAIL = 'joseph.showunmi@linuxjobber.com' if not settings.SES_EMAIL else settings.SES_EMAIL
# Using Django
def my_webhook_view(request):
    # Retrieve the request's body and parse it as JSON:
    # body=request
    print(request.body)

    event_json = json.loads(request.body.decode())

    # Do something with event_json

    # Return a response to acknowledge receipt of the event
    return HttpResponse(status=200)


def get_courses():
    return Course.objects.all()


def get_tools():
    return Tool.objects.all()

def test_mail(request):

    mailer = LinuxjobberMailer(
        subject="SoZme",
        to_address="azmayowa@gmail.com",
        header_text="Some item",
        type=None,
        message="This is a needed necessity for living a good live"
    )
    mailer.send_mail()
    return HttpResponse("Ok")

# INDEX VIEW
def index(request):
    return render(request, 'home/index2.html')


def unsubscribe(request):
    form = UnsubscribeForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if CustomUser.objects.filter(email=instance.email).exists():
            # CustomUser.objects.get_or_create(email=instance.email, is_subscribed = False)
            Unsubscriber.objects.get_or_create(email=instance.email)
            success = True
            return render(request, 'home/registration/unsubscribe.html', {'success': success, 'form': form})
        else:
            error = True
            return render(request, 'home/registration/unsubscribe.html', {'error': error, 'form': form})
    else:
        return render(request, 'home/registration/unsubscribe.html', {'form': form})


def generate_username(fullname):
    name = fullname.lower().split(' ')
    lastname = name[- 1]
    firstname = name[0]

    # try initials of first names and full-last name
    username = ' % s% s ' % (firstname[0], lastname)
    if CustomUser.objects.filter(username=username).count() > 0:
        # If that doesn't fit, try first full name plus initials of last names
        username = "{}{}".format(firstname, lastname[0])
        if CustomUser.objects.filter(username=username).count() > 0:
            # If it doesm't fit put first name and number
            users = CustomUser.objects.filter(username__startswith=firstname).order_by('-username').values(
                'username')
            print(users)
            number = 1
            if len(users) > 0:
                last_number_used = users[0]['username'][-1]
                try:
                    if isinstance(eval(last_number_used), int):
                        number = last_number_used + 1
                except Exception:
                    number = int(last_number_used) + 1
                username = '%s%s' % (firstname, number)
            else:
                username = '%s%s' % (firstname, 1)

    return username


def signup(request):
    next_url = ""
    if request.GET.get('next',None):
        next_url = request.GET.get('next',"")
        request.session['next_url'] = next_url
    next_url = request.session.get('next_url',"")
    if request.method == "POST":
        next_url = request.session.get('next_url',"")
        firstname = request.POST['fullname'].split()[0]
        lastname = request.POST['fullname'].split()[1] if len(request.POST['fullname'].split()) > 1 else \
        request.POST['fullname'].split()[0]
        email = request.POST['email']
        password = request.POST['password']
        username = email.split('@')[0]
        next_page = None
        if request.session.get('job_submission_next_page', None):
            next_page = request.session['job_submission_next_page']
        try:
            userd = CustomUser.objects.get(email=email)
            exists = True
            return render(request, 'home/registration/signup.html', {'exists': exists})
        except CustomUser.DoesNotExist:
            try:
                test = CustomUser.objects.get(username=username)
                username = generate_username(fullname=firstname + " " + lastname)
            except CustomUser.DoesNotExist:
                pass
            finally:
                if (firstname):
                    user = CustomUser(username=username, email=email)
                    user.set_password(password)
                    user.first_name = firstname
                    user.last_name = lastname

                    try:
                        user.save()
                    except IntegrityError:
                        username = generate_username(fullname=firstname + " " + lastname)
                        user.username = username
                        user.save()

                    file_path = os.path.join(settings.BASE_DIR, 'emails', 'signup.txt')
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                        

                    mail_message = file_content.format(
                        username =  username,
                        email = email,
                        firstname = firstname,
                        lastname = lastname,
                        env_url =  settings.ENV_URL
                    )
                    mailer = LinuxjobberMailer(
                        subject="Account has been created",
                        to_address= email,
                        header_text="Linuxjobber",
                        type=None,
                        message= mail_message
                    )
                    mailer.send_mail()
                    # send_mail('Account has been Created',
                    #           'Hello ' + firstname + ' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + ' and your email is ' + email + '\n Follow this url to login with your username and password ' + settings.ENV_URL + 'login \n\n Thanks & Regards \n Admin. \n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
                    #           settings.EMAIL_HOST_USER, [email])
                    login(request, user)
                    if 'job_email' in request.session:
                        try:
                            free = FreeAccountClick.objects.get(email=request.session['job_email'])
                            free.registered = 1
                            free.email = email
                            free.save(update_fields=["registered", "email"])
                            request.session["job_email"] = email
                        except FreeAccountClick.DoesNotExist:
                            pass

                    # ip = get_client_ip(request)
                    # add_location(ip,user)
                    if next_url:
                        return redirect(next_url)
                    return render(request, "home/registration/signupfeedback.html",
                                  {'user': user, 'next_page': next_page})
                else:
                    error = True
                    return render(request, 'home/registration/signup.html', {'error': error})
    else:
        if 'job_email' in request.session:
            try:
                free = FreeAccountClick.objects.get(email=request.session['job_email'])
                free.freeaccountclick = 1
                free.save(update_fields=["freeaccountclick"])
            except FreeAccountClick.DoesNotExist:
                pass

        return render(request, 'home/registration/signup.html')


@csrf_exempt
def ulocation(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            res = request.POST
            # print(res)
            try:
                loc = UserLocation.objects.get(user=request.user)
                pass
            except UserLocation.DoesNotExist:
                locuser = UserLocation.objects.create(user=request.user, ipaddress=res['ip'],
                                                      country=res['country_name'], region=res['region'],
                                                      latitude=res['latitude'], longtitude=res['longitude'], )
                locuser.save()

        return HttpResponse(status=200)
    return HttpResponse(status=200)


def add_location(ip, user):
    url = 'https://api.ipgeolocation.io/ipgeo?apiKey=a953f6ff477b431f9a77bfeb4572fd8e&ip=' + str(ip)
    try:
        r = requests.get(url)
        details = r.json()
        if details['country_name'] is not None:
            try:
                loc = UserLocation.objects.get(user=user)
                pass
            except UserLocation.DoesNotExist:
                locuser = UserLocation.objects.create(user=user, ipaddress=ip, country=details['country_name'],
                                                      region=details['city'], latitude=details['latitude'],
                                                      longtitude=details['longitude'], )
                locuser.save()
        else:
            pass
    except requests.exceptions.RequestException as e:
        pass


# Get users IP address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        ip = True
    return ip


def forgot_password(request):
    email = ''
    message = ''
    if request.method == "POST":
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            u = CustomUser.objects.get(email=email)
            u.pwd_reset_token = ''.join(random.choice(string.ascii_lowercase) for x in range(64))
            u.save()
            password_reset_link = 'reset_password/' + str(u.pwd_reset_token)
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'forgotpassword.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            mail_message = file_content.format(
                env = settings.ENV_URL,
                reset_link = password_reset_link
            )
            mailer = LinuxjobberMailer(
                subject="Account Password Reset",
                to_address=email,
                header_text="Linuxjobber",
                type=None,
                message=mail_message
            )
            mailer.send_mail()
            # send_mail('Linuxjobber Account Password Reset',
            #           'Hello, \n' + 'You are receiving this email because we received a request to reset your password,\n ignore this message if you did not initiate the request else click the link below to reset your password.\n' + settings.ENV_URL + '' + password_reset_link + '\n\n Thanks & Regards \n Linuxjobber. \n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])

            return render(request, 'home/registration/forgot_password.html', {
                'message': 'An email with password reset information has been sent to you. Check your email to proceede.'})
        else:
            return render(request, 'home/registration/forgot_password.html',
                          {'message': 'There is no account associated with this email'})
    else:
        return render(request, 'home/registration/forgot_password.html', {'message': message})


def reset_password(request, reset_token):
    message = ''
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            usr = CustomUser.objects.get(pwd_reset_token=reset_token)
            usr.pwd_reset_token = ''.join(random.choice(string.ascii_lowercase) for x in range(64))
            usr.set_password(request.POST['password1'])
            usr.save()
            message = "You have successfully changed your password."
            return render(request, 'home/registration/reset_password.html', {'message': message})
        else:
            message = "Passwords don't match"
            return render(request, 'home/registration/reset_password.html', {'message': message})
    else:
        return render(request, 'home/registration/reset_password.html', {'message': message})


def selfstudy(request):
    return render(request, 'home/selfstudy.html', {'courses': get_courses(), 'tools': get_tools()})


def faq(request):
    faqs = FAQ.objects.filter(is_wefaq=False)
    return render(request, 'home/faq.html', {'faqs': faqs})


def gainexperience(request):
    return render(request, 'home/gainexperience.html', {'courses': get_courses(), 'tools': get_tools()})


def internships(request):
    MAX_UPLOAD_SIZE = "2621440"
    internsh = InternshipDetail.objects.all()[0].date
    if request.method == "POST":
        form = InternshipForm(request.POST, request.FILES)
        if form.is_valid():
            internform = form.save(commit=False)
            internform.save()
            messages.success(request, 'Thanks for applying for the internship which starts on ' + str(internsh.strftime(
                '%b %d, %y')) + '. Please ensure you keep in touch with Linuxjobber latest updates on our various social media platform')

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'signup.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            mail_message = file_content
            mailer = LinuxjobberMailer(
                subject = "Linuxjobber Internship",
                to_address = request.POST['email'],
                header_text = "Linuxjobber",
                type = None,
                message=mail_message
            )
            mailer.send_mail()
            # send_mail('Linuxjobber Internship',
            #           'Hello, you are receiving this email because you applied for an internship at linuxjobber.com, we will review your application and get back to you.\n\n Thanks & Regards \n Linuxjobber.\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [request.POST['email']])
            return render(request, 'home/internships.html', {'form': form, })
    else:
        form = InternshipForm()
    form = InternshipForm()
    return render(request, 'home/internships.html', {'form': form})


def resumeservice(request):
    return render(request, 'home/resumeservice.html')


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
                amount=199 * 100,
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
    return render(request, 'home/resumepay.html', {'stripe_key': stripeset[0].publickey})


@login_required(login_url='/login')
def resumeupload(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resumeform = form.save(commit=False)
            resumeform.user = request.user
            resumeform.save()
            messages.success(request,
                             'Resume has been submitted succesfully, you will be contact by your mentor if more details are required')
            return render(request, 'home/resumeupload.html',
                          {'form': form, 'courses': get_courses(), 'tools': get_tools()})
    else:
        form = ResumeForm()
    form = ResumeForm()
    return render(request, 'home/resumeupload.html', {'form': form, 'courses': get_courses(), 'tools': get_tools()})


def aboutus(request):
    return redirect('home:contact_us')


def policies(request):
    return render(request, 'home/policies.html', {'courses': get_courses(), 'tools': get_tools()})


def jobs(request):
    posts = FullTimePostion.objects.all()
    return render(request, 'home/job_index.html', {'posts': posts})


@csrf_exempt
def position_detail(request, position_type="fulltime"):
    data = FullTimePostion if position_type == "fulltime" else PartTimePostion
    response_data = {}
    if request.POST.get('get_position_detail', None):
        # This method handles AJAX request for job details
        try:
            item = data.objects.get(id=request.POST.get('get_position_detail'))
            response_data['requirement'] = item.requirement
            response_data['responsibility'] = r"{}".format(item.responsibility.replace('\n', '<br>'))
            response_data['job_title'] = item.job_title
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        except:
            pass
    return HttpResponse(json.dumps(None),
                        content_type="application/json")


def partime(request):
    cv = None
    position = None
    high = None
    message = None
    pos = None
    if request.method == "POST":
        form = PartimeApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            pos = PartTimePostion.objects.get(id=request.POST['position'])
            try:
                PartTimeJob.objects.get(email=request.POST['email'], position=pos)
                messages.success(request,
                                 "Sorry We could not submit your application as you have applied for that role before.")
                return redirect("home:partime")
            except PartTimeJob.DoesNotExist:
                pass

            newform = form.save(commit=False)
            newform.save()
            request.session['job_email'] = request.POST['email']
            request.session['job_fullname'] = request.POST['fullname']
            request.session['page'] = 'Job Feedback'

            try:
                freeexist = FreeAccountClick.objects.get(email=request.session['job_email'])
            except FreeAccountClick.DoesNotExist:
                freeclick = FreeAccountClick(fullname=request.session['job_fullname'],
                                             email=request.session['job_email'], filled_jobs=1, freeaccountclick=0,
                                             from_what_page=request.session['page'], registered=0, visited_tryfree=0,
                                             paid=0)
                freeclick.save()

            if not request.POST['cv_link']:
                cv = newform.cv.url
            else:
                cv = request.POST['cv_link']

            position = PartTimePostion.objects.get(id=request.POST['position'])

            if request.POST['high_salary'] == '1':
                high = 'Yes'
            else:
                high = 'No'

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'parttimeapplicant.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'parttimeadmin.txt')
            with open(file_path, 'r') as f:
                file_content2 = f.read()

            message_applicant = file_content.format(
                env = settings.ENV_URL
            )



            # send_mail('Linuxjobber Newsletter', message, settings.EMAIL_HOST_USER, [request.POST['email']])
            message_admin = file_content2.format(
                fullname = request.POST['fullname'],
                email =  request.POST['email'],
                title = position.job_title,
                cv = cv,
                phone = request.POST['phone'],
                salary = high
            )

            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter",
                to_address=request.POST['email'],
                header_text="Linuxjobber Jobs",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            mailer_admin = LinuxjobberMailer(
                subject="Part-Time Job Application Alert",
                to_address = ADMIN_EMAIL,
                header_text="Linuxjobber Jobs",
                type=None,
                message=message_admin
            )
            mailer_admin.send_mail()
            # send_mail('Part-Time Job Application Alert',
            #           'Hello,\n' + request.POST['fullname'] + ' with email: ' + request.POST[
            #               'email'] + ' just applied for a part time role, ' + position.job_title + '.\nCV can be found here: ' + cv + '\n Phone number is: ' +
            #           request.POST[
            #               'phone'] + ' and high salary choice is: ' + high + '.\nplease kindly review.\n\n Thanks & Regards \n Linuxjobber. \n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, ['joseph.showunmi@linuxjobber.com'])
            return redirect("home:jobfeed")
        else:
            return render(request, 'home/job_application_parttime.html',
                          {'form': form, 'position': PartTimePostion.objects.all()})
    else:
        form = PartimeApplicationForm()
    form = PartimeApplicationForm()
    return render(request, 'home/job_application_parttime.html', {'form': form,
                                                                  'position': PartTimePostion.objects.all()})


@login_required
def jobchallenge(request, respon=None):
    if respon:
        file_path = os.path.join(settings.BASE_DIR, 'emails', 'jobchallenge.txt')
        with open(file_path, 'r') as f:
            file_content = f.read()

        message = file_content.format(
            env = settings.ENV_URL
        )
        
        mailer = LinuxjobberMailer(
            subject="Job Challenge",
            to_address = request.user.email,
            header_text="Linuxjobber Johs",
            type=None,
            message=message
        )
        mailer.send_mail()
        # send_mail('Linuxjobber Job Challenge', message, settings.EMAIL_HOST_USER, [request.user.email])
        return redirect("home:index")
    return render(request, 'home/jobchallenge.html')


from enum import Enum


class JobAnswers(Enum):
    """

    """
    interested = "interested"
    not_interested = "not_interested"
    skilled = "skilled"


def jobfeed(request, is_fulltime=0):
    """
    Handles page user is to be sent to after signing up
    We make use of a request.session key 'job_submission_next_page' to track

    :param request:
    :param is_fulltime:
    :return page:
    """
    if is_fulltime:

        job_id = request.session.get('selected_job_id', None)
        if job_id:
            try:
                selected_job = FullTimePostion.objects.get(id=job_id)
            except:
                pass
            if request.method == "POST":
                selected_option = request.POST.get('interest', None)
                applicant_email = request.session.get('job_email', None)
                if selected_job and applicant_email:
                    application_entry = Job.objects.get(position=selected_job, email=applicant_email)
                    application_entry.interest = selected_option
                    application_entry.save()
                if selected_option == JobAnswers.interested.value:  # Sets to already specified next_page_url for job
                    request.session['job_submission_next_page'] = selected_job.interested_page
                    return redirect("home:jobfeed")
                elif selected_option == JobAnswers.not_interested.value:  # Send to try free page
                    request.session['job_submission_next_page'] = selected_job.not_interested_page
                    return redirect('home:jobfeed')
                elif selected_option == JobAnswers.skilled.value:  # Send to Work Experience
                    request.session['job_submission_next_page'] = selected_job.skilled_page
                    return redirect('home:jobfeed')
                    # return redirect(selected_job.skilled_page)
            return TemplateResponse(request, 'home/job_application_submitted.html',
                                    {'is_fulltime': True, 'job': selected_job})

    return render(request, 'home/job_application_submitted.html')


def linux_start(request):
    return render(request, 'home/linux_start.html')


def jobapplication(request, job):
    try:
        posts = FullTimePostion.objects.get(id=job)
    except FullTimePostion.DoesNotExist:
        return redirect("home:jobs")
    cv = None

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            jobform = form.save(commit=False)
            try:
                Job.objects.get(email=request.POST['email'], position=posts)
                messages.success(request,
                                 "Sorry We could not submit your application as you have applied for this role before.")
                return redirect("home:jobapplication", job=job)
            except Job.DoesNotExist:
                pass
            jobform.position = posts
            jobform.save()

            request.session['job_email'] = request.POST['email']
            request.session['job_fullname'] = request.POST['fullname']
            request.session['page'] = 'Job Feedback'

            try:
                freeexist = FreeAccountClick.objects.get(email=request.session['job_email'])
            except FreeAccountClick.DoesNotExist:
                freeclick = FreeAccountClick(fullname=request.session['job_fullname'],
                                             email=request.session['job_email'], filled_jobs=1, freeaccountclick=0,
                                             from_what_page=request.session['page'], registered=0, visited_tryfree=0,
                                             paid=0)
                freeclick.save()

            if not request.POST['cv_link']:
                cv = jobform.resume.url
            else:
                cv = request.POST['cv_link']

            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you applied for a full-time role at linuxjobber.com, we will review your application and get back to you.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [request.POST['email']])


            # send_mail('Full-Time Job Application Alert',
            #           'Hello,\n' + request.POST['fullname'] + ' with email: ' + request.POST[
            #               'email'] + 'just applied for a full time role, ' + posts.job_title + '. \nCV can be found here: ' + cv + '\n Phone number is:' +
            #           request.POST[
            #               'phone'] + '\nplease kindly review.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, ['joseph.showunmi@linuxjobber.com'])
            
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'jobapplicationadmin.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'jobapplicationapplicant.txt')
            with open(file_path, 'r') as f:
                file_content2 = f.read()
            
            message_applicant = file_content2
            message_admin = file_content.format(
                fullname=request.POST['fullname'],
                email=request.POST['email'],
                title=posts.job_title,
                cv=cv,
                phone=request.POST['phone'],
            )

            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter",
                to_address=request.POST['email'],
                header_text="Linuxjobber Jobs",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            mailer_admin = LinuxjobberMailer(
                subject="Full-Time Job Application Alert",
                to_address=ADMIN_EMAIL,
                header_text="Linuxjobber Jobs",
                type=None,
                message=message_admin
            )
            mailer_admin.send_mail()

            # Set job_picked to session so they are redirected accordingly after login
            request.session['selected_job_id'] = posts.pk
            return redirect("home:jobfeed", is_fulltime=1)
        else:
            form = JobApplicationForm()
            return render(request, 'home/job_application.html', {'form': form, 'posts': posts})
    else:
        form = JobApplicationForm()
    form = JobApplicationForm()
    return render(request, 'home/job_application.html', {'form': form, 'posts': posts})


def resume(request):
    return render(request, 'home/resume.html', {'courses': get_courses(), 'tools': get_tools()})


def perform_registration_checks(user, next=""):
    if user.role == 4:
        check_permission_expiry(user)
    if next == "":
        # check if user paid for work experience and has not filled the form
        try:
            weps = wepeoples.objects.get(user=user)
            if not weps.types:
                return redirect("home:workexpform")
        except wepeoples.DoesNotExist:
            pass

        stats = UserInterest.objects.filter(user=user)

        if next:
            return redirect(next)
        elif stats:
            return redirect("home:index")
        else:
            return redirect("Courses:userinterest")
    else:
        return HttpResponseRedirect(next)


def log_in(request):
    next = ''
    if request.method == "GET":
        next = request.GET.get('next',"")
        request.session['next_url'] = next
    error_message = ''
    if request.user.is_authenticated:
        return perform_registration_checks(request.user, next)

    if request.method == "POST":
        next = request.session.get("next_url","")
        user_name = request.POST['username']
        password = request.POST['password']
        key = 'email' if '@' in user_name else 'username'
        try:
            if key == 'email':
                user = CustomUser.objects.get(email=user_name)
            else:
                user = CustomUser.objects.get(username=user_name)
                print(user)
            if not user.is_active:
                error_message = "Sorry, account disabled, contact the administrator"
            if not error_message:
                if check_password(password, user.password):
                    a = authenticate(username=user_name, password=password)
                    login(request, user)
                else:
                    error_message = "Invalid Password"
        except CustomUser.DoesNotExist:
            error_message = "Sorry, No account exists with the username"

        finally:
            if error_message:
                return TemplateResponse(request, "home/registration/login.html", {"error_message": error_message})

            return perform_registration_checks(request.user, next)

    return TemplateResponse(request, 'home/registration/login.html', {'error_message': error_message})


def check_permission_expiry(user):
    perms = ""
    try:
        perms = CoursePermission.objects.filter(user=user)
        print(perms)
        for perm in perms:
            # expired
            if perm.expiry_date.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
                perm.delete()
                return True
            else:
                return True
    except CoursePermission.DoesNotExist:
        return True


def log_out(request):
    logout(request)
    return render(request, "home/registration/logout.html")


def linux_full_training(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email=email)
            subscriber.save()
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'newsletter.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()

            message_applicant = file_content
            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter Subscription",
                to_address= email,
                header_text="Linuxjobber Newsletter",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()
            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])
            return render(request, 'home/linux_full_training.html',
                          {'news_letter_message': 'You have successfully subscribed to our news letter!',
                           'courses': get_courses(), 'tools': get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render(request, 'home/linux_full_training.html',
                          {'news_letter_message': 'Something went wrong please try again!', 'courses': get_courses(),
                           'tools': get_tools()})
    else:
        return render(request, 'home/linux_full_training.html', {'news_letter_message': news_letter_message})

def completeclass(request,course):
    expired = False
    today = False
    tomorrow = False
    try:
        page = CompleteClass.objects.get(slug=course)
        page_learn = CompleteClassLearn.objects.filter(completeclass=page)
        page_cert = CompleteClassCertificate.objects.filter(completeclass=page)
        courses = CourseTopic.objects.filter(course=page.course)
        tm = timezone.now() + timedelta(days=1)
        td = datetime.now()
        td = utc.localize(td)

        if tm.date() ==  page.due_date.date():
            tomorrow = True
        if td > page.due_date:
            expired = True
        if td.date() == page.due_date.date():
            today = True

        
    except CompleteClass.DoesNotExist:
        raise Http404

    return render(request, 'home/aws_full_train.html', {'page':page,'learn':page_learn,'cert':page_cert,'tomorrow':tomorrow,'today':today, 'expired':expired, 'curses': courses})

def aws_full_training(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email=email)
            subscriber.save()
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'newsletter.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content
            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter Subscription",
                to_address=email,
                header_text="Linuxjobber Newsletter",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()
            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])
            return render(request, 'home/aws_full_training.html',
                          {'news_letter_message': 'You have successfully subscribed to our news letter!',
                           'courses': get_courses(), 'tools': get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render(request, 'home/aws_full_train.html',
                          {'news_letter_message': 'Something went wrong please try again!', 'courses': get_courses(),
                           'tools': get_tools()})
    else:
        return render(request, 'home/aws_full_train.html',
                      {'news_letter_message': news_letter_message, 'courses': get_courses(), 'tools': get_tools()})


def oracledb_full_training(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email=email)
            subscriber.save()

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'newsletter.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content
            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter Subscription",
                to_address=email,
                header_text="Linuxjobber Newsletter",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])
            return render(request, 'home/oracledb_full_training.html',
                          {'news_letter_message': 'You have successfully subscribed to our news letter!',
                           'courses': get_courses(), 'tools': get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render(request, 'home/oracledb_full_training.html',
                          {'news_letter_message': 'Something went wrong please try again!', 'courses': get_courses(),
                           'tools': get_tools()})
    else:
        return render(request, 'home/oracledb_full_training.html',
                      {'news_letter_message': news_letter_message, 'courses': get_courses(), 'tools': get_tools()})


def linux_certification(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email=email)
            subscriber.save()

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'newsletter.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content
            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter Subscription",
                to_address=email,
                header_text="Linuxjobber Newsletter",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])
            return render(request, 'home/linux_certification.html',
                          {'news_letter_message': 'You have successfully subscribed to our news letter!',
                           'courses': get_courses(), 'tools': get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render(request, 'home/linux_certification.html',
                          {'news_letter_message': 'Something went wrong please try again!', 'courses': get_courses(),
                           'tools': get_tools()})
    else:
        return render(request, 'home/linux_certification.html',
                      {'news_letter_message': news_letter_message, 'courses': get_courses(), 'tools': get_tools()})


def aws_certification(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email=email)
            subscriber.save()

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'newsletter.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content
            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter Subscription",
                to_address=email,
                header_text="Linuxjobber Newsletter",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])
            return render(request, 'home/aws_certification.html',
                          {'news_letter_message': 'You have successfully subscribed to our newsletter!',
                           'courses': get_courses(), 'tools': get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render(request, 'home/aws_certification.html',
                          {'news_letter_message': 'Something went wrong please try again!', 'courses': get_courses(),
                           'tools': get_tools()})
    else:
        return render(request, 'home/aws_certification.html',
                      {'news_letter_message': news_letter_message, 'courses': get_courses(), 'tools': get_tools()})


def oracledb_certification(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email=email)
            subscriber.save()
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'newsletter.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content
            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter Subscription",
                to_address=email,
                header_text="Linuxjobber Newsletter",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()
            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])
            return render(request, 'home/oracledb_certification.html',
                          {'news_letter_message': 'You have successfully subscribed to our news letter!',
                           'courses': get_courses(), 'tools': get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render(request, 'home/oracledb_certification.html',
                          {'news_letter_message': 'Something went wrong please try again!', 'courses': get_courses(),
                           'tools': get_tools()})
    else:
        return render(request, 'home/oracledb_certification.html',
                      {'news_letter_message': news_letter_message, 'courses': get_courses(), 'tools': get_tools()})


def devops_class(request):
    return render(request, 'home/devops.html')


@login_required
def devops_pay(request):
    PRICE = 1225
    mode = "One Time Payment"
    PAY_FOR = "DevOps Course"
    DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time within 14 days for a full refund. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${} One Time".format(
        PRICE, PRICE)
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey

    if request.method == "POST":
        stripe.api_key = stripeset[0].secretkey
        token = request.POST.get("stripeToken")
        try:
            charge = stripe.Charge.create(
                amount=PRICE * 100,
                # Stripe uses cent notation for amount: 10 USD = 10 * 100
                currency='usd',
                description='DevOps Course Payment',
                source=token,
            )
        except stripe.error.CardError as ce:
            return False, ce
        else:
            try:
                UserPayment.objects.create(user=request.user, amount=PRICE,
                                           trans_id=charge.id, pay_for=charge.description, )

                # send_mail('Linuxjobber DevOps Course Subscription',
                #           'Hello, you have successfuly subscribed for our DevOps Course package.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
                #           settings.EMAIL_HOST_USER, [request.user.email])
                file_path = os.path.join(settings.BASE_DIR, 'emails', 'devopspay.txt')
                with open(file_path, 'r') as f:
                    file_content = f.read()
                message_applicant = file_content
                mailer_applicant = LinuxjobberMailer(
                    subject="DevOps Course Subscription",
                    to_address= request.user.email,
                    header_text="Linuxjobber",
                    type=None,
                    message=message_applicant
                )
                mailer_applicant.send_mail()

                return render(request, 'home/devops_pay_success.html')
            except SMTPException as error:
                print(error)
                return render(request, 'home/devops_pay_success.html')
            except Exception as error:
                print(error)
                return redirect("home:index")
    else:
        context = {"stripe_key": stripeset[0].publickey,
                   'price': PRICE,
                   'amount': str(PRICE) + '00',
                   'mode': mode,
                   'PAY_FOR': PAY_FOR,
                   'DISCLMR': DISCLMR,
                   'courses': get_courses(),
                   'tools': get_tools()}
        return render(request, 'home/devops_pay.html', context)


def workexperience(request):
    PRICE=None
    if request.user.is_authenticated:
        try:
            workexp = wepeoples.objects.get(user=request.user)
            return redirect("home:workexprofile")
        except wepeoples.DoesNotExist:
            pass
        try:
            wav = WorkExperiencePriceWaiver.objects.get(user=request.user)
            if wav.is_enabled:
                PRICE = wav.price
                PRICE = PRICE.replace(',','')
                PRICE = PRICE.split('.')[0]
        except WorkExperiencePriceWaiver.DoesNotExist:
            PRICE = None
    else:
        pass
    return render(request, 'home/work_experience.html', {'PRICE':PRICE})


def workterm(request):
    return render(request, 'home/workexpterm.html')


@login_required
def workexpform(request):
    form = WeForm()

    try:
        details =  WorkExperienceEligibility.objects.get(user=request.user)
    except  WorkExperienceEligibility.DoesNotExist:
        return redirect("home:eligibility")
    
    try:
        deta = WorkExperienceIsa.objects.get(user=request.user)
    except WorkExperienceIsa.DoesNotExist:
        return redirect("home:isa")

    try:
        eta = WorkExperienceIsa.objects.get(user=request.user)
        if eta.is_signed_isa == True:
            pass
        else:
            return redirect("home:workexpisa2")
    except WorkExperienceIsa.DoesNotExist:
        return redirect("home:isa")

    try:
        jot =  WorkExperienceIsa.objects.get(user=request.user)
        comp = jot.estimated_date_of_program_completion
        comp = comp.strftime('%Y-%m-%d')

    except WorkExperienceIsa.DoesNotExist:
        jot = None
        comp = None
        

    if request.method == 'POST':
        trainee = request.POST['types']
        trainee = wetype.objects.get(id=trainee)
        current = request.POST['current_position']
        state = request.POST['state']
        income = request.POST['income']
        relocate = request.POST['relocate']
        date = request.POST['date']

        today = datetime.now().strftime("%Y-%m-%d")
        month6 = datetime.now() + timedelta(days=180)
        month6 = month6.strftime("%Y-%m-%d")

            

        if date < today:
            try:
                person = werole.objects.get(roles='Trainee')
            except werole.DoesNotExist:
                person = werole.objects.create(roles='Trainee')
                person.save()

        else:
            if today < date < month6:
                try:
                    person = werole.objects.get(roles='Graduant')
                except werole.DoesNotExist:
                    person = werole.objects.create(roles='Graduant')
                    person.save()
            else:
                try:
                    person = werole.objects.get(roles='Student')
                except werole.DoesNotExist:
                    person = werole.objects.create(roles='Student')
                    person.save() 

        try:
            weps = wepeoples.objects.get(user=request.user)
            weps.types = trainee
            weps.current_position = current
            weps.person = person
            weps.state = state
            weps.income = income
            weps.relocation = relocate
            weps.profile_picture = None
            weps.last_verification = None
            weps.Paystub = None
            weps.start_date = None
            weps.graduation_date = None
            weps.save()
        except wepeoples.DoesNotExist:
            weps = wepeoples.objects.create(user=request.user, types=trainee,
                                            current_position=current, person=person, state=state, income=income,
                                            relocation=relocate, last_verification=None, Paystub=None,
                                            graduation_date=None, start_date=None)
            weps.save()
        return redirect("home:workexprofile")
    else:
        return render(request, 'home/workexpform.html', {'form': form,'details': details,'comp':comp})

def work_experience_eligible_pdf(user):
    try:
        details =  WorkExperienceEligibility.objects.get(user=user)
        date = details.date_of_birth
        date = date.strftime('%m/%d/%Y')
        created = details.date_created
        created = created.strftime('%Y/%m/%d')
        ssn = details.SSN
        ssn = ssn[-4:]
        ssn = "•••••" + ssn
        
    except  WorkExperienceEligibility.DoesNotExist:
        details = None
        date = None
        created = None
    #return render(request, 'home/workexpeligibilitypdf.html')
    html_template = get_template('home/workexpeligibilitypdf.html').render({'details':details,'date':date,'ssn':ssn,'created':created})


    pdf_file = HTML(string=html_template).write_pdf( stylesheets=[CSS("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css")],presentational_hints=True)
    details.pdf = SimpleUploadedFile('Work-Experience-Eligibility-'+ details.user.first_name +' '+details.user.last_name +'.pdf', pdf_file, content_type='application/pdf')
    details.save()
    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return True


def work_experience_isa_pdf(user):
    #return render(request, 'home/workexpisapdf.html')

    try:
        details =  WorkExperienceEligibility.objects.get(user=user)
        
    except  WorkExperienceEligibility.DoesNotExist:
        details = None

    try: 
        det = WorkExperienceIsa.objects.get(user=user)
    except WorkExperienceIsa.DoesNotExist:
        det = None

    html_template = get_template('home/workexpisapdf.html').render({'user':details})


    pdf_file = HTML(string=html_template).write_pdf( stylesheets=[CSS("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css")],presentational_hints=True)
    det.pdf = SimpleUploadedFile('Work-Experience-ISA-'+ details.user.first_name +' '+details.user.last_name +'.pdf', pdf_file, content_type='application/pdf')
    det.save()
    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return True

def work_experience_term_pdf(user):
    #return render(request, 'home/workexptermpdf.html')
    try:
        details =  WorkExperienceEligibility.objects.get(user=user)
        
    except  WorkExperienceEligibility.DoesNotExist:
        details = None


    html_template = get_template('home/workexptermpdf.html').render({'user':details})


    pdf_file = HTML(string=html_template).write_pdf( stylesheets=[CSS("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css")],presentational_hints=True)
    details.terms = SimpleUploadedFile('Work-Experience-Terms-'+ details.user.first_name +' '+details.user.last_name +'.pdf', pdf_file, content_type='application/pdf')
    details.save()
    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return True

@login_required
def work_experience_eligible(request):

    try:
        details =  WorkExperienceEligibility.objects.get(user=request.user)
        date = details.date_of_birth
        date = date.strftime('%m/%d/%Y')
        created = details.date_created
        created = created.strftime('%Y-%m-%d') 
    except  WorkExperienceEligibility.DoesNotExist:
        details = None
        date = None
        created = None
        

    dater = datetime.now().strftime('%Y-%m-%d')


    if request.method == "POST":
        print(request.POST)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        middleinitial = request.POST['initial']
        othername = request.POST['othername']
        state = request.POST['state']
        address = request.POST['address']
        Apt = request.POST['aptno']
        city = request.POST['city']
        zipc = request.POST['zip']
        dob = request.POST['dob']
        dob = datetime.strptime(dob,'%m/%d/%Y').date()
        ssn = request.POST['ssn']
        email = request.POST['eadress']
        eadress = request.POST['eadress']
        tel = request.POST['tel']
        i_am = request.POST['selector']
        translator = request.POST['selectza']


        if translator == 1:
            result = True
        else:
            result = False

        if i_am == '2':
            alien_no = request.POST['alien1']
        else:
            alien_no = None

        if i_am == '3':
            expiry_date = request.POST['exp']
            form19 = request.POST['form19']
            foreign = request.POST['foreign']
        else:
            expiry_date = None
            form19 = None
            foreign = None

        try: 
            det = WorkExperienceEligibility.objects.get(user=request.user)
            det.first_name = firstname
            det.last_name = lastname
            det.middle_initial = middleinitial
            det.middle_name = othername
            det.address = address
            det.apt_number = Apt
            det.city = city
            det.zip_code=zipc
            det.date_of_birth = dob
            det.SSN= ssn
            det.state = state
            det.employee_address = eadress
            det.employee_email = email
            det.employee_phone = tel
            det.expiry_date = expiry_date
            det.preparer_or_translator = result
            det.i_am_a = i_am
            det.Alien_reg_num=alien_no
            det.form_19_num=form19
            det.foreign_pass_num=foreign

            det.save()
            work_experience_eligible_pdf(det.user)
            work_experience_term_pdf(det.user)
            return redirect("home:isa")
        except WorkExperienceEligibility.DoesNotExist:
            state = WorkExperienceEligibility.objects.create(user=request.user,first_name=firstname,last_name=lastname,middle_initial=middleinitial,middle_name=othername,state=state,address=address,apt_number=Apt,city=city,zip_code=zipc,date_of_birth=dob,SSN=ssn,employee_address=eadress,employee_email=email,employee_phone=tel,expiry_date=expiry_date,preparer_or_translator=translator,i_am_a=i_am,Alien_reg_num=alien_no,form_19_num=form19,foreign_pass_num=foreign)
            state.save()
            work_experience_eligible_pdf(request.user)
            work_experience_term_pdf(request.user)
        return redirect("home:isa")  
    return render(request, 'home/workexpeligibility.html',{'details':details,'date':date,'dater':dater,'created':created})

@login_required
def work_experience_isa_part_1(request):
    try:
        details =  WorkExperienceEligibility.objects.get(user=request.user)
        date = details.date_of_birth
        date = date.strftime('%Y-%m-%d')
        ssn = details.SSN
        ssn = ssn[-4:]
        ssn = "•••••" + ssn

    except  WorkExperienceEligibility.DoesNotExist:
        return redirect("home:eligibilty")
        details = None
        date = None
        ssn = None

    try:
        paid = WorkExperiencePay.objects.get(user=request.user)
    except WorkExperiencePay.DoesNotExist:
        return redirect("home:pay")

    try:
        jot =  WorkExperienceIsa.objects.get(user=request.user)
        comp = jot.estimated_date_of_program_completion
        comp = comp.strftime('%Y-%m-%d')
        grad = None

    except WorkExperienceIsa.DoesNotExist:
        jot = None
        comp = None
        grad = datetime.now() + timedelta(days=90)
        grad = grad.strftime('%Y-%m-%d')

    if request.method == "POST":
        email = request.POST['email']
        income = request.POST['income']
        pay = request.POST['payment']
        edu = request.POST['edu']
        status = request.POST['status']
        completion = request.POST['date']

        try:
            det = WorkExperienceIsa.objects.get(user=request.user)
            det.is_signed_isa=False
            det.current_annual_income=income
            det.monthly_House_payment=pay
            det.highest_level_education=edu
            det.employment_status=status
            det.estimated_date_of_program_completion=completion
            det.email = email
            det.save()
        except WorkExperienceIsa.DoesNotExist:
            state = WorkExperienceIsa.objects.create(user=request.user,email=email,is_signed_isa=False,current_annual_income=income,monthly_house_payment=pay,highest_level_education=edu,employment_status=status,estimated_date_of_program_completion=completion)
            state.save()


        if paid.includes_job_placement:
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'workexperience.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content
        else:
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'workexperience2.txt')
            with open(file_path, 'r') as f:
                file_content2 = f.read()
            message_applicant = file_content2

        mailer_applicant = LinuxjobberMailer(
            subject="Agreement Signed Successful",
            to_address=request.user.email,
            header_text="Linuxjobber Work Experience",
            type=None,
            message=message_applicant
        )
        mailer_applicant.send_mail()


        return redirect("home:workexpisa2")
    return render(request, 'home/workexpisa.html',{'details':details,'ssn':ssn,'paid':paid,'grad':grad,'jot':jot,'date':date,'comp':comp})

def work_experience_isa_part_2(request):

    try:
        details =  WorkExperienceEligibility.objects.get(user=request.user)
    except  WorkExperienceEligibility.DoesNotExist:
        details = None


    try:
        jot = WorkExperienceIsa.objects.get(user=request.user)
    except WorkExperienceIsa.DoesNotExist:
        return redirect("home:isa")
        

    if request.method == "POST":
        sign = request.POST['fullname']

        try:
            jot = WorkExperienceIsa.objects.get(user=request.user)
            jot.is_signed_isa = True
            jot.save()
            work_experience_isa_pdf(details.user)
            return redirect("home:workexpform")
        except WorkExperienceIsa.DoesNotExist:
            return redirect("home:isa")
        
    
    return render(request, 'home/workexpisa2.html', {'details':details})

@login_required
def workexprofile(request):

    try:
        details =  WorkExperienceEligibility.objects.get(user=request.user)
    except  WorkExperienceEligibility.DoesNotExist:
        return redirect("home:eligibility")

    try:
        isa = WorkExperienceIsa.objects.get(user=request.user)
        if isa.is_signed_isa == False:
            return redirect("home:workexpisa2")
    except WorkExperienceIsa.DoesNotExist:
        return redirect("home:isa")

    try:
        eta = WorkExperienceIsa.objects.get(user=request.user)
        
    except WorkExperienceIsa.DoesNotExist:
        return redirect("home:isa")
    
    group = []
    try:
        weps = wepeoples.objects.get(user=request.user)

        if not weps.types:
            return redirect("home:workexpform")
    except wepeoples.DoesNotExist:
        return redirect("home:workexperience")

    status = wework.objects.filter(we_people__user=request.user)

    for sta in status:
        group.append(sta.task.id)

    listask = wetask.objects.filter(types=weps.types)

    if request.method == "POST":
        if request.POST['type'] == '1':
            last_verify = request.FILES['verify']
            weps.Paystub = last_verify
            weps.last_verification = datetime.now()
            weps.save(update_fields=["Paystub", "last_verification"])

            link = weps.Paystub.url

            # send_mail('Pay Stub verification needed',
            #           'Hello,\n ' + request.user.email + ' just uploaded is pay stub at: ' + link + '.\nPlease review and confirm last verification\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, ['joseph.showunmi@linuxjobber.com'])
            
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'workexperienceprofile.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content.format(
                email =  request.user.email,
                link = link
            )
            mailer_applicant = LinuxjobberMailer(
                subject="Paystub Verification Needed",
                to_address=ADMIN_EMAIL,
                header_text="Linuxjobber Work Experience",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            messages.success(request,
                             'Paystub uploaded successfully, Last verification would be confirmed as soon as Paystub is verified')
            return redirect("home:workexprofile")
        elif request.POST['type'] == '2':
            income = request.POST['income']
            weps.income = income
            weps.save(update_fields=['income'])
            messages.success(request, 'Total monthly income updated successfully')
            return redirect("home:workexprofile")
        elif request.POST['type'] == '3':
            u = CustomUser.objects.get(email=request.user.email)
            u.first_name = request.POST['first_name']
            u.last_name = request.POST['last_name']
            u.save(update_fields=["last_name", "first_name"])
            messages.success(request, 'Your names have been updated successfully')
            return redirect("home:workexprofile")
        elif request.POST['type'] == '4':
            weps.state = request.POST['state']
            weps.save(update_fields=["state"])
            messages.success(request, 'State updated successfully')
            return redirect("home:workexprofile")
        elif request.POST['type'] == '5':
            weps.profile_picture = request.FILES['profile']
            weps.save(update_fields=['profile_picture'])
            messages.success(request, 'Profile picture updated successfully')
            return redirect("home:workexprofile")
        else:
            messages.error(request, 'Sorry, an error occured. please contact admin@linuxjobber.com')
            return redirect("home:workexprofile")

    if not weps.profile_picture:
        messages.error(
            request,
            "!!! Profile picture is required. Please upload it now"
        )

    
    url = settings.ENV_URL

    work_experience_eligible_pdf(details.user)
    work_experience_term_pdf(details.user)
    work_experience_isa_pdf(details.user)
    if not details.pdf:
        return redirect("home:workexprofile")
    pdf = details.pdf.url
    pdf2 = details.terms.url
    pdf3 = isa.pdf.url
    
    


    return render(request, 'home/workexprofile.html',
                  {'weps': weps, 'status': status, 'group': group, 'listask': listask, 'details':details, 'url':url, 'pdf':pdf, 'pdf2':pdf2, 'pdf3':pdf3})


def workexpfaq(request):
    above_fifty_percent = FAQ.objects.filter(
        is_wefaq=True, is_fifty_percent_faq=True
    )

    below_fifty_percent = FAQ.objects.filter(
        is_wefaq=True, is_fifty_percent_faq=False
    )

    context = {
        'above_fifty_percent': above_fifty_percent,
        'below_fifty_percent': below_fifty_percent,
        'faq_above_fifty_is_visible': FAQ.wefaq_is_visible_for(
            request.user, wepeoples
        )
    }

    return render(request, 'home/workexpfaq.html', context)


def jobplacements(request):
    return render(request, 'home/jobplacements.html', {'courses': get_courses(), 'tools': get_tools()})


def get_application_grade(exp, certif, train, reloc):
    grade = 10
    if exp > 0: grade += 20
    if certif.lower() == 'yes': grade += 30
    if train.lower() == 'yes': grade += 30
    if reloc.lower() == 'yes': grade += 10
    return grade


@login_required
def apply(request, level):
    if request.method == "GET":
        return render(request, 'home/apply.html', {'level': level, 'courses': get_courses()})
    else:
        form = JobPlacementForm(request.POST)
        if form.is_valid():
            certificates = request.FILES.getlist('certificates')
            if certificates:
                for f in certificates:
                    fs.save(os.path.join('certs', request.user.username, f.name), f)
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
            placement_grade = get_application_grade(experience, is_certified,
                                                    training, can_relocate)
            try:
                Jobplacement.objects.create(user=request.user, level=lvl,
                                            education=education, career=career, resume=resume,
                                            placement_grade=placement_grade, experience=experience,
                                            is_certified=is_certified, training=training, can_relocate=can_relocate,
                                            awareness=awareness,
                                            )
                if placement_grade != 100:
                    context = {
                        'issue_lvl': 1,
                        'msg': 'Sorry, you did not meet the job requirements',
                        'redirinfo': {
                            'txt': "Apply Now" if level == 'snr' else "Get Certificate",
                            'msg': 'Click the Apply Now button below for placement to junior level role.' if level == 'snr' else "Click the Get Certificate button below to apply for our certification course.",
                            'url': reverse('home:apply', args=['jnr']) if level == 'snr' else reverse('home:selfstudy'),
                        },
                        'level': level,
                    }
                    return render(request, 'home/failed_application.html', context)
                # send_mail('Linuxjobber Jobplacement Program',
                #           'Hello, you have succesfully signed up for Linuxjobber Jobplacement program,\n\nIf you havent signed the agreement, visit this link to do so: https://leif.org/commit?product_id=5b304639e59b74063647c484#/.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
                #           settings.EMAIL_HOST_USER, [request.user.email])
                
                file_path = os.path.join(settings.BASE_DIR, 'emails', 'apply.txt')
                with open(file_path, 'r') as f:
                    file_content = f.read()
                message_applicant = file_content
                mailer_applicant = LinuxjobberMailer(
                    subject="Subscription Success",
                    to_address=request.user.email,
                    header_text="Linuxjobber Job Placement",
                    type=None,
                    message=message_applicant
                )
                mailer_applicant.send_mail()
                message_admin = """
                    Hello, 
                    {email}
                    just succesfully applied for Jobplacement Program.
                    
                    Warm Regards,
                    Linuxjobber

                """.format(
                    email =  request.user.email
                )
                mailer = LinuxjobberMailer(
                        subject="Jobplacement registration successful",
                        to_address= ADMIN_EMAIL,
                        header_text="Linuxjobber",
                        type=None,
                        message= message_admin
                    )
                mailer.send_mail()

                return render(request, 'home/jobaccepted.html')
            except Exception as error:
                print(error)
                context = {
                    'issue_lvl': 2,
                    'msg': 'Sorry, you did not meet the job requirements',
                }
                return render(request, 'home/failed_application.html', context)



@login_required
def pay(request):
    PRICE = 399
    mode = "One Time"
    PAY_FOR = "Work Experience"
    DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${}".format(
        PRICE, PRICE)
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey
    optiona = False
    try:
        workexp = wepeoples.objects.get(user=request.user)
        return redirect("home:workexprofile")
    except wepeoples.DoesNotExist:
        pass

    try:
        wav = WorkExperiencePriceWaiver.objects.get(user=request.user)
        if wav.is_enabled:
            PRICE = wav.price
            PRICE = PRICE.replace(',','')
            PRICE = PRICE.split('.')[0]
    except WorkExperiencePriceWaiver.DoesNotExist:
        PRICE = 399
        pass

    if request.method == "POST":
        token = request.POST.get("stripeToken")
        jobplacement = request.POST["workexperience"]


        if PRICE == '0':
            UserPayment.objects.create(user=request.user, amount=PRICE, trans_id='-', pay_for=PAY_FOR)
        else:
            try:
                charge = stripe.Charge.create(
                    amount=int(PRICE) * 100,
                    currency="usd",
                    source=token,
                    description=PAY_FOR
                )

                UserPayment.objects.create(user=request.user, amount=PRICE, trans_id=charge.id, pay_for=charge.description)
            except stripe.error.CardError as ce:
                return False, ce

            
        
        if jobplacement == '1':
            optiona = True
        try:
            wepeoples.objects.update_or_create(user=request.user, types=None, current_position=None,
                                            person=None, state=None, income=None, relocation=None,
                                            last_verification=None, Paystub=None, graduation_date=None)
            
            state = WorkExperiencePay.objects.create(user=request.user,is_paid=True,includes_job_placement=optiona)
            
        
            # New mail implementation


            # send_mail('Linuxjobber Work-Experience Program',
            #           'Hello, you have succesfully paid for Linuxjobber work experience program,\n\nIf you havent signed the agreement, visit this link to do so: https://leif.org/commit?product_id=5b30461fe59b74063647c483#/.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [request.user.email])
            
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'pay.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content

            message_admin = """
                Hello, 
                {email}
                just succesfully paid for Linuxjobber Work Experience Program.
                

                Warm Regards,
                Linuxjobber

            """.format(
                email =  request.user.email
            )

            mailer_applicant = LinuxjobberMailer(
                subject="Payment Successful",
                to_address=request.user.email,
                header_text="Linuxjobber Work Experience",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            mailer_admin = LinuxjobberMailer(
                subject="Workexperience Payment Alert",
                to_address=ADMIN_EMAIL,
                header_text="Linuxjobber Jobs",
                type=None,
                message=message_admin
            )
            mailer_admin.send_mail()


            return redirect("home:eligibility")
        except stripe.error.CardError as ce:
            return False, ce
    else:
        context = {"stripe_key": stripeset[0].publickey,
                   'price': PRICE,
                   'amount': str(PRICE) + '00',
                   'mode': mode,
                   'PAY_FOR': PAY_FOR,
                   'DISCLMR': DISCLMR}
        return render(request, 'home/pay.html', context)

def accepted(request):
    return render(request, 'home/accepted.html')


@csrf_exempt
def check_subscription_status(request):
    data = """ PASTE COPIED JSON REQUEST HERE """

    if request.method == "POST":
        event_json = json.loads(request.body.decode())
        jsonObject = event_json

        subscription_id = jsonObject['data']['object']
        customer_id = jsonObject['data']['object']
        amount_paid = jsonObject['data']['object']
        types = jsonObject['type']

        customersubscription = UserOrder.objects.all()

        for e in customersubscription:
            sud_id = e.subscription
            name = e.user

        if types == 'customer.subscription.deleted' and customer_id:
            if customersubscription:
                BillingHistory.objects.create(user=CustomUser.objects.get(email=customersubscription.get(user=name)),
                                              amount=29, subscription_id=sud_id, status="inactive/deleted")
                customersubscription.update(status="inactive/deleted")

                user = CustomUser.objects.get(email=customersubscription.get(user=name))
                user.role = 6
                user.save()

        if types == 'invoice.payment_failed' and customer_id:
            if customersubscription:
                BillingHistory.objects.create(user=CustomUser.objects.get(email=customersubscription.get(user=name)),
                                              amount=29, subscription_id=sud_id, status="failed")
                customersubscription.update(status="failed")

                user = CustomUser.objects.get(email=customersubscription.get(user=name))
                user.role = 6
                user.save()

        if types == 'invoice.payment_succeeded' and customer_id:
            if customersubscription:
                BillingHistory.objects.create(user=CustomUser.objects.get(email=customersubscription.get(user=name)),
                                              amount=29, subscription_id=sud_id, status="success")
                customersubscription.update(status="success")

                user = CustomUser.objects.get(email=customersubscription.get(user=name))
                user.role = 3
                user.save()

        # Record time of response from webhook

        try:
            tryf = TryFreeRecord.objects.get(user=CustomUser.objects.get(email=customersubscription.get(user=name)))
            tryf.webhook_response = datetime.now()
            tryf.save(update_fields=['webhook_response'])
        except TryFreeRecord.DoesNotExist:
            pass

        return HttpResponse(status=200)
    return HttpResponse(status=200)


@login_required
def monthly_subscription(request):
    # From Group Class Monthly Payment
    try:
        nexturl = request.session['nexturl']
    except KeyError:
        nexturl = None

    try:
        g_id = request.session['gclass']
    except KeyError:
        g_id = None

    group_item = None

    email = request.user.email
    customersubscription = UserOrder.objects.all()

    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey
    plan_id = stripeset[0].planid

    if 'job_email' in request.session:
        try:
            free = FreeAccountClick.objects.get(email=request.session['job_email'])
            free.visited_tryfree = 1
            free.save(update_fields=["visited_tryfree"])
        except FreeAccountClick.DoesNotExist:
            freeclick = FreeAccountClick(fullname=request.user.get_full_name(), email=request.user.email, filled_jobs=0,
                                         freeaccountclick=1, from_what_page='Not from Jobs', registered=1,
                                         visited_tryfree=1, paid=0)
            freeclick.save()
            request.session['job_email'] = request.user.email

    if request.method == "POST":
        token = request.POST.get("stripeToken")
        plan = stripe.Plan.retrieve(plan_id)
        amount = plan.amount

        try:
            customer = stripe.Customer.create(
                source=token,
                email=request.user.email,
            )

            subscription = stripe.Subscription.create(
                customer=customer.id,
                plan=plan_id,
            )

            UserOrder.objects.create(
                user=request.user,
                order_id=customer.id,
                subscription=subscription.id,
                status="pending",
                order_amount=int(amount) / 100
            )

            TryFreeRecord.objects.create(user=request.user, webhook_response=None)
            # return HttpResponse(status=200)

            messages.success(request,
                             'Thanks for your sucbscription! Please allow 10-20 seconds for your account to be updated as we have to wait for confirmation from the credit card processor.')
            user = CustomUser.objects.get(email=request.user.email)
            user.role = 3
            user.save()

            if 'job_email' in request.session:
                try:
                    free = FreeAccountClick.objects.get(email=request.session['job_email'])
                    free.paid = 1
                    free.save(update_fields=["paid"])
                except FreeAccountClick.DoesNotExist:
                    freeclick = FreeAccountClick(fullname=request.user.get_full_name(), email=request.user.email,
                                                 filled_jobs=0, freeaccountclick=1, from_what_page='Not from Jobs',
                                                 registered=1, visited_tryfree=1, paid=0)
                    freeclick.save()

            if nexturl:
                if nexturl == 'group':
                    group_item = Groupclass.objects.get(id=g_id)
                    group_item.users.add(request.user)
                return redirect("home:" + nexturl)
            else:
                return render(request, 'home/standardPlan_pay_success.html')
        except stripe.error.CardError as ce:
            return False, ce

    return render(request, 'home/monthly_subscription.html', {'email': email, 'publickey': stripeset[0].publickey})


def group(request, pk):
    group_item = get_object_or_404(Groupclass, pk=pk)
    user = None
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user)
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
            the_user = authenticate(email=email, password=password)

            if the_user:
                login(request, the_user)
            else:
                messages.error(request, 'Account found, invalid password entered.')

        except MultiValueDictKeyError:
            print('Error')

        except CustomUser.DoesNotExist:
            firstname = request.POST['fullname'].split()[0]
            lastname = request.POST['fullname'].split()[1] if len(request.POST['fullname'].split()) > 1 else \
            request.POST['fullname'].split()[0]
            password = request.POST['password']
            username = email.split('@')[0]
            if (firstname):
                user = CustomUser.objects.create_user(username, email, password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                #  ('Linuxjobber Free Account Creation', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + '\n Follow this link http://35.167.153.1:8001/login to login to you account\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' +settings.ENV_URL+'unsubscribe', 'settings.EMAIL_HOST_USER', [email])

                groupreg = GroupClassRegister.objects.create(user=user, is_paid=0, amount=group_item.price,
                                                             type_of_class=group_item.type_of_class)
                groupreg.save()

                new_user = authenticate(
                    username=username,
                    password=password,
                )
                login(request, new_user)
                user = new_user

        if user:
            groupreg = GroupClassRegister.objects.create(user=user, is_paid=0, amount=29,
                                                         type_of_class=group_item.type_of_class)
            groupreg.save()
            login(request, user)
            if int(choice) == 1:
                request.session['gclass'] = int(group_item)
                return redirect("home:monthly_subscription")
            return redirect("home:group_pay", pk=group_item.pk)
    user_token = ""
    if user:
        user_token, _ = Token.objects.get_or_create(user=user)
    return render(request, 'home/group_class_item.html',
                  {'group': group_item, 'user': user, 'GROUP_URL': settings.GROUP_CLASS_URL, 'token': user_token})

def fmail(request):
    user = None
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user)

    user_token = None
    if request.user.is_authenticated:
        user_token, _ = Token.objects.get_or_create(user=request.user)

    return TemplateResponse(request, 'home/fasmail.html', {'FMAIL_URL': settings.FASMAIL_URL,
                                                               'token': user_token})

@login_required
def group_pay(request, pk):
    group_item = get_object_or_404(Groupclass, pk=pk)
    amount = group_item.price * 100

    # Implementation for free internship - Azeem Animashaun (Updated 21 January)
    if amount == 0:
        messages.success(request, 'You are registered in ' + group_item.name + ' group class successfully..')
        _, created = GroupClassRegister.objects.update_or_create(
            user=request.user,
            is_paid=1,
            amount=amount,
            type_of_class=group_item.type_of_class,
        )
        user = get_object_or_404(CustomUser, email=request.user.email)
        group_item.users.add(user)
        return redirect("home:group")
    stripeset = StripePayment.objects.all()
    # Stripe uses cent notation for amount 10 USD = 10 * 100
    stripe.api_key = stripeset[0].secretkey
    context = {"stripe_key": stripeset[0].publickey,
               'amount': amount,
               'group': group_item,

               }
    if request.method == "POST":

        stripe.api_key = stripeset[0].secretkey
        token = request.POST.get("stripeToken")
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Group Course Payment',
                source=token,
            )
            messages.success(request, 'You are registered in ' + group_item.name + ' group class successfully.')
            _, created = GroupClassRegister.objects.update_or_create(
                user=request.user,
                is_paid=1,
                amount=29,
                type_of_class=group_item.type_of_class,
            )
            # After payment, add user to the group
            user = get_object_or_404(CustomUser, email=request.user.email)
            group_item.users.add(user)
            return redirect("home:group")
        except stripe.error.CardError as ce:
            return False, ce

    return render(request, 'home/group_pay.html', context)


def contact_us(request):
    error = ''
    success = ''
    if request.method == "POST":
        fname = request.POST['full_name']
        phone = request.POST['phonenumber']
        # email = request.POST['email']
        from_email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        message+= """
        \n
        Mail address : {}       
        """.format(from_email)

        try:
            # send_mail(message, subject, from_email, ['elena.edwards@linuxjobber.com'])
            mailer = LinuxjobberMailer(
                subject=subject,
                to_address=ADMIN_EMAIL,
                header_text="{} via Linuxjobber Support".format(fname),
                type=None,
                message=message
            )
            mailer.send_mail()
            # contact_message = ContactMessages(full_name=fname, phone_no=phone, email=email, message_subject=subj, message=message)
            # contact_message.save()
        except Exception as e:
            error = 'yes'
        else:
            success = 'yes'
        return render(request, 'home/contact_us.html', {'error': error, 'success': success})
    else:
        return render(request, 'home/contact_us.html',
                      {'error': error, 'success': success, 'courses': get_courses(), 'tools': get_tools()})


def location(request):
    return render(request, 'home/location.html', {'courses': get_courses(), 'tools': get_tools()})


@login_required()
def account_settings(request):
    form = AWSCredUpload()
    if request.method == "POST":
        form = AWSCredUpload(request.POST, request.FILES)
        csv_file = request.FILES['document']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload csv files only')
            return render(request, 'home/account_settings.html',
                          {'form': form, 'courses': get_courses(), 'tools': get_tools()})

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
            elif count == 2:
                username = ""
                access_key = column[0]
                secret_key = column[1]
            else:
                messages.error(request,
                               'There was an error while validating credentials, please confirm your credential file is correct. Please contact admin@linuxjobber.com')
                return render(request, 'home/account_settings.html',
                              {'form': form, 'courses': get_courses(), 'tools': get_tools()})

        V_AWS_ACTION = 'verify';
        V_MACHINE_ID = 'verify';
        command = ['python3.6 ' + settings.BASE_DIR + "/home/utils/s3_sample.py %s %s %s %s" % (
        access_key, secret_key, V_AWS_ACTION, V_MACHINE_ID)]

        try:
            output = subprocess.check_output(command, shell=True)
            return_code = 0

            _, created = AwsCredential.objects.update_or_create(
                user=request.user,
                username=username,
                accesskey=access_key,
                secretkey=secret_key,
            )

            if form.is_valid():
                messages.success(request, 'AWS credentials have been uploaded successfully')
                return redirect("home:ec2dashboard")

        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output

            # types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"
            error3 = "OptInRequired"

            output = bytes(output)
            output = output.decode()
            if error1 in output:
                messages.error(request,
                               'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                return render(request, 'home/account_settings.html', {'form': form})
            elif error2 in output:
                messages.error(request,
                               'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                return render(request, 'home/account_settings.html', {'form': form})
            elif error3 in output:
                messages.error(request,
                               'You are not subscribed to the AWS service, Please go to http://aws.amazon.com to subscribe.')
                return render(request, 'home/account_settings.html', {'form': form})
            else:
                messages.error(request, 'Unhandled exception has occurred. Please contact admin@linuxjobber.com')
                return render(request, 'home/account_settings.html', {'form': form})
    else:
        try:
            check = AwsCredential.objects.get(user=request.user)
        except AwsCredential.DoesNotExist:
            check = None
        if check:
            return redirect("home:ec2dashboard")

        return render(request, 'home/account_settings.html', {'form': form})


def ec2dashboard(request, command=None):
    form = AWSCredUpload()
    awscred = AwsCredential.objects.get(user=request.user)

    # Launch an instance
    if command and command == "launch":
        print("enter")
        AWS_ACTION = 'launch_instance';
        MACHINE_ID = "new";
        command = ['python3.6 ' + settings.BASE_DIR + "/home/utils/s3_sample.py %s %s %s %s" % (
        awscred.accesskey, awscred.secretkey, AWS_ACTION, MACHINE_ID)]

        try:
            print("worked")
            output = subprocess.check_output(command, shell=True)
            return_code = 0
            messages.success(request,
                             'Machine is starting up, wait and click refresh in 2 minutes. Username is : sysadmin , Password is : 8iu7*IU& . We advice you to use this console for all your EC2 instances. If you have started other instances, please turn them all off now')
            return redirect("home:ec2dashboard")
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output
            output = bytes(output)
            output = output.decode()

            # types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"
            error3 = "InstanceLimitExceeded"

            if error1 in output:
                messages.error(request,
                               'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")
            elif error2 in output:
                messages.error(request,
                               'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")
            elif error3 in output:
                messages.error(request, 'Sorry, you can only launch one machine at a time')
                return redirect("home:ec2dashboard")
            else:
                messages.error(request, 'Unhandled exception has occurred. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")

    # Running instance
    running_machine = []
    RUNING_AWS_ACTION = 'instance_running';
    RUNING_MACHINE_ID = 'running';
    command = ['python3.6 ' + settings.BASE_DIR + "/home/utils/s3_sample.py %s %s %s %s" % (
    awscred.accesskey, awscred.secretkey, RUNING_AWS_ACTION, RUNING_MACHINE_ID)]

    try:
        outputs = subprocess.check_output(command, shell=True)
        return_code = 0
        outputs = bytes(outputs)
        output = outputs.decode()

        output = output.split(",")

        for i in range(0, len(output) - 1):
            out = output[i].split()
            running_machine.append(out)

    except subprocess.CalledProcessError as grepexc:
        print("error code", grepexc.returncode, grepexc.output)
        return_code = grepexc.returncode
        output = grepexc.output

    # stopped Instance
    stopped_machine = []
    STOP_AWS_ACTION = 'instance_stopped';
    STOP_MACHINE_ID = 'stopped';

    command = ['python3.6 ' + settings.BASE_DIR + "/home/utils/s3_sample.py %s %s %s %s" % (
    awscred.accesskey, awscred.secretkey, STOP_AWS_ACTION, STOP_MACHINE_ID)]

    try:
        stopped_outputs = subprocess.check_output(command, shell=True)
        return_code = 0
        stopped_outputs = bytes(stopped_outputs)
        output = stopped_outputs.decode()

        output = output.split(",")

        for i in range(0, len(output) - 1):
            out = output[i].split()
            stopped_machine.append(out)

    except subprocess.CalledProcessError as grepexc:
        print("error code", grepexc.returncode, grepexc.output)
        return_code = grepexc.returncode
        output = grepexc.output

    context = {
        'form': form,
        'running_machine': running_machine,
        'stopped_machine': stopped_machine,
    }

    if request.method == "POST":
        form = AWSCredUpload(request.POST, request.FILES)
        csv_file = request.FILES['document']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload csv files only')
            return redirect("home:ec2dashboard")

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
            elif count == 2:
                username = ""
                access_key = column[0]
                secret_key = column[1]
            else:
                messages.error(request,
                               'There was an error while validating credentials, please confirm your credential file is correct. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")

        V_AWS_ACTION = 'verify';
        V_MACHINE_ID = 'verify';
        command = ['python3.6 ' + settings.BASE_DIR + "/home/utils/s3_sample.py %s %s %s %s" % (
        access_key, secret_key, V_AWS_ACTION, V_MACHINE_ID)]

        try:
            output = subprocess.check_output(command, shell=True)
            return_code = 0
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output

            output = bytes(output)
            output = output.decode()

            # types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"
            error3 = "OptInRequired"

            if error1 in output:
                messages.error(request,
                               'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")
            elif error2 in output:
                messages.error(request,
                               'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")
            elif error3 in output:
                messages.error(request,
                               'You are not subscribed to the AWS service, Please go to http://aws.amazon.com to subscribe.')
                return redirect("home:ec2dashboard")

            # return render(request,'courses/result.html',{'gradingerror':"There was an error encountered during grading",'coursetopic':topic})
        awscred.accesskey = access_key
        awscred.secretkey = secret_key
        awscred.username = username
        awscred.save(update_fields=['username', 'accesskey', 'secretkey'])

        if form.is_valid():
            messages.success(request, 'AWS credentials have been uploaded successfully')
            return redirect("home:ec2dashboard")

    return render(request, 'home/ec2dashboard.html', context)


def startmachine(request, machine_id):
    awscred = AwsCredential.objects.get(user=request.user)

    if machine_id:
        AWS_ACTION = 'start_instance';
        MACHINE_ID = machine_id;
        command = ['python3.6 ' + settings.BASE_DIR + "/home/utils/s3_sample.py %s %s %s %s" % (
        awscred.accesskey, awscred.secretkey, AWS_ACTION, MACHINE_ID)]

        try:
            output = subprocess.check_output(command, shell=True)
            return_code = 0
            messages.success(request,
                             'Machine is starting up, wait and click refresh in 2 minutes. Username is : sysadmin , Password is : 8iu7*IU& . We advice you to use this console for all your EC2 instances. If you have started other instances, please turn them all off now')
            return redirect("home:ec2dashboard")
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output
            output = bytes(output)
            output = output.decode()

            # types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"

            if error1 in output:
                messages.error(request,
                               'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")
            elif error2 in output:
                messages.error(request,
                               'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")
            else:
                messages.error(request, 'Unhandled exception has occurred. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")


def stopmachine(request, machine_id):
    awscred = AwsCredential.objects.get(user=request.user)
    if machine_id:
        AWS_ACTION = 'stop_instance';
        MACHINE_ID = machine_id;
        command = ['python3.6 ' + settings.BASE_DIR + "/home/utils/s3_sample.py %s %s %s %s" % (
        awscred.accesskey, awscred.secretkey, AWS_ACTION, MACHINE_ID)]

        try:
            output = subprocess.check_output(command, shell=True)
            return_code = 0
            messages.success(request,
                             'Machine is shutting down, wait and click refresh in 2 minutes. Username is : sysadmin , Password is : 8iu7*IU& . We advice you to use this console for all your EC2 instances. If you have started other instances, please turn them all off now')
            return redirect("home:ec2dashboard")
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            return_code = grepexc.returncode
            output = grepexc.output
            output = bytes(output)
            output = output.decode()

            # types of errors expected from AWS
            error1 = "UnauthorizedOperation"
            error2 = "AuthFailure"

            if error1 in output:
                messages.error(request,
                               'You are not authorized to perform this operation. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")
            elif error2 in output:
                messages.error(request,
                               'There was an error while validating credentials. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")
            else:
                messages.error(request, 'Unhandled exception has occurred. Please contact admin@linuxjobber.com')
                return redirect("home:ec2dashboard")


def order_list(request):
    return render(request, 'home/orderlist.html',
                  {'order': UserOrder.objects.filter(user=request.user), 'courses': get_courses(),
                   'tools': get_tools()})


def students_packages(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email=email)
            subscriber.save()
            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'newsletter.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()

            message_applicant = file_content
            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter Subscription",
                to_address=email,
                header_text="Linuxjobber Newsletter",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            return render(request, 'home/students_packages.html',
                          {'news_letter_message': 'You have successfully subscribed to our news letter!',
                           'courses': get_courses(), 'tools': get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render(request, 'home/students_packages.html',
                          {'news_letter_message': 'Something went wrong please try again!', 'courses': get_courses(),
                           'tools': get_tools()})
    else:
        return render(request, 'home/students_packages.html',
                      {'news_letter_message': news_letter_message, 'courses': get_courses(), 'tools': get_tools()})


def server_service(request):
    news_letter_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsLetterSubscribers(email=email)
            subscriber.save()
            # send_mail('Linuxjobber Newsletter',
            #           'Hello, you are receiving this email because you have subscribed to our newsletter on linuxjobber.com.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
            #           settings.EMAIL_HOST_USER, [email])
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'newsletter.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            message_applicant = file_content
            mailer_applicant = LinuxjobberMailer(
                subject="Newsletter Subscription",
                to_address=email,
                header_text="Linuxjobber Newsletter",
                type=None,
                message=message_applicant
            )
            mailer_applicant.send_mail()

            return render(request, 'home/server_service.html',
                          {'news_letter_message': 'You have successfully subscribed to our news letter!',
                           'courses': get_courses(), 'tools': get_tools()})
        except Exception as e:
            standard_logger.error('error')
            return render(request, 'home/server_service.html',
                          {'news_letter_message': 'Something went wrong please try again!', 'courses': get_courses(),
                           'tools': get_tools()})
    else:
        return render(request, 'home/server_service.html',
                      {'news_letter_message': news_letter_message, 'courses': get_courses(), 'tools': get_tools()})


def live_help(request):
    return render(request, 'home/live_help.html', {'courses': get_courses(), 'tools': get_tools()})


@login_required
def pay_live_help(request):
    PRICE = 399
    mode = "One Time"
    PAY_FOR = "Live Help"
    DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${}".format(
        PRICE, PRICE)
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey
    if request.method == "POST":
        token = request.POST.get("stripeToken")
        try:
            charge = stripe.Charge.create(
                amount=PRICE * 100,
                currency="usd",
                source=token,
                description=PAY_FOR
            )
        except stripe.error.CardError as ce:
            return False, ce
        else:
            try:
                UserPayment.objects.create(user=request.user, amount=PRICE,
                                           trans_id=charge.id, pay_for=charge.description,
                                           )

                # send_mail('Linuxjobber Live Help Subscription',
                #           'Hello, you have successfuly subscribed for Live Help on Linuxjobber.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
                #           settings.EMAIL_HOST_USER, [request.user.email])
                file_path = os.path.join(settings.BASE_DIR, 'emails', 'livehelp.txt')
                with open(file_path, 'r') as f:
                    file_content = f.read()
                message_applicant = file_content
                mailer_applicant = LinuxjobberMailer(
                    subject="Live Help Subscription",
                    to_address=request.user.email
                ,header_text="Linuxjobber",
                    type=None,
                    message=message_applicant
                )
                mailer_applicant.send_mail()
                return render(request, 'home/live_help_pay_success.html')
            except SMTPException as error:
                print(error)
                return render(request, 'home/live_help_pay_success.html')
            except Exception as error:
                print(error)
                return redirect("home:index")
    else:
        context = {"stripe_key": stripeset[0].publickey,
                   'price': PRICE,
                   'amount': str(PRICE) + '00',
                   'mode': mode,
                   'PAY_FOR': PAY_FOR,
                   'DISCLMR': DISCLMR}
        return render(request, 'home/live_help_pay.html', context)


def in_person_training(request):
    return render(request, 'home/in_person_training.html', {'courses': get_courses(), 'tools': get_tools()})

@login_required
def full_train_pay(request, class_id):
    try:
        comclass = CompleteClass.objects.get(id=class_id)
    except CompleteClass.DoesNotExist:
        raise Http404
    PAY_FOR = comclass.name
    PRICE = comclass.fee
    mode = "One Time Payment"
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey
    DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time within 14 days for a full refund. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${}/Monthly".format(
        PRICE, PRICE)


    if request.method == "POST":
        token = request.POST.get("stripeToken")
        amt = PRICE.replace(',','')
        amt = amt.split('.')[0]
        
        
        try:
            charge = stripe.Charge.create(
                amount=int(amt) * 100,
                currency="usd",
                source=token,
                description=comclass.name
            )


        except stripe.error.CardError as ce:
            return False, ce
        else:
            try:
                UserPayment.objects.create(user=request.user, amount=amt,
                                            trans_id=charge.id, pay_for=charge.description,
                                            )
                user = request.user
                user.role = 3
                user.save()
                # send_mail('Linuxjobber '+ comclass.name +' Subscription',
                #             'Hello, you have successfuly subscribed for our ' +comclass.name+' Plan package.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
                #             settings.EMAIL_HOST_USER, [request.user.email])
                message_applicant = """
                    Hello, you have successfuly subscribed for our {comclass.name} Plan package.
                    
                    Thanks & Regards 
                    Linuxjobber
                    

                    To Unsubscribe go here 
                    {settings.ENV_URL}unsubscribe,
                """
                mailer_applicant = LinuxjobberMailer(
                    subject="Linuxjobber "+ comclass.name +" Subscription",
                    to_address=request.user.email,
                    header_text="Linuxjobber "+comclass.name,
                    type=None,
                    message=message_applicant
                )
                mailer_applicant.send_mail()
                return render(request, 'home/complete_pay_success.html', {'class': comclass.name})
            except Exception as error:
                print("An error occured")
                print(error)
                messages.error(request, 'An error occurred while trying to pay please try again')
                return redirect("home:index")
    else:
        amt = PRICE.replace(',','')
        amt = amt.split('.')[0]
        context = {"stripe_key": stripeset[0].publickey,
            'price': PRICE,
            'amount': str(amt) + '00',
            'mode': mode,
            'PAY_FOR': PAY_FOR,
            'DISCLMR': DISCLMR,
        }
        return render(request, 'home/complete_pay.html', context)

@login_required
def tryfree(request, sub_plan='standardPlan'):
    if sub_plan == 'standardPlan':
        PRICE = 29
        mode = "Monthly Subscription"
        PAY_FOR = "14 days free trial"
        DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time within 14 days for a full refund. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${}/Monthly".format(
            PRICE, PRICE)
        stripeset = StripePayment.objects.all()
        stripe.api_key = stripeset[0].secretkey

        if request.method == "POST":
            token = request.POST.get("stripeToken")
            try:
                charge = stripe.Charge.create(
                    amount=PRICE * 100,
                    currency="usd",
                    source=token,
                    description=sub_plan.lower()
                )
            except stripe.error.CardError as ce:
                return False, ce
            else:
                try:
                    UserPayment.objects.create(user=request.user, amount=PRICE,
                                               trans_id=charge.id, pay_for=charge.description,
                                               )

                    user = request.user
                    user.role = 3
                    user.save()
                    # send_mail('Linuxjobber Standard Plan Subscription',
                    #           'Hello, you have successfuly subscribed for our Standard Plan package.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
                    #           settings.EMAIL_HOST_USER, [request.user.email])
                    file_path = os.path.join(settings.BASE_DIR, 'emails', 'tryfree.txt')
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    
                    message_applicant = file_content
                    mailer_applicant = LinuxjobberMailer(
                        subject="Standard Plan Subscription",
                        to_address=request.user.email,
                        header_text="Linuxjobber",
                        type=None,
                        message=message_applicant
                    )
                    mailer_applicant.send_mail()

                    return render(request, 'home/standardPlan_pay_success.html')
                except SMTPException as error:
                    print(error)
                    return render(request, 'home/standardPlan_pay_success.html')
                except Exception as error:
                    print(error)
                    return redirect("home:index")
        else:
            context = {"stripe_key": stripeset[0].publickey,
                       'price': PRICE,
                       'amount': str(PRICE) + '00',
                       'mode': mode,
                       'PAY_FOR': PAY_FOR,
                       'DISCLMR': DISCLMR,
                       'courses': get_courses(),
                       'tools': get_tools()}
            return render(request, 'home/standard_plan_pay.html', context)
        # return HttpResponse(status=200)

    if sub_plan == 'awsPlan':
        PRICE = 1225
        mode = "One Time Payment"
        PAY_FOR = "AWS Full Training"
        DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time within 14 days for a full refund. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${} One Time".format(
            PRICE, PRICE)
        stripeset = StripePayment.objects.all()
        stripe.api_key = stripeset[0].secretkey
        if request.method == "POST":
            token = request.POST.get("stripeToken")
            try:
                charge = stripe.Charge.create(
                    amount=PRICE * 100,
                    currency="usd",
                    source=token,
                    description=sub_plan.lower()
                )


            except stripe.error.CardError as ce:
                return False, ce
            else:
                try:
                    UserPayment.objects.create(user=request.user, amount=PRICE,
                                               trans_id=charge.id, pay_for=charge.description,
                                               )
                    user = request.user
                    user.role = 3
                    user.save()
                    # send_mail('Linuxjobber AWS Full Training Subscription',
                    #           'Hello, you have successfuly subscribed for our AWS Full Training Plan package.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
                    #           settings.EMAIL_HOST_USER, [request.user.email])
                    file_path = os.path.join(settings.BASE_DIR, 'emails', 'awsplan.txt')
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    message_applicant = file_content
                    mailer_applicant = LinuxjobberMailer(
                        subject="AWS Full Training Subscription",
                        to_address=request.user.email,
                        header_text="Linuxjobber",
                        type=None,
                        message=message_applicant
                    )
                    mailer_applicant.send_mail()
                    return render(request, 'home/awsFull_pay_success.html')
                except SMTPException as error:
                    print(error)
                    return render(request, 'home/awsFull_pay_success.html')
                except Exception as error:
                    print(error)
                    return redirect("home:index")
        else:
            context = {"stripe_key": stripeset[0].publickey,
                       'price': PRICE,
                       'amount': str(PRICE) + '00',
                       'mode': mode,
                       'PAY_FOR': PAY_FOR,
                       'DISCLMR': DISCLMR,
                       'courses': get_courses(),
                       'tools': get_tools()}
            return render(request, 'home/awsFull_plan_pay.html', context)
        # return HttpResponse(status=200)



    else:
        PRICE = 2495
        mode = "One Time Payment"
        PAY_FOR = "PREMIUM PLAN"
        DISCLMR = "Please note that you will be charged ${} upfront. However, you may cancel at any time within 14 days for a full refund. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ONE TIME ${}".format(
            PRICE, PRICE)
        stripeset = StripePayment.objects.all()
        stripe.api_key = stripeset[0].secretkey
        if request.method == "POST":
            token = request.POST.get("stripeToken")
            try:
                charge = stripe.Charge.create(
                    amount=PRICE * 100,
                    currency="usd",
                    source=token,
                    description=sub_plan.lower()
                )
            except stripe.error.CardError as ce:
                return False, ce
            else:
                try:
                    UserPayment.objects.create(user=request.user, amount=PRICE,
                                               trans_id=charge.id, pay_for=charge.description,
                                               )
                    user = request.user
                    user.role = 4
                    user.save()
                    # send_mail('Linuxjobber Premium Plan Subscription',
                    #           'Hello, you have successfuly subscribed for our Premium Plan package.\n\n Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL + 'unsubscribe',
                    #           settings.EMAIL_HOST_USER, [request.user.email])
                    file_path = os.path.join(settings.BASE_DIR, 'emails', 'preniumplan.txt')
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    message_applicant = file_content
                    mailer_applicant = LinuxjobberMailer(
                        subject="Premiun Plan Subscription",
                        to_address=request.user.email,
                        header_text="Linuxjobber",
                        type=None,
                        message=message_applicant
                    )
                    mailer_applicant.send_mail()
                    return render(request, 'home/premiumPlan_pay_success.html')
                except SMTPException as error:
                    print(error)
                    return render(request, 'home/premiumPlan_pay_success.html')
                except Exception as error:
                    print(error)
                    return redirect("home:index")
        else:
            context = {"stripe_key": stripeset[0].publickey,
                       'price': PRICE,
                       'amount': str(PRICE) + '00',
                       'mode': mode,
                       'PAY_FOR': PAY_FOR,
                       'DISCLMR': DISCLMR,
                       'courses': get_courses(),
                       'tools': get_tools()}
            return render(request, 'home/premium_plan_pay.html', context)
    

@login_required
def rhcsa_order(request):
    orders = RHCSAOrder.objects.filter(user=request.user)
    orders_not_empty = RHCSAOrder.objects.filter(user=request.user).exists()

    return render(request, 'home/rhcsa_order.html',
                  {'orders_not_empty': orders_not_empty, 'orders': orders, 'courses': get_courses(),
                   'tools': get_tools()})


def user_interest(request):
    return render(request, 'home/user_interest.html', {'courses': get_courses(), 'tools': get_tools()})


def upload_profile_pic(request):
    update_feedback = ''
    if request.method == 'POST' and request.FILES['profile_picture']:
        if request.FILES['profile_picture'].name.endswith('.png') or request.FILES['profile_picture'].name.endswith(
                '.jpg'):
            picture = request.FILES['profile_picture']
            filename = FileSystemStorage().save(picture.name, picture)
            picture_url = FileSystemStorage().url(filename)
            current_user = request.user
            current_user.profile_img = picture_url
            current_user.save()
            update_feedback = 'Your profile update was successful'
            return render(request, 'home/upload_profile_pic.html', {'update_feedback': update_feedback})
        else:
            update_feedback = 'This file format is not supported'
            return render(request, 'home/upload_profile_pic.html', {'update_feedback': update_feedback})
    else:
        return render(request, 'home/upload_profile_pic.html')


def noobaid(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        location = request.POST['location']
        availability = request.POST['availability']
        requesta = request.POST['request']

        file_path = os.path.join(settings.BASE_DIR, 'emails', 'noobaid.txt')
        with open(file_path, 'r') as f:
            file_content = f.read()
        mail_message = file_content.format(
                    name=name,
                    email=email,
                    location=location,
                    availability=availability,
                    requesta=requesta
                )
        mailer = LinuxjobberMailer(
            subject="Noobaid Demo Request",
            to_address=ADMIN_EMAIL,
            header_text="Linuxjobber",
            type=None,
            message=mail_message
        )
        mailer.send_mail()

        messages.success(request,'Your request has been made successfully, you will get a response from us shortly')

    return render(request, 'home/noobaid.html')


def group_list(request):
    user = None
    ans = None
    request.session['nexturl'] = "group"

    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user)

    if request.method == "POST":
        email = request.POST['email']
        choice = request.POST['choice']
        gclass = request.POST['grouptype']
        try:
            group_item = Groupclass.objects.get(id=int(gclass))
        except:
            redirect('home:group')

        # type_of_class = request.POST['name']
        # amount = request.POST['price']

        # request.session['email'] = email
        # request.session['amount'] = amount
        # request.session['class'] = type_of_class
        try:
            password = request.POST['password']
            user = CustomUser.objects.get(email=email)
            username = email.split('@')[0]
            the_user = authenticate(username=username, password=password)

            if the_user:
                login(request, the_user)
            else:
                messages.error(request, 'Account found, invalid login details entered.')
                return redirect('home:group')

        except MultiValueDictKeyError:
            print('Error')

        except CustomUser.DoesNotExist:
            firstname = request.POST['fullname'].split()[0]
            lastname = request.POST['fullname'].split()[1] if len(request.POST['fullname'].split()) > 1 else \
            request.POST['fullname'].split()[0]
            password = request.POST['password']
            username = email.split('@')[0]
            if (firstname):
                user = CustomUser.objects.create_user(username, email, password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()

                file_path = os.path.join(settings.BASE_DIR, 'emails', 'group_list.txt')
                with open(file_path, 'r') as f:
                    file_content = f.read()
                mail_message = file_content.format(
                    username=username,
                    email=email,
                    firstname=firstname,
                    lastname=lastname,
                    env_url=settings.ENV_URL
                )
                mailer = LinuxjobberMailer(
                    subject="Account has been created",
                    to_address=email,
                    header_text="Linuxjobber",
                    type=None,
                    message=mail_message
                )
                mailer.send_mail()

                # send_mail('Account has been Created', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + ' and your email is ' +email + '\n Follow this url to login with your username and password '+settings.ENV_URL+'login \n\n Thanks & Regards \n Admin.\n\n\n\n\n\n\n\n To Unsubscribe go here \n' +settings.ENV_URL+'unsubscribe', settings.EMAIL_HOST_USER, [email])

                groupreg = GroupClassRegister.objects.create(user=user, is_paid=0, amount=29,
                                                             type_of_class=group_item.type_of_class)
                groupreg.save()

                new_user = authenticate(username=username,
                                        password=password,
                                        )
                login(request, new_user)

                if int(choice) == 1:
                    request.session['gclass'] = int(group_item.id)
                    return redirect("home:monthly_subscription")
                return redirect("home:group_pay", pk=group_item.id)

        if user:
            login(request, user)
            try:
                ans = Groupclass.objects.get(users=user, id=group_item.id)
            except Groupclass.DoesNotExist:
                pass
            if ans:
                messages.success(request,
                                 'You are already registered in ' + group_item.name + ' group class successfully..')
                return redirect('home:group')
            if user.role == 3:
                group_item.users.add(user)
                messages.success(request, 'You registered in ' + group_item.name + ' group class successfully..')
                return redirect("home:group")
            groupreg = GroupClassRegister.objects.create(user=user, is_paid=0,
                                                         amount=29, type_of_class=group_item.type_of_class)
            groupreg.save()
            if int(choice) == 1:
                request.session['gclass'] = int(group_item.id)
                return redirect("home:monthly_subscription")
            return redirect("home:group_pay", pk=group_item.id)

    user_token = None
    if request.user.is_authenticated:
        user_token, _ = Token.objects.get_or_create(user=request.user)

    return TemplateResponse(request, 'home/group_class.html', {'groups': Groupclass.objects.all(),
                                                               'GROUP_URL': settings.GROUP_CLASS_URL,
                                                               'token': user_token})


def handler_404(request):
    return TemplateResponse(request, 'home/404.html', status=404)


def handler_401(request):
    return TemplateResponse(request, 'home/404.html', status=401)


def handler_500(request):
    return render(request, 'home/404.html', status=404)


def timeout_handler(request):
    if request.method == "POST":
        user = CustomUser.objects.get(username=request.user.username)
        success = user.check_password(request.POST.get('password', None))
        if success:
            request.session['has_timeout'] = False
            return redirect(request.session['from_timeout_next'])
        return TemplateResponse(request, 'home/timeout.html', {"error_message": " Invalid password, try again"})
    else:
        return TemplateResponse(request, 'home/timeout.html')


def to_monthly(request):
    return redirect("home:monthly_subscription")


@login_required()
def combined_class_pay(request):
    try:
        workexp = wepeoples.objects.get(user=request.user)
        return redirect("home:workexprofile")
    except wepeoples.DoesNotExist:
        pass
    course = request.GET.get('course_picked', 1)
    request.session['combined_class'] = course
    PRICE = 798
    mode = "One Time Payment"
    PAY_FOR = "Combined Class"
    DISCLMR = "Please note that you will be charged ${price} upfront." \
              " However, you may cancel at any time within 14 days for a full refund. " \
              "By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${price} One Time".format(
        price=PRICE)
    stripeset = StripePayment.objects.all()
    stripe.api_key = stripeset[0].secretkey

    try:
        workexp = wepeoples.objects.get(user=request.user)
        return redirect("home:workexprofile")
    except wepeoples.DoesNotExist:
        pass

    context = {"stripe_key": stripeset[0].publickey,
               'price': PRICE,
               'amount': str(PRICE) + '00',
               'mode': mode,
               'PAY_FOR': PAY_FOR,
               'DISCLMR': DISCLMR
               }

    if request.method == "POST":
        token = request.POST.get("stripeToken")
        try:
            charge = stripe.Charge.create(
                amount=PRICE * 100,
                currency="usd",
                source=token,
                description=PAY_FOR.lower()
            )

        except stripe.error.CardError as ce:
            return False, ce
        else:
            try:
                UserPayment.objects.create(user=request.user, amount=PRICE,
                                           trans_id=charge.id, pay_for=charge.description,
                                           )
                user = request.user
                user.role = 4
                user.save()
                wepeoples.objects.update_or_create(user=request.user, types=None, current_position=None,
                                                   person=None, state=None, income=None, relocation=None,
                                                   last_verification=None, Paystub=None, graduation_date=None)
                # send_mail('Linuxjobber Combined Class Payment',
                #           'Hello, you have successfuly beem enrolled in our Combined Class '
                #           'which gives you access to full technical training with Work Experience package included \n\n'
                #           'Thanks & Regards \n Linuxjobber\n\n\n\n\n\n\n\n To Unsubscribe go here \n' + settings.ENV_URL
                #           + 'unsubscribe',
                #           settings.EMAIL_HOST_USER, [request.user.email])

                file_path = os.path.join(settings.BASE_DIR, 'emails', 'combined_class_pay.txt')
                with open(file_path, 'r') as f:
                    file_content = f.read()
                message_applicant = file_content
                mailer_applicant = LinuxjobberMailer(
                    subject="Combined Class Payment Successful",
                    to_address=request.user.email,
                    header_text="Linuxjobber",
                    type=None,
                    message=message_applicant
                )
                mailer_applicant.send_mail()


                return render(request, 'home/combined_class_pay_success.html')
            except SMTPException as error:
                print(error)
                return render(request, 'home/combined_class_pay_success.html')
            except Exception as error:
                print(error)
                return redirect("home:combined_class")
    else:

        return TemplateResponse(request, 'home/combined_class_pay.html', context)


def combined_class(request):
    if request.user.is_authenticated:
        try:
            workexp = wepeoples.objects.get(user=request.user)
            return redirect("home:workexprofile")
        except wepeoples.DoesNotExist:
            pass
    return TemplateResponse(request, 'home/combined_class.html')


@login_required()
def combined_class_terms(request):
    return TemplateResponse(request, 'home/combined_class_terms.html')


@csrf_exempt
def career_switch(request, position_id=None):
    from .forms import CareerSwitchApplicationForm
    response_data = {}
    if request.POST.get('get_position_detail', None):
        # This method handles AJAX request for job details
        item = FullTimePostion.objects.get(id=request.POST.get('get_position_detail'))
        response_data['requirement'] = item.requirement
        response_data['responsibility'] = r"{}".format(item.responsibility.replace('\n', '<br>'))
        response_data['job_title'] = item.job_title
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

    form = CareerSwitchApplicationForm()
    if request.method == "POST":
        form = CareerSwitchApplicationForm(request.POST, request.FILES)
        cv = None
        if form.is_valid():
            jobform = form.save(commit=False)
            try:
                CareerSwitchApplication.objects.get(
                    email=request.POST['email'],
                    new_career=jobform.new_career
                )
                messages.success(request,
                                 "Sorry We could not submit your application as you have applied for this role before.")
                return redirect("home:career_switch")
            except CareerSwitchApplication.DoesNotExist:
                pass
            jobform.save()
            request.session['job_email'] = request.POST['email']
            request.session['job_fullname'] = request.POST['fullname']
            request.session['page'] = 'Switch Career'

            try:
                freeexist = FreeAccountClick.objects.get(email=request.session['job_email'])
            except FreeAccountClick.DoesNotExist:
                freeclick = FreeAccountClick(fullname=request.session['job_fullname'],
                                             email=request.session['job_email'],
                                             filled_jobs=1,
                                             freeaccountclick=0,
                                             from_what_page=request.session['page'],
                                             registered=0,
                                             visited_tryfree=0,
                                             paid=0)
                freeclick.save()
            except Exception:
                pass

            if not request.POST['cv_link']:
                cv = jobform.resume.url
            else:
                cv = request.POST['cv_link']
            
            file_path = os.path.join(settings.BASE_DIR, 'emails', 'career_switch.txt')
            with open(file_path, 'r') as f:
                file_content = f.read()
            applicant_template = file_content.format(
                fullname=jobform.fullname,
                new_career=jobform.new_career,
                unsubscribe_url=settings.ENV_URL + '/unsubscribe'
            )

            # send_mail('Your Career Switch application has been received - Linuxjobber',
            #           applicant_template, settings.EMAIL_HOST_USER,
            #           [request.POST['email']])

            mailer_applicant = LinuxjobberMailer(
                subject="Career Switch Application Received",
                to_address=request.POST['email'],
                header_text="Linuxjobber",
                type=None,
                message=applicant_template
            )
            mailer_applicant.send_mail()

            file_path = os.path.join(settings.BASE_DIR, 'emails', 'career_switch_admin.txt')
            with open(file_path, 'r') as f:
                file_content2 = f.read()

            admin_email_template = file_content2.format(
                fullname=jobform.fullname,
                new_career=jobform.new_career,
                old_career=jobform.old_career,
                phone=jobform.phone,
                cv_url=cv,
                email=jobform.email
            )
            # send_mail('Career Switch Application Received ', admin_email_template
            #           , settings.EMAIL_HOST_USER, ['joseph.showunmi@linuxjobber.com', ])


            mailer_admin = LinuxjobberMailer(
                subject="New Career Switch Application Received",
                to_address=ADMIN_EMAIL,
                header_text="Linuxjobber",
                type=None,
                message=admin_email_template
            )
            mailer_admin.send_mail()
            return redirect("home:jobfeed")
        else:
            return render(request, 'home/career_switch.html', {'form': form})
    return render(request, 'home/career_switch.html', {'form': form})


def job_submitted(request, type="fulltime"):
    return TemplateResponse(request, 'home/job_application_submitted.html')

@login_required
def installments(request):
    installments = InstallmentPlan.objects.filter(user=request.user)
    context = {
        'installments':installments
    }
    return TemplateResponse(request,'home/installments_new.html',context)

@login_required
def installment_pay(request):
    context = {}
    payment_id = None
    context['installments'] = InstallmentPlan.objects.filter(user=request.user)
    if request.POST.get('sub_payment_id',None) or request.POST.get("stripeToken",None)\
            or request.POST.get('installment_id',None):
        if request.POST.get('installment_id',None):
            installment_id = request.POST.get('installment_id',None)
            try:
                installment = InstallmentPlan.objects.get(pk=installment_id)
                unpaid = installment.subpayment_set.filter(is_paid=False)
                unpaid.update(is_disabled=True)
                item = SubPayment.objects.create(
                    installment=installment,
                    amount=installment.get_balance(),
                    due_in=0,
                    description='Total Balance Payment'
                )
                payment_id = item.pk
            except InstallmentPlan.DoesNotExist:
                messages.error(request, 'An error occured, please try again')
                return redirect('home:installments')

        else:
            payment_id = request.POST.get('sub_payment_id',None)
        context['sub_payment_id'] = payment_id
        try:
            sub_payment = SubPayment.objects.get(pk=payment_id)
        except SubPayment.DoesNotExist:
            messages.error(request, 'An error occured, please try again')
            return redirect('home:installments')

        if sub_payment.is_paid:
            messages.success('Double payment attempt detected, payment made previously')
            return redirect('home:installments')
        PRICE = int(sub_payment.amount)
        mode = "One Time Payment"
        PAY_FOR = "Installment payment for {}".format(sub_payment.installment.description.lower())
        DISCLMR = "Please note that you will be charged ${}. However, you may cancel at any time within 14 days for a full refund. By clicking Pay with Card you are agreeing to allow Linuxjobber to bill you ${} One Time".format(
            PRICE, PRICE)
        stripeset = StripePayment.objects.all()
        stripe.api_key = stripeset[0].secretkey

        if request.POST.get("stripeToken",None):
            stripe.api_key = stripeset[0].secretkey
            token = request.POST.get("stripeToken")
            try:
                charge = stripe.Charge.create(
                    amount= PRICE * 100,
                    # Stripe uses cent notation for amount: 10 USD = 10 * 100
                    currency='usd',
                    description='Installment for {installment}'.format(installment= sub_payment.installment.description),
                    source=token,
                )
            except stripe.error.CardError as ce:
                return False, ce
            else:
                sub_payment.approve_payment()
                try:
                    UserPayment.objects.create(user=request.user, amount=PRICE,
                                               trans_id=charge.id, pay_for=charge.description)
                    
                    file_path = os.path.join(settings.BASE_DIR, 'emails', 'installment_pay.txt')
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    
                    message_applicant = file_content.format(
                        balance=sub_payment.installment.get_balance(),
                        count=sub_payment.installment.subpayment_set.count(),
                        amount= sub_payment.amount
                    )
                    mailer_applicant = LinuxjobberMailer(
                        subject="Installment Payment",
                        to_address=request.user.email,
                        header_text="Linuxjobber",
                        type=None,
                        message=message_applicant
                    )
                    mailer_applicant.send_mail()
                    messages.success(request,'Installment Payment Successful!')
                    return render(request, 'home/installment_pay.html')
                except Exception as error:
                    messages.success(request,'Installment Payment Successful!')
                    return render(request, 'home/installment_pay.html')
                finally:

                    return redirect("home:installments")
        else:
            context.update({"stripe_key": stripeset[0].publickey,
                       'price': PRICE,
                       'amount': str( PRICE * 100 ),
                       'mode': mode,
                       'PAY_FOR': PAY_FOR,
                       'DISCLMR': DISCLMR,
                       'courses': get_courses(),
                       'tools': get_tools()})
            return render(request, 'home/installment_pay.html', context)
    else:
        messages.error(request,'Unable to validate installment, please select a valid installment plan')
        return redirect('home:installments')
@csrf_exempt
def mail_status(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id', None)
        try:
            group = EmailGroupMessageLog.objects.get(pk=group_id)
            stats = group.get_mail_statistics()
            # if stats['has_completed'] and group.get_failed_messages():
            #     handle_failed_campaign(group.id)
            #     stats['has_completed'] = False
            return JsonResponse(stats)
        except Exception as e:
            print(e)
            return JsonResponse({})


def it_partnership(request):
    if request.method == 'POST':
        it_partner = ItPartnershipForm(request.POST)
        if it_partner.is_valid():
            it_partner.save()
            messages.success(request,'Information Successful saved!')
            return redirect('home:it_partnership')
        else:
            # messages.error(request, message = form_errors,extra_tags="validation")
            return render(
                request, 
                'home/it_partnership.html', 
                {'form':it_partner}
            )
    return TemplateResponse(request, 'home/it_partnership.html') 

