from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, ImageGeneratorSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

from .models import User
from .renderers import UserRenderer


import json

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    
    def post(self, request, format = None):
        request.data['password'] = make_password(request.data['password'])
        serializer = UserRegistrationSerializer(data = request.data)
        if(serializer.is_valid(raise_exception= True)):

            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg' : 'Success', 'token' : token}, status=status.HTTP_201_CREATED)
        return Response({'msg' : 'Failed'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ImageGeneratorView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = ImageGeneratorSerializer(data = request.data)
        if serializer.is_valid() :
            imageObject = serializer.save()
            return Response(json.dumps(imageObject.image_generator()), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)