from django.contrib.auth.models import User
from django.db import models

class UserProfileWeb(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields can be added here (e.g., avatar, bio)
    # profile_picture = models.ImageField(null= True, blank= True)
    # status = models.BooleanField(default= False)

    def __str__(self):
        return self.user.username


class ChatMessages(models.Model):
    sender = models.ForeignKey(User, related_name='send_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receive_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_seen = models.BooleanField(default= False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sender+ " " + self.receiver

    