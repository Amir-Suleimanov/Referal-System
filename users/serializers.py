from random import random
import string
from rest_framework import serializers
from .models import User, Profile


class InvitedUserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields = ['phone_number']


class ProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta: 
        model = Profile 
        fields = ['first_name', 'last_name', 'invite_code', 'invite_code', 'activated_invite_code', 'invited_users']

        extra_kwargs = {
            'invite_code': {'read_only': True},
        }
    
    def get_invited_users(self, obj):
        users = User.objects.filter(profile__activated_invite_code=obj.invite_code) 
        return InvitedUserSerializer(users, many=True).data

    def create(self, validated_data):
        chars = string.ascii_letters + string.digits
        phrase = ''.join(random.choice(chars) for _ in range(6))
        validated_data['invite_code'] = phrase
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'profile']


class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    code = serializers.CharField(required=False)
