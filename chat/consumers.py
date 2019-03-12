from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser, User
from ewp_api.models import Message, ChatRoom
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['user'])
        if self.scope['user'] != AnonymousUser():
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        print(self.scope['user'])
        if self.scope['user'] != AnonymousUser():
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = User.objects.get(username=self.scope['user'].username)
        room = ChatRoom.objects.get(name=self.room_name)
        # print(self.room_name)
        msgobj = Message.objects.create(body=message, sender=sender, room=room)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender.username,
                'message': message,
                'created': msgobj.created.__str__(),
            }
        )
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        created = event['created']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'created': created,
        }))
