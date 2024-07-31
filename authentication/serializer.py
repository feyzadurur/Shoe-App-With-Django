from rest_framework import serializers
from . models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ['id','first_name','last_name','username','password','email']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("İki şifre uyuşmadı.")
        return data
    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Yeni şifre 6 karakterden daha uzun olmalı.")
        return value
    