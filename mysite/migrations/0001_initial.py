# Generated by Django 2.0.3 on 2018-03-27 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(blank=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_no', models.IntegerField(null=True)),
                ('stop_no', models.IntegerField(null=True)),
                ('airline_id', models.CharField(blank=True, max_length=4)),
                ('src_airport', models.CharField(blank=True, max_length=4)),
                ('dst_airport', models.CharField(blank=True, max_length=4)),
                ('num_of_seats', models.IntegerField(null=True)),
                ('num_of_stops', models.IntegerField(null=True)),
                ('src_time', models.TimeField(null=True)),
                ('dst_time', models.TimeField(null=True)),
                ('arrive_day', models.IntegerField(null=True)),
                ('working_days', models.CharField(blank=True, max_length=40)),
                ('fare', models.FloatField(null=True)),
                ('fare_restriction', models.CharField(blank=True, max_length=40)),
                ('status', models.CharField(blank=True, max_length=10)),
            ],
        ),
    ]
