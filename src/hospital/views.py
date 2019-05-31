from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .models import Patient, Doctor, Case, Medicament
from .forms import PatientForm

import time


# Create your views here.

@login_required
def home_view(request):
    old_cases = None
    active_cases = None

    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        doctor = None
    if doctor is not None:
        qs = Case.objects.filter(doctor__user_id=request.user.id)
        old_cases = qs.filter(end_date__isnull=False)
        active_cases = qs.filter(end_date__isnull=True)

    ctx = {
        'doctor': doctor,
        'active_cases': active_cases,
        'old_cases': old_cases,

    }
    return render(request, 'index.html', context=ctx)


def show_case_view(request, pk):

    case = get_object_or_404(Case, pk=pk)
    ctx = {
        'case': case,
        'patient': case.patient
    }

    # if request.method == 'POST':
    #     if request.post.get()
    if case.diagnose:

        meds = Medicament.objects.annotate(search=SearchVector('indication'),).filter(search=case.diagnose.disease.name)

        ctx['meds'] = meds

    return render(request, 'case.html', context=ctx)


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
