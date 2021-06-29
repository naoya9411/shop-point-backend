from rest_framework import generics, permissions, viewsets, views
from rest_framework.response import Response
from user.serializers import UserSerializer, UserProfileSerializer, UserInfoSerializer
from core.models import UserProfile, UserInfo
from django.db.models import Q


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            return self.queryset.filter(Q(user_email=self.request.user))
        except Exception:
            return Response(detail="ログインしてください")

    def perform_create(self, serializer):
        # try:
        serializer.save(user_email=self.request.user)
        # except Exception:
        #     raise ValidationError("User can have only unique request")


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(Q(user_email=self.request.user))

    def perform_create(self, serializer):
        serializer.save(user_email=self.request.user)



