# Generated by Django 2.2.2 on 2019-06-15 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair', models.CharField(max_length=10)),
                ('high', models.DecimalField(decimal_places=18, max_digits=21)),
                ('low', models.DecimalField(decimal_places=18, max_digits=21)),
                ('avg', models.DecimalField(decimal_places=18, max_digits=21)),
                ('vol', models.DecimalField(decimal_places=18, max_digits=28)),
                ('vol_cur', models.DecimalField(decimal_places=18, max_digits=28)),
                ('last', models.DecimalField(decimal_places=18, max_digits=21)),
                ('buy', models.DecimalField(decimal_places=18, max_digits=21)),
                ('sell', models.DecimalField(decimal_places=18, max_digits=21)),
                ('updated', models.BigIntegerField()),
            ],
        ),
    ]
