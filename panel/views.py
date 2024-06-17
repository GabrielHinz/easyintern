from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


class PanelView(TemplateView):
    # permission_required = "panel.view_panel"
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Dashboard"
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
