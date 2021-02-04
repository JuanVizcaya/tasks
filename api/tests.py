from django.test import TestCase
from django.shortcuts import get_object_or_404

from api.models import Task
from api.serializers import TaskSerializer

queryset = Task.objects.all()
task = get_object_or_404(queryset, pk=1)
data =  {'id': 1, 'descripcion': 'Correr', 'tiempo_estimado': 0, 'tiempo_registrado': 0, 'estatus': 'completada'}
serialized_data = TaskSerializer(task, data)
