from django.views.generic import TemplateView


class PanelView(TemplateView):
    # permission_required = "panel.view_panel"
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Dashboard"
        return context
