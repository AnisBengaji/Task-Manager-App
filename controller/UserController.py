from model.user import User

class UserController:
    def __init__(self):
        self.user_model = User()

    def create_user(self, username, email, password):
        """Create a new user"""
        if not username or not email or not password:
            return "All fields must be filled."
        
        existing_user = self.user_model.get_user_by_username(username)
        if existing_user:
            return "Username already exists."
        
        return self.user_model.create_user(username, email, password)

    def get_user_by_username(self, username):
        """Get user by username"""
        return self.user_model.get_user_by_username(username)

    def get_all_users(self):
        """Get all users"""
        return self.user_model.get_all_users()

    def delete_user(self, user_id):
        """Delete a user by ID"""
        return self.user_model.delete_user(user_id)

    def signup(self, username, email, password):
        """Handle user signup"""
        try:
            return self.user_model.create_user(username, email, password)
        except Exception as e:
            return f"Signup error: {str(e)}"

    def login(self, username, password):
        """Handle user login"""
        return self.user_model.validate_login(username, password)