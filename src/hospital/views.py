from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Patient, Country, Medicament, Applicant, Manufacturer, FarmGroup, MedType
# from .forms import PatientForm

import time, datetime
import csv

import requests
from bs4 import BeautifulSoup
import json

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


def csv_converter(path, f):
    with open(path + f, 'r', encoding='cp1251') as infile, open(path + 'final.csv', 'w', encoding='utf-8', newline='') as outfile:
        inputs = csv.reader(infile, delimiter=';')
        output = csv.writer(outfile)

        for index, row in enumerate(inputs):
            # Create file with no header
            if index == 0:
                continue
            output.writerow(row)


def med_db_fill_test():
    path = 'hospital/storage/'
    csv_converter(path, 'reestr.csv')

    data = csv.reader(open(path+'final.csv', 'r', encoding='utf-8'), delimiter=',')

    for row in data:
        applicant = {
                    'name': row[10],
                    'country': row[11],
                    'address': row[12]
                    }
        manufacturers = [{'name': row[x],
                        'country': row[x+1],
                        'address': row[x+2]} if row[x] != '' else None for x in range(14,28,3)]

        created_country = Country.objects.update_or_create(name = applicant['country'])[0]
        created_applicant = Applicant.objects.update_or_create(uk_name = applicant['name'][:500],
                                                            country=created_country,
                                                            address=applicant['address'])[0]
        
        created_manufactures = []
        for elem in manufacturers:
            if elem:
                created_country = Country.objects.update_or_create(name = elem['country'])[0]
                created_manufactures.append(Manufacturer.objects.update_or_create(uk_name = elem['name'][:500],
                                                            country=created_country,
                                                            address=elem['address'])[0])

        created_farm_group = FarmGroup.objects.update_or_create(name=row[6][:150])[0]

        ed = None
        if row[31] != 'необмежений':
            ed = datetime.datetime.strptime(row[31],'%d.%m.%Y').strftime('%Y-%m-%d')
        
        
        created_med_type = MedType.objects.update_or_create(name=row[32][:150])[0]

        bio = row[33] == 'Так'
        herbal = row[34] == 'Так'
        orphan = row[35] == 'Так'
        homeopathic = row[36] == 'Так'

        created_medicament = Medicament.objects.update_or_create(uk_name=row[1][:150],
                                                                uni_name=row[2][:150],
                                                                pharm_form=row[3],
                                                                containment=row[5],
                                                                ATS_code1=row[7][:8],
                                                                ATS_code2=row[8][:8],
                                                                ATS_code3=row[9][:8],
                                                                applicant=created_applicant,
                                                                reg_num=row[29],
                                                                start_date=datetime.datetime.strptime(row[30],'%d.%m.%Y').strftime('%Y-%m-%d'),
                                                                end_date=ed,
                                                                bio_origin=bio,
                                                                herbal_origin=herbal,
                                                                orphan=orphan,
                                                                homeopathic=homeopathic,
                                                                mnn=row[37],
                                                                instruction_url=row[41])[0]
        
        created_medicament.farm_group.add(created_farm_group) 
        created_medicament.med_type.add(created_med_type) 

        for elem in created_manufactures:
            created_medicament.manufacturer.add(elem)
    

def instruction_parser(name):
    t = requests.get(f'https://tabletki.ua/uk/{name}/')

    if t.status_code != 200:
        return None

    soup = BeautifulSoup(t.text,"html.parser")
    div = soup.find_all('div', attrs={'id':'ctl00_MAIN_ContentPlaceHolder_TranslatedPanel'})

    if not div:
        return None
    
    instriction_div = div[0]

    content = {}
    cur = ''

    for tag in instriction_div.contents[1:-1]:
        
        if tag.name == 'h2':
            content[tag.string] = ''
            cur = tag.string
        else:
            if tag.name != 'p':    #пофіксити цей момент, щоб вподальшому опрацьовувати і таблиці
                continue

            if cur == '':
                continue
            
            for text in tag.strings:
                content[cur] += text

    return content


def instruction_db_fill_test(request):
    meds = Medicament.objects.values_list('pk','uk_name').iterator()

    c = Medicament.objects.count()

    i = 0
    t = 0

    for med in meds:
        content = instruction_parser(med[1].replace('®',''))
        i += 1
        print(f'{i}/{c}')
        print(med[1])
        if content:
            t += 1
            print('!')
            json_content = json.dumps(content)
            if 'Показання' not in content.keys():
                content['Показання'] = '' 

            if 'Протипоказання' not in content.keys(): 
                content['Протипоказання'] = ''
            
            Medicament.objects.filter(pk=med[0]).update(contraindication=content['Протипоказання'],
                    indication=content['Показання'],
                    json_instruction=json_content)

    print(f'{c/t}% has instructions')