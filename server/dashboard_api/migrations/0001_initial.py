# Generated by Django 4.2.3 on 2023-08-01 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_category', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'device_categories',
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'goals',
            },
        ),
        migrations.CreateModel(
            name='SearchEngine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_engine', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'search_engines',
            },
        ),
        migrations.CreateModel(
            name='SearchPhrase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_phrase', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'search_phrases',
            },
        ),
        migrations.CreateModel(
            name='TrafficSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traffic_source', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'traffic_sources',
            },
        ),
        migrations.CreateModel(
            name='SearchResultsTop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('region_index', models.PositiveIntegerField()),
                ('value', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'search_results_tops',
                'unique_together': {('date', 'region_index')},
            },
        ),
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('visits', models.PositiveIntegerField()),
                ('new_users', models.PositiveIntegerField()),
                ('device_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard_api.devicecategory')),
                ('goal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard_api.goal')),
                ('search_engine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard_api.searchengine')),
                ('search_phrase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard_api.searchphrase')),
                ('traffic_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard_api.trafficsource')),
            ],
            options={
                'db_table': 'visits',
                'unique_together': {('date', 'traffic_source', 'device_category', 'search_engine', 'search_phrase', 'goal')},
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('region_index', models.PositiveIntegerField()),
                ('position', models.PositiveIntegerField()),
                ('search_phrase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard_api.searchphrase')),
            ],
            options={
                'db_table': 'site_positions',
                'unique_together': {('search_phrase', 'date', 'region_index')},
            },
        ),
    ]