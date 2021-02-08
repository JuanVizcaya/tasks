from django.test import TestCase
from api.models import Task


class APITests(TestCase):
    """  Test unitarios para la API de Tareas """

    def setUp(self):
        """ Preparación de objeto para hacer tests """
        self.dummy_task = Task.objects.create(
            descripcion='api test',
            tiempo_estimado=5
        )

    def test_api_create_json(self):
        """ Test Método Create - JSON:
        a) Prueba que la api responda correctamente a una peticion CREATE
        en formato JSON, verificando su status_code.
        b) Verifica que se haya creado un nuevo objeto en el modelo de base de datos.
        """
        response = self.client.post('/api/tasks/',
        {'descripcion': 'test create json', 'tiempo_estimado': 1},
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)

    def test_api_create_xml(self):
        """ Test Método Create - XML:
        a) Prueba que la api responda correctamente a una peticion CREATE
        en formato XML, verificando su status_code.
        b) Verifica que se haya creado un nuevo objeto en el modelo de base de datos.
        """
        response = self.client.post('/api/tasks/',
        '''<content>
            <descripcion>test create xml</descripcion>
            <tiempo_estimado>1</tiempo_estimado>
        </content>''',
        content_type='text/xml', accept='text/xml')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)

    def test_api_retrieve(self):
        """ Test Método Retrieve:
        a) Prueba que la api responda correctamente a una peticion RETRIEVE,
        verificando su status_code.
        b) Verifica que la tarea recibida en la respuesta, sea la que se requisitó por su ID.
        """
        response = self.client.get(f'/api/tasks/{self.dummy_task.id}/')
        self.assertEqual(response.status_code, 200)
        descripcion = response.json()['descripcion']
        self.assertEqual(self.dummy_task.descripcion, descripcion)

    def test_api_update(self):
        """ Test Método Update:
        a) Prueba que la api responda correctamente a una peticion UPDATE,
        verificando su status_code.
        b) Verifica que la tarea actualizada, se vea reflejada en el modelo de base de datos.
        c) Comprueba que no sea posible actualizar una tarea con estatus de "completada".
        """
        nueva_descripcion = 'api test updated'
        response = self.client.put(f'/api/tasks/{self.dummy_task.id}/',
            {'descripcion': nueva_descripcion, 'tiempo_registrado': 1, 'estatus': 'completada'},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        descripcion = response.json()['descripcion']
        db_task = Task.objects.get(id=self.dummy_task.id)
        self.assertEqual(descripcion, db_task.descripcion)
        self.assertEqual(descripcion, nueva_descripcion)
        response_2 = self.client.put(f'/api/tasks/{self.dummy_task.id}/',
            {'descripcion': 'api test updated - actualizar completada'},
            content_type='application/json')
        self.assertEquals(response_2.status_code, 403)

    def test_api_list(self):
        """ Test Método List:
        a) Prueba que la api responda correctamente a una peticion LIST,
        verificando su status_code.
        b) Verifica que la primera tarea recibida en la respuesta,
        sea la misma que la primera en la base de datos.
        c) Comprueba que la cantidad de elementos regresados,
        sea igual a la cantidad de elementos en el modelo de la base de datos.
        """
        response = self.client.get(f'/api/tasks/')
        self.assertEqual(response.status_code, 200)
        tasks_list = response.json()
        id_task = tasks_list[0]['id']
        self.assertEqual(self.dummy_task.id, id_task)
        self.assertEqual(Task.objects.count(), len(tasks_list))

    def test_api_destroy(self):
        """ Test Método Destroy:
        a) Prueba que la api responda correctamente a una peticion DESTROY,
        verificando su status_code.
        b) Verifica que la tarea eliminada, ya no se encuentre en el modelo de base de datos.
        """
        response = self.client.delete(f'/api/tasks/{self.dummy_task.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)

