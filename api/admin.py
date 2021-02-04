from django.contrib import admin

from api.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """ Se agregan las tareas al panel de administración """
    list_display = ('id' ,'descripcion', 'estatus')
    search_fields = ('descripcion', 'estatus')
