import stripe
import csv, io
import subprocess, json, os
from urllib.parse import urlparse
from django.conf import settings
from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse

from .models import *
from Courses.models import Course
from ToolsApp.models import Tool
from users.models import CustomUser
from users.forms import CustomUserCreationForm
from .forms import JobPlacementForm, JobApplicationForm, AWSCredUpload, InternshipForm, ResumeForm

fs = FileSystemStorage(location= settings.MEDIA_ROOT+'/uploads')



def get_courses():
    return Course.objects.all()

def get_tools():
    return Tool.objects.all()


#INDEX VIEW
def index(request):
    return render (request, 'home/index.html', {'courses' : get_courses(), 'tools' : get_tools()})

#SIGNUP VIEW
'''def signup(request):
    if request.method == "POST":
        firstname = request.POST['fullname'].split()[0]
        lastname = request.POST['fullname'].split()[1] if len(request.POST['fullname'].split()) > 1 else request.POST['fullname'].split()[0]
        email = request.POST['email']
        password = request.POST['password']
        username = email.split('@')[0]

        if (firstname):
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            send_mail('Linuxjobber Free Account Creation', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + '\n Follow this link http://35.167.153.1:8001/login to login to you account\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render(request, "home/registration/success.html", {'user': user})
        else:
            error = True
            return render(request, 'home/registration/signup.html', {'error':error})
    else:
        return render(request, 'home/registration/signup.html')'''


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
            send_mail('Linuxjobber Free Account Creation', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + '\n Follow this link http://35.167.153.1:8001/login to login to you account\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
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
            password_reset_link = 'reset_password/'+str(u.id)
            send_mail('Linuxjobber Account Password Reset', 'Hello, \n' + 'You are receiving this email because we received a request to reset your password,\nignore this message if you did not initiate the request else click the link below to reset your password.\n'+'http://54.149.10.37:8000/'+password_reset_link+'\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])

            return render(request, 'home/registration/forgot_password.html',{'message':'An email with password reset information has been sent to you. Check your email to proceede.'})
        else:
            return render(request, 'home/registration/forgot_password.html', {'message':'There is no account associated with this email'})
    else:
        return render(request, 'home/registration/forgot_password.html', {'message':message})

def reset_password(request, u_id):
    message = ''
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            usr = CustomUser.objects.get(id=u_id)
            usr.set_password(request.POST['password1'])
            #usr.save()
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
    if request.method == "POST":
        stripe.api_key = "sk_test_FInuRlOzwpM1b3RIw5fwirtv"
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
            return redirect("home:index")
        else:
            error_message = "yes"
            return render(request, "home/registration/login.html", {'error_message' : error_message})
    else:
        return render(request, "home/registration/login.html", {'courses' : get_courses(), 'tools' : get_tools()})


def log_out(request):
    logout(request)
    return redirect("home:login")

def linux_certification(request):
    return render(request, 'home/linux_certification.html', {'courses' : get_courses(), 'tools' : get_tools()})


def workexperience(request):
    return render(request, 'home/workexperience.html', {'courses' : get_courses(), 'tools' : get_tools()})


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
    stripeset = StripePayment.objects.all()
    email = request.user.email
    plan_id = stripeset[0].planid
    stripe.api_key = stripeset[0].secretkey
    publickey = stripeset[0].publickey

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

    return render(request, 'home/monthly_subscription.html', {'email':email, 'publickey': publickey })

def group(request):
    group = Groupclass.objects.all()

    if request.method == "POST":
        email = request.POST['email']
        choice = request.POST['choice']
        type_of_class = request.POST['name']
        amount = request.POST['price']

        request.session['email'] = email
        request.session['amount'] = amount
        request.session['class'] = type_of_class

        try:
            user = CustomUser.objects.get(email=email)
   
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
                send_mail('Linuxjobber Free Account Creation', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + '\n Follow this link http://35.167.153.1:8001/login to login to you account\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])

                groupreg = GroupClassRegister.objects.create(user= user, is_paid=0, amount=29, type_of_class = type_of_class)
                groupreg.save()
                send_mail('Linuxjobber Group Class', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Group Class, you will be contacted shortly.', 'settings.EMAIL_HOST_USER', [email])

                new_user = authenticate(username=username,
                                    password=password,
                                    )
                login(request, new_user)

                if int(choice) == 1:
                    return redirect("home:monthly_subscription")

                return redirect("home:group_pay")

        if user:

            groupreg = GroupClassRegister.objects.create(user= user, is_paid = 0, amount=29, type_of_class = type_of_class)
            groupreg.save()
            
            login(request, user)
            send_mail('Linuxjobber Group Class', 'Hello '+ user.first_name +' ' + user.last_name + ',\n' + 'Thank you for registering on Group Class, you will be contacted shortly.', 'settings.EMAIL_HOST_USER', [email])

            if int(choice) == 1:
                return redirect("home:monthly_subscription")

            return redirect("home:group_pay")

                
        
    return render(request, 'home/group_class.html', {'groups' : group})

@login_required
def group_pay(request):
    email = request.session['email']
    amount = request.session['amount']
    amount = int(amount) * 100
    type_class = request.session['class']
    stripeset = StripePayment.objects.all()

    context = { "stripe_key": stripeset[0].secretkey,
                   'amount': amount }

    if request.method == "POST":
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
                type_of_class= type_class,
            )
            return redirect("home:group_success")
        except stripe.error.CardError as ce:
            return False, ce
    return render(request, 'home/group_pay.html', context)

def  group_success(request):
    return render(request, 'home/group_success.html')


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
