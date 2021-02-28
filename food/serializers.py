from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
class LoginSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        password = serializers.CharField(required=True)
        email = serializers.CharField(required=True)
        fields = ['email','password']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model= Food
        fields = '__all__'

class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email','first_name','last_name')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            )

        user.set_password(validated_data['password'])
        user.save()
        return user