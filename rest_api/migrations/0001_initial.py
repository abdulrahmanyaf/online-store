# Generated by Django 4.1.3 on 2022-11-25 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('can_access_product_category', 'Can access product categories'), ('can_access_product', 'Can access products')),
                'managed': False,
            },
        ),
    ]
