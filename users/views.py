from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from panel.objects import get_users
from users.forms import UserCustomForm
from users.models import UserCustom


class UserListView(ListView):
    model = UserCustom
    template_name = "list/users.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Usuários"
        return context

    def get_queryset(self):
        return get_users(self.request.user).order_by("date_joined")


class UserCreateView(CreateView):
    model = UserCustom
    template_name = "forms/users.html"
    form_class = UserCustomForm
    success_url = "/user/list/"

    def form_valid(self, form):
        if "password" in form.cleaned_data:
            form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Usuários"
        context["segment_link"] = "/user/list/"
        context["pagetitle"] = "Criação de Usuário"
        return context


class UserUpdateView(UpdateView):
    model = UserCustom
    template_name = "forms/users.html"
    form_class = UserCustomForm
    success_url = "/user/list/"

    def form_valid(self, form):
        if "password" in form.cleaned_data and form.cleaned_data["password"] != "":
            print("alterado")
            form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Usuários"
        context["segment_link"] = "/user/list/"
        context["pagetitle"] = self.object.get_full_name()
        return context


class UserDeleteView(DeleteView):
    model = UserCustom
    template_name = "delete/user.html"
    success_url = "/user/list/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Usuários"
        context["segment_link"] = "/user/list/"
        context["pagetitle"] = "Exclusão de Usuário"
        return context
