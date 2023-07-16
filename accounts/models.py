from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from donations.models import Donation
# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
     
    bio = models.CharField( max_length=500, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    profile_picture=models.ImageField(upload_to='profpictures',null=True)
    rating = models.IntegerField(null=True)
    def __str__(self):
        return "%s" %(self.user)
    


    

 

class NotificationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation , on_delete=models.CASCADE,null=True)
    requested_by = models.ForeignKey(User , on_delete=models.CASCADE, related_name="requested_by",null=True)
    heading = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_req = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.heading


@receiver(post_save, sender=NotificationModel)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notifications = NotificationModel.objects.filter(user=instance.user, is_seen=False)
        messages = []
        for notification in notifications:
            message = {
                'id': notification.pk,
                'heading': notification.heading,
                'body': notification.body,
                'is_seen': notification.is_seen,
            }
            messages.append(message)

        async_to_sync(channel_layer.group_send)(
            group=instance.user.username.encode('utf-8'),
            message={
                'type': 'chat_message',
                'messages': messages,
            }
        )