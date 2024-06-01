from django.contrib.auth.models import AbstractUser
from django.db import models
from stdimage.models import StdImageField


class UserCustom(AbstractUser):
    ra = models.CharField(max_length=10)
    image = StdImageField(
        blank=True, null=True, upload_to="profile", variations={"thumb": (50, 50)}
    )
    email = models.EmailField(unique=True)
    type = models.CharField(
        max_length=1,
        choices=(("F", "Funcionário"), ("U", "Usuário"), ("E", "Empresa")),
        blank=False,
        null=False,
        default="P",
    )
    sex = models.CharField(
        max_length=1,
        choices=(("F", "Feminino"), ("M", "Masculino")),
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    contact = models.CharField(
        max_length=32,
        blank=False,
        null=False,
    )
