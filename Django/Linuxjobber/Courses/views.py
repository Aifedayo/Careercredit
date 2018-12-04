import subprocess, json, os, requests, random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django import template as temp#, forms
from django.views import generic
from django.conf import settings
from django.core.mail import send_mail

#################################################
#    IMPORTS FROM WITHIN Linuxjobber APPLICATION  #
from .models import GradesReport, Course, CourseTopic, CourseDescription, CoursePermission, Note, NoteComment, TopicStatus
from home.models import Location
from users.models import CustomUser
from .forms import *
from .utils.djangolabsutils import grade_django_lab

register = temp.Library()


""" Dummy method for listing courses """
@login_required
def courses(request):
    courses = Course.objects.all()
    context ={
            'courses': courses     
            }
    return render(request, 'courses/courses.html', context)


"""
     View for listing all topics on a particular course 
    Here we use the course name as passed in the url to obtain the course topics, by applying the Django models relationship manager
"""
class CourseTopicsView(generic.ListView):
    template_name = 'courses/topics.html'
 
    def get_queryset(self):
        return CourseTopic.objects.filter(course__course_title = self.kwargs.get('course_name').replace("_", " "))
 
    def get_context_data(self, **kwargs):
        ip = get_client_ip(self.request)
        add_location(ip,self.request.user)

        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(course_title = self.kwargs.get('course_name').replace("_", " "))
        #context['topicstatus'] = TopicStatus.objects.get(topic)
        if self.request.user.role == 4:
            try:
                context['permission'] = CoursePermission.objects.get(user=self.request.user,course=context['course'])
            except CoursePermission.DoesNotExist:
                context['permission'] = 0
        return context


"""
    View for presenting topic detail (Video), with a link to the lab (where the tasks are listed)
    As in the topics listing view, we also use the manager here to obtain the specific topic,
        using the topic number provided and the course name
"""
def add_location(ip,user):
    url = 'http://api.ipstack.com/'+str(ip)+'?access_key=456c503b74c8697e41cf68f67655842d'
    try:
        r = requests.get(url)
        details = r.json()
        if details['country_name'] is not None:
            locuser = Location(user=user,ipaddress=ip,country=details['country_name'],region=details['region_name'],latitude=details['latitude'],longtitude=details['longitude'],)
            locuser.save()
        else:
            pass
    except requests.exceptions.RequestException as e:
        pass

def TopicNote(request, course_name, lab_no):

    if request.user.is_authenticated:
        template = 'home/base.html'
    else:
        template = 'courses/visitor.html'

    Notes = Note.objects.get(Topic=lab_no)
    Topics = CourseTopic.objects.filter(course__course_title = course_name.replace("_", " "))
    Random = random.sample(list(Topics), 3)
    try:
        comments = NoteComment.objects.filter(Note=Notes)
    except NoteComment.DoesNotExist:
        comments = False

    if request.method == "POST":
        comment = request.POST['comment']

        if comment:
            com = NoteComment(User=request.user,Note=Notes,Comment=comment)
            com.save()
            return render(request, 'courses/note.html', {'template':template, 'note':Notes, 'randoms': Random, 'course': course_name, 'comments':comments})
        else:
            error = True
            return render(request, 'courses/note.html', {'template':template,'note':Notes, 'randoms': Random, 'course': course_name, 'error':error,  'comments':comments})



    return render(request, 'courses/note.html', {'template':template, 'note':Notes, 'randoms': Random, 'course': course_name, 'comments':comments})


def signup(request):
    if request.method == "POST":
        firstname = request.POST['fullname'].split()[0]
        lastname = request.POST['fullname'].split()[1] if len(request.POST['fullname'].split()) > 1 else request.POST['fullname'].split()[0]
        email = request.POST['email']
        password = CustomUser.objects.make_random_password()
        username = email.split('@')[0]

        if (firstname):
            user = CustomUser(username=username, email=email)
            user.set_password(password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            send_mail('Linuxjobber Free Account Creation', 'Hello '+ firstname +' ' + lastname + ',\n' + 'Thank you for registering on Linuxjobber, your username is: ' + username + 'and password is: '+ password +'\nFollow this link http://35.167.153.1:8001/login to login to you account\n\n Thanks & Regards \n Linuxjobber', 'settings.EMAIL_HOST_USER', [email])
            return render(request, "courses/success.html", {'user': user})
        else:
            error = True
            return render(request, 'home/registration/signup.html', {'error':error})
    else:
        return render(request, 'home/registration/signup.html') 

def success(request):
    return render(request, 'courses/success.html')

@login_required
def topicdetails(request, course_name, lab_no):
    context ={
            'topic': CourseTopic.objects.get(course__course_title = course_name.replace("_"," "),topic_number = lab_no)
            }
    return render(request, 'courses/topic_detail.html', context)


"""
    internal method for obtaining the list of accessible instances. Returns a list of all available instances, or an emtpy list if none
"""
def get_active_instances():
    return ['34.145.168.21','34.145.128.1']


"""
    internal method for instantiating the submission form for each lab.
    Uses the course topic and user information provided, to Instantiate the form
"""
def get_gradingform(course_topic, user_obj):
    submit_typ = course_topic.course.lab_submission_type
    form = None
    if submit_typ == 1:
        form = DocumentGradingForm()
    elif submit_typ == 2:
        # For this submission type, we need to obtain a list of instances, set the field widget type to select, set the select's options to the ip addresses returned.
        # If no instance was found to be available, display message "No instances found! Enter IP address"
        form = MachineGradingForm({'machine': '',
                                   'user_id': user_obj.id})
#         form.fields['machine'].widget = forms.Select(choices=(
#         (1, 'submit by uploading document'),
#         (2, 'submit by machine ID'),
#         (3, 'submit from repo')
#     ))
    else:
        form = MachineGradingForm({'machine': user_obj.email,
                                   'user_id': user_obj.id})
        form.fields['machine'].widget = HiddenInput()
        form.fields['machine'].label = "User_email"
    return form




"""
    View for presenting the labtasks, with a provision for submiting the labs.
    Accepts the course name and lab_number, and uses these two parameters to obtain the labID. Using the labID obtained, it queries the list of tasks.
"""
class LabDetailsView(generic.DetailView):
    template_name = 'courses/tasks.html'
    
    def get_object(self):
        return get_object_or_404(CourseTopic, course__course_title = self.kwargs.get('course_name').replace("_", " "),topic_number = self.kwargs.get('lab_no'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = get_gradingform(context['coursetopic'], self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        topic = self.get_object()
        course = topic.course.course_title.split()[0].upper()
        topic_id = str(topic.id)
        topic_slug = topic.lab_name
        user_ID = request.POST.get('user_id')
        user_Add = request.POST.get('machine')
        sub_type = topic.course.lab_submission_type
        if sub_type == 1:
            form = DocumentGradingForm(request.POST, request.FILES)
            if not form.is_valid():
                return HttpResponseBadRequest("Invalid Request")
            new_upload = form.save(commit = False)
            new_upload.user = request.user
            new_upload.course_topic = topic
            form.save()
            output = grade_django_lab(request.FILES['document'], topic.topic_number, request.user)                
            if output == 'Failed':
                return HttpResponse("Result: " + output +" \n <a href='/courses/Django/labs/"+str(topic.topic_number)+"/'>Click here to try again</a>")
            else:
                return HttpResponse(output)
        elif sub_type == 2:
            # GraderServer "machine" data['machine'] "sysadmin" topic_id course data['user_id']
            command = [ settings.BASE_DIR+"/Courses/utils/GraderServer.py","machine",user_Add, "sysadmin", topic_id, course, user_ID ]
            try:
                subprocess.check_call(command, stderr=subprocess.STDOUT, bufsize=-1)
            except:
                return render(request,'courses/result.html',{'gradingerror':"There was an error encountered during grading",'coursetopic':topic})
            handle_rslts(settings.BASE_DIR+"/Courses/utils/"+user_Add,request.user,topic)
        else:
            # /path/to/where/GraderServer.py "repo" course topic_id topic_slug data['user_id'] user_IP 
            command = [ settings.BASE_DIR+"/Courses/utils/GraderServer.py","repo", course, topic_id, topic_slug, user_ID, user_Add ]
            try:
                subprocess.check_call(command, stderr=subprocess.STDOUT, bufsize=-1)
            except:
                return render(request,'courses/result.html',{'gradingerror':"There was an error encountered during grading",'coursetopic':topic})
            handle_rslts(settings.BASE_DIR+"/Courses/utils/"+user_Add,request.user,topic)
        result = GradesReport.objects.filter(user = user_ID, course_topic = topic_id,)
        return render(request, 'courses/result.html',{'result':result,'coursetopic':topic})


"""
    Internal method for handling result.
"""
def handle_rslts(obj,userr,topic):
    with open(obj,"r") as f:
        data = json.load(f)
    user_id = data.pop('userID') # will use this for logging
    lab_id = data.pop('lab_id') # will use this for logging
    for elem in data:
        record, created = GradesReport.objects.get_or_create(user=userr, course_topic = topic, 
                                                             task_no = elem, grade= data[elem],
                                                             defaults={"score": 0}) # defaults used here will be replaced by score = get_scrore(blablabla)
        # here record and created can be used to ascertain when a record is either created or updated.
    os.remove(obj)

def description(request, course_name):
    course = course_name.replace("_"," ")
    #course = Course.objects.get(course=course)
    description = CourseDescription.objects.get(course__course_title=course)
    return render(request, 'courses/coursedescription.html', {'description':description})

def userinterest(request):
    return render(request, 'courses/userinterest.html')

#Get users IP address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
