from rest_framework import serializers
from .models import Donation
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields =('item_name','item_desc','Location','posted_date')
class AllDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields ='__all__'

        
    

