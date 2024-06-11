from django.db import models

class Facultad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70)

class ProgAcad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
