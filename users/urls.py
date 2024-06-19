from django.urls import path

from users.views import (
    DXUserView,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)

urlpatterns = [
    path("user/list/", UserListView.as_view(), name="panel_user_list"),
    path("user/create/", UserCreateView.as_view(), name="panel_user_create"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="panel_user_update"),
    path("user/delete/<int:pk>/", UserDeleteView.as_view(), name="panel_user_delete"),
    path("dx/user/view/<int:pk>/", DXUserView.as_view(), name="panel_user_view_dx"),
]
