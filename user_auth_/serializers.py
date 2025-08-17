from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.exceptions import ValidationError

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'age', 'address']

class RegistrationSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=12, write_only=True)
    confirm_password = serializers.CharField(max_length=12, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'age', 'address', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({'message':'parollar mos emas', 'status':status.HTTP_400_BAD_REQUEST})
        username = data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError({'message': 'bu username orqli oldin royxatdan otilgan', 'status':status.HTTP_400_BAD_REQUEST})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            age = validated_data['age'],
            address = validated_data['address']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


