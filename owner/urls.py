from django.urls import path, include
from owner import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('point-change', views.UserPointViewSet)

urlpatterns = [
    path('users/', views.UserListView.as_view()),
    path('visit/<pk>/', views.UserVisitView.as_view()),
    path('', include(router.urls)),
]
