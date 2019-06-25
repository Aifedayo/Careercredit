import subprocess, json, os, requests, random, datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django import template as temp#, forms
from django.views import generic
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q

#################################################
#    IMPORTS FROM WITHIN Linuxjobber APPLICATION  #
from .models import GradesReport, Course, CourseTopic, CourseDescription, CoursePermission, Note, NoteComment, TopicStat, LabTask, UserInterest, UserCourseStat
from home.models import UserLocation, AwsCredential
from users.models import CustomUser
from .forms import *
from .utils.djangolabsutils import grade_django_lab
#from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view


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
        #ip = get_client_ip(self.request)
        #add_location(ip,self.request.user)
        #stat = checkstat(self.request.user,Course.objects.get(course_title = self.kwargs.get('course_name').replace("_", " ")))

        #Coursestat(self.request.user,Course.objects.get(course_title = self.kwargs.get('course_name').replace("_", " ")))

        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(course_title = self.kwargs.get('course_name').replace("_", " "))
        context['aws'] = check_aws(self.request.user)
        #context['totalstats'] = totalstat(self.request.user,Course.objects.get(course_title = self.kwargs.get('course_name').replace("_", " ")))
        #context['totalstats'] = 0
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
    url = 'https://api.ipgeolocation.io/ipgeo?apiKey=a953f6ff477b431f9a77bfeb4572fd8e&ip='+str(ip)
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

def Coursestat(user,course):
    try:
        stat = UserCourseStat.objects.get(user=user,course=course)
        stat.visit = stat.visit + 1
        stat.save(update_fields=['visit'])
    except UserCourseStat.DoesNotExist:
        stat = UserCourseStat.objects.create(user=user,course=course,visit=1)
        stat.save()
def check_aws(user):
    try:
        aws = AwsCredential.objects.get(user=user)
        return True
    except AwsCredential.DoesNotExist:
        return False

def TopicNote(request, course_name, lab_no):

    if request.user.is_authenticated:
        template = 'home/base.html'
    else:
        template = 'courses/visitor.html'

    try:
        Notes = Note.objects.get(Topic__topic_number=lab_no,Topic__course__course_title = course_name.replace("_", " "))
    except Note.DoesNotExist:
        return redirect("/")
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

@csrf_exempt
def videostat(request, topic, stat):
    if request.method == "POST":
        topic = CourseTopic.objects.get(id=topic)

        #does not have lab
        if topic.has_labs == 0:
            if stat == 0:
                status='start_video'  
            else:
                status='stop_video'  
            video = 50
        #has lab
        else:
            if stat == 1:
                status='start_video'
            else:
                status='stop_video' 
            video = 25

        stats = TopicStat.objects.create(topic=topic,user=request.user,video=video,status=status)
        stats.save()
        return HttpResponse("Result:done")

def coursetot(request,lab_no):
    course = Course.objects.get(id=lab_no)
    topics = CourseTopic.objects.filter(course=course)
    stat = 0
    totscore= 0
    totstat = 0
    count = 0
    for topic in topics:
        leng = 0
        score = 0
        count = count + 1
        grades = GradesReport.objects.filter(user=request.user,course_topic=topic),
    
        try:
            start = TopicStat.objects.filter(topic=topic, user=request.user, status='start_video').last()
            stop = TopicStat.objects.filter(topic=topic, user=request.user, status='stop_video').last()
            #does not have lab
            if topic.has_labs == 0:
                if start is None:
                    stat = stat + 0
                else:
                    stat = stat + start.video
                
                if stop is None:
                    stat = stat + 0
                else:
                    stat = stat + stop.video
            else:
                if start is None:
                    stat = stat + 0
                else:
                    stat = stat + start.video
                
                if stop is None:
                    stat = stat + 0
                else:
                    stat = stat + stop.video

                for grade in grades:
                    for gra in grade:
                        leng = leng+1 
                        if gra.grade == "passed":
                            score = score + 1
                if leng == 0:
                    stat = stat + 0
                else:
                    percent = (score/ leng) * 100
                    if percent > 70:
                        stat = stat + 50
                    else:
                        pass

        except TopicStat.DoesNotExist:
            stat = 0
    if len(topics) == 0:
        totstat = 0
    else:
        totstat = stat / len(topics)
    totstat ={'totstat': totstat}
    return JsonResponse(totstat)

def topictot(request,lab_no):
    stat = 0
    leng = 0
    totscore= 0
    score = 0
    topics = CourseTopic.objects.get(id=lab_no)

    grades = GradesReport.objects.filter(user=request.user,course_topic=topics),
    

    try:
        start = TopicStat.objects.filter(topic=topics, user=request.user, status='start_video').last()
        stop = TopicStat.objects.filter(topic=topics, user=request.user, status='stop_video').last()
        #does not have lab
        if topics.has_labs == 0:
            if start is None:
                stat = stat + 0
            else:
                stat = stat + start.video
            
            if stop is None:
                stat = stat + 0
            else:
                stat = stat + stop.video
        else:
            if start is None:
                stat = stat + 0
            else:
                stat = stat + start.video
            
            if stop is None:
                stat = stat + 0
            else:
                stat = stat + stop.video

            for grade in grades:
                for gra in grade:
                    leng = leng+1 
                    if gra.grade == "passed":
                        score = score + 1
            if leng == 0:
                percent = 0
            else:
                percent = (score/ leng) * 100
                
                if percent > 70:
                    stat = stat + 50
                else:
                    pass
    except TopicStat.DoesNotExist:
        stat = 0
    stat ={'stat': stat}
    return JsonResponse(stat)

def totalstat(user,course):
    topics = CourseTopic.objects.filter(course=course)
    tostat = total = 0
    for topic in topics:
        stat = TopicStat.objects.get(topic=topic, user=user)
        tostat = tostat + stat.start_video + stat.stop_video + stat.lab
    
    if len(topics) == 0:
        total=0
        return total
    else:
        total = tostat / len(topics)
    return int(total)


def checkstat(user,course):
    topics = CourseTopic.objects.filter(course=course)
    for topic in topics:
        try:
            stat = TopicStat.objects.get(user=user,topic=topic)
        except TopicStat.DoesNotExist:
            stat = TopicStat(user=user,topic=topic,lab=0,start_video=0,stop_video=0)
            stat.save()
        
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
        form = None
    return form


@login_required
def labprofile(request):
    courses = Course.objects.filter().exclude(lab_submission_type=0)
    return render(request, 'courses/labprofile.html',{'coursed':courses})

@login_required
def labprofiledetail(request, course_name, lab_no):
    topics = CourseTopic.objects.filter(course__id=lab_no)
    course_name = course_name.replace("_", " ")
    return render(request, 'courses/labprofiledetail.html',{'topics':topics, 'course_name':course_name})

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
        context['course'] = Course.objects.get(course_title=self.kwargs.get('course_name').replace("_", " "))
        if context['course'].lab_submission_type == 2:
            context['machine'] = get_machine(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        topic = self.get_object()
        course = Course.objects.get(course_title=topic.course.course_title)
        topic_id = str(topic.id)
        topic_slug = topic.lab_name
        user_ID = request.POST.get('user_id')
        user_Add = request.POST.get('machine')
        sub_type = topic.course.lab_submission_type
        if sub_type == 1:
            if course.course_title == 'Django' or course.course_title == 'django' or course.course_title == 'DJANGO':
                form = DocumentGradingForm(request.POST, request.FILES)
                if not form.is_valid():
                    print(form.errors)
                    return HttpResponseBadRequest("Invalid Request")
                else:
                    context = grade_django_lab(request.FILES['document'], topic.topic_number, request.user, topic, course)

                    return render(request, 'courses/linux_result.html',context)
            else:
                return HttpResponse('Course does not exist')
        #For Linux and Rscha labs        
        elif sub_type == 2:
            IP = request.POST['ip_address']
            outps = None
            outps = subprocess.Popen(["sshpass","-p", settings.SERVER_PASSWORD, "ssh", "-o StrictHostKeyChecking=no", "-o LogLevel=ERROR", "-o UserKnownHostsFile=/dev/null", settings.SERVER_USER+"@"+str(IP), "python /home/sysadmin/GraderClient.py", settings.SERVER_USER,settings.SERVER_IP,str(topic.id),str(request.user.id)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if outps:
                labs = LabTask.objects.filter(lab=topic)

                for lab in labs:
                    try:
                        get_grade = GradesReport.objects.get(user=request.user,course_topic=topic,lab=lab)
                        get_grade.grade = "Grading"
                        get_grade.score= 0
                        get_grade.save(update_fields=['score','grade'])
                    except GradesReport.DoesNotExist:
                        grade = GradesReport(user=request.user,course_topic=topic,score=0,lab=lab,grade="pending")
                        grade.save()

            messages.success(request, "Please wait your task is currently being graded!")
            
            return redirect("Courses:linux_result", course_name=self.kwargs.get('course_name'), lab_no= topic.topic_number)
            
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


#Yet to be unleashed, an endpoint for graderserver to consume while grading.
"""@api_view(['GET', 'POST'])
def grader(request,topic):
    topicd = CourseTopic.objects.get(id = topic)
    queryset = LabTask.objects.filter(lab = topicd)
    serializer = GraderSerializer(queryset, many=True)
    data = serializer.data

    if request.method == 'POST':
        topic__id = request.POST['lab_id']
        user_ID = request.POST['userID']

        for report in reports:
            report.grade = request.POST[str(report.lab.task_number)]
            report.score = 1
            report.save(update_fields=['grade','score'])

        #add status
        reports = GradesReport.objects.filter(course_topic__id=topic_id,user__id=user_ID)
        for report in reports:
            if report.grade == "passed":
                scored = scored + 1
        expected = len(reports)
        total = (scored / expected) * 100

        status = TopicStat.objects.get(user__id =user_ID,topic__id=topic_id)
        if total >= 70:
            status.lab = 50
            status.save(update_fields=['lab'])
        elif total >= 50:
            status.lab = 25
            status.save(update_fields=['lab'])
        else:
            status.lab = 0
            status.save(update_fields=['lab'])
        return HttpResponse("Result:saved")


    return Response(data)
 """   
def linux_result(request,course_name=None,lab_no=None):
    
    if course_name:
        score = 0
        percent = 0
        stat = 0
        leng = 0
        topic = CourseTopic.objects.get(course__course_title = course_name.replace("_"," "), topic_number = lab_no)
        try:
            next_topic = CourseTopic.objects.get(course__course_title = course_name.replace("_"," "), topic_number = int(lab_no)+1)
        except CourseTopic.DoesNotExist:
            next_topic = None

        grades = GradesReport.objects.filter(user=request.user,course_topic=topic),
        for grade in grades:

            for gra in grade:
                leng = leng+1 
                if gra.grade == "passed":
                    score = score + 1
        if leng == 0:
            stat = "Not attempted"
        else:
            percent = (score/ leng) * 100
            
            if percent > 70:
                stat = "Passed"
            else:
                stat = "Failed"

        #check if still grading
        for grade in grades:
            for gra in grade:
                if gra.grade == "Grading":
                    stat = "Grading"

        context = {
            'topic' : topic,
            'result' : GradesReport.objects.filter(user=request.user,course_topic=topic),
            'related_topic': CourseTopic.objects.filter(course=topic.course),
            'course_name' : course_name,
            'lab_no': lab_no,
            'next_topic': next_topic,
            'percent': int(percent),
            'stat': stat
        }

    else:
        context = None
    return render(request, 'courses/linux_result.html', context)

def topic_stat(request,lab_no):
    leng=0
    score = 0
    percent = 0
    stat = 0
    try:
        grades = GradesReport.objects.filter(user=request.user,course_topic__id=lab_no),
        for grade in grades:
            if not grade:
                stat ={'stat': "not attempted"}
                return JsonResponse(stat)
            for gra in grade:
                leng = leng+1 
                if gra.grade == "passed":
                    score = score + 1
                elif gra.grade == "Grading":
                    stat ={'stat': "Grading"}
                    return JsonResponse(stat)

        percent = (score/ leng) * 100
            
        if percent > 70:
            stat ={'stat': "Passed"}
        else:
            stat ={'stat': "Failed"}

        #check if still grading
        for grade in grades:
            for gra in grade:
                if gra.grade == "Grading":
                    stat ={'stat': "Grading"}
        return JsonResponse(stat)
    except GradesReport.DoesNotExist:
        stat ={'stat': "not attempted"}
        return JsonResponse(stat)

def task_update(request,lab_no,task_no):
    lab = LabTask.objects.get(lab__id=lab_no,task_number=task_no)
    try:
        reports = GradesReport.objects.get(user=request.user,course_topic__id=lab_no,lab=lab)
        if reports.grade == "passed":
            report={'result':'done'}
            return JsonResponse(report)
        else:
            report={'result':'Not done'}
            return JsonResponse(report)
    except GradesReport.DoesNotExist:
        report={'result':'Not done'}
        return JsonResponse(report)
    return JsonResponse(report)

def linux_result_update(request,lab_no):
    reports = GradesReport.objects.filter(user=request.user,course_topic__id=lab_no),
    linuxresult = []
    for report in reports:
        for re in report:
            linuxresult.append(re.grade)

    data = {
        'results' : linuxresult,
    }
    return JsonResponse(data)
        


@csrf_exempt
def store_lab_result(request):
    scored =0
    if request.method == "POST":
        
        topic_id = request.POST['lab_id']
        user_ID = request.POST['userID']
        reports = GradesReport.objects.filter(course_topic__id=topic_id,user__id=user_ID)

        for report in reports:
            report.grade = request.POST[str(report.lab.task_number)]
            report.score = 1
            report.save(update_fields=['grade','score'])

        #add status
        reports = GradesReport.objects.filter(course_topic__id=topic_id,user__id=user_ID)
        for report in reports:
            if report.grade == "passed":
                scored = scored + 1
        expected = len(reports)
        total = (scored / expected) * 100

        status = TopicStat.objects.get(user__id =user_ID,topic__id=topic_id)
        if total >= 70:
            status.lab = 50
            status.save(update_fields=['lab'])
        elif total >= 50:
            status.lab = 25
            status.save(update_fields=['lab'])
        else:
            status.lab = 0
            status.save(update_fields=['lab'])
        return HttpResponse("Result:saved")



def get_machine(user):
    try:
        awscred = AwsCredential.objects.get(user = user)
    except AwsCredential.DoesNotExist:
        return False

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

        for machine in running_machine:

            outps = subprocess.Popen(["sshpass","-p", settings.SERVER_PASSWORD, "ssh", "-o StrictHostKeyChecking=no", "-o LogLevel=ERROR", "-o UserKnownHostsFile=/dev/null", settings.SERVER_USER+"@"+machine[1], " whoami"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            
            outps = bytes(outps[0])
            outps = outps.decode('UTF-8')
            
            #Check if users machine is accessible, if it is check if GraderClient is deploy or not, if not, deploy!
            if "sysadmin" in outps:
                machine.append(True)
                outs = subprocess.Popen(["sshpass","-p", settings.SERVER_PASSWORD, "ssh", "-o StrictHostKeyChecking=no", "-o LogLevel=ERROR", "-o UserKnownHostsFile=/dev/null", settings.SERVER_USER+"@"+machine[1], " [ -f /home/sysadmin/GraderClient.py ] && echo $?"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                outs = bytes(outs[0])
                outs = outs.decode('UTF-8')

                if "0" in str(outs):
                    pass
                else:
                    out = subprocess.Popen(["/bin/bash", settings.BASE_DIR+"/home/utils/deploy_clientapp.sh", machine[1], "/home/sysadmin", settings.BASE_DIR+"/home/utils"])  
            else:
                machine.append(False)
            
        return running_machine    

    except subprocess.CalledProcessError as grepexc:
        print("error code", grepexc.returncode, grepexc.output)
        return_code = grepexc.returncode
        output = grepexc.output
        return False


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

@login_required
def description(request, course_name):
    course = course_name.replace("_"," ")
    coursed = Course.objects.get(course_title=course)
    description = CourseDescription.objects.get(course__course_title=coursed)

    #record type
    try:
        interest = UserInterest.objects.get(user=request.user, course=coursed)
    except UserInterest.DoesNotExist:
        newobj = UserInterest.objects.create(user=request.user, course=coursed)
        newobj.save()
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
