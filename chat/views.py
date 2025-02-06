from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Conversation, Message, UnreadMessage
from .serializers import ConversationSerializer, MessageSerializer
from django.db import transaction

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    @action(detail=False, methods=['post'])
    def create_or_get(self, request):
        email = request.data.get('email')
        try:
            other_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
        if not conversation:
            with transaction.atomic():
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, other_user)
                conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return self.queryset.filter(conversation_id=conversation_id)
        return self.queryset.none()

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        conversation = message.conversation
        for user in conversation.participants.all():
            if user != self.request.user:
                unread, created = UnreadMessage.objects.get_or_create(
                    user=user,
                    conversation=conversation,
                    defaults={'count': 1}
                )
                if not created:
                    unread.count += 1
                    unread.save()

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        conversation_id = request.data.get('conversation_id')
        if conversation_id:
            UnreadMessage.objects.filter(user=request.user, conversation_id=conversation_id).delete()
            return Response({'status': 'messages marked as read'})
        return Response({'error': 'conversation_id is required'}, status=status.HTTP_400_BAD_REQUEST)

