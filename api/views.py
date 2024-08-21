# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import  Message, UserProfile
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Q
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from .serializers import  MessageSerializer, UserSerializer, UserProfileSerializer
# NotificationSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            # Create UserProfile with additional data
            profile_data = {
                'profile_picture': request.data.get('profile_picture'),
                'address': request.data.get('address'),
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save(user=user)  # Link the profile to the user
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message':'User registerd sucessfully',
                    'user': user_serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status= status.HTTP_201_CREATED)
            return Response(profile_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status= status.HTTP_404_NOT_FOUND)

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  
                return Response(serializer.data)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status= status.HTTP_404_NOT_FOUND)



class UserProfileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(profile)
        
        return Response(serializer.data,status= status.HTTP_200_OK)


class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = UserProfile.objects.exclude(user=request.user.id)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status= status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status= status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # For Simple jwt token authentication
    def post(self, request):
            try:
                refresh_token = request.data["refresh"]
                if refresh_token:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                    
                access_token = request.auth
                if access_token:
                    token = AccessToken(access_token)
                    token.blacklist()
                              
                return Response({"message": "Successfully logged out"}, status= status.HTTP_205_RESET_CONTENT) 
            except Exception as e:
                return Response({"error": str(e)}, status= status.HTTP_400_BAD_REQUEST)
    # For django defualt authentication
    # def post(self, request):
    #     logout(request)
    #     return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    
    # For token-based authentication, you can delete the user's token
    # def post(self, request):
        # request.user.auth_token.delete()
        # return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        
class UserMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        try:
            receiver = User.objects.get(username=username)
            messages = Message.objects.filter(
                (Q(sender=request.user) & Q(receiver=receiver)) |
                (Q(sender=receiver) & Q(receiver=request.user))
            ).order_by('-timestamp')

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Receiver does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, username):
        receiver_username = username
        content = request.data.get('content')

        try:
            receiver = User.objects.get(username=receiver_username)
            print(receiver.id)
            serializer = MessageSerializer(data={'receiver': receiver.id, 'content': content}, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Receiver does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        
class MessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def post(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


# class ChatRoomListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         chat_rooms = ChatRoom.objects.all()
#         serializer = ChatRoomSerializer(chat_rooms, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ChatRoomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DirectMessageListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         direct_messages = DirectMessage.objects.filter(receiver=request.user).order_by('-timestamp')
#         serializer = DirectMessageSerializer(direct_messages, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = DirectMessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(sender=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NotificationListView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
#         serializer = NotificationSerializer(notifications, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = NotificationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
