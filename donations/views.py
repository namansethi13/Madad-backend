from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .serializers import DonationSerializer,AllDonationSerializer,RatingSerializer
from donations.models import Donation
from django.contrib.auth.models import User
from .models import Rating
from rest_framework import status
from accounts.models import UserDetails
import os
import uuid
from django.shortcuts import get_object_or_404
@api_view(['GET'])
def showdonations(request,id=None):
    
    if id is not None :
        
        eve=Donation.objects.get(id=id)
        
       
        serializer=AllDonationSerializer(eve)
        return Response(serializer.data)
    eve=Donation.objects.all()
    serializer=AllDonationSerializer(eve,many=True)
    return Response(serializer.data)
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])

def updatedonation(request, id):
    try:
        eve = Donation.objects.get(d_id=id, createdby=request.user)
        serializer = DonationSerializer(eve, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'updated successfully'}
            return Response(res)
        else:
            return Response(serializer.errors, status=400)
    except Donation.DoesNotExist:
        res = {'msg': 'Donation not found or you are not authorized to update it.'}
        return Response(res, status=404)
                
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def deletedonation(request, id):
    try:
        boo = Donation.objects.get(d_id=id, createdby=request.user)
        boo.delete()
        res = {'msg': 'deleted successfully'}
        return Response(res)
    except Donation.DoesNotExist:
        res = {'msg': 'Donation not found or you are not authorized to delete it.'}
        return Response(res, status=404)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submitrating(request, donation_id):
    serializer = RatingSerializer(data=request.data)
    print(serializer)
    user = get_object_or_404(User, id=request.user.id)
    userdetails = UserDetails.objects.get(user=user)
    print(user)
    donation = get_object_or_404(Donation, d_id=donation_id)
    rating_exists = Rating.objects.filter(claimedby=user, donation=donation).exists()
    print(donation)
    
    if serializer.is_valid()and not(rating_exists):
        serializer.save(donation=donation, claimedby=user,donor=donation.createdby)
        res = {'msg': 'rated succesfully','rating':request.data['rating']}
        donor = donation.createdby
        print(donor)
        donoruserdetails = UserDetails.objects.get(user=donor)
        
        if donoruserdetails.rating is None:
            donoruserdetails.rating=int(request.data['rating'])
            print("userdetails.rating",donoruserdetails.rating)
            donoruserdetails.save()
            print("saved")

        # else :
        #     userdetails.rating+=int(request.data['rating'])
        #     print("userdetails.rating",userdetails.rating)
        #     userdetails.save()
        #     print("saved")
             
        
        totalrating(request=request,id=user,donation=donation)
        return Response(res)
    
    else:
        res = {'msg': 'you have already rated for this item '}
        return Response(res, status=400)
    
    
         
    
    
def totalrating(request, id,donation):
    print("in total ratings")
    instanceuser = User.objects.get(username=id)
    print("the instrance uyser ",instanceuser)
    donor = donation.createdby
    print(donor)
    userdetails = UserDetails.objects.get(user=donor)
    print("the userdetailsuser ",userdetails)
    count_ratings = Rating.objects.filter(donor=donor).count()
    print(count_ratings)
    totalrating=userdetails.rating
    #print(totalrating)
    if userdetails.rating is not None:
        userdetails.rating = (totalrating*count_ratings +int(request.data['rating'])) /(count_ratings+1)
        print("the final user rating ",userdetails.rating)
        userdetails.save()
        print("saved")

    else :
         userdetails.rating=int(request.data['rating'])
         userdetails.save()
             
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def createdonation(request):
    serializer = DonationSerializer(data=request.data)
    if serializer.is_valid():
        validated_data=serializer.validated_data
        user=User.objects.get(id=request.user.id)
        item_picture = request.data['item_picture']
        filename, ext = os.path.splitext(item_picture.name)
        unique_filename = f"{request.user.username}_{validated_data['item_name']}_{uuid.uuid4().hex}{ext}"
        request.data['item_picture'].name = unique_filename

        instance=Donation.objects.create(createdby=user,item_name=validated_data['item_name'],item_desc=validated_data['item_desc'],Location=validated_data['Location'],item_picture=request.data['item_picture'])
        instance.save()
        res = {'msg': 'created successfully'}
        return Response(res)
    else:
         return Response(serializer.errors, status=400)
        

      

