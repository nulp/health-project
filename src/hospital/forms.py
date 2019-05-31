from django import forms


class PatientForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    middle_name = forms.CharField(max_length=40)
    birthday = forms.DateField()
    street = forms.CharField(max_length=50)
    city = forms.CharField(max_length=20)
    zip_code = forms.CharField(max_length=5)

    gender = forms.CharField(max_length=10)