from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView

from .models import Patient, Doctor, Case, Medicament
from .forms import PatientForm
from .utils import get_url_without_param

import json
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
        meds = Medicament.objects.annotate(search=SearchVector('indication'), ).filter(
            search=case.diagnose.disease.name)

        ctx['meds'] = meds

    return render(request, 'case.html', context=ctx)


class MedicamentListView(ListView):
    model = Medicament
    template_name = 'medicament_list.html'
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        meds = Medicament.objects.all()
        if self.request.GET.get('q', None):
            meds = Medicament.objects.annotate(search=
                                               SearchVector('uk_name') +
                                               SearchVector('indication') +
                                               SearchVector('uni_name')
                                               ).filter(
                search=self.request.GET.get('q'))
        return meds

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.object_list.count()
        context['path_without_page'] = get_url_without_param(self.request.get_full_path())
        return context


def show_med_instruction_view(request, pk):
    
    med = get_object_or_404(Medicament, pk=pk)
    
    instruction = None
    
    if med.json_instruction:
        instruction = json.loads(med.json_instruction)

    ctx = {
        'instruction' : instruction,
        'name' : med.uk_name,
        'uni_name' : med.uni_name
    }

    return render(request, 'med_instruction.html', context=ctx)

    
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
