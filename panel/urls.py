from django.urls import path

from panel.views import PanelView

urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
]
