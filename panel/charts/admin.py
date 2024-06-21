from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from college.models import CollegeClass, Department
from documents.models import Report
from internship.models import Internship
from panel.objects import get_reports_approved
from users.models import UserCustom


def get_reports_chart():
    four_months_ago = timezone.now().date() - timedelta(days=120)
    reports = Report.objects.filter(date_report__gte=four_months_ago)
    reports_approved = get_reports_approved().filter(date_report__gte=four_months_ago)
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
    labels_approved = [data["month"].strftime("%Y-%m") for data in report_data_approved]
    counts_approved = [data["count"] for data in report_data_approved]

    return {
        "labels": labels,
        "labels_approved": labels_approved,
        "counts": counts,
        "counts_approved": counts_approved,
    }


def get_department_chart():
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


def get_dep_internship_chart():
    departments = Department.objects.all()
    internships = Internship.objects.all()
    chart_data = []
    for department in departments:
        chart_data.append(
            {
                "name": department.name,
                "value": internships.filter(department=department).count(),
            }
        )
    return chart_data


def get_last_10_logins():
    users = UserCustom.objects.filter(last_login__isnull=False).order_by("-last_login")[
        :10
    ]
    logins = []
    for user in users:
        time_difference = timezone.now() - user.last_login
        days_ago = int(time_difference.total_seconds() / 86400)
        hours_ago = int(time_difference.total_seconds() / 3600) % 24
        minutes_ago = int(time_difference.total_seconds() / 60) % 60
        if days_ago > 0:
            logins.append(
                (user.get_type_display(), user.get_full_name(), f"{days_ago} d")
            )
        elif hours_ago > 0:
            logins.append(
                (user.get_type_display(), user.get_full_name(), f"{hours_ago} h")
            )
        else:
            logins.append(
                (user.get_type_display(), user.get_full_name(), f"{minutes_ago} m")
            )
    return logins


def get_charts():
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
        "reports_chart": get_reports_chart(),
        "departments_chart": get_department_chart(),
        "dep_internship_chart": get_dep_internship_chart(),
        "last_login": get_last_10_logins(),
    }
