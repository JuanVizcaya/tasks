from django.db import models

class Task(models.Model):
    
    class Meta:
        verbose_name = "Tarea"
    
    description = models.CharField(verbose_name="Descripción", max_lenth=100)
    estimated_duration = models.DurationField(verbose_name="Duración estimada")
    registred_duration = models.DurationField(verbose_name="Tiempo registrado")
    status = models.CharField(
        verbose_name="Estatus",
        max_length=10,
        choices=(('pending', "Pendiente"), ('completed', "Completada"))
        )
    
    def __str__(self):
        return f'{self.description}'
    
    def save(self, *args, **kwargs):
        """Method that saves instances in database
        Raises:
            Exception: Raises an exception if the task has been already
            completed and someone is trying to update it.
        """
        if self.estatus == 'completed':
            raise Exception("The task can not be updated")
        super(Task, self).save(*args, **kwargs)