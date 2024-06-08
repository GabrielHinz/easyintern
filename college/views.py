from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from college.forms import CollegeClassForm
from college.models import CollegeClass, Department


class DepartmentListView(ListView):
    model = Department
    template_name = "list/department.html"
    context_object_name = "departments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Departamentos"
        return context


class DepartmentCreateView(CreateView):
    model = Department
    template_name = "forms/department.html"
    fields = "__all__"
    success_url = reverse_lazy("panel_department_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Departamentos"
        context["segment_link"] = "/department/list/"
        context["pagetitle"] = "Novo Departamento"
        return context


class DepartmentUpdateView(UpdateView):
    model = Department
    template_name = "forms/department.html"
    fields = "__all__"
    success_url = reverse_lazy("panel_department_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Departamentos"
        context["segment_link"] = "/department/list/"
        context["pagetitle"] = self.object.name
        return context


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = "department_delete.html"
    success_url = reverse_lazy("panel_department_list")


class CollegeClassListView(ListView):
    model = CollegeClass
    template_name = "list/collegeclass.html"
    context_object_name = "classes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Turmas"
        return context


class CollegeClassCreateView(CreateView):
    model = CollegeClass
    template_name = "forms/collegeclass.html"
    form_class = CollegeClassForm
    success_url = reverse_lazy("panel_collegeclass_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Turmas"
        context["segment_link"] = "/class/list/"
        context["pagetitle"] = "Nova Turma"
        return context


class CollegeClassUpdateView(UpdateView):
    model = CollegeClass
    template_name = "forms/collegeclass.html"
    form_class = CollegeClassForm
    success_url = reverse_lazy("panel_collegeclass_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "Turmas"
        context["segment_link"] = "/class/list/"
        context["pagetitle"] = self.object.name
        return context


class CollegeClassDeleteView(DeleteView):
    model = CollegeClass
    template_name = "collegeclass_delete.html"
    success_url = reverse_lazy("collegeclass_list")
