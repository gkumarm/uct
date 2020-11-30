from django.contrib import admin

# Register your models here.
from .models import Todo, Resource

admin.site.register (Todo)
admin.site.register (Resource)