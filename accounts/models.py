from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
    college = models.CharField(max_length=200 , blank=True , null= True )
    is_college_amabassador = models.BooleanField(default=False) 
    bio = models.CharField( max_length=500, null=True, blank=True)
    is_email_verified = models.BooleanField()
    profile_picture=models.ImageField(upload_to='profpictures',null=True)
    def __str__(self):
        return "%s" %(self.user)

 

    