# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Message, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserProfile
        fields = ['username','first_name', 'last_name', 'email', 'address', 'profile_picture']
        
    def create(self, validated_data):
        user = validated_data.pop('user')  # Get the user instance
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'is_seen', 'timestamp']
        read_only_fields = ['sender', 'timestamp']  # Make sender and timestamp read-only

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user  # Set the sender to the logged-in user
        return super().create(validated_data)

# class ChatRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatRoom

# class DirectMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DirectMessage
#         fields = ['id', 'sender', 'receiver', 'content', 'is_seen', 'timestamp']
#         read_only_fields = ['sender', 'timestamp']

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ['id', 'user', 'message', 'is_read', 'created_at']
