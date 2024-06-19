from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from college.forms import CollegeClassForm
from college.models import CollegeClass, Department


class DepartmentListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Department
    template_name = "list/department.html"
    context_object_name = "departments"
    permission_required = "college.view_department"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Universidade"
        context["pagetitle"] = "Departamentos"
        return context


class DepartmentCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Department
    template_name = "forms/department.html"
    fields = "__all__"
    success_url = reverse_lazy("panel_department_list")
    permission_required = "college.add_department"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Departamentos"
        context["segment_link"] = "/department/list/"
        context["pagetitle"] = "Novo Departamento"
        return context


class DepartmentUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Department
    template_name = "forms/department.html"
    fields = "__all__"
    success_url = reverse_lazy("panel_department_list")
    permission_required = "college.change_department"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Departamentos"
        context["segment_link"] = "/department/list/"
        context["pagetitle"] = self.object.name
        return context


class DepartmentDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Department
    template_name = "department_delete.html"
    success_url = reverse_lazy("panel_department_list")
    permission_required = "college.delete_department"
    login_url = "/login/"


class CollegeClassListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = CollegeClass
    template_name = "list/collegeclass.html"
    context_object_name = "classes"
    permission_required = "college.view_collegeclass"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Universidade"
        context["pagetitle"] = "Turmas"
        return context


class CollegeClassCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = CollegeClass
    template_name = "forms/collegeclass.html"
    form_class = CollegeClassForm
    success_url = reverse_lazy("panel_collegeclass_list")
    permission_required = "college.add_collegeclass"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Turmas"
        context["segment_link"] = "/class/list/"
        context["pagetitle"] = "Nova Turma"
        return context


class CollegeClassUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = CollegeClass
    template_name = "forms/collegeclass.html"
    form_class = CollegeClassForm
    success_url = reverse_lazy("panel_collegeclass_list")
    permission_required = "college.change_collegeclass"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Turmas"
        context["segment_link"] = "/class/list/"
        context["pagetitle"] = self.object.name
        return context


class CollegeClassDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = CollegeClass
    template_name = "collegeclass_delete.html"
    success_url = reverse_lazy("collegeclass_list")
    permission_required = "college.delete_collegeclass"
    login_url = "/login/"
