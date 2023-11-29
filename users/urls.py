from django.urls import path
from users.views import register, user_login, user_logout, UserUpdateView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('<int:pk>/profile/', UserUpdateView.as_view(), name='profile'),
]

app_name = 'users'
