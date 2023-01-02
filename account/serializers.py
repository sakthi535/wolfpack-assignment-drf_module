from rest_framework import serializers
from .models import User, Images

class UserRegistrationSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields=['email', 'name', 'password']
    extra_kwargs={
      'password':{'write_only':True}
    }
    
    def create(self, validate_data):
      return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
  
  email = serializers.EmailField(max_length = 255)
  class Meta:
    model = User
    fields = ['email', 'password']
    
    
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']
    
class ImageGeneratorSerializer(serializers.ModelSerializer):
  
  image = serializers.ImageField()
  class Meta:
    model = Images
    fields = ['image']