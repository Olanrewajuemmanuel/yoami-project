# Generated by Django 4.0.6 on 2022-07-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('HW', 'HEADWEAR'), ('APPA', 'APPARELS'), ('TOYS', 'TOYS'), ('PROPS', 'PROPS'), ('OTH', 'OTHERS')], default='OTHERS', max_length=5),
        ),
    ]
