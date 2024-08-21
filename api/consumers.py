# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from .serializers import MessageSerializer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.accept()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        print(f"Received message: {message_content}")
        
        # thank_you_message = "Thank you, I got your message!"
        # await self.send(text_data=json.dumps({
        #     'message': thank_you_message
        # }))
        
        # # Save message to the database
        # room = await database_sync_to_async(ChatRoom.objects.get)(id=self.room_id)
        # message = await database_sync_to_async(Message.objects.create)(
        #     user=self.scope['user'],
        #     room=room,
        #     content=message_content
        # )

        # # Serialize the message
        # serializer = MessageSerializer(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': "I am replaing from the group layer"
                    # message_content
                # serializer.data
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))




# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Print the received message in the terminal
#         print(f"Received message: {message}")

#         # Send a thank you message back to the client
#         thank_you_message = "Thank you, I got your message!"
#         await self.send(text_data=json.dumps({
#             'message': thank_you_message
#         }))

#         # Optionally, send the message to the room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
