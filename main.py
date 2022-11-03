from app.domain import entities
from app.application import usecases
from app.infrastructure.sqlite import repository

REPO = repository.TaskRepositorySQLite('./sqlite.db')

def add_task():
    task_uc = usecases.TaskUC(REPO)
    result = task_uc.create_task(0,"prueba")

add_task()