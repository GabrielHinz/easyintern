from django import forms

from college.models import CollegeClass


class CollegeClassForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs = {
                    "class": "selectpicker",
                    "data-live-search": "true",
                }
            elif isinstance(field, forms.DateField):
                field.widget.attrs = {"class": "form-control this-datepicker"}

    class Meta:
        model = CollegeClass
        fields = "__all__"
