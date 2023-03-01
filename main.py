from application.tasks import (
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