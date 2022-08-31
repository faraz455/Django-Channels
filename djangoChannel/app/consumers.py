from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from app.models import Chat, Group
import time
import asyncio
import json

class MySyncConsumer(SyncConsumer):

    # When websocket connects this functions get called
    def websocket_connect(self, event):
        print('Websocket connect...', event)
        # This first convert asyn to sync function and 
        # Then add the channel layer to the group
        self.channel_group = self.scope['url_route']['kwargs']['group_name']
        self.group = Group.objects.get(name=self.channel_group)
        async_to_sync (self.channel_layer.group_add)(
            self.channel_group,
            self.channel_name
            )
        # Accepts the connection
        self.send({
            'type': 'websocket.accept'
        })

    # When websocket recieves data from the front end
    def websocket_receive(self,event):
        print('Message recieved...', event['text'])
        text = json.loads(event['text'])
        chat = Chat(UserName = text['user'], content = text['msg'], groupName = self.group)
        chat.save()

        # Send message and user from front end to the group of channels
        async_to_sync (self.channel_layer.group_send)(
            self.channel_group, 
                {
                'type': 'chat.message',
                'message': event['text']
                }
            )
    # Send the message to group
    def chat_message(self, event):
        if event['message'] != '':
            self.send({
                'type': 'websocket.send',
                'text': event['message']
            })

    # When the websockets get disconnected
    def websocket_disconnect(self,event):
        print('Websocket disconnect...', event)
        async_to_sync (self.channel_layer.group_discard)(
            self.channel_group, 
            self.channel_name
            )
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('Websocket connect...', event)

        await self.send({
            'type': 'websocket.accept'
        })
    async def websocket_receive(self,event):
        print('Message recieved...', event)

        for i in range(50):
            self.send({
                'type' : 'websocket.send',
                'text' : str(i)
            })
            await asyncio.time.sleep(1)
    
    async def websocket_disconnect(self,event):
        print('Websocket disconnect...', event)
        raise StopConsumer()
