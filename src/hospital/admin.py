from django.contrib import admin
from .models import Patient, Medicament, Country, Manufacturer, Applicant
# Register your models here.

admin.site.register(Patient)
admin.site.register(Medicament)
admin.site.register(Country)
admin.site.register(Manufacturer)
admin.site.register(Applicant)