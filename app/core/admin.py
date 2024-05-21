"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  
from django.utils.translation import gettext_lazy as _
""" # le cambiamos el nombre por que queremos utilizar UserAdmin y 
para no crear conflictos entre la clase y la administración
La lines de translation es una buena práctica para que, en caso 
de necesitar traducir la app se pueda hacer sin esfuerzo y ya tengamos todo
preparado. En este proyecto no lo vamos a utilizar """
from core import models

class UserAdmin(BaseUserAdmin):
    """ Define de admin pages for users  """
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email','password')}),
        (
            _('Permissions'),
            {
                'fields' : (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        
        }),
    )

admin.site.register(models.User, UserAdmin)
