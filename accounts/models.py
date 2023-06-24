from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
     
    bio = models.CharField( max_length=500, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    profile_picture=models.ImageField(upload_to='profpictures',null=True)
    rating = models.IntegerField(null=True)
    def __str__(self):
        return "%s" %(self.user)
    


    

 

    