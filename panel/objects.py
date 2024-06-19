from college.models import CollegeClass
from documents.models import Contract, Report
from internship.models import Internship
from users.models import UserCustom


def get_classes(user):
    # Admin: Tudo liberado
    # Professor: Apenas as turmas que ele leciona
    # Aluno: Apenas a turma que ele está
    full_obj = CollegeClass.objects.all()
    if user.is_superuser or user.is_staff or user.type == "admin":
        return full_obj
    if user.type == "teacher":
        return full_obj.filter(teachers__in=[user])
    if user.type == "student":
        return full_obj.filter(id=user.student_class.id)
    return full_obj


def get_users(user) -> UserCustom:
    # Admin: Tudo liberado
    # Professor: Apenas os alunos da turma que ele leciona e se ele for responsável por algum departamento,
    # as classes desse departamento também
    # Aluno: Apenas ele mesmo, os professores dele e as empresas dos estágios dele
    # Empresa: Apenas ela mesma, os alunos dos estágios dela

    # TODO: Falta implementar os professores para a empresa

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
    if user.type == "student":
        teachers = user.student_class.teachers.all()
        companies = user.student_internship.all().values("company")
        return (
            full_obj.filter(id__in=teachers)
            | full_obj.filter(id=user.id)
            | full_obj.filter(id__in=companies)
        )
    if user.type == "company":
        internships = Internship.objects.filter(company=user)
        return full_obj.filter(student_internship__in=internships) | full_obj.filter(
            id=user.id
        )


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
