from django.contrib.auth.models import AbstractUser
from django.db import models
from stdimage.models import StdImageField


class UserCustom(AbstractUser):
    ra = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="RA",
        help_text="RA único de cada aluno",
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
    is_student = models.BooleanField(default=False, verbose_name="Aluno")
    is_teacher = models.BooleanField(default=False, verbose_name="Professor")

    def __str__(self):
        return self.first_name + " " + self.last_name + " - (" + self.ra + ")"
