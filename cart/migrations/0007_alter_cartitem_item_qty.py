# Generated by Django 4.0.6 on 2022-07-25 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_cartitem_user_alter_cartitem_item_qty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='item_qty',
            field=models.IntegerField(default=0),
        ),
    ]
