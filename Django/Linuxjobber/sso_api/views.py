import json

from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, permissions, status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
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

from Linuxjobber import settings
from .serializers import GroupClassSerializer, UserSerializer, CourseSerializer, CourseTopicSerializer, \
    AttendanceSerializer
from Courses.models import Course,CourseTopic

from datetime import datetime

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
def confirm_api(request):
    token = request.data.get("token")
    try:
        token= Token.objects.get(key=token)
        return Response({'username':token.user.username,
                         'token':token.key,
                         'id':token.user.pk,
                         'role':token.user.role},status=status.HTTP_202_ACCEPTED)
    except Token.DoesNotExist:
        return Response("Nothing",status=status.HTTP_403_FORBIDDEN)

def set_last_login(group,user):

    obj,created = GroupClassLog.objects.update_or_create(group=group,user=user,defaults={'last_login':''})
    AttendanceLog.objects.create(group=group,user=user,timestamp=datetime.now().strftime('%A %d %B, %Y @ %I:%M%p'))
    print(obj,created)


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
            set_last_login(g,request.user)
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

        return Response({'url':a.upload.url[1:],'type':type},status=status.HTTP_201_CREATED)


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
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.FILES['file']
        a=ChatUpload.objects.create(upload=file)
        type=""
        extention = a.upload.url.split(".")[-1]
        extention=extention.lower()
        if extention not in ['jpg','jpeg','png','ico']:
            a.delete()
            return Response({},status.HTTP_400_BAD_REQUEST)
        b=CustomUser.objects.get(email=request.user)
        b.profile_img='http://'+settings.SERVER_IP+a.upload.url
        b.save()
        return Response(UserSerializer(b).data,status=status.HTTP_201_CREATED)

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

