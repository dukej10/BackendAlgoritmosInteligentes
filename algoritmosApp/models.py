#from django.db import models
from email.policy import default
from tkinter import Y
from djongo import models

# Create your models here.


class Coordenates(models.Model):
    x = models.IntegerField(null=False)
    Y = models.IntegerField(null=False)

    class Meta:
        abstract = True


class Nodes(models.Model):
    id = models.IntegerField(null=False)
    name = models.CharField(max_length=25)
    label = models.CharField(max_length=20)
    data = models.CharField(max_length=20, default="{}")
    type = models.CharField(max_length=20, default="")
    radius = models.FloatField(null=False, default=30)
    coordenates = models.EmbeddedField(
        model_container=Coordenates, default=None
    )

    class Meta:
        abstract = True


class Links(models.Model):
    source = models.IntegerField(null=False)
    target = models.IntegerField(null=False)
    distance = models.IntegerField(null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.source)


class Graphs(models.Model):
    grafoId = models.AutoField(primary_key=True)
    grafoName = models.CharField(max_length=50, null=True)
    nodes = models.ArrayField(
        model_container=Nodes, null=True, default=[]
    )
    links = models.ArrayField(
        model_container=Links, null=True, default=[]
    )
