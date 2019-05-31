from django.contrib.auth.models import User
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Location(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=15)
    building = models.CharField(max_length=4)
    apartment = models.CharField(max_length=5)

    def __str__(self):
        return str(self.country) + ', ' + str(self.city) + ',' + str(self.street) + ' ' + str(self.building) + '/' \
               + str(self.apartment)


class Patient(models.Model):
    # user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    # ssn = models.CharField(max_length=9, unique=True)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)

    birthday = models.DateField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=32)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non binary')
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    @property
    def full_name(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    def __str__(self):
        return self.surname + ' ' + self.name


class DoctorSpeciality(models.Model):
    specialty = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = 'Doctors specialties'


class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='doctor')
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)

    specialty = models.ForeignKey(DoctorSpeciality, on_delete=models.CASCADE)

    # certification_CHOICES = (
    #     ('A', 'American Board'),
    #     ('B', 'Bachelor'),
    # )
    # certification = models.CharField(max_length=30, choices=certification_CHOICES)

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic


class FarmGroup(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class MedType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Substance(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Applicant(models.Model):
    uk_name = models.CharField(max_length=500)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.uk_name


class Manufacturer(models.Model):
    uk_name = models.CharField(max_length=500)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.uk_name


class Medicament(models.Model):
    uk_name = models.CharField(max_length=150)
    uni_name = models.CharField(max_length=150)
    med_type = models.ManyToManyField('MedType')
    bio_origin = models.BooleanField()
    herbal_origin = models.BooleanField()
    orphan = models.BooleanField()
    homeopathic = models.BooleanField()
    substance = models.ManyToManyField('Substance')
    containment = models.TextField()
    pharm_form = models.TextField()
    ATS_code1 = models.CharField(max_length=8, null=True)
    ATS_code2 = models.CharField(max_length=8, null=True)
    ATS_code3 = models.CharField(max_length=8, null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    manufacturer = models.ManyToManyField('Manufacturer')
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    reg_num = models.CharField(max_length=20)
    instruction_url = models.URLField()
    flora = models.ManyToManyField('Flora')
    disease = models.ManyToManyField('Disease')

    mnn = models.CharField(max_length=50)
    farm_group = models.ManyToManyField('FarmGroup')

    contraindication = models.TextField(null=True)
    indication = models.TextField(null=True)
    json_instruction = JSONField(null=True)

    def __str__(self):
        return self.uk_name


class Disease(models.Model):
    name = models.CharField(max_length=250)
    disease_type = models.CharField(max_length=250)


class Diagnose(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    valid = models.BooleanField(default=True)
    localization = models.CharField(max_length=150)


class PatientPathology(models.Model):
    pathology = models.ForeignKey(Disease, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    permanent = models.BooleanField(default=None, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Flora(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Case(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    diagnose = models.ForeignKey(Diagnose, on_delete=models.CASCADE, null=True)

    comment = models.TextField(null=True, blank=True)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-pk']

    # @property
    # def pathologies(self):
    #     return PatientPathology.objects.filter()


class Event(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='events')

    # do we need this?
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    data = JSONField()  # {type: '[measurement, analysis, diagnose_change, flora, patient_pathology]', id: 1}
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-pk']


class CaseFlora(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='floras')
    flora = models.ForeignKey(Flora, on_delete=models.CASCADE)


# реалізувати через event ?
# class CasePathology(models.Model):
#     case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='patient_pathologies')
#     patient_pathology = models.ForeignKey(PatientPathology, on_delete=models.CASCADE)


class Analysis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='analysis')
    data = JSONField()

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)


class Prescription(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=256)
    reaction = models.CharField(max_length=256)


class Measurement(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    data = JSONField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


# class EventComment(models.Model):
#     comment = models.TextField()
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.comment


"""
 + Вакцинації поки забрати
    (Лишити на перспективу, але поки забрати)

+ Показники стану пацієнта (об'єднати вагу і тд в одну штуку так само в Джейсон)
    Тип + таблиці з данами. Краще підвязати динаміку до кейсу, а не до пацієнта.

(обговорити) Чойсом добавити вибір розмірності

(обговорити) Патології об'єднати з хворобами , так як це те саме по суті. Тільки інший тип


(обговорити) Протипоказання зробити проміжною між хворобами і медикаментами менітумені

+ Реакція на лікування в прекрипшін. Зв'язок є через хвороби. 

+ Флора повинна впливати на мадекамент менітумені.

+ Івент підвязати до лікаря. Якщо потрібно консультація.

+ Перекинути лікаря з кейсу в івенти. (Додали до івенту)

+ Прескрипшин, аналізи і діагноз до івенту а не до кейсу. Бо прив'язка до лікаря.

+++ Зробити трошки з назвами для кращого розуміння.



/*Переробити патологію на алергію, з реакцією на препарати і тд*/ це вже закоментовано, не дивитися
"""
