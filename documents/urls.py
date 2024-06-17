from django.urls import path

from documents.views import (
    ContractCreateView,
    ContractDeleteView,
    ContractListView,
    ContractUpdateView,
    CreateSignatureContractView,
    CreateSignatureReportView,
    ReportCreateView,
    ReportDeleteView,
    ReportListView,
    ReportUpdateView,
)

urlpatterns = [
    path("contract/list/", ContractListView.as_view(), name="panel_contract_list"),
    path(
        "contract/create/",
        ContractCreateView.as_view(),
        name="panel_contract_create",
    ),
    path(
        "contract/update/<int:pk>/",
        ContractUpdateView.as_view(),
        name="panel_contract_update",
    ),
    path(
        "contract/delete/<int:pk>/",
        ContractDeleteView.as_view(),
        name="panel_contract_delete",
    ),
    path("report/list/", ReportListView.as_view(), name="panel_report_list"),
    path(
        "report/create/",
        ReportCreateView.as_view(),
        name="panel_report_create",
    ),
    path(
        "report/update/<int:pk>/",
        ReportUpdateView.as_view(),
        name="panel_report_update",
    ),
    path(
        "report/delete/<int:pk>/",
        ReportDeleteView.as_view(),
        name="panel_report_delete",
    ),
    # Ajax Routes
    path(
        "dx/contract/signature/create/<int:pk>/",
        CreateSignatureContractView.as_view(),
        name="panel_contract_signature_create",
    ),
    path(
        "dx/report/signature/create/<int:pk>/",
        CreateSignatureReportView.as_view(),
        name="panel_report_signature_create",
    ),
]
