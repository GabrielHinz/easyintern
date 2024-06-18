from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from panel.objects import get_users
from users.forms import UserCustomForm
from users.models import UserCustom


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UserCustom
    template_name = "list/users.html"
    context_object_name = "users"
    permission_required = "users.view_usercustom"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Usuários"
        return context

    def get_queryset(self):
        return get_users(self.request.user).order_by("date_joined")


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = UserCustom
    template_name = "forms/users.html"
    form_class = UserCustomForm
    success_url = "/user/list/"
    permission_required = "users.add_usercustom"
    login_url = "/login/"

    def form_valid(self, form):
        if "password" in form.cleaned_data:
            form.instance.set_password(form.cleaned_data["password"])
        form.instance.save()
        form.instance.groups.add(Group.objects.get(name=form.instance.type))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Usuários"
        context["segment_link"] = "/user/list/"
        context["pagetitle"] = "Criação de Usuário"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = UserCustom
    template_name = "forms/users.html"
    form_class = UserCustomForm
    success_url = "/user/list/"
    permission_required = "users.change_usercustom"
    login_url = "/login/"

    def form_valid(self, form):
        if "password" in form.cleaned_data and form.cleaned_data["password"] != "":
            form.instance.set_password(form.cleaned_data["password"])
        form.instance.groups.clear()
        form.instance.groups.add(Group.objects.get(name=form.instance.type))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Usuários"
        context["segment_link"] = "/user/list/"
        context["pagetitle"] = self.object.get_full_name()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        return get_users(self.request.user)


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = UserCustom
    template_name = "delete/user.html"
    success_url = "/user/list/"
    permission_required = "users.delete_usercustom"
    login_url = "/login/"

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

    def get_queryset(self):
        return get_users(self.request.user)
