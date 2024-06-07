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

    @property
    def get_type(self):
        if self.is_student:
            return "Aluno"
        elif self.is_teacher:
            return "Professor"
        else:
            return "Usuário"

    def __str__(self):
        if self.type == "student":
            return self.first_name + " " + self.last_name + " - (" + self.ra + ")"
        if self.type == "teacher":
            return self.first_name + " " + self.last_name + " - (Professor)"
        if self.type == "company":
            return self.first_name + " " + self.last_name + " - (Empresa)"
