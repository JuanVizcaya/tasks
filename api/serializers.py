from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail

from api.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'creacion', 'actualizacion', 'descripcion', 'tiempo_estimado', 'tiempo_registrado', 'estatus')

    def save_updated(self, *args, **kwargs):
        # Se registra la fecha y hora de actualización antes de salvar
        self.validated_data['actualizacion'] = timezone.now()
        super(TaskSerializer, self).save(*args, **kwargs)

    def save_new(self, *args, **kwargs):
        # Se ignoran parámetos != ('descripcion', 'tiempo_estimado')
        for key in self.validated_data.keys():
            if key not in ('descripcion', 'tiempo_estimado'):
                del self.validated_data[key]
        super(TaskSerializer, self).save(*args, **kwargs)

