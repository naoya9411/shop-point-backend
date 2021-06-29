from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('info', views.UserInfoViewSet)

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('', include(router.urls)),
]
