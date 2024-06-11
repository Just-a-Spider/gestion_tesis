from django.db import models
from accounts.models import Usuario

class PropuestaTesis(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    docu = models.FileField(upload_to='propuestas/', null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    tesista = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - ' + self.tesista.username

class Tesis(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    linea = models.CharField(max_length=100)
    docu = models.FileField(upload_to='tesis/')
    tesista = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='tesista_id'
    )
    asesor = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='asesor_id'
    )
    jurado1 = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='jurado1_id'
    )
    jurado2 = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='jurado2_id'
    )
    jurado3 = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='jurado3_id'
    )

class Observacion(models.Model):
    id = models.AutoField(primary_key=True)
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
    escrita_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    observacion = models.TextField()
    estado = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)
