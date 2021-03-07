from django.db import models
from django.contrib.auth.models import User

class Block(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker_user')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_user')
    blocker_name = models.CharField(max_length=300, null=True)
    blocked_name = models.CharField(max_length=300, null=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_user')
    sender_name = models.CharField(max_length=300, null=True)
    receiver_name = models.CharField(max_length=300, null=True)
    message_detail = models.CharField(max_length=300)

class Log(models.Model):
    logging_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logging_user')
    log_detail = models.CharField(max_length=300)

