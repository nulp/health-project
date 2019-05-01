from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Patient
from .forms import PatientForm

import time
# Create your views here.

def home(request):
    return render(request, 'index.html')

def patient_form_view(request):
    qs = Patient.objects.all()
    form = PatientForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        t = str(int(round(time.time()*1000)))
        usr = User.objects.create_user(username=('test'+t),
        password='test123',
        first_name=data['first_name'],
        last_name=data['last_name']
        )
        patient = Patient.objects.create(user=User.objects.get(username=('test'+t)),
        ssn=data['zip_code'],
        birthday=data['birthday'],
        street=data['street'],
        city=data['city'],
        state=data['city'],
        zip_code=data['zip_code'],
        gender=data['gender'][0])


    context = {'object_list': qs, 'form': form}
    return render(request, 'patient_form.html', context)