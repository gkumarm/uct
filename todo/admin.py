from django.contrib import admin

# Register your models here.
from .models import Context, TodoType

admin.site.register (Context)
admin.site.register (TodoType)

admin.site.site_header = 'UCT TODO'
admin.site.site_title = 'UCT'
