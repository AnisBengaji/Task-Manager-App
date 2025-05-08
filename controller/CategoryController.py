from model.database import Database
import mysql.connector

class Category:
    def __init__(self):
        self.db = Database()

    def add_category(self, name):
        """Add a new category"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
            conn.commit()
            conn.close()
            return "Category added successfully."
        except mysql.connector.IntegrityError:
            conn.close()
            return "Category name already exists."
        except mysql.connector.Error as e:
            conn.close()
            raise Exception(f"Failed to add category: {str(e)}")

    def get_all_categories(self):
        """Get all categories"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        conn.close()
        return categories

    def delete_category(self, category_id):
        """Delete a category by ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
            conn.commit()
            conn.close()
            return "Category deleted successfully."
        except mysql.connector.Error as e:
            conn.close()
            raise Exception(f"Failed to delete category: {str(e)}")

class CategoryController:
    def __init__(self):
        self.category_model = Category()

    def add_category(self, name):
        """Add a new category"""
        return self.category_model.add_category(name)

    def get_all_categories(self):
        """Get all categories"""
        return self.category_model.get_all_categories()

    def delete_category(self, category_id):
        """Delete a category by ID"""
        return self.category_model.delete_category(category_id)