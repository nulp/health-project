from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Patient
from .forms import PatientForm

import time


# Create your views here.

def home_view(request):
    return render(request, 'index.html')


def patient_form_view(request):
    qs = Patient.objects.all()
    form = PatientForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        t = str(int(round(time.time() * 1000)))
        usr = User.objects.create_user(username=('test' + t),
                                       password='test123',
                                       first_name=data['first_name'],
                                       last_name=data['last_name']
                                       )
        patient = Patient.objects.create(user=User.objects.get(username=('test' + t)),
                                         ssn=data['zip_code'],
                                         birthday=data['birthday'],
                                         street=data['street'],
                                         city=data['city'],
                                         state=data['city'],
                                         zip_code=data['zip_code'],
                                         gender=data['gender'][0])

    context = {'object_list': qs, 'form': form}
    return render(request, 'patient_form.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET.get('next'))
                else:
                    return redirect('home')

        # if form is not valid or user is None
        messages.error(request, "Будь ласка, введіть правильні ім'я користувача та пароль.")
        messages.error(request, "Зауважте, що обидва поля чутливі до регістру.")

    if request.user.is_authenticated:
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'))
        else:
            return redirect('home')

    return render(request=request, template_name="login.html", context={})
