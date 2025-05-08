import hashlib
from model.database import Database

class User:
    def __init__(self):
        self.db = Database()
        self.create_users_table()

    def create_users_table(self):
        """Create the users table if it doesn't exist."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def hash_password(self, password):
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, email, password):
        """Create a new user"""
        try:
            password_hash = self.hash_password(password)
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            conn.commit()
            conn.close()
            return "User created successfully!"
        except mysql.connector.IntegrityError:
            conn.close()
            return "Username or email already exists."
        except mysql.connector.Error as e:
            conn.close()
            raise Exception(f"Failed to create user: {str(e)}")

    def validate_login(self, username, password):
        """Validate user login credentials"""
        password_hash = self.hash_password(password)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password_hash = %s",
            (username, password_hash)
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            return {"id": user[0], "username": user[1], "email": user[2]}
        return None

    def get_user_by_username(self, username):
        """Get user by username"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_all_users(self):
        """Get all users"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username, email, created_at FROM users")
            users = cursor.fetchall()
            conn.close()
            return users
        except mysql.connector.Error as e:
            conn.close()
            raise Exception(f"Failed to fetch users: {str(e)}")

    def delete_user(self, user_id):
        """Delete a user by ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            conn.close()
            return "User deleted successfully."
        except mysql.connector.Error as e:
            conn.close()
            raise Exception(f"Failed to delete user: {str(e)}")