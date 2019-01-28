from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from classroom.models import DjangoStudent, ChatRoom, ChatMessage
import json
import hashlib

"""
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
    async def disconnect(self, close_code):
        print(close_code)
        pass
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = text_data_json['user']
        message = text_data_json['message']
        print(user, message)
        await self.send(text_data=json.dumps({'user': user, 'message': message}))




"""

#For when you do have redis; You can see everyone's chat.
class ChatConsumer(AsyncWebsocketConsumer):

    def getRecentMessages(self):
        messages = []
        for message in self.room_object.chatmessage_set.order_by('-pk')[:30]:
            messages.insert(0, {'user': message.user, 'message': message.message,'the_type':message.the_type
                ,'timestamp':message.timestamp})
        # del messages[-1]
        return messages

    def getCount(self, object):
        return object.count()

    def firstObject(self, object):
        return object[0]

    def generate_room(self, this_name, this_hash):
        new_room = ChatRoom(name=this_name, hash=this_hash)
        new_room.save()
        return new_room

    def generate_message(self, this_room, this_user, this_message,this_type,this_timestamp):
        new_message = ChatMessage(room=this_room, user=this_user, message=this_message, the_type=this_type, timestamp=this_timestamp)
        new_message.save()

    async def connect(self):
        self.room_group_name = hashlib.sha256(b'._global_chat_.').hexdigest()
        # self.room_group_name = self.scope['url_route']['kwargs']['group_id']
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': 'SERVER INFO', 'message': self.user + ' has left.'})
        # await database_sync_to_async(self.generate_message)(self.room_object, 'SERVER INFO', str(self.user + ' has left.'))
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.user = text_data_json['user']
        message = text_data_json['message']
        _type = text_data_json['the_type']
        timestamp = text_data_json['timestamp']
        if message[:6] == '!join ':
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            self.room_group_name = hashlib.sha256(message[6:].encode('UTF-8')).hexdigest()
            print(self.room_group_name)
            print (ChatRoom.objects.all())
            room = await database_sync_to_async(ChatRoom.objects.filter)(hash=self.room_group_name)
            room_count = await database_sync_to_async(self.getCount)(room)

            if room_count == 0:
                new_room = await database_sync_to_async(self.generate_room)(message[6:66], self.room_group_name)
                await database_sync_to_async(self.generate_message)(new_room, 'SERVER INFO', '=== Welcome to the groupchat.. ===',_type,timestamp)
                self.room_object = new_room
            else:
                self.room_object = await database_sync_to_async(self.firstObject)(room)
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            # await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': 'SERVER INFO', 'message': self.user + ' has joined.'})
            # await database_sync_to_async(self.generate_message)(self.room_object, 'SERVER INFO', str(self.user + ' has joined.'))

            messages = await database_sync_to_async(self.getRecentMessages)()
            await self.send(text_data=json.dumps({'messages': messages}))
        else:
            print(message)
            await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': self.user, 'message': message,
                                                                       'timestamp':timestamp , 'the_type':_type})
            await database_sync_to_async(self.generate_message)(self.room_object, self.user, message, _type, timestamp)

    async def chat_message(self, event):
        user = event['user']
        message = event['message']
        _type = event['the_type']
        timestamp = event['timestamp']
        await self.send(text_data=json.dumps({'user': user, 'message': message,'the_type':_type,'timestamp':timestamp}))
