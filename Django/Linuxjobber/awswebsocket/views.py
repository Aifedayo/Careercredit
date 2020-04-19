import json
import os
import boto3
import re
from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import CursorPagination 
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from classroom.models import ChatMessage, ChatRoom, Connection, RoomDate

from .models import ChatMessageWithProfile, ChatQoute
from .serializers import ChatSerializer
from .pagination import PaginatedChatMessage

class AwsWebsocketGatewayView(APIView):
    permission_classes = [] 

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
            active_group = request.data['body']['active_group']
            room, _ = ChatRoom.objects.get_or_create(name=active_group)

            room_date, created = RoomDate.objects.get_or_create(
                room=room,defaults={'date':date.today()}
            )

            # Get all current connections
            connections = Connection.objects.all()

            date_message = _save_date_message(
               room_date,created,room,active_group,connections 
            )

            message = _save_message(body,room)
            messages = [message] if date_message == {} else [date_message,message]
            
            data = {
                "active_group":active_group,
                "from_where":"send",
                "messages":messages
            }
            
            _send_message_to_all(data,connections)

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
                "content": _format_user_mention(m.message),
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


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_messages(request): 
    token = request.data['token']
    try:
        token= Token.objects.get(key=token)

        active_group = request.data['active_group']
        offset_id = request.data.get('offset_id',0)

        if offset_id != -1:
            per_page = 30
            room, _ = ChatRoom.objects.get_or_create(
                name=active_group
            )

            message_qs = ChatMessageWithProfile.objects.filter(room=room) \
            .exclude(user__username='SERVER INFO') 
            if offset_id != 0: message_qs = message_qs.filter(id__lt=offset_id)
            message_qs = message_qs.select_related('user','qoute').order_by('-pk')[:per_page]

            messages = [ _format_message(m) for m in message_qs]
            messages.reverse()
            
            data = {
                "active_group": active_group,
                "messages": messages
            }

            data["next_offset_id"] = message_qs[per_page-1].id \
            if len(messages) == per_page else -1

            return Response(data,status.HTTP_200_OK)
        return Response({"error":"out of range"},status.HTTP_404_NOT_FOUND)

    except Token.DoesNotExist:
        return Response("Nothing",status=status.HTTP_403_FORBIDDEN)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_mention_users(request):
    token = request.data['token']
    try:
        token= Token.objects.get(key=token)
        user_count_limit = 10
        search_text = request.data.get('search_text','')
        room, _ = ChatRoom.objects.get_or_create(
            name=request.data['active_group']
        )        
        all_user_qs = ChatMessage.objects.filter(room=room) \
        .exclude(user='SERVER INFO').exclude(user='DATE-INFO')
        mention_user_qs = all_user_qs.filter(user__istartswith=search_text)
        if len(mention_user_qs) < 1: mention_user_qs = all_user_qs
        mention_user_qs = mention_user_qs.values_list('user', flat=True) \
        .distinct()[:user_count_limit]
        return Response(mention_user_qs,status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response("Nothing",status=status.HTTP_403_FORBIDDEN)


#Helper
def _save_message(body,room):
    # Add the new message to the database
    m_instance = ChatMessage(
        user=body['user'],
        message=body['content'],
        the_type=body['the_type'],
        timestamp=body['timestamp'],
        room=room
    ).save()

    chatWithProfile = ChatMessageWithProfile.objects \
    .select_related('user').get(id=m_instance.id)

    if 'qoute_message' in body:
        qoute_m = body['qoute_message']
        chat_q = ChatQoute(
            message=chatWithProfile,
            username=qoute_m['username'],
            content=qoute_m['content'],
            the_type=qoute_m['the_type'],
            timestamp=qoute_m['timestamp']            
        ).save()
        chatWithProfile.qoute = chat_q
    # # Send the message data to all connections
    message = _format_message(chatWithProfile)

    return message

def _save_date_message(room_date,created,room,active_group,connections):
    message = {}
    if room_date.date != str(date.today()) or created == True:
        date_message = ChatMessage(
            user='DATE-INFO',
            message=date.today(),
            the_type='date',
            timestamp='---',
            room=room
        ).save()

        if room_date.date != str(date.today()):
            room_date.date = date.today()
            room_date.save()

        message = {
            'username':date_message.user,
            'content':date_message.message.strftime('%x'),
            'the_type':date_message.the_type
        }

    return message
    
def _send_message_to_all(data,connections):

    for connection in connections:
        try:
            _send_to_connection(
                connection.connection_id, data
            )
        except Exception as e:
            print(connection.connection_id)
            Connection.objects.filter(
                connection_id=connection.connection_id
            ).delete()

def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url = str( settings.AWS_WS_GATEWAY),
        region_name=str(settings.S3DIRECT_REGION),
        aws_access_key_id=str(settings.AWS_ACCESS_KEY_ID_WEBSOCKET),
        aws_secret_access_key=str(settings.AWS_SECRET_ACCESS_KEY_WEBSOCKET),
    )
    return gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(data).encode('utf-8')
    )

def _format_message(m):
    message = {
        "username":m.user.username,
        "profile_img":m.user.profile_img,
        "content": _format_user_mention(m.message),
        "timestamp": m.timestamp,
        "the_type": m.the_type
    }

    qoute_m = getattr(m, 'qoute', None)
    if qoute_m is not None:
        message['qoute_message'] = {
            'username':qoute_m.username,
            'content':_format_user_mention(qoute_m.content),
            'the_type':qoute_m.the_type,
            'timestamp':qoute_m.timestamp  
        }
    return message

def _format_user_mention(text):
    return re.sub("(^@\w{1,50}|\s@\w{1,50})", r" <b>\1</b>", text)
