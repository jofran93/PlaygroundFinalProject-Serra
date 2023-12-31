# Generated by Django 4.2.6 on 2023-11-30 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TuFeriaCL', '0004_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255, null=True)),
                ('link', models.URLField(max_length=100, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatares/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
