# Generated by Django 3.0 on 2019-12-06 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cors', '0003_item_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
