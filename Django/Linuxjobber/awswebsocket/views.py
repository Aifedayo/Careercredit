import boto3
import json
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from classroom.models import ChatMessage, ChatRoom, Connection
from .models import ChatMessageWithProfile
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token


url = settings.AWS_WS_GATEWAY


class AwsWebsocketGatewayView(APIView):
    permission_classes = [] 

    #get_recent_message
    def get(self,request):
        return Response(
            {'message':'get worked.'},
            status.HTTP_200_OK
        )
        

    #connect
    def post(self,request):
        connection_id = request.data['connectionId']
        Connection(connection_id=connection_id).save()
        return Response(
            {'message':'Connect successful.'},
            status.HTTP_200_OK
        )

    #disconnect
    def delete(self,request):
        connection_id = request.data['connectionId']
        Connection.objects.filter(connection_id=connection_id).delete()
        return Response(
            {'message':'successfully disconnect'},
            status.HTTP_200_OK
        )

    #send_message
    def put(self,request):
        token = request.data['body']['token']
        try:
            token= Token.objects.get(key=token)
    
            body = request.data['body']
            room, _ = ChatRoom.objects.get_or_create(
                name=body['active_group']
            )
            # Add the new message to the database
            instance = ChatMessage(
                user=body['user'],
                message=body['content'],
                the_type=body['the_type'],
                timestamp=body['timestamp'],
                room=room
            ).save()

            chatWithProfile = ChatMessageWithProfile.objects.get(id=instance.id)
            # # Get all current connections
            connections = Connection.objects.all()

            # # Send the message data to all connections
            message = {
                "user":{
                    "username":chatWithProfile.user.username,
                    "profile_img":chatWithProfile.user.profile_img
                }, 
                "content": body['content'],
                "timestamp": body['timestamp'],
                "the_type": body['the_type'],
                "type": 'chat_message'
            }

            data = {
                "active_group": body['active_group'],
                "messages": [message]
            }

            for connection in connections:
                _send_to_connection(
                    connection.connection_id, data
                )

            return Response({'message':'successful'},status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response("Nothing",status=status.HTTP_403_FORBIDDEN)

    #default
    def patch(self,request):
        return Response(
            {'message':'Unrecognized WebSocket action.'},
            status.HTTP_200_OK
        )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_recent_messages(request):
    token = request.data['body']['token']
    try:
        token= Token.objects.get(key=token)

        active_group = request.data['body']['active_group']
        room, _ = ChatRoom.objects.get_or_create(
            name=active_group
        )
        recent_messages = ChatMessageWithProfile.objects \
        .filter(room=room).exclude(user__username='SERVER INFO') \
        .select_related('user').order_by('-pk')[:30]
        # Extract the relevant data and order chronologically
        messages = [
            {
                "user":{
                    "username":m.user.username,
                    "profile_img":m.user.profile_img
                }, 
                "content": m.message,
                "timestamp": m.timestamp,
                "the_type": m.the_type
            } for m in recent_messages
        ]

        messages.reverse()

        # Send them to the client who asked for it
        data = {
            "active_group": active_group,
            "messages": messages
        }

        _send_to_connection(
            request.data['connectionId'], data
        )
            
        return Response(
            {'message':'successfully send'},
            status.HTTP_200_OK
        )
    except Token.DoesNotExist:
        return Response("Nothing",status=status.HTTP_403_FORBIDDEN)

    
#Helper
def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client(
        "apigatewaymanagementapi",endpoint_url = str(url)
    )
    return gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(data).encode('utf-8')
    )
   