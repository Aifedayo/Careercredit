import json

from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, permissions, status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser

from home.models import Groupclass

from home.models import GroupClassLog

from classroom.models import ChatUpload

from classroom.models import AttendanceLog

from django.conf import settings
from .serializers import GroupClassSerializer, UserSerializer, CourseSerializer, CourseTopicSerializer, \
    AttendanceSerializer, TopicLabSerializer, NoteSerializer
from Courses.models import Course,CourseTopic,LabTask,Note

from datetime import datetime

# To be removed
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_403_FORBIDDEN)
    user = authenticate(username=username, password=password)
    user1= authenticate(email=username, password=password)
    print(user1)
    if not user and not user1:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_400_BAD_REQUEST)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'username':user.get_full_name()},
                        status=status.HTTP_200_OK)
    token, _ = Token.objects.get_or_create(user=user1)
    return Response({'token': token.key, 'username': user1.get_full_name()},
                    status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def confirm_api(request,group_id):
    video_required = False
    uploaded = False
    token = request.data.get("token")
    print(token,"Pasted token")
    try:
        token= Token.objects.get(key=token)
        g= Groupclass.objects.get(pk=group_id)
        print(g)
        print(g.video_required)
        set_last_login(g,token.user)
        if g.video_required:
            video_required = True
            b = AttendanceLog.objects.filter(group=group_id, user=token.user,
                                             timestamp__contains=datetime.now().strftime('%A %d %B, %Y'),
                                             video_url__contains=".webm"
                                             )
            if b:
                uploaded = True

        return Response({'username':token.user.username,
                         'token':token.key,
                         'id':token.user.pk,
                         'role':token.user.role,
                         'video_required':video_required,
                         'uploaded':uploaded,
                         'profile_img':token.user.profile_img,
                         'email':token.user.email
                         },status=status.HTTP_202_ACCEPTED)
    except Token.DoesNotExist:
        return Response("Nothing",status=status.HTTP_403_FORBIDDEN)

def set_last_login(group,user):
    obj,created = GroupClassLog.objects.update_or_create(group=group,user=user,defaults={'last_login':''})
    AttendanceLog.objects.create(group=group,user=user,timestamp=datetime.now().strftime('%A %d %B, %Y @ %I:%M%p'))

def get_last_login(group,user):
    try:
        AttendanceLog.objects.filter(group=group,user=user,
                                   timestamp__contains=datetime.now().strftime('%A %d %B, %Y')
                                   ).order_by('-id')[0]
    except IndexError:
        set_last_login(group,user)
    finally:
        return AttendanceLog.objects.filter(group=group,user=user,
                                   timestamp__contains=datetime.now().strftime('%A %d %B, %Y')
                                   ).order_by('-id')[0]

def video_uploaded(request,group_id):
    print("in verification")
    a=AttendanceLog.objects.filter(group=group_id,user=request.user,
                                   timestamp__contains=datetime.now().strftime('%A %d %B, %Y'),
                                   video_url__contains=".webm"
                                   )
    if a:
        return Response({'uploaded','true'},status.HTTP_200_OK)
    return Response({'uploaded','false'},status.HTTP_404_NOT_FOUND)

class Verification(APIView):
    """
    View to list all groups in the system.

    * Requires token authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, group_id):
        a = AttendanceLog.objects.filter(group=group_id, user=request.user,
                                         timestamp__contains=datetime.now().strftime('%A %d %B, %Y'),
                                         video_url__contains=".webm"
                                         )
        if a:
            return Response({'uploaded': True}, status.HTTP_200_OK)
        return Response({'uploaded': False}, status.HTTP_404_NOT_FOUND)


class UserGroups(APIView):
    """
    View to list all groups in the system.

    * Requires token authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, group_id=0):
        """
        Return a list of all users in the group.
        Returns list of groups associated to the user as well
        """
        group_list= Groupclass.objects.filter(users__email=request.user)
        item= GroupClassSerializer(group_list,many=True)
        return Response(item.data)


class GroupMembers(APIView):
    """
    View to list all groups in the system.
    * Requires token authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, group_id=0):
        """
        Return a list of all users in the group.
        Returns list of groups associated to the user as well
        """
        try:
            g=Groupclass.objects.get(id=group_id)
            users=UserSerializer(g.users,many=True)
            # set_last_login(g,request.user)
            log=GroupClassLog.get_log(g)

            return Response(log)

        except Groupclass.DoesNotExist:
            return Response("Not found",status.HTTP_404_NOT_FOUND)

class GroupUsers(APIView):
    """
    View to list all groups in the system.

    * Requires token authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, group_id=0):
        """
        Return a list of all users in the group.
        Returns list of groups associated to the user as well
        """
        try:
            g=Groupclass.objects.get(id=group_id)
            users=UserSerializer(g.users,many=True)
            return Response(users.data)

        except Groupclass.DoesNotExist:
            return Response("Not found",status.HTTP_404_NOT_FOUND)

class GroupCourseDetail(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    def get(self,request,group_id):
        try:
            group_item=Groupclass.objects.get(pk=group_id)
            if request.user in group_item.users.all():
                # data=CourseTopicSerializer(CourseTopic.objects.filter(course=group_item.course),many=True)
                data=CourseSerializer(group_item.course)
                group_list = Groupclass.objects.filter(users__email=request.user)
                item = GroupClassSerializer(group_list, many=True)
                context={'sessions':item.data,'course_data':data.data}
                return Response(data.data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Groupclass.DoesNotExist:
            pass
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class MyUploadView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    # parser_class = (FileUploadParser,)

    def put(self, request):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        file = request.FILES['file']
        fs=FileSystemStorage(location='/media/chat_uploads')
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        extention=filename.split(".")[-1]
        a=ChatUpload.objects.create(upload=file)
        type=""
        extention = a.upload.url.split(".")[-1] 
        extention=extention.lower()
        if extention not in ['jpg','jpeg','png','ico']:
            type='file'
        else:
            type='image'
        # url = a.upload.url
        url = a.upload.url[1:] if settings.DEBUG else a.upload.url
        return Response({'url':url,'type':type},status=status.HTTP_201_CREATED)


# class UserAttendance(generics.ListAPIView):
#     authentication_classes = (authentication.TokenAuthentication,)
#     serializer_class = AttendanceSerializer
#
#     def get_queryset(self):
#         group_id= self.kwargs['group_id']
#         try:
#             user_id=self.kwargs['user_id']
#         except KeyError:
#             return AttendanceLog.objects.filter(user=self.request.user, group=group_id)[:5]
#         return AttendanceLog.objects.filter(user=user_id,group=group_id)[:5]

class UserAttendance(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self,request,group_id,user_id=None):
        if user_id:

            return Response(AttendanceSerializer(AttendanceLog.objects.filter(user=user_id,group=group_id).order_by("-id")[:5],many=True).data,status.HTTP_200_OK)
        return Response(AttendanceSerializer(AttendanceLog.objects.filter(user=request.user.id,group=group_id).order_by("-id")[:5],many=True).data,status.HTTP_200_OK)


class UserView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = UserSerializer

    def get(self,request,user_id=None):
        if user_id:
            return Response(UserSerializer(CustomUser.objects.get(pk=user_id)).data,status.HTTP_200_OK)
        return Response(UserSerializer(CustomUser.objects.get(email=request.user.email)).data,status.HTTP_200_OK)

    def put(self,request):
        if 'file' not in request.data and 'video' not in request.data:
            return Response('Empty',status=status.HTTP_404_NOT_FOUND)
        if 'file' in request.data:
            print('file used')
            file = request.FILES['file']
            a=ChatUpload.objects.create(upload=file)
            type=""
            extention = a.upload.url.split(".")[-1]
            extention = extention.lower()
            if extention not in ['jpg','jpeg','png','ico']:
                a.delete()
                return Response({},status.HTTP_400_BAD_REQUEST)
            b=CustomUser.objects.get(email=request.user)
            # b.profile_img = a.upload.url
            b.profile_img = a.upload.url[1:] if settings.DEBUG else a.upload.url
            b.save()
            return Response(UserSerializer(b).data,status=status.HTTP_201_CREATED)
        else:
            print('here')
            file = request.FILES['video']
            group=request.data.get('active_group')
            group = Groupclass.objects.get(pk=group)
            a = ChatUpload.objects.create(upload=file)
            b = get_last_login(group,request.user)
            b.video_url = a.upload.url[1:]
            b.save()
            return Response(AttendanceSerializer(b).data, status=status.HTTP_201_CREATED)

    def post(self,request):
        u=CustomUser.objects.get(pk=request.user.id)
        u.first_name=request.data.get('first_name')
        u.last_name=request.data.get('last_name')
        u.save()

        return Response(UserSerializer(u).data,status.HTTP_200_OK)


class GroupDetail(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self,request,group_id):
        g=Groupclass.objects.get(pk=group_id)
        gs=GroupClassSerializer(g)
        return Response(gs.data,status.HTTP_200_OK)

    def post(self,request,group_id):
        g=Groupclass.objects.get(pk=group_id)
        g.video_required=request.data.get('video_required')
        print(g.video_required)
        g.save()
        return Response(GroupClassSerializer(g).data,status.HTTP_200_OK)


class CourseInfo(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = CourseSerializer

    def get(self,id=None,topic_id=None,the_type=None):
        print(id,topic_id,the_type)
        print(type(topic_id))
        if type(id) == int:
            try:
                c= Course.objects.get(pk=id)
                return Response(CourseSerializer(c).data,status=status.HTTP_200_OK)

            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if topic_id:

            if the_type == 'note':
                try:
                    n=Note.objects.get(Topic__pk=topic_id)
                    return Response(NoteSerializer(n).data, status=status.HTTP_200_OK)
                except Note.DoesNotExist:
                    return Response("Not found",status=status.HTTP_404_NOT_FOUND)

            if the_type== "labs":
                l = LabTask.objects.filter(lab=topic_id).order_by('task_number')
                c=CourseTopic.objects.get(pk=topic_id)
                return Response({'labs': TopicLabSerializer(l,many=True).data,'topic':c.topic}, status=status.HTTP_200_OK)

