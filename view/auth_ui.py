import tkinter as tk
from tkinter import ttk, messagebox
from controller.UserController import UserController
from view.TaskManagerUI import TaskManagerUI

class AuthUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager - Authentication")
        self.root.geometry("400x500")
        self.root.configure(bg="#e8ecef")
        self.user_controller = UserController()

        self.username = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)

        self.style = ttk.Style()
        self.configure_styles()

        self.create_login_ui()

    def configure_styles(self):
        """Configure custom styles for widgets"""
        self.style.configure("TLabel", background="#ffffff", font=("Segoe UI", 11))
        self.style.configure("TEntry", font=("Segoe UI", 11))
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"))
        self.style.map("TButton",
                       background=[("active", "#0052cc"), ("!active", "#0066ff")],
                       foreground=[("active", "white"), ("!active", "white")])
        self.style.configure("TCheckbutton", background="#ffffff", font=("Segoe UI", 10))

    def create_login_ui(self):
        """Create the login UI"""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#e8ecef")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg="#1a3c6e", pady=15)
        header_frame.pack(fill="x")
        tk.Label(
            header_frame, text="Task Manager Login", font=("Segoe UI", 16, "bold"),
            fg="white", bg="#1a3c6e"
        ).pack()

        # Form Frame
        form_frame = tk.Frame(main_frame, bg="#ffffff", padx=20, pady=20)
        form_frame.pack(pady=20, fill="x")

        # Username
        tk.Label(form_frame, text="Username:", font=("Segoe UI", 11), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        username_entry = ttk.Entry(form_frame, textvariable=self.username, width=30)
        username_entry.grid(row=0, column=1, pady=5, padx=5)
        username_entry.focus()

        # Password
        tk.Label(form_frame, text="Password:", font=("Segoe UI", 11), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form_frame, textvariable=self.password, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)
        self.password_entry.bind("<Return>", lambda event: self.login())

        # Show Password
        ttk.Checkbutton(
            form_frame, text="Show Password", variable=self.show_password,
            command=self.toggle_password, style="TCheckbutton"
        ).grid(row=2, column=1, sticky="w", pady=5)

        # Buttons
        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Login", command=self.login, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Sign Up", command=self.create_signup_ui, style="TButton").grid(row=0, column=1, padx=5)

        # Welcome Message
        tk.Label(
            main_frame, text="Welcome to Task Manager!", font=("Segoe UI", 12, "italic"),
            bg="#e8ecef", fg="#555"
        ).pack(pady=10)

    def create_signup_ui(self):
        """Create the signup UI"""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#e8ecef")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg="#1a3c6e", pady=15)
        header_frame.pack(fill="x")
        tk.Label(
            header_frame, text="Task Manager Sign Up", font=("Segoe UI", 16, "bold"),
            fg="white", bg="#1a3c6e"
        ).pack()

        # Form Frame
        form_frame = tk.Frame(main_frame, bg="#ffffff", padx=20, pady=20)
        form_frame.pack(pady=20, fill="x")

        # Username
        tk.Label(form_frame, text="Username:", font=("Segoe UI", 11), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        username_entry = ttk.Entry(form_frame, textvariable=self.username, width=30)
        username_entry.grid(row=0, column=1, pady=5, padx=5)
        username_entry.focus()

        # Email
        tk.Label(form_frame, text="Email:", font=("Segoe UI", 11), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.email, width=30).grid(row=1, column=1, pady=5, padx=5)

        # Password
        tk.Label(form_frame, text="Password:", font=("Segoe UI", 11), bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form_frame, textvariable=self.password, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)
        self.password_entry.bind("<Return>", lambda event: self.signup())


        
       

        # Show Password
        ttk.Checkbutton(
            form_frame, text="Show Password", variable=self.show_password,
            command=self.toggle_password, style="TCheckbutton"
        ).grid(row=3, column=1, sticky="w", pady=5)

        # Buttons
        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Sign Up", command=self.signup, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Back to Login", command=self.create_login_ui, style="TButton").grid(row=0, column=1, padx=5)

    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def signup(self):
        """Handle signup action"""
        username = self.username.get().strip()
        email = self.email.get().strip()
        password = self.password.get().strip()

        if not username or not email or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Input Error", "Please enter a valid email address.")
            return

        if len(password) < 6:
            messagebox.showwarning("Input Error", "Password must be at least 6 characters long.")
            return

        try:
            result = self.user_controller.signup(username, email, password)
            messagebox.showinfo("Signup", result)
            if "successfully" in result.lower():
                self.create_login_ui()
                self.username.set("")
                self.email.set("")
                self.password.set("")
        except Exception as e:
            messagebox.showerror("Signup Error", f"Failed to sign up: {str(e)}")

    def login(self):
        """Handle login action"""
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            user = self.user_controller.login(username, password)
            if user:
                messagebox.showinfo("Login Success", f"Welcome, {user['username']}!")
                self.root.destroy()
                root = tk.Tk()
                app = TaskManagerUI(root, user_id=user['id'])
                root.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")
        except Exception as e:
            messagebox.showerror("Login Error", f"Failed to login: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthUI(root)
    root.mainloop()