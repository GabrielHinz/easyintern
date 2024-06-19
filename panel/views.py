from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.views.generic import TemplateView

from college.models import CollegeClass, Department
from documents.models import Report
from panel.objects import get_reports_approved
from users.models import UserCustom


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "pages/index.html"
    login_url = "/login/"

    def get_department_chart(self):
        departments = Department.objects.all()
        classes = CollegeClass.objects.all()
        chart_data = []
        for department in departments:
            chart_data.append(
                {
                    "name": department.name,
                    "value": classes.filter(department=department).count(),
                }
            )

        return chart_data

    def get_reports_chart(self):
        four_months_ago = timezone.now().date() - timedelta(days=120)
        reports = Report.objects.filter(date_report__gte=four_months_ago)
        reports_approved = get_reports_approved().filter(
            date_report__gte=four_months_ago
        )
        report_data = (
            reports.annotate(month=TruncMonth("date_report"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        report_data_approved = (
            reports_approved.annotate(month=TruncMonth("date_report"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        labels = [data["month"].strftime("%Y-%m") for data in report_data]
        counts = [data["count"] for data in report_data]
        labels_approved = [
            data["month"].strftime("%Y-%m") for data in report_data_approved
        ]
        counts_approved = [data["count"] for data in report_data_approved]

        return {
            "labels": labels,
            "labels_approved": labels_approved,
            "counts": counts,
            "counts_approved": counts_approved,
        }

    def get_all_charts(self):
        users = UserCustom.objects.all()
        reports = Report.objects.all()

        return {
            "students": users.filter(type="student").count(),
            "students_in_internship": users.filter(
                student_internship__isnull=False, type="student"
            )
            .distinct()
            .count(),
            "companies": users.filter(type="company").count(),
            "companies_offering_internship": users.filter(
                internships__isnull=False, type="company"
            )
            .distinct()
            .count(),
            "reports": reports.count(),
            "reports_approved": reports.filter(
                signatures__user__in=users.filter(type__in=["teacher", "company"]),
            )
            .distinct()
            .count(),
            "reports_chart": self.get_reports_chart(),
            "departments_chart": self.get_department_chart(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Dashboard"
        context["charts"] = self.get_all_charts()
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
