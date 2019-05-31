from django.contrib import admin
from .models import Patient, Doctor, DoctorSpeciality, Case, Medicament, Country, Manufacturer, Applicant
# Register your models here.

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(DoctorSpeciality)
admin.site.register(Case)

admin.site.register(Medicament)
admin.site.register(Country)
admin.site.register(Manufacturer)
admin.site.register(Applicant)
