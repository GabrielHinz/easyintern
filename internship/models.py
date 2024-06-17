from django.db import models

from college.models import Department
from documents.models import Contract
from users.models import UserCustom


class Internship(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do Estágio")
    description = models.TextField(
        verbose_name="Descrição",
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="Departamento",
        help_text="Departamento relacionado com o estágio que será realizado.",
        null=True,
    )
    company = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "company"},
        verbose_name="Empresa",
        help_text="Empresa que está oferecendo o estágio.",
    )
    date_start = models.DateField(
        verbose_name="Data de Início",
        help_text="Data de início do estágio.",
    )
    date_end = models.DateField(
        verbose_name="Data de Término",
        help_text="Data de término do estágio.",
    )
    have_contract = models.BooleanField(
        verbose_name="Possui Contrato",
        default=False,
    )

    @property
    def can_apply(self):
        if self.have_contract:
            contract = Contract.objects.filter(internship=self).last()
            if contract:
                return contract.is_approved
            return False
        return True

    def __str__(self):
        return self.name
