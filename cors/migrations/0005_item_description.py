# Generated by Django 3.0 on 2019-12-06 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cors', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='new discription'),
            preserve_default=False,
        ),
    ]
