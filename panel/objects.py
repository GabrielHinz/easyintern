from college.models import CollegeClass
from documents.models import Contract, Report
from internship.models import Internship
from users.models import UserCustom


def get_users(user) -> UserCustom:
    full_obj = UserCustom.objects.all()

    if user.is_superuser or user.is_staff or user.type == "admin":
        return full_obj

    if user.type == "teacher":
        if user.responsible_department:
            classes = CollegeClass.objects.filter(
                department__in=user.responsible_department.all()
            )
        else:
            classes = CollegeClass.objects.filter(teachers__in=[user])
        return (
            full_obj.filter(student_class__in=classes)
            | UserCustom.objects.filter(id=user.id)
            | full_obj.filter(type="company")
        )

    return full_obj.filter(id=user.id)


def get_internships(user):
    full_obj = Internship.objects.all()
    if user.type == "student":
        return full_obj.filter(id__in=user.student_internship.all())
    if user.type == "teacher":
        classes = CollegeClass.objects.filter(teachers__in=[user])
        return full_obj.filter(department__in=classes.values("department"))
    if user.type == "company":
        return full_obj.filter(company=user)
    return full_obj


def get_contracts(user):
    full_obj = Contract.objects.all()

    if user.is_superuser or user.is_staff or user.type == "admin":
        return full_obj

    if user.type == "teacher":
        return full_obj.filter(internship__department__responsible=user)
    elif user.type == "student":
        return full_obj.filter(internship__in=user.student_internship.all())
    elif user.type == "company":
        return full_obj.filter(internship__company=user)


def get_reports(user):
    full_obj = Report.objects.all()
    if user.type == "student":
        return full_obj.filter(internship__in=user.student_internship.all())
    if user.type == "teacher":
        classes = CollegeClass.objects.filter(teachers__in=[user])
        return full_obj.filter(student__student_class__in=classes)
    if user.type == "company":
        return full_obj.filter(internship__company=user)
    return full_obj
