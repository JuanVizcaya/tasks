from django.shortcuts import get_object_or_404, redirect

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_xml.parsers import XMLParser

from django.conf import settings
from api.models import Task
from api.serializers import TaskSerializer
from api.utils import set_dummy

# Valor del header "Accept" para respuesta XML
XMLRenderer.media_type = settings.XML_MEDIA_TYPE
# Valor del header "Content-Type" para respuesta XML
XMLParser.media_type = settings.XML_MEDIA_TYPE


class FillDummyAPI(APIView):
    """ API para el llenado de dummy-data en la base de datos """
    renderer_classes = (JSONRenderer, XMLRenderer)
    parser_classes = (JSONParser, XMLParser)

    def post(self, request):
        serialized_data = TaskSerializer(data=request.data, many=True)
        if serialized_data.is_valid():
            # Preparación de la información faltante.
            set_dummy(serialized_data.validated_data)
            serialized_data.save()
            return Response(serialized_data.data, status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status.HTTP_400_BAD_REQUEST)


class SearchTaskAPI(APIView):
    """ API para la petición de búsqueda de tareas por descripción y/o estatus """
    renderer_classes = (JSONRenderer, XMLRenderer)
    parser_classes = (JSONParser, XMLParser)

    def get(self, request):
        if 'q' not in request.query_params:
            return Response({'error': 'Parámetros insuficientes', 'q': 'Requerido'},
                            status=status.HTTP_400_BAD_REQUEST)
        q = request.query_params.get('q')
        order_by = 'id'

        if 'orderby' in request.query_params: # Si se pide ordenamiento
            order_by = request.query_params.get('orderby')
            order_choices = ['creacion', 'actualizacion', 'descripcion',
                            'tiempo_estimado', 'tiempo_registrado', 'estatus']

            if not order_by in order_choices: # valida opción
                return Response({'error': f'[{order_by}] Valor inválido',
                                'orderby': 'opciones: creacion, actualizacion, descripcion, tiempo_estimado, tiempo_registrado, estatus'},
                                status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.search(q, order_by)

        serialized_data = TaskSerializer(tasks, many=True)
        return Response({'results': serialized_data.data})


class TaskViewSet(viewsets.ViewSet):
    """ API para gestión de tareas. """
    renderer_classes = (JSONRenderer, XMLRenderer)
    parser_classes = (JSONParser, XMLParser)

    def list(self, request):
        """ (GET): Regresa todos los elementos en forma de lista (JSON/XML). """
        queryset = Task.objects.all()
        serialized_data = TaskSerializer(queryset, many=True)
        return Response(serialized_data.data)

    def create(self, request):
        """ (POST): Crea una nueva tarea en el modelo de base de datos. """
        if not request.data.get('tiempo_estimado'):
            return Response({"tiempo_estimado": ["Este campo es requerido."]},
            status.HTTP_400_BAD_REQUEST)

        serialized_data = TaskSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save_new()
            return Response(serialized_data.data, status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ (GET): Regresa el elemento solicitado mediante su ID.
        Args:
            pk (int, optional): ID de la tarea a retornar.
        Returns:
            Response: Respuesta en el formato requerido por el header "Accept"
        """
        try:
            queryset = Task.objects.all()
            task = get_object_or_404(queryset, pk=pk)
        except ValueError:
            return Response({'detail': "El id debe ser un entero."},
                status.HTTP_400_BAD_REQUEST)
        serialized_data = TaskSerializer(task)
        return Response(serialized_data.data)

    def update(self, request, pk=None):
        """ (PUT): Actualiza el elemento solicitado mediante su ID.
        Args:
            pk (int, optional): ID de la tarea a actualizar.
        Returns:
            Response: Respuesta en el formato requerido por el header "Accept"
        """
        try:
            queryset = Task.objects.all()
            task = get_object_or_404(queryset, pk=pk)
        except ValueError:
            return Response({'detail': "El id debe ser un entero."},
                status.HTTP_400_BAD_REQUEST)
        # Validaciones
        serialized_data = TaskSerializer(task, data=request.data, partial=True)
        if serialized_data.is_valid():
            if task.estatus == 'completada': # No actualiza si el estatus es "completada"
                return Response({'estatus': "La tarea ya ha sido completada."},
                                status.HTTP_403_FORBIDDEN)
            serialized_data.save_updated()
            return Response(serialized_data.data) # Tarea actualizada.

        return Response(serialized_data.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ (DELETE): Elimina el elemento solicitado mediante su ID.
        Args:
            pk (int, optional): ID de la tarea a eliminar.
        Returns:
            Response: Respuesta en el formato requerido por el header "Accept".
        """
        try:
            queryset = Task.objects.all()
            task = get_object_or_404(queryset, pk=pk)
        except ValueError:
            return Response({'detail': "El id debe ser un entero."},
                status.HTTP_400_BAD_REQUEST)
        delete_response = task.delete()
        return Response({'id': pk,'estatus': 'eliminada'}, status.HTTP_204_NO_CONTENT)


def redirect_view(request):
    response = redirect('/admin/')
    return response