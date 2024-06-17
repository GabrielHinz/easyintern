from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from documents.forms import ContractForm, ReportForm
from documents.models import Contract, ContractSignature, Report, ReportSignature
from panel.objects import get_contracts, get_reports


class ContractListView(ListView):
    model = Contract
    template_name = "list/contract.html"
    context_object_name = "contracts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Contratos"
        context["signed_contracts"] = Contract.objects.filter(
            signatures__user=self.request.user
        )
        return context

    def get_queryset(self):
        return get_contracts(self.request.user).order_by("pk")


class ContractCreateView(CreateView):
    model = Contract
    template_name = "forms/contract.html"
    form_class = ContractForm
    success_url = reverse_lazy("panel_contract_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Contratos"
        context["segment_link"] = "/contract/list/"
        context["pagetitle"] = "Novo Contrato"
        return context


class ContractUpdateView(UpdateView):
    model = Contract
    template_name = "forms/contract.html"
    form_class = ContractForm
    success_url = reverse_lazy("panel_contract_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Contratos"
        context["segment_link"] = "/contract/list/"
        context["pagetitle"] = "Contrato - " + self.object.internship.name
        return context


class ContractDeleteView(DeleteView):
    model = Contract
    template_name = "contract_delete.html"
    success_url = reverse_lazy("panel_contract_list")


class ReportListView(ListView):
    model = Report
    template_name = "list/report.html"
    context_object_name = "reports"

    def get_queryset(self):
        return get_reports(self.request.user).order_by("pk")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Relatórios"
        context["signed_reports"] = Report.objects.filter(
            signatures__user=self.request.user
        )
        return context


class ReportCreateView(CreateView):
    model = Report
    template_name = "forms/report.html"
    form_class = ReportForm
    success_url = reverse_lazy("panel_report_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Relatórios"
        context["segment_link"] = "/report/list/"
        context["pagetitle"] = "Novo Relatório"
        return context

    def form_valid(self, form):
        internship = form.cleaned_data.get("internship")
        contract = Contract.objects.filter(internship=internship).first()
        user = self.request.user

        if not ContractSignature.objects.filter(user=user, contract=contract).exists():
            form.add_error(
                "internship",
                "Você precisa assinar o contrato com este estágio antes de enviar um relatório.",
            )
            return self.form_invalid(form)

        return super().form_valid(form)


class ReportUpdateView(UpdateView):
    model = Report
    template_name = "forms/report.html"
    form_class = ReportForm
    success_url = reverse_lazy("panel_report_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Relatórios"
        context["segment_link"] = "/report/list/"
        context["pagetitle"] = "Relatório - " + self.object.internship.name
        return context

    def form_valid(self, form):
        internship = form.cleaned_data.get("internship")
        contract = Contract.objects.filter(internship=internship).first()
        user = self.request.user

        if not ContractSignature.objects.filter(user=user, contract=contract).exists():
            form.add_error(
                "internship",
                "Você precisa assinar o contrato com este estágio antes de enviar um relatório.",
            )
            return self.form_invalid(form)

        return super().form_valid(form)


class ReportDeleteView(DeleteView):
    model = Report
    template_name = "report_delete.html"
    success_url = reverse_lazy("panel_report_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return super().delete(request, *args, **kwargs)


# Ajax Views
class CreateSignatureContractView(View):
    def post(self, request, *args, **kwargs):
        contract_id = kwargs.get("pk")
        password = request.POST.get("password")
        user = request.user

        if not user.check_password(password):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Erro ao assinar este contrato. Senha incorreta, preencha e tente novamente.",
                },
                status=400,
            )

        try:
            contract = Contract.objects.get(id=contract_id)
            signature_contract = ContractSignature.objects.create(
                contract=contract, user=user
            )
            return JsonResponse(
                {
                    "success": True,
                    "message": "Sua assinatura foi registrada com sucesso.",
                },
                status=201,
            )
        except Contract.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Erro ao assinar. Este contrato não existe.",
                },
                status=400,
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": str(e)},
                status=500,
            )


class CreateSignatureReportView(View):
    def post(self, request, *args, **kwargs):
        report_id = kwargs.get("pk")
        password = request.POST.get("password")
        user = request.user

        if not user.check_password(password):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Erro ao assinar este relatório. Senha incorreta, preencha e tente novamente.",
                },
                status=400,
            )

        try:
            report = Report.objects.get(id=report_id)
            signature_contract = ReportSignature.objects.create(
                report=report, user=user
            )
            return JsonResponse(
                {
                    "success": True,
                    "message": "Sua assinatura foi registrada com sucesso.",
                },
                status=201,
            )
        except Contract.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Erro ao assinar. Esta assinatura não existe.",
                },
                status=400,
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": str(e)},
                status=500,
            )
