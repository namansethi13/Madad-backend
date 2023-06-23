from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .serializers import DonationSerializer,AllDonationSerializer
from donations.models import Donation
from django.contrib.auth.models import User


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])

def createdonation(request):
    
    serializer = DonationSerializer(data=request.data)

    if serializer.is_valid():
        validated_data=serializer.validated_data
        user=User.objects.get(id=request.user.id)
        instance=Donation.objects.create(createdby=user,item_name=validated_data['item_name'],item_desc=validated_data['item_desc'],Location=validated_data['Location'],posted_date=validated_data['posted_date'],item_picture=request.data['item_picture'])
        instance.save()
        res = {'msg': 'created successfully'}
        return Response(res)
    else:
         return Response(serializer.errors, status=400)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def showdonations(request,id=None):
    #print("username  :",request.user.id)
    if id is not None :
        
        eve=Donation.objects.get(id=id)
        
       
        serializer=AllDonationSerializer(eve)
        return Response(serializer.data)
    eve=Donation.objects.all()
    serializer=AllDonationSerializer(eve,many=True)
    return Response(serializer.data)
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])

def updatedonation(request,id):
    if id is not None :
            eve=Donation.objects.get(d_id=id)
            serializer=DonationSerializer(eve,data=request.data,partial=True)#model data to python data 
            if serializer.is_valid():
                serializer.save()
                res = {'msg': 'updated succesfully'}
                return Response(res)
            else:
                return Response(serializer.errors, status=400)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])

def deletedonation(request,id):
    if id is not None :
            boo=Donation.objects.get(d_id=id)
            boo.delete()
            res = {'msg': 'deleted succesfully'}
            return Response(res)
    res = {'msg': 'not able to delete the book !some errror occured'}
    return Response(res, status=400)
        

        

      

