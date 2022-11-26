from django.conf import settings
from django.contrib.auth.models import Group
from django.db import migrations

def create_system_admin_group(apps, schema_editor):
    Group.objects.create(name=settings.SYSTEM_ADMIN_GROUP)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_system_admin_group)
    ]
