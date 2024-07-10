from django.db import models

class Facultad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'

class ProgAcad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' - ' + self.facultad.nombre
    
    class Meta:
        verbose_name = 'Programa Académico'
        verbose_name_plural = 'Programas Académicos'
