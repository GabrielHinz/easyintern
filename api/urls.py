from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (
    IsUserSuperAdmin,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="EasyIntern API",
        default_version="v1",
        description="API básica de criação de usuários para o sistema EasyIntern.",
        terms_of_service="",
        contact=openapi.Contact(email="gabrielhinz001@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(IsUserSuperAdmin,),
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("user/list/", UserListView.as_view(), name="api_user_list"),
    path("user/create/", UserCreateView.as_view(), name="api_user_create"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="api_user_update"),
    path("user/delete/<int:pk>/", UserDeleteView.as_view(), name="api_user_delete"),
]
