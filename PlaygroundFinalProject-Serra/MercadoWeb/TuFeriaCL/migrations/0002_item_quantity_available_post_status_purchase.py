# Generated by Django 4.2.6 on 2023-11-25 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TuFeriaCL', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity_available',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(default='available', max_length=20),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TuFeriaCL.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TuFeriaCL.userprofile')),
            ],
        ),
    ]
