# Generated by Django 2.2 on 2019-05-14 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='doctor', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]