from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from panel.charts.admin import get_charts


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "pages/index.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Dashboard"
        context["charts"] = get_charts()
        return context


class PanelLoginView(LoginView):
    template_name = "pages/login.html"
    success_url = "/"
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Login"
        return context
