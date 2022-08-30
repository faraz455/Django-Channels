from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import time
import asyncio
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print('Websocket connect...', event)

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self,event):
        print('Message recieved...', event)
        for i in range(50):
            self.send({
                'type' : 'websocket.send',
                'text' : str(i)
            })
            time.sleep(1)
    
    def websocket_disconnect(self,event):
        print('Websocket disconnect...', event)
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
