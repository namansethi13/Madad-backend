from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer , ChangePasswordSerializer ,NotificationSerializer, UserDetailSerializer
from rest_framework import permissions
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import UserDetails,NotificationModel
from django.core.exceptions import PermissionDenied
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated   
from rest_framework.response import Response
from rest_framework import generics
import os
import uuid
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO  #basic input/output operation
from PIL import Image #Imported to compress images
specialCharacters="!@#$%^&*?//"

# Register API
from django.core.files import File

from django.core.files import File

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the validated data from the serializer
        validated_data = serializer.validated_data

        # Create the user instance
        
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        if password != confirm_password:
            return Response({"error": "password and confirm password don't match"}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) <8:
             return Response({"error": "password should be greater than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
        elif(any(char.isalpha() for char in password) == False):
            return Response({"error": "password should contain atleast 1 alphabet"}, status=status.HTTP_400_BAD_REQUEST)
        elif(any(char.isupper() for char in password) == False):
            return Response({"error": "password should contain atleast 1 uppercase letter"}, status=status.HTTP_400_BAD_REQUEST)
        elif(any(char.islower() for char in password) == False):
            return Response({"error": "password should contain atleast 1 lowercase letter"}, status=status.HTTP_400_BAD_REQUEST)
        elif(any(char.isdigit() for char in password) == False):
            return Response({"error": "password should contain atleast 1 digit"}, status=status.HTTP_400_BAD_REQUEST)
        elif all(x not in specialCharacters for x in password):
            return Response({"error": "password should contain atleast 1 special character"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        token = default_token_generator.make_token(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })



#Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getuser(request,id):
    user = User.objects.get(id=id)
    s = UserSerializer(user)
    return Response({"user": s.data})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getprofile(request):
    user = request.user
    s = UserSerializer(user)
    return Response({"user": s.data})
# @permission_classes([permissions.IsAuthenticated])
def notifications(request):
    notifications = NotificationModel.objects.filter(user = request.user)
    messages = serializers.serialize("json", notifications)

    new_messages = []
    for msg in json.loads(messages):
        new_messages.append({
                "id" : msg["pk"],
                "heading" : msg['fields']['heading'],
                "body" : msg['fields']['body'],
                "is_seen" : msg['fields']['is_seen'],
        })
    return Response({'notifications': new_messages})
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_notification(request):
    user = request.user
    notifications = NotificationModel.objects.filter(user=user)
    serializer = NotificationSerializer(notifications , many = True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def updateprofile(request):
    user = request.user
    user_details = UserDetails.objects.get(user=user)
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user_details.bio = request.data.get('bio', user_details.bio)
    
    # Handle profile picture update
    profile_picture = request.data.get('profile_picture')
    if profile_picture:
        # Rename the profile picture file
        filename, ext = os.path.splitext(profile_picture.name)
        unique_filename = f"{user.username}_{uuid.uuid4().hex}{ext}"
        profile_picture.name = unique_filename
        user_details.profile_picture = profile_picture

        im = Image.open(profile_picture)
        im_io = BytesIO() 
        im.save(im_io, 'JPEG', quality=60) 
        new_image = File(im_io, name=image.name)
        user_details.profile_picture = new_image
    
    user.save()
    user_details.save()
    
    # Return the updated user details if needed
    return Response({'msg':'updated'})
