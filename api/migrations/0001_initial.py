# Generated by Django 3.0.5 on 2020-04-23 12:36

from django.db import migrations, models
import django.db.models.deletion
from core.utils.timezone import local_today


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RouteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('distance', models.FloatField(default=0)),
                ('local_date', models.DateField(default=local_today)),
            ],
            options={
                'db_table': 'route_routes',
            },
        ),
        migrations.CreateModel(
            name='LongestRouteModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('route_date', models.DateField(unique=True)),
                ('route', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.RouteModel')),
            ],
            options={
                'db_table': 'route_longest_route',
            },
        ),
        migrations.CreateModel(
            name='CoordinatesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lat', models.DecimalField(decimal_places=8, max_digits=10)),
                ('lon', models.DecimalField(decimal_places=8, max_digits=11)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coordinates', to='api.RouteModel')),
            ],
            options={
                'db_table': 'route_coordinates',
                'ordering': ['created_at'],
            },
        ),
    ]