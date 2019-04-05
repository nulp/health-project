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
        return self.country + ', ' + self.city + ',' + self.street + ' ' + self.building + '/' + self.apartment


class Patient(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    ssn = models.CharField(max_length=9, unique=True)
    birthday = models.DateField()
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non_binary')
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class PatientWeight(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    value = models.DecimalField(max_digits=10, decimal_places=3)


class PatientPreasure(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    value_up = models.IntegerField()
    value_low = models.IntegerField()


class PatientPulse(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    value = models.IntegerField()


class DoctorSpeciality(models.Model):
    specialty = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = 'Doctors specialties'


class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    specialty = models.ForeignKey(DoctorSpeciality, on_delete=models.CASCADE)

    certification_CHOICES = (
        ('A', 'American Board'),
        ('B', 'Bachelor'),
    )
    certification = models.CharField(max_length=30, choices=certification_CHOICES)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


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
    uk_name = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.uk_name


class Manufacturer(models.Model):
    uk_name = models.CharField(max_length=250)
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

    MNN_CHOICES = (
        ('M', 'Моно'),
        ('C', 'Комбінований'),
        ('N', 'Без МНН')
    )

    mnn = models.CharField(max_length=1, choices=MNN_CHOICES)
    issuance = models.BooleanField()
    farm_group = models.ManyToManyField('FarmGroup')
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.uk_name


# class Department(models.Model):
#     name = models.CharField(max_length=50)
#     director = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
#     staff = models.ManyToManyField(User, related_name='+')

#     def __str__(self):
#         return self.name

class Disease(models.Model):
    name = models.CharField(max_length=250)


class Vaccine(models.Model):
    name = models.CharField(max_length=100)
    live = models.NullBooleanField()
    absorved = models.NullBooleanField()
    inactivated = models.NullBooleanField()
    oral = models.NullBooleanField()

    def __str__(self):
        return self.name


class VaccineApplied(models.Model):
    date = models.DateTimeField()
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return '%s | by (%s)' % (self.patient, self.date)


class Diagnoses(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    valid = models.BooleanField(default=True)


class Pathologie(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class PatientPathologie(models.Model):
    pathologie = models.ForeignKey(Pathologie, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    permanent = models.BooleanField(default=None, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Flora(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Case(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comment = models.TextField()
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=True)


class CaseDiagnos(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    diagnos = models.ForeignKey(Diagnoses, on_delete=models.CASCADE)


class CaseFlora(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    flora = models.ForeignKey(Flora, on_delete=models.CASCADE)


class CasePathologie(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    pathologie = models.ForeignKey(Pathologie, on_delete=models.CASCADE)


class Analysis(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=True)
    data = JSONField()


class Prescription(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantity = models.TextField()


class Event(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    data = JSONField()


class EventComment(models.Model):
    comment = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
