
from mysql.connector import connect, Error
from model.database import Database


class Category:
    def __init__(self):
        self.db = Database()

    def get_all_categories(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        conn.close()
        return categories

    def add_category(self, name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
        conn.commit()
        conn.close()
