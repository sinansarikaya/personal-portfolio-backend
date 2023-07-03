from django.urls import path
from user.views import loginView, registerView, CookieTokenRefreshView, logoutView, user, UserViewSet

app_name = "user"

urlpatterns = [
    path('login', loginView),
    path('register', registerView),
    path('refresh-token', CookieTokenRefreshView.as_view()),
    path('logout', logoutView),
    path("user", user),

    path("users/", UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("users/<int:pk>/", UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]

# GET /users/: Kullanıcı listesini alır.
# POST /users/: Yeni bir kullanıcı oluşturur.
# GET /users/<id>/: Belirtilen ID'ye sahip kullanıcının detaylarını alır.
# PUT /users/<id>/: Belirtilen ID'ye sahip kullanıcının bilgilerini günceller.
# DELETE /users/<id>/: Belirtilen ID'ye sahip kullanıcıyı siler.
