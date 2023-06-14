from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView, RegisterView, logout, me

urlpatterns = [
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', me, name='me'),
    path("logout/", logout, name="logout"),
]
