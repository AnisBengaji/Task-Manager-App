import mysql.connector
from model.database import Database

class Task:
    def __init__(self):
        self.db = Database()

    def add_task(self, user_id, task_name, description, due_date, priority, category_id=None):
        """Add a new task to the database"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO tasks (user_id, category_id, task_name, description, due_date, priority)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, category_id, task_name, description, due_date, priority))
            conn.commit()
            conn.close()
            return "Task added successfully."
        except mysql.connector.Error as e:
            conn.close()
            raise Exception(f"Failed to add task: {str(e)}")

    def get_tasks_by_user(self, user_id):
        """Fetch all tasks for a specific user"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
            tasks = cursor.fetchall()
            conn.close()
            return tasks
        except mysql.connector.Error as e:
            conn.close()
            raise Exception(f"Failed to fetch tasks: {str(e)}")

    def delete_task(self, task_id):
        """Delete a task by its ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()
            conn.close()
            return "Task deleted successfully."
        except mysql.connector.Error as e:
            conn.close()
            raise Exception(f"Failed to delete task: {str(e)}")