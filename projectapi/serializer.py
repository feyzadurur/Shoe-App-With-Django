from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    username=serializers.CharField(max_length=50)
    email=serializers.EmailField()
    password=serializers.CharField()
    first_name=serializers.CharField(max_length=50)
    last_name=serializers.CharField(max_length=50)
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username=validated_data.get("username",instance.username)
        instance.email=validated_data.get("email",instance.email)
        instance.password=validated_data.get("password",instance.password)
        instance.first_name=validated_data.get("first_name",instance.first_name)
        instance.last_name=validated_data.get("last_name",instance.last_name)
        instance.save()
        return instance