from django import forms

from users.models import UserCustom


class UserCustomForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        required=False,
        help_text="Deixe em branco para não alterar.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].required = True

        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs = {
                    "class": "selectpicker",
                    "data-live-search": "true",
                }
            elif isinstance(field, forms.DateField):
                field.widget.attrs = {"class": "form-control this-datepicker"}
            if field_name == "image":
                field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = UserCustom
        exclude = [
            "date_joined",
            "last_login",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        ]
