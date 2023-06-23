from rest_framework import serializers
from .models import Donation
class DonationSerializer(serializers.ModelSerializer):
    item_picture = serializers.ImageField(required=True)
    class Meta:
        model = Donation
        fields =('item_name','item_desc','Location','posted_date','item_picture')
class AllDonationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Donation
        fields ='__all__'

        
    

