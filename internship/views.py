from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from internship.forms import InternshipForm
from internship.models import Internship
from panel.objects import get_internships


class InternshipListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Internship
    template_name = "list/internship.html"
    context_object_name = "internships"
    login_url = "/login/"
    permission_required = "internship.view_internship"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Estágios"
        return context

    def get_queryset(self):
        return get_internships(self.request.user).order_by("pk")


class InternshipCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Internship
    template_name = "forms/internship.html"
    form_class = InternshipForm
    success_url = reverse_lazy("panel_internship_list")
    login_url = "/login/"
    permission_required = "internship.add_internship"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Estágios"
        context["segment_link"] = "/internship/list/"
        context["pagetitle"] = "Novo Estágio"
        return context


class InternshipUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Internship
    template_name = "forms/internship.html"
    form_class = InternshipForm
    success_url = reverse_lazy("panel_internship_list")
    login_url = "/login/"
    permission_required = "internship.change_internship"

    def get_queryset(self):
        return get_internships(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Estágios"
        context["segment_link"] = "/internship/list/"
        context["pagetitle"] = self.object.name
        return context


class InternshipDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Internship
    template_name = "internship_delete.html"
    success_url = reverse_lazy("panel_internship_list")
    login_url = "/login/"
    permission_required = "internship.delete_internship"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return super().delete(request, *args, **kwargs)
