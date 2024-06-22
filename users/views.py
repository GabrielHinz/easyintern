from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from panel.objects import get_users
from users.forms import UserCustomForm, UserProfileForm
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


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserCustom
    template_name = "forms/profile.html"
    form_class = UserProfileForm
    success_url = "/user/list/"
    login_url = "/login/"

    def form_valid(self, form):
        if "password" in form.cleaned_data and form.cleaned_data["password"] != "":
            form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Usuários"
        context["segment_link"] = "/user/list/"
        context["pagetitle"] = "Atualização de Perfil"
        return context

    def get_object(self, queryset=None):
        return self.request.user


# Ajax Views
class DXUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "users.view_usercustom"
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = get_users(request.user).filter(id=user_id).first()
        if user:
            image = (
                user.image.url if user.image else "/static/assets/img/default-user.jpg"
            )
            card_body = f"""
                <div class="card-body ">
                    <div class="text-center">
                        <img src="{image}" style="width:150px" alt="Profile" class="rounded-circle">
                        <h3 class="card-title">{user.get_full_name()}
                        <br><span class="card-text text-muted">{user.get_type_display()}</span>
                    </h3>
                    </div>

                    <hr><h5 class="card-text text-muted"><b>Dados</b></h5><hr>
                    <p class="card-text text-muted">E-mail: {user.email}</p>
                    <p class="card-text text-muted">Contatos: {user.contact} / {user.extra_contact or "N/A"}</p>
            """
            if user.type == "student":
                card_body += f"""
                    <p class="card-text text-muted">Turma: {user.student_class}</p>
                    <p class="card-text text-muted">RA: {user.ra}</p>
                    <hr><h5 class="card-text text-muted"><b>Estágios</b></h5><hr>
                """
                for internship in user.student_internship.all():
                    card_body += f"""
                        <p class="card-text text-muted">Estágio: {internship.name}</p>
                    """
            elif user.type == "company":
                card_body += f"""
                    <p class="card-text text-muted">Endereço: {user.address}</p>
                    <p class="card-text text-muted">CNPJ: {user.company_cnpj}</p>
                    <p class="card-text text-muted">Setor: {user.company_sector}</p>
                """
            card_body += "</div>"
            return HttpResponse(card_body)
        else:
            return JsonResponse({"error": "User not found"}, status=404)
