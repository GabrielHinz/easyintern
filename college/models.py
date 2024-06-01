from django.db import models

from users.models import CustomUser


class Department(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Nome do Departamento"
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código do Departamento",
        help_text="Código único do departamento.",
    )
    responsible = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"is_teacher": True},
        verbose_name="Responsável",
        help_text="Professor responsável pelo departamento.",
    )

    def __str__(self):
        return self.name


class CollegeClass(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Turma")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="Departamento",
        help_text="Departamento ao qual a turma pertence.",
    )
    students = models.ManyToManyField(
        CustomUser,
        related_name="classes",
        limit_choices_to={"is_student": True},
        verbose_name="Alunos",
    )
    teachers = models.ManyToManyField(
        CustomUser,
        related_name="teaching_classes",
        limit_choices_to={"is_teacher": True},
        verbose_name="Professores",
        help_text="Professores responsáveis pela turma.",
    )
    start_date = models.DateField(
        verbose_name="Data de Início", help_text="Data de início do ano letivo."
    )
    end_date = models.DateField(
        verbose_name="Data de Término", help_text="Data de término do ano letivo."
    )

    def __str__(self):
        return self.name
