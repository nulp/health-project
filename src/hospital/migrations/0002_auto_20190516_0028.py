# Generated by Django 2.1.2 on 2019-05-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='uk_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='uk_name',
            field=models.CharField(max_length=500),
        ),
    ]