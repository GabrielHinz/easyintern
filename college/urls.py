from django.urls import path

from college.views import (
    CollegeClassCreateView,
    CollegeClassDeleteView,
    CollegeClassListView,
    CollegeClassUpdateView,
    DepartmentCreateView,
    DepartmentDeleteView,
    DepartmentListView,
    DepartmentUpdateView,
)

urlpatterns = [
    path(
        "department/list/", DepartmentListView.as_view(), name="panel_department_list"
    ),
    path(
        "department/create/",
        DepartmentCreateView.as_view(),
        name="panel_department_create",
    ),
    path(
        "department/update/<int:pk>/",
        DepartmentUpdateView.as_view(),
        name="panel_department_update",
    ),
    path(
        "department/delete/<int:pk>/",
        DepartmentDeleteView.as_view(),
        name="panel_department_delete",
    ),
    path(
        "class/list/",
        CollegeClassListView.as_view(),
        name="panel_collegeclass_list",
    ),
    path(
        "class/create/",
        CollegeClassCreateView.as_view(),
        name="panel_collegeclass_create",
    ),
    path(
        "class/update/<int:pk>/",
        CollegeClassUpdateView.as_view(),
        name="panel_collegeclass_update",
    ),
    path(
        "class/delete/<int:pk>/",
        CollegeClassDeleteView.as_view(),
        name="panel_collegeclass_delete",
    ),
]
