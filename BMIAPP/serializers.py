from django.db import models
from rest_framework import fields, serializers

from BMIAPP.models import BMI_History
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email','password')
    def create(self, validated_data):
        user= super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class BMISerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = BMI_History
        fields = '__all__'
        read_only_fields = ['created_at']

    def create(self, validated_data):
        obj = super().create(validated_data)
        obj.created_at = timezone.now()
        obj.save()
        return obj

class ReadBMISerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BMI_History
        fields = '__all__'
        read_only_fields = ['created_at']

    
