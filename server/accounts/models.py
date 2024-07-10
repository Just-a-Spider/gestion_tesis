from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from prog_acad.models import ProgAcad, Facultad
from django.utils.translation import gettext_lazy as _

#ROLES = [
#    ('tesista', 'Tesista'),
#    ('asesor', 'Asesor'),
#    ('jurado', 'Jurado'),
#    ('coordinador', 'Coordinador'),
#    ('decana', 'Decana'),
#]

class BaseUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    password = models.CharField(_('password'), max_length=128)
    code = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    dni = models.CharField(max_length=8, unique=True)
    genero = models.BooleanField(default=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'code'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.code + ' - ' + self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        help_text=_('Specific permissions for this user.'),
    )

class Tesista(BaseUser):
    prog_acad = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, null=True, blank=True)
    password_changed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Tesista'
        verbose_name_plural = 'Tesistas'

class Profesor(BaseUser):
    prog_acad = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, null=True, blank=True)
    tesis_dirigidas = models.IntegerField(default=0)
    tesis_juradas = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'

class Coordinador(BaseUser):
    prog_acad = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, null=True, blank=True)
    

    class Meta:
        verbose_name = 'Coordinador'
        verbose_name_plural = 'Coordinadores'

class Decana(BaseUser):
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Decano'
        verbose_name_plural = 'Decanos'

#class Usuario(AbstractUser):
#    prog_acad = models.ForeignKey(ProgAcad, on_delete=models.CASCADE, null=True, blank=True)
#    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=True, blank=True)
#    dni = models.CharField(max_length=8)
#    role = models.CharField(max_length=30, choices=ROLES, default='tesista')
#    genero = models.BooleanField(default=True)
#    telefono = models.CharField(max_length=9)
