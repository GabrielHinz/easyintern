from datetime import datetime

from django.core.validators import FileExtensionValidator
from django.db import models

from users.models import UserCustom


class Contract(models.Model):
    internship = models.ForeignKey(
        "internship.Internship",
        on_delete=models.CASCADE,
        related_name="contracts",
        limit_choices_to={"have_contract": True},
        verbose_name="Estágio",
        help_text="Estágio relacionado com o contrato.",
    )
    contract_pdf = models.FileField(
        upload_to="contracts/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        verbose_name="Contrato",
        help_text="Contrato do estágio em (apenas PDF).",
    )

    @property
    def is_approved(self):
        teacher_signature = ContractSignature.objects.filter(
            user__type="teacher",
            contract=self,
        ).exists()
        company_signature = ContractSignature.objects.filter(
            user=self.internship.company,
            contract=self,
        ).exists()
        return teacher_signature and company_signature

    @property
    def get_signatures(self):
        callback = ""
        if ContractSignature.objects.filter(
            contract=self, user__type="teacher"
        ).exists():
            callback += "<span><i style='font-size: 16px; color: green;'class='bi bi-check-all'></i> Professor</span><br>"
        else:
            callback += "<span><i style='font-size: 16px; color: red;' class='bi bi-x'></i> Professor</span><br>"
        if ContractSignature.objects.filter(
            contract=self, user__type="company"
        ).exists():
            callback += "<span><i style='font-size: 16px; color: green;' class='bi bi-check-all'></i> Empresa</span><br>"
        else:
            callback += "<span><i style='font-size: 16px; color: red;' class='bi bi-x'></i> Empresa</span>"
        return callback

    def __str__(self):
        return self.internship.name


class ContractSignature(models.Model):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="signatures"
    )
    date_signed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.contract.internship.name}"


class Report(models.Model):
    student = models.ForeignKey(
        UserCustom,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="Aluno",
        limit_choices_to={"type": "student"},
    )
    internship = models.ForeignKey(
        "internship.Internship",
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="Estágio",
    )
    description = models.TextField(
        verbose_name="Relatório",
        help_text="Descrição do que foi realizado no estágio.",
        null=True,
    )
    start_hour = models.TimeField(verbose_name="Hora de Início")
    end_hour = models.TimeField(verbose_name="Hora de Término")
    date_report = models.DateField(verbose_name="Data do Relatório")

    @property
    def total_hours(self):
        start = datetime.combine(self.date_report, self.start_hour)
        end = datetime.combine(self.date_report, self.end_hour)
        duration = end - start
        total_hours = duration.total_seconds() / 3600
        return total_hours

    @property
    def is_approved(self):
        teacher_signature = ReportSignature.objects.filter(
            user__type="teacher",
            report=self,
        ).exists()
        company_signature = ReportSignature.objects.filter(
            user=self.internship.company,
            report=self,
        ).exists()
        return teacher_signature and company_signature

    @property
    def get_signatures(self):
        callback = ""
        if ReportSignature.objects.filter(report=self, user__type="teacher").exists():
            callback += "<span><i style='font-size: 16px; color: green;'class='bi bi-check-all'></i> Professor</span><br>"
        else:
            callback += "<span><i style='font-size: 16px; color: red;' class='bi bi-x'></i> Professor</span><br>"
        if ReportSignature.objects.filter(report=self, user__type="company").exists():
            callback += "<span><i style='font-size: 16px; color: green;' class='bi bi-check-all'></i> Empresa</span><br>"
        else:
            callback += "<span><i style='font-size: 16px; color: red;' class='bi bi-x'></i> Empresa</span>"
        return callback

    def __str__(self):
        return (
            f"{self.student.get_full_name()} {self.date_report}: {self.internship.name}"
        )


class ReportSignature(models.Model):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="signatures"
    )
    date_signed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.report.internship.name}"
