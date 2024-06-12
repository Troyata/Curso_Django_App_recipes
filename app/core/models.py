"""
Database models

"""
import uuid
import os

from django.conf import settings
from django.db import models  #type: ignore
from django.contrib.auth.models import (  #type: ignore
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

def recipe_image_file_path(instance, filename):
    """Generate image file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)



class UserManager(BaseUserManager):
    """ Manager for users. """

    def create_user(self, email, password=None, **extra_fields):
        """ create, save and return new users. Dejamos el pwd en None 
         porque para desarrollo es util. Al fin y al cabo estas creando
         un usuario sin contraseña por lo que será un usuario inutilizable
         Por otro lado, extrafields te da flexibilidad puesto que puedes pasar
         otros argumentos sin necesidad de especificarlos desde el ppio. Util
         por si hay cambios."""
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        """ El set password se encarga de criptografíar el pass para almacenaje en BBDD"""
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password):
        ''' Create a new superuser '''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
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

class Recipe(models.Model):
    """Recipe Object. """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Ingredients for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name