from django.urls import path
from user.views import loginView, registerView, CookieTokenRefreshView, logoutView, user, UserListCreateView, UserRetrieveUpdateDestroyView, GroupListAPIView

app_name = "user"

urlpatterns = [
    path('login', loginView),
    path('register', registerView),
    path('refresh-token', CookieTokenRefreshView.as_view()),
    path('logout', logoutView),
    path("user", user),

    path("users/", UserListCreateView.as_view()),
    path("users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view()),
    path("groups/", GroupListAPIView.as_view()),
]

