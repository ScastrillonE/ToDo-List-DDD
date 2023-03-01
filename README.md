# Tutorial: ToDo List con Python y DDD

### Requisitos
- Instalar pysqlite3, usa ```pip3 install pysqlite3```


En este tutorial, implementaremos una aplicación básica de ToDo List utilizando el patrón de diseño de Arquitectura de Dominio Dirigido (DDD) en Python. La aplicación permitirá a los usuarios crear, actualizar, eliminar y listar tareas pendientes.

Comencemos por crear la estructura de carpetas y archivos del proyecto:


```markdown
todo_list/
├── application/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── services.py
│   └── tasks.py
├── domain/
│   ├── __init__.py
│   ├── entities.py
│   └── repositories.py
├── infrastructure/
│   ├── __init__.py
│   ├── database.py
│   └── repositories.py
├── __init__.py
└── main.py
```

En este proyecto, se ha dividido la lógica en tres capas principales:

-   **Infraestructura**: se encarga de la conexión a la base de datos y de proporcionar los repositorios concretos para acceder a los datos.
-   **Dominio**: se encarga de modelar las entidades y la lógica de negocio de la aplicación.
-   **Aplicación**: se encarga de coordinar las operaciones entre la capa de infraestructura y la capa de dominio.

### Capa de Infraestructura

Comencemos con la capa de infraestructura. En el archivo `database.py`, crearemos una conexión a la base de datos SQLite utilizando el módulo `sqlite3` de Python:

```python
# todo_list/infrastructure/database.py

import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("todo_list.db")
        self.connection.row_factory = sqlite3.Row

    def execute(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor

    def close(self):
        self.connection.close()
```

La clase `Database` proporciona una interfaz para ejecutar consultas en la base de datos. También establece el modo de fila de resultados en `sqlite3.Row`, lo que permite acceder a los resultados como si fueran diccionarios.

A continuación, crearemos los repositorios concretos en la capa de infraestructura. En el archivo `repositories.py`, implementaremos el repositorio `SqliteTaskRepository` que utiliza la clase `Database` para acceder a la base de datos y manipular los datos de las tareas pendientes:

```python
# todo_list/infrastructure/repositories.py

from typing import List

from todo_list.domain.entities import Task
from todo_list.domain.repositories import TaskRepository
from todo_list.infrastructure.database import Database


class SqliteTaskRepository(TaskRepository):
    def __init__(self, database: Database):
        self._database = database

    def get_all(self) -> List[Task]:
        cursor = self._database.execute("SELECT * FROM tasks")
        return [Task(**row) for row in cursor.fetchall()]

    def get_by_id(self, task_id: int) -> Task:
        cursor = self._database.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return Task(**row)

    def add(self, task: Task):
        cursor = self._database.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            (task.title, task.description, task.status),
        )
        task.id = cursor.lastrowid

    def update(self, task: Task):
        self._database.execute(
            "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
            (task.title, task.description, task.status, task.id),
        )

    def delete(self, task_id: int):
        self._database.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
```

Este repositorio implementa todos los métodos definidos en la interfaz `TaskRepository`. La mayoría de los métodos simplemente ejecutan consultas SQL y devuelven los resultados en forma de objetos `Task`. El método `add` es un poco diferente porque tiene que asignar un valor a la propiedad `id` del objeto `Task` después de insertarlo en la base de datos.

Ahora, pasamos a la capa de dominio. En el archivo `entities.py`, definimos la clase `Task` que representa una tarea pendiente:

```python
# todo_list/domain/entities.py

class Task:
    def __init__(self, title: str, description: str, status: str, id: int = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
```

La clase `Task` tiene cuatro propiedades: `id`, `title`, `description` y `status`. La propiedad `id` se utiliza para identificar de forma única cada tarea y se establece en `None` por defecto.

En el archivo `repositories.py`, definimos la interfaz `TaskRepository` que describe los métodos necesarios para manipular las tareas pendientes:

```python
# todo_list/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List

from todo_list.domain.entities import Task


class TaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task:
        pass

    @abstractmethod
    def add(self, task: Task):
        pass

    @abstractmethod
    def update(self, task: Task):
        pass

    @abstractmethod
    def delete(self, task_id: int):
        pass

```

La interfaz `TaskRepository` define cinco métodos abstractos que representan las operaciones CRUD básicas: `get_all`, `get_by_id`, `add`, `update` y `delete`. Cada uno de estos métodos recibe y devuelve objetos `Task`.

En el archivo `exceptions.py`, definimos una excepción personalizada `TaskNotFoundException` que se utiliza en la capa de aplicación para indicar que una tarea con un identificador específico no se ha encontrado:

```python
# todo_list/application/exceptions.py

class TaskNotFoundException(Exception):
    def __init__(self, task_id: int):
        self.message = f"Task not found: {task_id}"
        super().__init__(self.message)

```

Ahora, pasamos a la capa de aplicación. En el archivo `services.py` de la capa de aplicación, definimos la clase `TaskService` que coordina las operaciones entre la capa de infraestructura y la capa de dominio:

```python
# todo_list/application/services.py

from typing import List

from todo_list.application.exceptions import TaskNotFoundException
from todo_list.domain.entities import Task
from todo_list.domain.repositories import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self._repository = task_repository

    def get_all_tasks(self) -> List[Task]:
        return self._repository.get_all()

    def get_task_by_id(self, task_id: int) -> Task:
        task = self._repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        return task

    def create_task(self, title: str, description: str) -> Task:
        task = Task(title=title, description=description, status="pending")
        self._repository.add(task)
        return task

    def update_task(self, task_id: int, title: str, description: str, status: str) -> Task:
        task = self.get_task_by_id(task_id)
        task.title = title
        task.description = description
        task.status = status
        self._repository.update(task)
        return task

    def delete_task(self, task_id: int):
        task = self.get_task_by_id(task_id)
        self._repository.delete(task.id)
```

La clase `TaskService` define cinco métodos que corresponden a las operaciones CRUD básicas de una tarea pendiente: `get_all_tasks`, `get_task_by_id`, `create_task`, `update_task` y `delete_task`. Cada uno de estos métodos delega las operaciones correspondientes al repositorio `TaskRepository` y realiza algunas validaciones adicionales. Por ejemplo, el método `get_task_by_id` lanza una excepción `TaskNotFoundException` si la tarea con el identificador especificado no existe.

En el archivo `tasks.py` de la capa de aplicación, creamos un punto de entrada para la aplicación que utiliza la clase `TaskService` para manejar las solicitudes del usuario:

```python
# todo_list/application/tasks.py

from typing import List

from todo_list.application.exceptions import TaskNotFoundException
from todo_list.domain.entities import Task
from todo_list.domain.repositories import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self._repository = task_repository

    def get_all_tasks(self) -> List[Task]:
        return self._repository.get_all()

    def get_task_by_id(self, task_id: int) -> Task:
        task = self._repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        return task

    def create_task(self, title: str, description: str) -> Task:
        task = Task(title=title, description=description, status="pending")
        self._repository.add(task)
        return task

    def update_task(self, task_id: int, title: str, description: str, status: str) -> Task:
        task = self.get_task_by_id(task_id)
        task.title = title
        task.description = description
        task.status = status
        self._repository.update(task)
        return task

    def delete_task(self, task_id: int):
        task = self.get_task_by_id(task_id)
        self._repository.delete(task.id)
```

La clase `TaskService` es la implementación de la capa de aplicación que se encarga de coordinar las operaciones entre la capa de infraestructura y la capa de dominio. Define cinco métodos que corresponden a las operaciones CRUD básicas de una tarea pendiente: `get_all_tasks()`, `get_task_by_id()`, `create_task()`, `update_task()` y `delete_task()`. Cada uno de estos métodos utiliza el repositorio `TaskRepository` correspondiente para manipular los datos de la base de datos y realiza algunas validaciones adicionales.

El método `get_all_tasks()` utiliza el método `get_all()` del repositorio para recuperar todas las tareas pendientes de la base de datos y devolverlas como una lista de objetos `Task`. El método `get_task_by_id()` utiliza el método `get_by_id()` del repositorio para buscar una tarea pendiente específica por su identificador y devuelve un objeto `Task` si se encuentra. Si la tarea no se encuentra, lanza la excepción personalizada `TaskNotFoundException`. El método `create_task()` crea una nueva tarea pendiente utilizando el título y la descripción proporcionados por el usuario, establece el estado en "pending" y luego utiliza el método `add()` del repositorio para insertar la tarea en la base de datos. Devuelve la tarea recién creada. El método `update_task()` actualiza los datos de una tarea pendiente existente utilizando el identificador de la tarea y los nuevos valores proporcionados por el usuario. Llama al método `get_task_by_id()` para recuperar la tarea existente, actualiza sus propiedades y luego utiliza el método `update()` del repositorio para guardar los cambios en la base de datos. Devuelve la tarea actualizada. Finalmente, el método `delete_task()` elimina una tarea pendiente específica utilizando su identificador. Llama al método `get_task_by_id()` para recuperar la tarea existente y luego utiliza el método `delete()` del repositorio para eliminarla de la base de datos.

```python
# todo_list/main.py

from todo_list.application.tasks import (
    create_task_service,
    create_task,
    update_task,
    delete_task,
    list_tasks,
)


def main():
    task_service = create_task_service()

    while True:
        print("\n")
        print("Menu:")
        print("1. Listar tareas")
        print("2. Crear tarea")
        print("3. Actualizar tarea")
        print("4. Borrar tarea")
        print("0. Salir")

        choice = input("Digite la opcion: ")
        if choice == "1":
            list_tasks(task_service)
        elif choice == "2":
            title = input("Ingrese el titulo: ")
            description = input("Ingrese una descripcion: ")
            create_task(task_service, title, description)
        elif choice == "3":
            task_id = int(input("ingrese el id de la tarea: "))
            title = input("Ingrese el titulo: ")
            description = input("Ingrese una descripcion: ")
            status = input("Ingrese el estado: ")
            update_task(task_service, task_id, title, description, status)
        elif choice == "4":
            task_id = int(input("ingrese el id de la tarea: "))
            delete_task(task_service, task_id)
        elif choice == "0":
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()
```
La función `main()` utiliza las funciones de punto de entrada `list_tasks()`, `create_task()`, `update_task()` y `delete_task()` de la capa de aplicación para proporcionar una interfaz de línea de comandos básica. Primero, crea una instancia de la clase `TaskService` utilizando el método `create_task_service()`. Luego, muestra un menú interactivo en un bucle infinito hasta que el usuario selecciona la opción "0" para salir. Cada opción del menú corresponde a una función de punto de entrada específica que interactúa con la capa de aplicación a través de la instancia de `TaskService`. El usuario puede ingresar los datos necesarios en la línea de comandos para realizar la operación correspondiente.

Al ejecutar por primera vez el programa se debe de crear la tabla tasks con el siguinete comando:

    create  table  tasks( id  integer  primary  key  autoincrement,title  text,description  text,status  text)

Para ver el ejemplo en funcionamiento ejecuta 
    ``` python3 main.py ```

[Aca el repositorio con el ejemplo completo](https://github.com/ScastrillonE/ToDo-List-DDD)