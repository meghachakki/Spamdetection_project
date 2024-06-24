# models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    consecutive_spam_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_spam = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)  # New field for read status

    spam_alert_sent = models.BooleanField(default=False)  # To track if alert sent to receiver
    spam_warning_sent = models.BooleanField(default=False)  # To track if warning sent to sender

    def __str__(self):
        return f'{self.sender} to {self.receiver}'

    class Meta:
        ordering = ('created_at',)
