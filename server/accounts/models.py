from django.db import models
from django.contrib.auth.models import AbstractUser
from prog_acad.models import ProgAcad, Facultad

ROLES = [
    ('tesista', 'Tesista'),
    ('asesor', 'Asesor'),
    ('jurado', 'Jurado'),
    ('coordinador', 'Coordinador'),
    ('sec_coord', 'Secretaria de Coordinacion'),
    ('decana', 'Decana'),
    ('sec_facultad', 'Secretaria de Facultad'),
]

class Usuario(AbstractUser):
    prog_acad = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, null=True, blank=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=True, blank=True)
    dni = models.CharField(max_length=8)
    role = models.CharField(max_length=30, choices=ROLES, default='tesista')
    genero = models.BooleanField(default=True)
    telefono = models.CharField(max_length=9)
