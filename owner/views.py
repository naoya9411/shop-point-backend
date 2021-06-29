from rest_framework import generics, permissions, viewsets, views
from rest_framework.response import Response
from owner.serializers import UserSerializer, UserPointSerializer, UserVisitSerializer
from core.models import UserProfile, UserInfo
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from datetime import datetime, date, timedelta
from pytz import timezone


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


# 来店ユーザへの日付の更新、ポイント付与するView
class UserVisitView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def patch(self, request, pk, *args, **kwargs):
        print(pk)
        user_info = get_object_or_404(UserInfo, pk=pk)
        print(datetime.now())
        data = request.data.copy()

        # 初来店の場合、現在時刻をセット
        if user_info.first_visit is None:
            print('初回')
            data['first_visit'] = datetime.now()

        #  来店回数をプラス
        data['visit_count'] = user_info.visit_count + 1

        # 最終来店日が前日の場合、連続来店回数をプラス
        twice_visit_today = False
        if user_info.last_visit:
            last_visit_add = user_info.last_visit + timedelta(days=1)
            if last_visit_add.astimezone(timezone('Asia/Tokyo')).date() == date.today():
                data['continuous_visit_count'] = user_info.continuous_visit_count + 1
            elif last_visit_add.astimezone(timezone('Asia/Tokyo')).date() < date.today():
                data['continuous_visit_count'] = 1
            else:
                twice_visit_today = True
        else:
            data['continuous_visit_count'] = 1

        # 最終来店日を前回来店日にコピー
        if user_info.last_visit:
            data['previous_visit'] = user_info.last_visit

        # 最終来店日を現日時で更新
        data['last_visit'] = datetime.now()

        # 連続来店回数の値によりポイント付与
        if not twice_visit_today:
            if data['continuous_visit_count'] == 1:
                data['point'] = user_info.point + 100
            elif data['continuous_visit_count'] == 2:
                data['point'] = user_info.point + 200
            elif data['continuous_visit_count'] == 3:
                data['point'] = user_info.point + 300
            elif data['continuous_visit_count'] == 4:
                data['point'] = user_info.point + 400
            elif data['continuous_visit_count'] >= 5:
                data['point'] = user_info.point + 500

        serializer = UserVisitSerializer(instance=user_info, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


# 手動でポイント増減する場合のView
class UserPointViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserPointSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)


# ユーザ情報一覧取得View
class UserListView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get(self, request):
        users = get_user_model().objects.exclude(is_staff=True)
        user_list = []
        for user in users:
            user_data = {'email': user.email}
            try:
                print('aaa')
                print(user)
                user_profile = UserProfile.objects.get(user_email=user)
                profile_list = {
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'birth_date': user_profile.birth_date,
                    'address_prefecture': user_profile.address_prefecture,
                    'address_city': user_profile.address_city,
                    'hear_from': user_profile.hear_from,
                    'introduced': user_profile.introduced,
                    'phone_number': user_profile.phone_number,
                }
                user_data.update(profile_list)
            except:
                profile_list = {
                    'first_name': '',
                    'last_name': '',
                    'birth_date': '',
                    'address_prefecture': '',
                    'address_city': '',
                    'hear_from': '',
                    'introduced': '',
                    'phone_number': '',
                }
                user_data.update(profile_list)

            try:
                user_info = UserInfo.objects.get(user_email=user)
                info_list = {
                    'user_email': user_info.user_email_id,
                    'info_id': user_info.id,
                    'point': user_info.point,
                    'visit_count': user_info.visit_count,
                    'continuous_visit_count': user_info.continuous_visit_count,
                    'first_visit': user_info.first_visit,
                    'previous_visit': user_info.previous_visit,
                    'last_visit': user_info.last_visit,
                }
                user_data.update(info_list)
            except:
                info_list = {
                    'point': '',
                    'visit_count': '',
                    'first_visit': '',
                    'last_visit': '',
                }
                user_data.update(info_list)

            user_list.append(user_data)

        return Response(user_list)

