from django.contrib import admin

# Register your models here.
from .models import Context, TodoType, TodoStatus

admin.site.register (Context)
admin.site.register (TodoType)
admin.site.register (TodoStatus)

admin.site.site_header = 'UCT TODO'
admin.site.site_title = 'UCT'
