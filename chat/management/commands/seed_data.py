from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chat.models import Conversation, Message, UnreadMessage
from django.utils import timezone
import random
from datetime import timedelta
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample users, conversations, and messages'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create users with realistic names
        users_data = [
            {'username': 'Abraham Lincoln', 'email': 'abraham@example.com', 'first_name': 'Abraham', 'last_name': 'Lincoln'},
            {'username': 'Marie Curie', 'email': 'marie@example.com', 'first_name': 'Marie', 'last_name': 'Curie'},
            {'username': 'Albert Einstein', 'email': 'albert@example.com', 'first_name': 'Albert', 'last_name': 'Einstein'},
            {'username': 'Grace Hopper', 'email': 'grace@example.com', 'first_name': 'Grace', 'last_name': 'Hopper'},
            {'username': 'Ada Lovelace', 'email': 'ada@example.com', 'first_name': 'Ada', 'last_name': 'Lovelace'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                email=user_data['email'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # Sample messages for realistic conversations
        message_templates = [
            "Kindly check out this image, they are very interesting!",
            "I've reviewed the documents you sent. They look great!",
            "Can we schedule a meeting for tomorrow at 2 PM?",
            "Thanks for your help with the project!",
            "Have you seen the latest updates?",
            "The presentation went really well today.",
            "I'll send you the revised version soon.",
            "Looking forward to our collaboration!",
            "Great work on the recent changes!",
            "Let me know when you're free to discuss.",
        ]

        # Create conversations between pairs of users
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                with transaction.atomic():
                    conversation = Conversation.objects.create()
                    conversation.participants.add(users[i], users[j])
                    conversation.save()
                
                # Generate between 5 and 15 messages for each conversation
                num_messages = random.randint(5, 15)
                base_time = timezone.now() - timedelta(days=1)
                
                for k in range(num_messages):
                    sender = random.choice([users[i], users[j]])
                    receiver = users[j] if sender == users[i] else users[i]
                    message_time = base_time + timedelta(minutes=k*30)
                    
                    message = Message.objects.create(
                        conversation=conversation,
                        sender=sender,
                        content=random.choice(message_templates),
                        timestamp=message_time,
                        is_read=random.choice([True, False])
                    )

                    # Create or update unread message count
                    if not message.is_read:
                        unread, created = UnreadMessage.objects.get_or_create(
                            user=receiver,
                            conversation=conversation,
                            defaults={'count': 1}
                        )
                        if not created:
                            unread.count += 1
                            unread.save()
                
                self.stdout.write(f'Created conversation between {users[i].username} and {users[j].username}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))

