from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer , ChangePasswordSerializer
from rest_framework import permissions
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import UserDetails
from django.core.exceptions import PermissionDenied
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated   
from rest_framework.response import Response
from rest_framework import generics
import os
import uuid
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
        # Check if profile_picture field exists in the request data
        if 'profile_picture' in request.data:
            profile_picture = request.data['profile_picture']
            filename, ext = os.path.splitext(profile_picture.name)
            unique_filename = f"{validated_data['username']}_{uuid.uuid4().hex}{ext}"
            # Rename the file within the request.data
            request.data['profile_picture'].name = unique_filename

            # Create the UserDetails instance with profile picture
            user_details = UserDetails.objects.create(
                user=user,
                bio='',
                is_email_verified=True,
                profile_picture=request.data['profile_picture']
            )
        else:
            # Create the UserDetails instance without profile picture
            user_details = UserDetails.objects.create(
                user=user,
                bio='',
                is_email_verified=True
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
        user_details = user.user_details.get()
        if not user_details.is_email_verified:
             return Response(
                {"error": "Email is not verified."},
                status=status.HTTP_403_FORBIDDEN
            )
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
@permission_classes([permissions.IsAuthenticated])
def getuser(request):
    return Response({"user": request.user.username})