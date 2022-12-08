# Generated by Django 3.1.12 on 2022-04-13 23:04

import algoritmosApp.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('departamentId', models.AutoField(primary_key=True, serialize=False)),
                ('departamentName', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Graphs',
            fields=[
                ('grafoId', models.AutoField(primary_key=True, serialize=False)),
                ('grafoName', models.CharField(max_length=50, null=True)),
                ('nodes', djongo.models.fields.ArrayField(default=[], model_container=algoritmosApp.models.Nodes, null=True)),
                ('links', djongo.models.fields.ArrayField(default=[], model_container=algoritmosApp.models.Links, null=True)),
            ],
        ),
    ]
