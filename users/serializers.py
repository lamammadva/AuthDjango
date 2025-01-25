from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ['username','email','is_active','date_joined']
     
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
         model = User
         fields = ['username','email','password']
    def create(self,validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username   )
        except ObjectDoesNotExist:
            raise serializers.ValidationError("İstifadəçi adı/email  yanlışdır.")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect credentials")
        tokens = self.get_token(user)
        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
            'username': user.username,
            'email': user.email,
        }
    

