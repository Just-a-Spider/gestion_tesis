from django.db import models
from accounts.models import *
from server.uuid_model import UUID_Model

class PropuestaTesis(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    docu = models.FileField(upload_to='propuestas/', null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    tesista = models.ForeignKey(Tesista, on_delete=models.CASCADE)
    posible_asesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.BooleanField(default=False) # False: Pendiente, True: Aceptada

    def __str__(self):
        return self.titulo + ' - ' + self.tesista.username
    
    class Meta:
        ordering = ['fecha']
        verbose_name = 'Propuesta de Tesis'
        verbose_name_plural = 'Propuestas de Tesis'

#-------------------------- PARA LA TESIS --------------------------#
class Tesis(UUID_Model):
    titulo = models.CharField(max_length=200)
    linea = models.CharField(max_length=100)
    docu = models.FileField(upload_to='tesis/', null=True, blank=True)
    enlace = models.URLField(null=True, blank=True)
    tesista = models.ForeignKey(
        Tesista, 
        on_delete=models.CASCADE, 
        related_name='tesista_id'
    )
    asesor = models.ForeignKey(
        Profesor, 
        on_delete=models.CASCADE, 
        related_name='asesor_id'
    )
    jurado1 = models.ForeignKey(
        Profesor, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='jurado1_id'
    )
    jurado2 = models.ForeignKey(
        Profesor, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='jurado2_id'
    )
    jurado3 = models.ForeignKey(
        Profesor, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='jurado3_id'
    )
    fecha = models.DateField(auto_now_add=True)
    fecha_presentacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo + ' - ' + self.tesista.username
    
    class Meta:
        ordering = ['fecha']
        verbose_name = 'Tesis'
        verbose_name_plural = 'Tesis'
# Lote 1
class Causas(UUID_Model):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    desc = models.TextField()

class Consecuencias(UUID_Model):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    desc = models.TextField()

class Aportes(UUID_Model):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    desc = models.TextField()

# Lote 2
class Variables(UUID_Model):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    nombre_var = models.CharField(max_length=150)
    tipo_var = models.CharField(max_length=150)
    just = models.TextField()
    
class ObjetivosEsp(UUID_Model):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    desc = models.TextField()

class HipotesisEsp(UUID_Model):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    desc = models.TextField()

#-------------------------- PARA LAS OBSERVACIONES --------------------------#
class Observacion(models.Model):
    id = models.AutoField(primary_key=True)
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    escrita_por = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    observacion = models.TextField()
    estado = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.escrita_por.username + ' - ' + self.tesis.titulo
    
    class Meta:
        ordering = ['fecha']
        verbose_name = 'Observacion'
        verbose_name_plural = 'Observaciones'
