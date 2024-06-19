from django.contrib.auth.models import AbstractUser
from django.db import models
from stdimage.models import StdImageField


class UserCustom(AbstractUser):
    ra = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name="R.A",
        help_text="R.A único em caso de aluno",
    )
    image = StdImageField(
        blank=True,
        null=True,
        upload_to="profile",
        variations={
            "thumb": (50, 50),
        },
        verbose_name="Imagem do Perfil",
    )
    student_class = models.ForeignKey(
        "college.CollegeClass",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Turma",
        help_text="Turma do aluno.",
    )
    student_internship = models.ManyToManyField(
        "internship.Internship",
        blank=True,
        verbose_name="Estágios",
        related_name="students",
        help_text="Estágios em que o aluno está participando. Selecione todos os aplicáveis.",
    )
    address = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name="Endereço",
    )
    contact = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        verbose_name="Contato",
    )
    extra_contact = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Contato de Emergência",
        help_text="Número de telefone de emergência.",
    )
    type = models.CharField(
        max_length=10,
        verbose_name="Tipo",
        help_text="Tipo de usuário do sistema",
        choices=[
            ("student", "Aluno"),
            ("teacher", "Professor"),
            ("company", "Empresa"),
        ],
        default="student",
    )
    company_sector = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name="Setor",
        help_text="Setor da empresa.",
    )
    company_cnpj = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        verbose_name="CNPJ",
        help_text="CNPJ da empresa.",
    )

    @property
    def get_type(self):
        if self.is_student:
            return "Aluno"
        elif self.is_teacher:
            return "Professor"
        else:
            return "Usuário"

    @property
    def is_staff_teacher(self):
        return self.type == "teacher" and self.responsible_department.exists()

    def __str__(self):
        if self.type == "student":
            return self.first_name + " " + self.last_name + " - (" + self.ra + ")"
        if self.type == "teacher":
            return self.first_name + " " + self.last_name + " - (Professor)"
        if self.type == "company":
            return self.first_name + " " + self.last_name + " - (Empresa)"
