from django import forms

from documents.models import Contract, Report
from panel.objects import get_internships, get_users


class ContractForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["internship"] = forms.ModelChoiceField(
            queryset=get_internships(user).filter(have_contract=True),
            label="Estágio",
            empty_label="Não Selecionado",
        )

        for field_name, field in self.fields.items():
            if isinstance(field, forms.FileField):
                field.widget.attrs = {
                    "class": "form-control",
                }
            elif isinstance(field, forms.ChoiceField):
                field.widget.attrs = {
                    "class": "selectpicker",
                    "data-live-search": "true",
                }

    class Meta:
        model = Contract
        fields = "__all__"


class ReportForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"] = forms.ModelChoiceField(
            queryset=get_users(user).filter(type="student"),
            label="Aluno",
            empty_label="Não Selecionado",
        )
        self.fields["internship"] = forms.ModelChoiceField(
            queryset=get_internships(user),
            label="Estágio",
            empty_label="Não Selecionado",
        )

        for field_name, field in self.fields.items():
            if isinstance(field, forms.FileField):
                field.widget.attrs = {
                    "class": "form-control",
                }
            elif isinstance(field, forms.DateField):
                field.widget.attrs = {
                    "class": "form-control this-datepicker",
                    "placeholder": "dd/mm/yyyy",
                }
            elif isinstance(field, forms.TimeField):
                field.widget.attrs = {
                    "class": "form-control this-timepicker",
                    "placeholder": "00:00",
                }
            elif isinstance(field, forms.ChoiceField):
                field.widget.attrs = {
                    "class": "selectpicker",
                    "data-live-search": "true",
                }

    class Meta:
        model = Report
        fields = "__all__"
