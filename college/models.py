from django.db import models

from users.models import UserCustom


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
        UserCustom,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "teacher"},
        verbose_name="Responsável",
        help_text="Professor responsável pelo departamento.",
        null=True,
        blank=True,
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
    teachers = models.ManyToManyField(
        UserCustom,
        related_name="teaching_classes",
        limit_choices_to={"type": "teacher"},
        verbose_name="Professores",
        help_text="Professores responsáveis pela turma.",
        blank=True,
    )
    start_date = models.DateField(
        verbose_name="Data de Início", help_text="Data de início do ano letivo."
    )
    end_date = models.DateField(
        verbose_name="Data de Término", help_text="Data de término do ano letivo."
    )

    def __str__(self):
        return self.name
