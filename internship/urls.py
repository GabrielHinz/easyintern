from django.urls import path

from internship.views import (
    InternshipCreateView,
    InternshipDeleteView,
    InternshipListView,
    InternshipUpdateView,
)

urlpatterns = [
    path(
        "internship/list/", InternshipListView.as_view(), name="panel_internship_list"
    ),
    path(
        "internship/create/",
        InternshipCreateView.as_view(),
        name="panel_internship_create",
    ),
    path(
        "internship/update/<int:pk>/",
        InternshipUpdateView.as_view(),
        name="panel_internship_update",
    ),
    path(
        "internship/delete/<int:pk>/",
        InternshipDeleteView.as_view(),
        name="panel_internship_delete",
    ),
]
