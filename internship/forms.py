from django import forms

from internship.models import Internship
from panel.objects import get_users


class InternshipForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company"] = forms.ModelChoiceField(
            queryset=get_users(user).filter(type="company"),
            label="Empresa",
            empty_label="Não Selecionado",
        )

        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs = {
                    "class": "selectpicker",
                    "data-live-search": "true",
                }
            elif isinstance(field, forms.DateField):
                field.widget.attrs = {"class": "form-control this-datepicker"}

    class Meta:
        model = Internship
        fields = "__all__"
