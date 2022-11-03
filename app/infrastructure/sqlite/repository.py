from app.domain.entities import Task
from app.domain.repository import TaskRepository
import sqlite3
from sqlite3 import Error

class TaskRepositorySQLite(TaskRepository):
    def __init__(self, db_file_path):
        try:
            self._db_conn = sqlite3.connect(db_file_path)
        except Error as e:
            print(e)

    def create_task(self, new_task: Task):
        sql = """ 
            INSERT INTO
                'Task' (task_id, user_id, name, status)
            VALUES(?, ?, ?, ?)
        """
        param = (new_task.task_id, new_task.user_id, new_task.name, new_task.status.value)
        cur = self._db_conn.cursor()
        cur.execute(sql, param)
        self._db_conn.commit()

    def get_tasks_by_user_id(self, user_id):
        sql = '''SELECT task_id, user_id, state FROM Task WHERE user_id = ?'''

        cur = self._db_conn.cursor()
        cur.execute(sql, (user_id,))

        rows = cur.fetchall()

        result = []
        for row in rows:
            result.append(Task(row[0], row[1], row[2]))

        return result

    