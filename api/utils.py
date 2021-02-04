from random import choice
from django.utils import timezone


class RandomChoiceUtils:
    """ Objeto con métodos estáticos con funcionalidad de aleatoriedad """
    @staticmethod
    def timedelta(n_days=7):
        """ Método de timedelta aleatorio
        Returns:
            [timedelta]: timedelta para restar a un objeto tipo datetime
        """
        days = choice(range(n_days))
        hours = choice(range(24))
        minutes = choice(range(60))
        return timezone.timedelta(days=days, hours=hours, minutes=minutes)

    @staticmethod
    def minutes(min_mins=5, max_mins=120):
        """ Método para elección de minutos aleatoriamente
        Returns:
            [int]: Cantidad aleatoria de minutos.
        """
        return choice(range(min_mins, max_mins+1))

    @staticmethod
    def percent(min_percent=80, max_percent=100):
        """ Método para elección de minutos aleatoriamente
        Returns:
            [float]: Porcentaje aletorio.
        """
        return choice(range(min_percent, max_percent+1)) / 100


def set_dummy(tasks):
    """ Preparación de la dummy-data (Proceso para cada "Task"):
        a) Si no contiene "actualización" y/o "creacion"
            1. Tarea finalizada dentro de últimos 7 días (aleatorio).
            2. Tarea creada dentro de los 5 días anteriores a su finalización (aleatorio).
        b) Si no contiene "tiempo_estimado" y/o "tiempo_registrado"
            3. Tiempo estimado entre 5 y 120 minutos (aleatorio).
            4. Tiempo registrado entre el 80% y 100% del tiempo estimado (aleatorio).
        c) Si no contiene "estatus"
            5. Estatus "completada"
    Args:
        tasks (OrderedDict): Diccionario ordenado con el listado de las tareas dummy.
    Returns:
        [OrderedDict]: Tareas dummy editadas con los parámetros descritos más arriba.
    """
    rand = RandomChoiceUtils()
    for task in tasks:
        if not task.get('actualizacion') or not task.get('creacion'):
            task['actualizacion'] = timezone.now() - rand.timedelta()
            task['creacion'] = task['actualizacion'] - rand.timedelta(5)
        if not task.get('tiempo_estimado') or not task.get('tiempo_registrado'):
            task['tiempo_estimado'] = rand.minutes()
            task['tiempo_registrado'] = int(task['tiempo_estimado'] * rand.percent())
        if not task.get('estatus'):
            task['estatus'] = 'completada'
    return tasks