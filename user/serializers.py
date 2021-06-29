from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import UserProfile, UserInfo


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'user_email', 'last_name', 'first_name', 'birth_date', 'address_prefecture', 'address_city',
                  'hear_from', 'introduced', 'phone_number', 'hope_rate')
        extra_kwargs = {'user_email': {'read_only': True}}


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ('id', 'user_email', 'point', 'visit_count', 'first_visit', 'previous_visit', 'last_visit',
                  'created_on')
        extra_kwargs = {'user_email': {'read_only': True}}


