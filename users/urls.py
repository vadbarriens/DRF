from django.urls import path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserCreateApiView, UserUpdateApiView, UserListApiView, UserDestroyApiView, \
    UserRetrieveApiView
from rest_framework.permissions import AllowAny

app_name = UsersConfig.name

router = DefaultRouter()

urlpatterns = [
    path('register/', UserCreateApiView.as_view(), name='user_create'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('users/', UserListApiView.as_view(), name='users_list'),
    path('user/<int:pk>/', UserRetrieveApiView.as_view(), name='user_retrieve'),
    path('user/<int:pk>/update/', UserUpdateApiView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDestroyApiView.as_view(), name='user_delete'),

]
urlpatterns += router.urls
