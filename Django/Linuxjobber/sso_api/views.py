
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser

from home.models import Groupclass

from sso_api.serializers import GroupClassSerializer

from sso_api.serializers import UserSerializer

from Courses.models import Course
from sso_api.serializers import CourseSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def groups(request):

    return Response("Something")

class Groups(APIView):
    def get(self,request):

        return None


class GroupUsers(APIView):
    """
    View to list all groups in the system.

    * Requires token authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, group_id=0):
        """
        Return a list of all users in the group.
        Returns list og groups associated to the user as well
        """
        group_item= Groupclass.objects.filter(users__email=request.user)
        item= GroupClassSerializer(group_item,many=True)
        return Response(item.data)

class CourseDetail(APIView):
    def get(self,request):
        id=request.get['course_id']
        try:
            course=Course.objects.get(pk=id)
            data=CourseSerializer(course,many=True)
            return Response(data.data)

        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


