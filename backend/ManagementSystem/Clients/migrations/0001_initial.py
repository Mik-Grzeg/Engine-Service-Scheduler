# Generated by Django 3.1.5 on 2021-02-24 23:39

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('fuel_type', models.CharField(choices=[('1', 'One'), ('2', 'Two')], max_length=1)),
                ('type', models.CharField(choices=[('2', 'Type 2'), ('3', 'Type 3')], max_length=1)),
                ('start_running', models.DateTimeField(null=True)),
                ('stop_running', models.DateTimeField(blank=True, null=True)),
                ('stopped_till', models.DateTimeField(blank=True, null=True)),
                ('oph', models.FloatField(default=0)),
                ('oph_per_month', models.FloatField()),
                ('interval', models.FloatField()),
                ('general_interval', models.FloatField()),
                ('interval_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('general_cost', models.DecimalField(decimal_places=2, max_digits=11)),
                ('half_general_cost', models.DecimalField(decimal_places=2, max_digits=9)),
                ('six_k_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'set of parts',
                'verbose_name_plural': 'sets of parts',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('1', 'Inspection'), ('2', 'Semi general'), ('3', 'General')], max_length=1)),
                ('date', models.DateField()),
                ('interval', models.FloatField()),
                ('confirmed', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clients.company')),
                ('engine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Clients.engine')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=50)),
                ('units_in_stock', models.PositiveIntegerField()),
                ('parent_category', models.CharField(max_length=300)),
                ('set_of_parts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clients.parts')),
            ],
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installation_name', models.CharField(max_length=200)),
                ('installation_location', models.CharField(max_length=300)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clients.company')),
            ],
        ),
        migrations.AddField(
            model_name='engine',
            name='installation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Clients.installation'),
        ),
        migrations.AddField(
            model_name='engine',
            name='parts',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Clients.parts'),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_start', models.DateField()),
                ('contract_end', models.DateField()),
                ('date_of_signing', models.DateField()),
                ('price_per_hour', models.FloatField()),
                ('oph_yet', models.FloatField(default=0)),
                ('annotation', models.TextField(blank=True, null=True)),
                ('installation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Clients.installation')),
            ],
        ),
    ]