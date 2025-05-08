from model.database import Database


class TaskManager:
    def __init__(self):
        self.db = Database()

    def get_all_tasks(self):
        return self.db.fetch_all_tasks()

    def add_new_task(self, task_name):
        self.db.add_task(task_name)

    def remove_task(self, task_id):
        self.db.delete_task(task_id)

    def get_all_tasks(self):
        return self.db.fetch_all_tasks()  # returns [{'id': 1, 'task_name': 'Task A'}, ...]
