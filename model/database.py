import mysql.connector

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root" 
        self.password = ""  
        self.database = "task_manager"  
        self.create_tables()

    def create_tables(self):
        """Create users, categories, and tasks tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                category_id INT,
                task_name VARCHAR(100) NOT NULL,
                description TEXT,
                due_date VARCHAR(50),
                priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)

        conn.commit()
        conn.close()

    def get_connection(self):
        """Return a database connection"""
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as e:
            raise Exception(f"Database connection failed: {str(e)}")

    def fetch_all_tasks(self):
        """Fetch all tasks from the database"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        return tasks

    def add_task(self, task_name):
        """Insert a new task into the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task_name) VALUES (%s)", (task_name,))
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        """Delete a task by its ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        conn.close()