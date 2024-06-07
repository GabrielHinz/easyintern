from django import forms

from users.models import UserCustom


class UserCustomForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        required=False,
        help_text="Deixe em branco para não alterar.",
    )

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
