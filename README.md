# API - Gestión de Tareas

Es una app *django/django_restframework*, que tiene como función principal la administración de __tareas__.
Con esta API, se pueden ,`crear`, `editar`, `eliminar`, `elistar`, `buscar` y `prellenar` tareas en una base de datos mediante servicios `REST`.
Puede responder con solicitudes `JSON` y `XML`.


<div id='id0'/>

## Índice

[1.](#id1) __Instalación__
  - [Requisitos](#id11)
  - [Guía](#id12)

[2.](#id2) __Utilización__
  - [Panel de Administración](#id21)
  - [Endpoint](#id22)
  - [Media Types](#id23)
  - [Tabla de Métodos](#id24)

[3.-](#id3) __Métodos__
  - [Create](#id31)
  - [Retrieve](#id32)
  - [Update](#id33)
  - [Fill dummy](#id35)
  - [Search](#id36)
  - [List](#id37)
  - [Destroy](#id34)

[4.-](#id4) __Tests__
  - [Tests unitarios](#id41)


<div id='id1' />

## Instalación

<div id='id11' />

#### Requisitos
- Docker

<div id='id12' />

#### Guía

- Clonar proyecto:

`git clone https://github.com/JuanVizcaya/tasks.git`

- Entrar a la carpeta "tasks":

`cd tasks`

- Construir los contenedores:

`docker-compose up --build`

- Hacer migraciones a la base de datos:

`docker exec -it django_app sh -c "python /code/manage.py makemigrations"`

`docker exec -it django_app sh -c "python /code/manage.py makemigrations api"`

`docker exec -it django_app sh -c "python /code/manage.py migrate"`

- Crear super usuario para la administración:

`docker exec -it django_app sh -c "python /code/manage.py createsuperuser"`

[Volver al índice](#id0)

<div id='id2' />

## Utilización

<div id='id21' />

### Panel de Administración
Se podrá acceder al panel de administración con las credenciales ingresadas al crear el super usuario.
`URL: http://localhost:5001/`

<div id='id22' />

#### Endpoint
`URL: http://localhost:5001/api/tasks/`

<div id='id23' />

#### Media Types
- JSON   `application/json`
- XML   `text/xml`

<div id='id24' />

#### Tabla de Métodos

| Nombre | Tipo | URL | Accept header | Descripción |
| ------------- | ----------- | ----------- | ----------- | ------------------- |
| **Create** | POST |  `endpoint/`  | application/json  text/xml | Crea una nueva tarea. |
| **Retrieve** | GET |  `endpoint/task_id/`  | application/json  text/xml | Devuelve la tarea solicitada mediente su ID. |
| **Update** | PUT |  `endpoint/task_id/`  | application/json  text/xml | Actualiza la tarea solicitada mediante su ID. |
| **Destroy** | DELETE |  `endpoint/task_id/`  | application/json  text/xml | Elimina la tarea solicitada mediante su ID. |
| **Fill dummy data** | POST |  `endpoint/fill-dummy`  | application/json  text/xml | Llena la base de datos con información ficticia. |
| **Search** | GET |  `endpoint/search`  | application/json  text/xml | Busca tareas que contengan el parámetro de búsqueda "q" dentro de su descripción y/o estatus y ordena los resultados con su parámetro "orderby". |
| **List** | GET | `endpoint/` | application/json  text/xml | Enlista todas las tareas. |

[Volver al índice](#id0)


<div id='id3' />

## Métodos

<div id='id31' />

#### Create - `POST`
Método para crear una nueva tarea en la base de datos.

##### Parámetros

| Nombre | Requerido | Opciones | Default | Descripción |
| ----------- | -----------| ----------- | ----------- | ------------------- |
| **descripcion** | Sí | NA | NA | Descripción de la tarea a crear |
| **tiempo_estimado** | Sí | NA | NA | Tiempo estimado en minutos para realizar la tarea |

##### Consideraciones
- El `tiempo_estimado` debe ser numérico entero.
- Ignorará cualquier parámetro que no sea `descripcion` o `tiempo_estimado`.

##### Ejemplo - `JSON`:
`Header: Accept = application/json`

`POST: http://localhost:5001/api/tasks/`

`body: JSON`
```
{
  "descripcion": "Hacer el README.md",
  "tiempo_estimado": 120
}
```

*Respuesta:*
```
{
  "id": 1,
  "creacion": "2021-02-05T04:22:32.810289-06:00",
  "actualizacion": "2021-02-05T04:22:32.810299-06:00",
  "descripcion": "Hacer el README.md",
  "tiempo_estimado": 120,
  "tiempo_registrado": 0,
  "estatus": "pendiente"
}
```

##### Ejemplo - `XML`:
`Header: Accept = text/xml`

`Header: Content-Type = text/xml`

`POST: http://localhost:5001/api/tasks/`

`body: XML`
```
<content>
    <descripcion>Probar la respuesta XML</descripcion>
    <tiempo_estimado>25</tiempo_estimado>
</content>
```

*Respuesta:*
```
<?xml version="1.0" encoding="utf-8"?>
<root>
    <id>2</id>
    <creacion>2021-02-05T05:23:34.340677-06:00</creacion>
    <actualizacion>2021-02-05T05:23:34.340686-06:00</actualizacion>
    <descripcion>Probar la respuesta XML</descripcion>
    <tiempo_estimado>25</tiempo_estimado>
    <tiempo_registrado>0</tiempo_registrado>
    <estatus>pendiente</estatus>
</root>
```

[Volver al índice](#id0)
***

<div id='id32' />

#### Retrieve - `GET`
Regresa la tarea solicitada al servidor por medio de su `id`.

##### Parámetros

| Nombre | Requerido | Opciones | Default | Descripción |
| ----------- | -----------| ----------- | ----------- | ------------------- |
| **id** | Sí | NA | NA | ID de la tarea solicitada. |

##### Consideraciones
- El __id__ debe ser numérico y existente.

##### Ejemplo - `JSON`:
`Header: Accept = application/json`

`GET: http://localhost:5001/api/tasks/1/`

*Respuesta:*
```
{
  "id": 1,
  "creacion": "2021-02-05T04:22:32.810289-06:00",
  "actualizacion": "2021-02-05T04:22:32.810299-06:00",
  "descripcion": "Hacer el README.md",
  "tiempo_estimado": 120,
  "tiempo_registrado": 0,
  "estatus": "pendiente"
}
```

##### Ejemplo - `XML`:
`Header: Accept = text/xml`

`GET: http://localhost:5001/api/tasks/2/`

*Respuesta:*
```
<?xml version="1.0" encoding="utf-8"?>
<root>
    <id>2</id>
    <creacion>2021-02-05T05:23:34.340677-06:00</creacion>
    <actualizacion>2021-02-05T05:23:34.340686-06:00</actualizacion>
    <descripcion>Probar la respuesta XML</descripcion>
    <tiempo_estimado>25</tiempo_estimado>
    <tiempo_registrado>0</tiempo_registrado>
    <estatus>pendiente</estatus>
</root>
```

[Volver al índice](#id0)
***

<div id='id33' />

#### Update - `PUT`
Actualiza la tarea indicada con el `id`, con los parámetros enviados.

##### Parámetros

| Nombre | Requerido | Opciones | Default | Descripción |
| ----------- | -----------| ----------- | ----------- | ------------------- |
| **id** | Sí | NA | NA | ID de la tarea a editar. |
| **descripcion** | No | NA | NA | Nueva descripción. |
| **tiempo_estimado** | No | NA | NA | Nuevo tiempo estimado, en minutos. |
| **tiempo_registrado** | No | NA | NA | Tiempo registrado que ha tomado la tarea, en minutos. |
| **estatus** | No | pendiente / completada | pendiente | Nuevo estatus de la tarea. |

##### Consideraciones
- El `id` debe ser numérico y existente.
- Una tarea __"completada"__ no puede ser actualizada con la API.
- Para modificar una tarea __"completada"__ se deberá hacer desde el panel de administración `/admin`.
- Se debe enviar al menos un parámetro a demás del `id`.

##### Ejemplo - `JSON`:
`Header: Accept = application/json`

`PUT: http://localhost:5001/api/tasks/1/`

`body: JSON`
```
{
  "descripcion": "Hacer el README.md",
  "tiempo_registrado": 110,
  "estatus": "completada"
}
```

*Respuesta:*
```
{
    "id": 1,
    "creacion": "2021-02-05T04:22:32.810289-06:00",
    "actualizacion": "2021-02-05T06:38:59.296568-06:00",
    "descripcion": "Hacer el README.md",
    "tiempo_estimado": 120,
    "tiempo_registrado": 110,
    "estatus": "completada"
}
```

##### Ejemplo - `XML`:
`Header: Accept = text/xml`

`PUT: http://localhost:5001/api/tasks/2/`

`body: XML`
```
<content>
    <descripcion>Probar la respuesta XML</descripcion>
    <tiempo_registrado>20</tiempo_registrado>
    <estatus>completada</estatus>
</content>
```

*Respuesta:*
```
<?xml version="1.0" encoding="utf-8"?>
<root>
    <id>2</id>
    <creacion>2021-02-05T05:23:34.340677-06:00</creacion>
    <actualizacion>2021-02-05T06:50:43.782621-06:00</actualizacion>
    <descripcion>Probar la respuesta XML</descripcion>
    <tiempo_estimado>25</tiempo_estimado>
    <tiempo_registrado>20</tiempo_registrado>
    <estatus>completada</estatus>
</root>
```

[Volver al índice](#id0)
***

<div id='id35' />

#### Fill Dummy Data - `POST`
Llena las tablas de la base de datos con __dummy data__, enviando un array con las tareas que se quieran precargar, estas tareas son generadas por *default* con el `estatus` de __"completada"__.

##### Parámetros - `[array]`

| Nombre | Requerido | Opciones | Default | Descripción |
| ----------- | -----------| ----------- | ----------- | ------------------- |
| **descripcion** | Sí | NA | NA | Descripción de la tarea a crear |
| **creacion** | No | NA | NA | Descripción de la tarea a crear |
| **actualizacion** | No | NA | NA | Descripción de la tarea a crear |
| **tiempo_estimado** | No | NA | NA | Tiempo estimado en minutos para realizar la tarea |
| **tiempo_registrado** | No | NA | NA | Tiempo registrado que ha tomado la tarea, en minutos. |
| **estatus** | No | pendiente / completada | completada | Nuevo estatus de la tarea. |

##### Consideraciones
- Se *recomienda* enviar `descripcion` y `tiempo_estimado` para cada tarea.
- Es posible enviar todos los parámetros deseados, tomándo en cuenta lo siguiente:

  a) Si no contiene `actualización` y/o `creacion`
    - `actualización` dentro de últimos 7 días (aleatorio).
    - `creacion` dentro de los 5 días anteriores a su `actualización` (aleatorio).

  b) Si no contiene `tiempo_estimado`
    - Tiempo estimado entre __5__ y __120__ minutos (aleatorio).

  c) Si no contiene `tiempo_registrado`
    - Tiempo registrado entre el 80% y 100% del tiempo estimado (aleatorio).

  c) Si no contiene `estatus`
    - `estatus` = __"completada"__.

##### Ejemplo - `JSON`:
`Header: Accept = application/json`

`POST: http://localhost:5001/api/tasks/fill-dummy`

`body: JSON`
```
[
    {
        "descripcion": "Planear API - JSON",
        "tiempo_estimado": 200
    },
    {
        "descripcion": "Programar API - JSON",
        "tiempo_estimado": 240,
        "creacion": "2021-01-30T05:20:09.474743-06:00"
    },
    {
        "descripcion": "Leer Documentación - JSON",
        "tiempo_estimado": 120,
        "creacion": "2021-02-01T19:55:09.474769-06:00",
        "actualizacion": "2021-02-05T07:52:09.474769-06:00"
    },
    {
        "descripcion": "Debuggear APIs - JSON",
        "tiempo_estimado": 90,
        "tiempo_registrado": 89
    },
    {
        "descripcion": "Deployar nuevos servicios - JSON",
        "tiempo_estimado": 200,
        "tiempo_registrado": 15,
        "estatus": "pendiente"
    },
    {
        "descripcion": "Compilar el proyecto viejo",
        "tiempo_estimado": 255,
        "estatus": "pendiente"
    },
    {
        "descripcion": "Completar la documentación",
        "tiempo_estimado": 135,
        "estatus": "pendiente"
    },
    {
        "descripcion": "Realizar las comprobaciones a la data",
        "tiempo_estimado": 75,
        "estatus": "pendiente"
    },
    {
        "id": 24,
        "descripcion": "Hacer más comprensible el código",
        "tiempo_estimado": 270,
        "estatus": "pendiente"
    }
]
```

*Respuesta:*
```
[
    {
        "id": 11,
        "creacion": "2021-02-03T05:51:33.882825-06:00",
        "actualizacion": "2021-02-06T11:26:33.882825-06:00",
        "descripcion": "Planear API - JSON",
        "tiempo_estimado": 200,
        "tiempo_registrado": 174,
        "estatus": "completada"
    },
    {
        "id": 12,
        "creacion": "2021-02-02T12:26:33.882859-06:00",
        "actualizacion": "2021-02-04T18:30:33.882859-06:00",
        "descripcion": "Programar API - JSON",
        "tiempo_estimado": 240,
        "tiempo_registrado": 211,
        "estatus": "completada"
    },
    {
        "id": 13,
        "creacion": "2021-02-01T19:55:09.474769-06:00",
        "actualizacion": "2021-02-05T07:52:09.474769-06:00",
        "descripcion": "Leer Documentación - JSON",
        "tiempo_estimado": 120,
        "tiempo_registrado": 109,
        "estatus": "completada"
    },
    {
        "id": 14,
        "creacion": "2021-02-02T04:50:33.882881-06:00",
        "actualizacion": "2021-02-05T15:51:33.882881-06:00",
        "descripcion": "Debuggear APIs - JSON",
        "tiempo_estimado": 90,
        "tiempo_registrado": 89,
        "estatus": "completada"
    },
    {
        "id": 15,
        "creacion": "2021-02-01T23:23:33.882896-06:00",
        "actualizacion": "2021-02-03T08:00:33.882896-06:00",
        "descripcion": "Deployar nuevos servicios - JSON",
        "tiempo_estimado": 200,
        "tiempo_registrado": 15,
        "estatus": "pendiente"
    }
]
```

##### Ejemplo - `XML`:
`Header: Accept = text/xml`

`Header: Content-Type = text/xml`

`POST: http://localhost:5001/api/tasks/fill-dummy`

`body: XML`
```
<content>
    <list-item>
        <descripcion>Planear API - XML</descripcion>
        <tiempo_estimado>200</tiempo_estimado>
    </list-item>
    <list-item>
        <descripcion>Programar API - XML</descripcion>
        <tiempo_estimado>240</tiempo_estimado>
        <creacion>2021-01-30T05:20:09.474743-06:00</creacion>
    </list-item>
    <list-item>
        <descripcion>Leer Documentación - XML</descripcion>
        <tiempo_estimado>120</tiempo_estimado>
        <creacion>2021-02-01T19:55:09.474769-06:00</creacion>
        <actualizacion>2021-02-05T07:52:09.474769-06:00</actualizacion>
    </list-item>
    <list-item>
        <descripcion>Debuggear APIs - XML</descripcion>
        <tiempo_estimado>90</tiempo_estimado>
        <tiempo_registrado>89</tiempo_registrado>
    </list-item>
    <list-item>
        <descripcion>Deployar nuevos servicios - XML</descripcion>
        <tiempo_estimado>200</tiempo_estimado>
        <tiempo_registrado>15</tiempo_registrado>
        <estatus>pendiente</estatus>
    </list-item>
</content>
```

*Respuesta:*
```
<?xml version="1.0" encoding="utf-8"?>
<root>
    <list-item>
        <id>16</id>
        <creacion>2021-02-04T04:45:16.696550-06:00</creacion>
        <actualizacion>2021-02-04T18:04:16.696550-06:00</actualizacion>
        <descripcion>Planear API - XML</descripcion>
        <tiempo_estimado>200</tiempo_estimado>
        <tiempo_registrado>170</tiempo_registrado>
        <estatus>completada</estatus>
    </list-item>
    <list-item>
        <id>17</id>
        <creacion>2021-01-28T07:19:16.696576-06:00</creacion>
        <actualizacion>2021-01-31T01:34:16.696576-06:00</actualizacion>
        <descripcion>Programar API - XML</descripcion>
        <tiempo_estimado>240</tiempo_estimado>
        <tiempo_registrado>211</tiempo_registrado>
        <estatus>completada</estatus>
    </list-item>
    <list-item>
        <id>18</id>
        <creacion>2021-02-01T19:55:09.474769-06:00</creacion>
        <actualizacion>2021-02-05T07:52:09.474769-06:00</actualizacion>
        <descripcion>Leer Documentación - XML</descripcion>
        <tiempo_estimado>120</tiempo_estimado>
        <tiempo_registrado>100</tiempo_registrado>
        <estatus>completada</estatus>
    </list-item>
    <list-item>
        <id>19</id>
        <creacion>2021-02-02T17:36:16.696594-06:00</creacion>
        <actualizacion>2021-02-05T20:24:16.696594-06:00</actualizacion>
        <descripcion>Debuggear APIs - XML</descripcion>
        <tiempo_estimado>90</tiempo_estimado>
        <tiempo_registrado>89</tiempo_registrado>
        <estatus>completada</estatus>
    </list-item>
    <list-item>
        <id>20</id>
        <creacion>2021-01-30T07:42:16.696607-06:00</creacion>
        <actualizacion>2021-02-03T09:43:16.696607-06:00</actualizacion>
        <descripcion>Deployar nuevos servicios - XML</descripcion>
        <tiempo_estimado>200</tiempo_estimado>
        <tiempo_registrado>15</tiempo_registrado>
        <estatus>pendiente</estatus>
    </list-item>
</root>
```

[Volver al índice](#id0)
***

<div id='id36' />

#### Search - `GET`
Busca las tareas coincidentes con el parámetro `q` indicado.
La búsqueda se realiza sobre los campos `descripcion` y `estatus`.

##### Parámetros

| Nombre | Requerido | Opciones | Default | Descripción |
| ----------- | -----------| ----------- | ----------- | ------------------- |
| **q** | Si | NA | NA | Cadena de texto a buscar. |
| **orderby** | No | *id*, *creacion*, *actualizacion*, *descripcion*, *tiempo_estimado*, *tiempo_registrado*, *estatus* | id | Orden en el que las tareas serán devueltas por la API. |

##### Consideraciones
- El valor de __q__ debe ser al menos un caractér.

##### Ejemplo - `JSON`:
`Header: Accept = application/json`

`GET: http://localhost:5001/api/tasks/search?q=comp&orderby=estatus`

*Respuesta:*
```
{
    "results": [
        {
            "id": 1,
            "creacion": "2021-02-08T03:40:58.328168-06:00",
            "actualizacion": "2021-02-08T03:42:48.716786-06:00",
            "descripcion": "Probar la respuesta XML",
            "tiempo_estimado": 120,
            "tiempo_registrado": 21,
            "estatus": "completada"
        },
        {
            "id": 2,
            "creacion": "2021-02-08T03:41:17.176918-06:00",
            "actualizacion": "2021-02-08T03:42:07.525447-06:00",
            "descripcion": "Hacer el README.md",
            "tiempo_estimado": 25,
            "tiempo_registrado": 110,
            "estatus": "completada"
        },
        {
            "id": 3,
            "creacion": "2021-01-29T17:15:54.428889-06:00",
            "actualizacion": "2021-02-01T04:40:54.428889-06:00",
            "descripcion": "Planear API - JSON",
            "tiempo_estimado": 200,
            "tiempo_registrado": 196,
            "estatus": "completada"
        },
        {
            "id": 4,
            "creacion": "2021-02-03T09:31:54.428937-06:00",
            "actualizacion": "2021-02-04T08:28:54.428937-06:00",
            "descripcion": "Programar API - JSON",
            "tiempo_estimado": 240,
            "tiempo_registrado": 199,
            "estatus": "completada"
        },
        {
            "id": 5,
            "creacion": "2021-02-01T19:55:09.474769-06:00",
            "actualizacion": "2021-02-05T07:52:09.474769-06:00",
            "descripcion": "Leer Documentación - JSON",
            "tiempo_estimado": 120,
            "tiempo_registrado": 97,
            "estatus": "completada"
        },
        {
            "id": 6,
            "creacion": "2021-01-29T18:34:54.428960-06:00",
            "actualizacion": "2021-02-03T00:50:54.428960-06:00",
            "descripcion": "Debuggear APIs - JSON",
            "tiempo_estimado": 90,
            "tiempo_registrado": 89,
            "estatus": "completada"
        },
        {
            "id": 12,
            "creacion": "2021-02-05T02:06:34.974672-06:00",
            "actualizacion": "2021-02-05T23:07:34.974672-06:00",
            "descripcion": "Planear API - XML",
            "tiempo_estimado": 200,
            "tiempo_registrado": 178,
            "estatus": "completada"
        },
        {
            "id": 13,
            "creacion": "2021-02-04T10:27:34.974709-06:00",
            "actualizacion": "2021-02-06T16:58:34.974709-06:00",
            "descripcion": "Programar API - XML",
            "tiempo_estimado": 240,
            "tiempo_registrado": 232,
            "estatus": "completada"
        },
        {
            "id": 14,
            "creacion": "2021-02-01T19:55:09.474769-06:00",
            "actualizacion": "2021-02-05T07:52:09.474769-06:00",
            "descripcion": "Leer Documentación - XML",
            "tiempo_estimado": 120,
            "tiempo_registrado": 99,
            "estatus": "completada"
        },
        {
            "id": 15,
            "creacion": "2021-01-29T06:51:34.974734-06:00",
            "actualizacion": "2021-02-02T14:22:34.974734-06:00",
            "descripcion": "Debuggear APIs - XML",
            "tiempo_estimado": 90,
            "tiempo_registrado": 89,
            "estatus": "completada"
        },
        {
            "id": 8,
            "creacion": "2021-02-04T18:03:54.428989-06:00",
            "actualizacion": "2021-02-06T07:08:54.428989-06:00",
            "descripcion": "Compilar el proyecto viejo",
            "tiempo_estimado": 255,
            "tiempo_registrado": 234,
            "estatus": "pendiente"
        },
        {
            "id": 9,
            "creacion": "2021-02-06T05:56:54.429006-06:00",
            "actualizacion": "2021-02-06T14:54:54.429006-06:00",
            "descripcion": "Completar la documentación",
            "tiempo_estimado": 135,
            "tiempo_registrado": 129,
            "estatus": "pendiente"
        },
        {
            "id": 10,
            "creacion": "2021-02-06T04:41:54.429022-06:00",
            "actualizacion": "2021-02-07T04:50:54.429022-06:00",
            "descripcion": "Realizar las comprobaciones a la data",
            "tiempo_estimado": 75,
            "tiempo_registrado": 60,
            "estatus": "pendiente"
        },
        {
            "id": 11,
            "creacion": "2021-02-06T17:19:54.429039-06:00",
            "actualizacion": "2021-02-07T03:30:54.429039-06:00",
            "descripcion": "Hacer más comprensible el código",
            "tiempo_estimado": 270,
            "tiempo_registrado": 234,
            "estatus": "pendiente"
        }
    ]
}
```

##### Ejemplo - `XML`:
`Header: Accept = text/xml`

`GET: http://localhost:5001/api/tasks/search?q=API&orderby=tiempo_estimado`

*Respuesta:*
```
<<?xml version="1.0" encoding="utf-8"?>
<root>
    <results>
        <list-item>
            <id>6</id>
            <creacion>2021-01-29T18:34:54.428960-06:00</creacion>
            <actualizacion>2021-02-03T00:50:54.428960-06:00</actualizacion>
            <descripcion>Debuggear APIs - JSON</descripcion>
            <tiempo_estimado>90</tiempo_estimado>
            <tiempo_registrado>89</tiempo_registrado>
            <estatus>completada</estatus>
        </list-item>
        <list-item>
            <id>15</id>
            <creacion>2021-01-29T06:51:34.974734-06:00</creacion>
            <actualizacion>2021-02-02T14:22:34.974734-06:00</actualizacion>
            <descripcion>Debuggear APIs - XML</descripcion>
            <tiempo_estimado>90</tiempo_estimado>
            <tiempo_registrado>89</tiempo_registrado>
            <estatus>completada</estatus>
        </list-item>
        <list-item>
            <id>3</id>
            <creacion>2021-01-29T17:15:54.428889-06:00</creacion>
            <actualizacion>2021-02-01T04:40:54.428889-06:00</actualizacion>
            <descripcion>Planear API - JSON</descripcion>
            <tiempo_estimado>200</tiempo_estimado>
            <tiempo_registrado>196</tiempo_registrado>
            <estatus>completada</estatus>
        </list-item>
        <list-item>
            <id>12</id>
            <creacion>2021-02-05T02:06:34.974672-06:00</creacion>
            <actualizacion>2021-02-05T23:07:34.974672-06:00</actualizacion>
            <descripcion>Planear API - XML</descripcion>
            <tiempo_estimado>200</tiempo_estimado>
            <tiempo_registrado>178</tiempo_registrado>
            <estatus>completada</estatus>
        </list-item>
        <list-item>
            <id>4</id>
            <creacion>2021-02-03T09:31:54.428937-06:00</creacion>
            <actualizacion>2021-02-04T08:28:54.428937-06:00</actualizacion>
            <descripcion>Programar API - JSON</descripcion>
            <tiempo_estimado>240</tiempo_estimado>
            <tiempo_registrado>199</tiempo_registrado>
            <estatus>completada</estatus>
        </list-item>
        <list-item>
            <id>13</id>
            <creacion>2021-02-04T10:27:34.974709-06:00</creacion>
            <actualizacion>2021-02-06T16:58:34.974709-06:00</actualizacion>
            <descripcion>Programar API - XML</descripcion>
            <tiempo_estimado>240</tiempo_estimado>
            <tiempo_registrado>232</tiempo_registrado>
            <estatus>completada</estatus>
        </list-item>
    </results>
</root>
```

[Volver al índice](#id0)
***

<div id='id37' />

#### List - `GET`
Enlista todas las tareas existentes en la base de datos, sin ningún filtro.

##### Parámetros

| Nombre | Requerido | Opciones | Default | Descripción |
| ----------- | -----------| ----------- | ----------- | ------------------- |
| **NA** | NA | NA | NA | NA. |

:bat:

##### Consideraciones
- El __id__ debe ser numérico y existente.

##### Ejemplo - `JSON`:
`GET: http://localhost:5001/api/tasks/`

*Respuesta:*
```
[
    {
        "id": 2,
        "creacion": "2021-02-08T03:41:17.176918-06:00",
        "actualizacion": "2021-02-08T03:42:07.525447-06:00",
        "descripcion": "Hacer el README.md",
        "tiempo_estimado": 25,
        "tiempo_registrado": 110,
        "estatus": "completada"
    },
    {
        "id": 1,
        "creacion": "2021-02-08T03:40:58.328168-06:00",
        "actualizacion": "2021-02-08T03:42:48.716786-06:00",
        "descripcion": "Probar la respuesta XML",
        "tiempo_estimado": 120,
        "tiempo_registrado": 21,
        "estatus": "completada"
    },
    {
        "id": 3,
        "creacion": "2021-01-29T17:15:54.428889-06:00",
        "actualizacion": "2021-02-01T04:40:54.428889-06:00",
        "descripcion": "Planear API - JSON",
        "tiempo_estimado": 200,
        "tiempo_registrado": 196,
        "estatus": "completada"
    },
    {
        "id": 4,
        "creacion": "2021-02-03T09:31:54.428937-06:00",
        "actualizacion": "2021-02-04T08:28:54.428937-06:00",
        "descripcion": "Programar API - JSON",
        "tiempo_estimado": 240,
        "tiempo_registrado": 199,
        "estatus": "completada"
    },
    {
        "id": 5,
        "creacion": "2021-02-01T19:55:09.474769-06:00",
        "actualizacion": "2021-02-05T07:52:09.474769-06:00",
        "descripcion": "Leer Documentación - JSON",
        "tiempo_estimado": 120,
        "tiempo_registrado": 97,
        "estatus": "completada"
    },
    {
        "id": 6,
        "creacion": "2021-01-29T18:34:54.428960-06:00",
        "actualizacion": "2021-02-03T00:50:54.428960-06:00",
        "descripcion": "Debuggear APIs - JSON",
        "tiempo_estimado": 90,
        "tiempo_registrado": 89,
        "estatus": "completada"
    },
    {
        "id": 7,
        "creacion": "2021-01-31T01:31:54.428975-06:00",
        "actualizacion": "2021-02-01T21:13:54.428975-06:00",
        "descripcion": "Deployar nuevos servicios - JSON",
        "tiempo_estimado": 200,
        "tiempo_registrado": 15,
        "estatus": "pendiente"
    },
    {
        "id": 8,
        "creacion": "2021-02-04T18:03:54.428989-06:00",
        "actualizacion": "2021-02-06T07:08:54.428989-06:00",
        "descripcion": "Compilar el proyecto viejo",
        "tiempo_estimado": 255,
        "tiempo_registrado": 234,
        "estatus": "pendiente"
    },
    {
        "id": 9,
        "creacion": "2021-02-06T05:56:54.429006-06:00",
        "actualizacion": "2021-02-06T14:54:54.429006-06:00",
        "descripcion": "Completar la documentación",
        "tiempo_estimado": 135,
        "tiempo_registrado": 129,
        "estatus": "pendiente"
    },
    {
        "id": 10,
        "creacion": "2021-02-06T04:41:54.429022-06:00",
        "actualizacion": "2021-02-07T04:50:54.429022-06:00",
        "descripcion": "Realizar las comprobaciones a la data",
        "tiempo_estimado": 75,
        "tiempo_registrado": 60,
        "estatus": "pendiente"
    },
    {
        "id": 11,
        "creacion": "2021-02-06T17:19:54.429039-06:00",
        "actualizacion": "2021-02-07T03:30:54.429039-06:00",
        "descripcion": "Hacer más comprensible el código",
        "tiempo_estimado": 270,
        "tiempo_registrado": 234,
        "estatus": "pendiente"
    },
    {
        "id": 12,
        "creacion": "2021-02-05T02:06:34.974672-06:00",
        "actualizacion": "2021-02-05T23:07:34.974672-06:00",
        "descripcion": "Planear API - XML",
        "tiempo_estimado": 200,
        "tiempo_registrado": 178,
        "estatus": "completada"
    },
    {
        "id": 13,
        "creacion": "2021-02-04T10:27:34.974709-06:00",
        "actualizacion": "2021-02-06T16:58:34.974709-06:00",
        "descripcion": "Programar API - XML",
        "tiempo_estimado": 240,
        "tiempo_registrado": 232,
        "estatus": "completada"
    },
    {
        "id": 14,
        "creacion": "2021-02-01T19:55:09.474769-06:00",
        "actualizacion": "2021-02-05T07:52:09.474769-06:00",
        "descripcion": "Leer Documentación - XML",
        "tiempo_estimado": 120,
        "tiempo_registrado": 99,
        "estatus": "completada"
    },
    {
        "id": 15,
        "creacion": "2021-01-29T06:51:34.974734-06:00",
        "actualizacion": "2021-02-02T14:22:34.974734-06:00",
        "descripcion": "Debuggear APIs - XML",
        "tiempo_estimado": 90,
        "tiempo_registrado": 89,
        "estatus": "completada"
    },
    {
        "id": 16,
        "creacion": "2021-01-31T13:53:34.974752-06:00",
        "actualizacion": "2021-02-04T15:27:34.974752-06:00",
        "descripcion": "Deployar nuevos servicios - XML",
        "tiempo_estimado": 200,
        "tiempo_registrado": 15,
        "estatus": "pendiente"
    }
]
```

[Volver al índice](#id0)
***

<div id='id34' />

#### Destroy - `DELETE`

Elimina la tarea solicitada al servidor por medio de su `id`.

##### Parámetros

| Nombre | Requerido | Opciones | Default | Descripción |
| ----------- | -----------| ----------- | ----------- | ------------------- |
| **id** | Sí | NA | NA | ID de la tarea a eliminar. |

##### Consideraciones
- El __id__ debe ser numérico y existente.

##### Ejemplo - `JSON`:
`Header: Accept = application/json`

`DELETE: http://localhost:5001/api/tasks/1/`

*Respuesta:*
```
{
  "id": 1,
  "estatus": "eliminada"
}
```

##### Ejemplo - `XML`:
`Header: Accept = text/xml`

`DELETE: http://localhost:5001/api/tasks/2/`

*Respuesta:*
```
<?xml version="1.0" encoding="utf-8"?>
<root>
    <id>2</id>
    <estatus>eliminada</estatus>
</root>
```

[Volver al índice](#id0)
***

<div id='id4' />

### Tests
Se crearon tests unitarios para la url principal y para los métodos básicos de la API

<div id='id41' />

#### Tests unitarios
Ejecutar tests:

`docker exec -it django_app sh -c "python /code/manage.py test"`

- __Test URL Principal:__

  a) Prueba que la url principal redireccione hacia el panel de administración.

- __Test Método Create__ - `JSON`:

  a) Prueba que la api responda correctamente a una peticion __create__ en formato `JSON`, verificando su *status_code*.

  b) Verifica que se haya creado un nuevo objeto en el modelo de base de datos.

- __Test Método Create__ - `XML`:

  a) Prueba que la api responda correctamente a una peticion __create__ en formato `XML`, verificando su *status_code*.

  b) Verifica que se haya creado un nuevo objeto en el modelo de base de datos.

- __Test Método Retrieve__:

  a) Prueba que la api responda correctamente a una peticion __retrieve__, verificando su *status_code*.

  b) Verifica que la tarea recibida en la respuesta, sea la que se requisitó por su `id`.


- __Test Método Update__:

  a) Prueba que la api responda correctamente a una peticion __update__, verificando su *status_code*.

  b) Verifica que la tarea actualizada, se vea reflejada en el modelo de base de datos.

  c) Comprueba que no sea posible actualizar una tarea con `estatus` de __"completada"__.

- __Test Método List__:

  a) Prueba que la api responda correctamente a una peticion __list__, verificando su *status_code*.

  b) Verifica que la primera tarea recibida en la respuesta, sea la misma que la primera en la base de datos.

  c) Comprueba que la cantidad de elementos regresados, sea igual a la cantidad de elementos en el modelo de la base de datos.

- __Test Método Destroy__:

  a) Prueba que la api responda correctamente a una peticion __destroy__, verificando su *status_code*.

  b) Verifica que la tarea eliminada, ya no se encuentre en el modelo de base de datos.

[Volver al índice](#id0)
