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


class UserPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ('user_email', 'point')
        extra_kwargs = {
            'user_email': {'read_only': True},
        }


class UserVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ('user_email', 'point', 'visit_count', 'continuous_visit_count', 'first_visit', 'previous_visit',
                  'last_visit')
        extra_kwargs = {
            'user_email': {'read_only': True},
        }

