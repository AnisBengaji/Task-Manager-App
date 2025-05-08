from controller.UserController import UserController
from controller.CategoryController import CategoryController
from model.tasks import Task  

class TaskManagerController:
    def __init__(self):
        self.user_controller = UserController()
        self.category_controller = CategoryController()
        self.task_model = Task()

    def create_user(self, username, email, password):
        """Create a new user through UserController"""
        return self.user_controller.create_user(username, email, password)

    def get_user_by_username(self, username):
        """Get user details by username"""
        return self.user_controller.get_user_by_username(username)

    def get_all_users(self):
        """Get all users"""
        return self.user_controller.get_all_users()

    def delete_user(self, user_id):
        """Delete a user by ID"""
        return self.user_controller.delete_user(user_id)

    def get_categories(self):
        """Get all categories"""
        return self.category_controller.get_all_categories()

    def add_category(self, name):
        """Add a new category"""
        return self.category_controller.add_category(name)

    def delete_category(self, category_id):
        """Delete a category by ID"""
        return self.category_controller.delete_category(category_id)

    def add_task(self, user_id, task_name, description, due_date, priority, category_id=None):
        """Add a new task for a user"""
        return self.task_model.add_task(user_id, task_name, description, due_date, priority, category_id)

    def delete_task(self, task_id):
        """Delete a task by its ID"""
        return self.task_model.delete_task(task_id)

    def delete_task_by_name(self, task_name, user_id):
        """Delete a task by its name for a specific user"""
        tasks = self.task_model.get_tasks_by_user(user_id)
        for task in tasks:
            if task['task_name'] == task_name:
                return self.task_model.delete_task(task['id'])
        return "Task not found."

    def get_tasks_by_user(self, user_id):
        """Get all tasks for a specific user"""
        return self.task_model.get_tasks_by_user(user_id)