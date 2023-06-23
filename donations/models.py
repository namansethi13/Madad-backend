from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Donation(models.Model):
    d_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=500,null=True)
    createdby=models.ForeignKey(User, on_delete=models.CASCADE)
    item_picture=models.ImageField(upload_to='item_pictures',null=True)
    Location=models.TextField()
    posted_date=models.DateField("startdate(mm/dd/yyyy)",auto_now_add=False,auto_now=False,blank=True)
    # end_date=models.DateField("enddate(mm/dd/yyyy)",auto_now_add=False,auto_now=False,blank=True)

    def __str__(self):
        return "%s" %(self.item_name)