import json
import uuid
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
            self.conversation = await self.get_conversation()
            
            if self.conversation:
                await self.channel_layer.group_add(
                    f"chat_{self.conversation_id}",
                    self.channel_name
                )
                await self.accept()
            else:
                await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'conversation_id'):
            await self.channel_layer.group_discard(
                f"chat_{self.conversation_id}",
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        
        if message_type == 'chat_message':
            message = text_data_json['message']
            sender_id = text_data_json['sender_id']
            sender_username = text_data_json['sender_username']
            conversation_id = text_data_json['conversation_id']

            # Save the message to the database
            await self.save_message(message, sender_id, conversation_id)

            # Send message to room group
            await self.channel_layer.group_send(
                f"chat_{self.conversation_id}",
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'sender_username': sender_username,
                    'conversation_id': conversation_id,
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'id': event.get('id', str(uuid.uuid4())),  # Generate a temporary ID if not provided
            'content': event['message'],
            'sender': {
                'id': event['sender_id'],
                'username': event['sender_username'],
            },
            'conversation': event['conversation_id'],
            'timestamp': datetime.now().isoformat(),
        }))

    @database_sync_to_async
    def get_conversation(self):
        try:
            return Conversation.objects.get(id=self.conversation_id, participants=self.user)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, content, sender_id, conversation_id):
        sender = User.objects.get(id=sender_id)
        conversation = Conversation.objects.get(id=conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content
        )

