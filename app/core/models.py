"""
Database models

"""

from django.db import models  #type: ignore
from django.contrib.auth.models import (  #type: ignore
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """ Manager for users. """

    def create_user(self, email, password=None, **extra_fields):
        """ create, save and return new users. Dejamos el pwd en None 
         porque para desarrollo es util. Al fin y al cabo estas creando
         un usuario sin contraseña por lo que será un usuario inutilizable
         Por otro lado, extrafields te da flexibilidad puesto que puedes pasar
         otros argumentos sin necesidad de especificarlos desde el ppio. Util
         por si hay cambios."""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        """ El set password se encarga de criptografíar el pass para almacenaje en BBDD"""
        user.save(using=self._db)
        
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system
     AbstractBaseUser incluye todas las funcionalidades para loggearse
      pero no incluye campos. Permissions mixins más de los mismo
       por eso definimos los campos del modelo aquí. """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    """ Es la manera de decirle al programa cual será el valor que utilzaremos 
    para authentication"""
    USERNAME_FIELD = 'email'