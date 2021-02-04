from django.db import models
from django.utils import timezone


class TaskManager(models.Manager):
    """ TaskManager para búsqueda de tareas por descripción o estatus """
    def search(self, query=None, order_by=None):
        """ Método para búsqueda de tareas
        Args:
            query (string): cadena de texto que será buscada dentro de los campos
            "descripción" y "estatus".
        Returns:
            queryset: queryset que contiene los elementos coincidentes
            con la búsqueda solicitada solicitada.
        """
        qs = self.get_queryset()
        if query:
            lookup = (models.Q(descripcion__icontains=query) | models.Q(estatus__icontains=query))
            qs = qs.filter(lookup).distinct()
        return qs.order_by(order_by)


class Task(models.Model):
    class Meta:
        verbose_name = "Tarea"
    creacion = models.DateTimeField(verbose_name="Fecha de creación", default=timezone.now)
    actualizacion = models.DateTimeField(verbose_name="Fecha de actualización", default=timezone.now)
    descripcion = models.CharField(verbose_name="Descripción", max_length=100)
    tiempo_estimado = models.IntegerField(verbose_name="Duración estimada (min)", default=0)
    tiempo_registrado = models.IntegerField(verbose_name="Tiempo registrado (min)", default=0)
    estatus = models.CharField(
        verbose_name="Estatus",
        max_length=10,
        choices=(('pendiente', "pendiente"), ('completada', "completada")),
        default='pendiente'
        )

    objects = TaskManager()

    def __str__(self):
        return f'{self.descripcion}'