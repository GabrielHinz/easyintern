from django.contrib.auth.views import LogoutView
from django.urls import path

from panel.views import PanelLoginView, PanelView

urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
    path("login/", PanelLoginView.as_view(), name="panel_login"),
    path("logout/", LogoutView.as_view(next_page="/login/"), name="panel_logout"),
]
