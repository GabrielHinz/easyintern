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
        "classes/list/",
        CollegeClassListView.as_view(),
        name="panel_collegeclass_list",
    ),
    path(
        "classes/create/",
        CollegeClassCreateView.as_view(),
        name="panel_collegeclass_create",
    ),
    path(
        "classes/update/<int:pk>/",
        CollegeClassUpdateView.as_view(),
        name="panel_collegeclass_update",
    ),
    path(
        "classes/delete/<int:pk>/",
        CollegeClassDeleteView.as_view(),
        name="panel_collegeclass_delete",
    ),
]
