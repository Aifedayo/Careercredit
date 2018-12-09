
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser

from home.models import Groupclass

from .serializers import GroupClassSerializer,UserSerializer,CourseSerializer,CourseTopicSerializer
from Courses.models import Course,CourseTopic



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
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)
@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def groups(request):

    return Response("Something")

class Groups(APIView):
    def get(self,request):

        return None


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
