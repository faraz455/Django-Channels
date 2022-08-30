from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import time
import asyncio
import json

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print('Websocket connect...', event)

        async_to_sync (self.channel_layer.group_add)(
            'channel_group',
            self.channel_name
            )

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self,event):
        print('Message recieved...', event['text'])
        # for i in range(50):
        #     self.send({
        #         'type' : 'websocket.send',
        #         'text' : json.dumps({'count': i})
        #     })
        #     time.sleep(1)
        async_to_sync (self.channel_layer.group_send)(
            'channel_group', 
                {
                'type': 'chat.message',
                'message': event['text']
                }
            )
    def chat_message(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self,event):
        print('Websocket disconnect...', event)

        async_to_sync (self.channel_layer.group_discard)(
            'channel_group', 
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
