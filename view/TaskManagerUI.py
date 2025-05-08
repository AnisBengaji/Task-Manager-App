import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
from controller.task_manager_controller import TaskManagerController

class TaskManagerUI:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Task Manager - Admin Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f2f5")
        self.style = ttk.Style()
        self.image_references = []  # Store image references to prevent garbage collection
        self.configure_styles()
        self.load_images()

        try:
            self.controller = TaskManagerController()
            self.create_widgets()
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize UI: {str(e)}")
            raise

    def configure_styles(self):
        """Configure modern styles for widgets"""
        self.style.configure("TFrame", background="#ffffff")
        self.style.configure("TLabel", background="#ffffff", font=("Inter", 12))
        self.style.configure("TEntry", font=("Inter", 12), padding=8)
        self.style.configure("TCombobox", font=("Inter", 12), padding=8)
        self.style.configure("TButton", font=("Inter", 12, "bold"), padding=10)
        self.style.configure("Sidebar.TButton", font=("Inter", 13), background="#1e2a44", foreground="white")
        self.style.configure("TCheckbutton", background="#ffffff", font=("Inter", 11))
        self.style.configure("Treeview", font=("Inter", 12), rowheight=40)
        self.style.configure("Treeview.Heading", font=("Inter", 12, "bold"), background="#e8ecef")
        
        # Button hover effects
        self.style.map("TButton",
                       background=[("active", "#3b82f6"), ("!active", "#2563eb")],
                       foreground=[("active", "white"), ("!active", "white")])
        self.style.map("Sidebar.TButton",
                       background=[("active", "#2d3b55"), ("!active", "#1e2a44")],
                       foreground=[("active", "white"), ("!active", "white")])

        # Custom listbox style (simulated via Treeview)
        self.style.configure("Custom.Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#1f2937")
        self.style.map("Custom.Treeview",
                       background=[("selected", "#bfdbfe")])

    def load_images(self):
        """Load icons and images"""
        self.icons = {}
        icon_names = {
            "tasks": "tasks.png",
            "categories": "categories.png",
            "users": "users.png",
            "logout": "logout.png",
            "logo": "logo.png"
        }
        try:
            for key, filename in icon_names.items():
                path = os.path.join("images", filename)
                if os.path.exists(path):
                    img = Image.open(path).resize((24, 24), Image.LANCZOS)
                    self.icons[key] = ImageTk.PhotoImage(img)
                    self.image_references.append(self.icons[key])
                else:
                    # Fallback placeholder
                    self.icons[key] = None
        except Exception as e:
            print(f"Error loading images: {str(e)}")
            self.icons = {key: None for key in icon_names}

    def create_widgets(self):
        """Create and arrange all UI widgets"""
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.add_header()
        self.add_sidebar()
        self.add_content_area()

    def add_header(self):
        """Add modern header with logo and logout button"""
        header_frame = tk.Frame(self.root, bg="#1e3a8a", pady=20)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Logo and title
        logo_frame = tk.Frame(header_frame, bg="#1e3a8a")
        logo_frame.pack(side="left", padx=20)
        if self.icons.get("logo"):
            tk.Label(logo_frame, image=self.icons["logo"], bg="#1e3a8a").pack(side="left")
        tk.Label(
            logo_frame, text="Task Manager", font=("Inter", 22, "bold"),
            fg="white", bg="#1e3a8a"
        ).pack(side="left", padx=10)

        # Logout button
        logout_button = ttk.Button(
            header_frame, text="Logout", image=self.icons.get("logout"), compound="left",
            command=self.logout, style="TButton", width=12
        )
        logout_button.pack(side="right", padx=20)

    def add_sidebar(self):
        """Add modern sidebar with icon navigation"""
        self.sidebar_frame = tk.Frame(self.root, bg="#1e2a44", width=220)
        self.sidebar_frame.grid(row=1, column=0, sticky="ns")
        self.sidebar_frame.grid_propagate(False)

        tk.Label(
            self.sidebar_frame, text="Admin Panel", font=("Inter", 16, "bold"),
            fg="white", bg="#1e2a44"
        ).pack(pady=20)

        nav_items = [
            ("Tasks", "tasks", lambda: self.show_frame("tasks")),
            ("Categories", "categories", lambda: self.show_frame("categories")),
            ("Users", "users", lambda: self.show_frame("users"))
        ]
        for text, icon_key, command in nav_items:
            btn = ttk.Button(
                self.sidebar_frame, text=text, image=self.icons.get(icon_key), compound="left",
                style="Sidebar.TButton", command=command
            )
            btn.pack(fill="x", padx=15, pady=8)

    def add_content_area(self):
        """Add content area with card-like frames"""
        self.content_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=30, pady=30)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.create_task_frame()
        self.create_category_frame()
        self.create_user_frame()

        self.show_frame("tasks")

    def show_frame(self, frame_name):
        """Show the specified frame"""
        for frame in self.frames.values():
            frame.grid_remove()
        self.frames[frame_name].grid(row=0, column=0, sticky="nsew")

    def create_task_frame(self):
        """Create modern task management frame"""
        frame = ttk.Frame(self.content_frame, style="TFrame")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.frames["tasks"] = frame

        # Task input card
        input_card = tk.Frame(frame, bg="#ffffff", bd=1, relief="flat")
        input_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        input_card.configure(highlightbackground="#e5e7eb", highlightthickness=1)
        self.add_task_input(input_card)

        # Task list card
        list_card = tk.Frame(frame, bg="#ffffff", bd=1, relief="flat")
        list_card.grid(row=1, column=0, sticky="nsew")
        list_card.configure(highlightbackground="#e5e7eb", highlightthickness=1)
        self.add_task_list(list_card)

    def create_category_frame(self):
        """Create modern category management frame"""
        frame = ttk.Frame(self.content_frame, style="TFrame")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.frames["categories"] = frame

        # Category input card
        input_card = tk.Frame(frame, bg="#ffffff", bd=1, relief="flat")
        input_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        input_card.configure(highlightbackground="#e5e7eb", highlightthickness=1)
        input_card.grid_columnconfigure(1, weight=1)

        tk.Label(input_card, text="Category Name:", font=("Inter", 12), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=10, padx=20)
        self.category_name_entry = ttk.Entry(input_card, width=50, font=("Inter", 12))
        self.category_name_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=20)

        button_frame = tk.Frame(input_card, bg="#ffffff")
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Add Category", command=self.add_category, style="TButton").grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Clear", command=lambda: self.category_name_entry.delete(0, tk.END), style="TButton").grid(row=0, column=1, padx=10)

        # Category list card
        list_card = tk.Frame(frame, bg="#ffffff", bd=1, relief="flat")
        list_card.grid(row=1, column=0, sticky="nsew")
        list_card.configure(highlightbackground="#e5e7eb", highlightthickness=1)
        list_card.grid_rowconfigure(1, weight=1)
        list_card.grid_columnconfigure(0, weight=1)

        tk.Label(list_card, text="Categories", font=("Inter", 14, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w", padx=20, pady=10)

        listbox_frame = tk.Frame(list_card, bg="#ffffff")
        listbox_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)

        self.category_listbox = ttk.Treeview(listbox_frame, columns=("Name",), show="headings", style="Custom.Treeview")
        self.category_listbox.heading("Name", text="Category Name")
        self.category_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.category_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.category_listbox.configure(yscrollcommand=scrollbar.set)

        action_frame = tk.Frame(list_card, bg="#ffffff")
        action_frame.grid(row=2, column=0, pady=20)
        ttk.Button(action_frame, text="Delete Category", command=self.delete_category, style="TButton").grid(row=0, column=0, padx=10)
        ttk.Button(action_frame, text="Refresh", command=self.load_categories_list, style="TButton").grid(row=0, column=1, padx=10)

        self.load_categories_list()

    def create_user_frame(self):
        """Create modern user management frame"""
        frame = ttk.Frame(self.content_frame, style="TFrame")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.frames["users"] = frame

        list_card = tk.Frame(frame, bg="#ffffff", bd=1, relief="flat")
        list_card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        list_card.configure(highlightbackground="#e5e7eb", highlightthickness=1)
        list_card.grid_rowconfigure(1, weight=1)
        list_card.grid_columnconfigure(0, weight=1)

        tk.Label(list_card, text="Users", font=("Inter", 14, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w", padx=20, pady=10)

        listbox_frame = tk.Frame(list_card, bg="#ffffff")
        listbox_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)

        self.user_listbox = ttk.Treeview(listbox_frame, columns=("User",), show="headings", style="Custom.Treeview")
        self.user_listbox.heading("User", text="Username (Email)")
        self.user_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.user_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.user_listbox.configure(yscrollcommand=scrollbar.set)

        action_frame = tk.Frame(list_card, bg="#ffffff")
        action_frame.grid(row=2, column=0, pady=20)
        ttk.Button(action_frame, text="Delete User", command=self.delete_user, style="TButton").grid(row=0, column=0, padx=10)
        ttk.Button(action_frame, text="Refresh", command=self.load_users, style="TButton").grid(row=0, column=1, padx=10)

        self.load_users()

    def add_task_input(self, parent):
        """Add modern task input section"""
        parent.grid_columnconfigure(1, weight=1)

        tk.Label(parent, text="Task Name:", font=("Inter", 12), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=10, padx=20)
        self.task_name_entry = ttk.Entry(parent, width=50, font=("Inter", 12))
        self.task_name_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=20)

        tk.Label(parent, text="Description:", font=("Inter", 12), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=10, padx=20)
        self.description_entry = ttk.Entry(parent, width=50, font=("Inter", 12))
        self.description_entry.grid(row=1, column=1, sticky="ew", pady=10, padx=20)

        tk.Label(parent, text="Due Date:", font=("Inter", 12), bg="#ffffff").grid(row=2, column=0, sticky="w", pady=10, padx=20)
        self.due_date_entry = DateEntry(parent, width=47, font=("Inter", 12), date_pattern="yyyy-mm-dd")
        self.due_date_entry.grid(row=2, column=1, sticky="ew", pady=10, padx=20)

        tk.Label(parent, text="Priority:", font=("Inter", 12), bg="#ffffff").grid(row=3, column=0, sticky="w", pady=10, padx=20)
        self.priority_combobox = ttk.Combobox(parent, values=["Low", "Medium", "High"], width=47, font=("Inter", 12))
        self.priority_combobox.grid(row=3, column=1, sticky="ew", pady=10, padx=20)
        self.priority_combobox.set("Medium")

        tk.Label(parent, text="Category:", font=("Inter", 12), bg="#ffffff").grid(row=4, column=0, sticky="w", pady=10, padx=20)
        self.category_combobox = ttk.Combobox(parent, width=47, font=("Inter", 12))
        self.category_combobox.grid(row=4, column=1, sticky="ew", pady=10, padx=20)
        self.load_categories()

        button_frame = tk.Frame(parent, bg="#ffffff")
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Add Task", command=self.add_task, style="TButton").grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Clear", command=self.clear_inputs, style="TButton").grid(row=0, column=1, padx=10)

    def add_task_list(self, parent):
        """Add modern task list and details section"""
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        tk.Label(parent, text="Tasks", font=("Inter", 14, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w", padx=20, pady=10)

        listbox_frame = tk.Frame(parent, bg="#ffffff")
        listbox_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        listbox_frame.grid_rowconfigure(0, weight=1)
        listbox_frame.grid_columnconfigure(0, weight=1)

        self.task_listbox = ttk.Treeview(listbox_frame, columns=("Task", "Priority", "Due Date"), show="headings", style="Custom.Treeview")
        self.task_listbox.heading("Task", text="Task Name")
        self.task_listbox.heading("Priority", text="Priority")
        self.task_listbox.heading("Due Date", text="Due Date")
        self.task_listbox.column("Task", width=300)
        self.task_listbox.column("Priority", width=100)
        self.task_listbox.column("Due Date", width=150)
        self.task_listbox.grid(row=0, column=0, sticky="nsew")
        self.task_listbox.bind('<<TreeviewSelect>>', self.show_task_details)

        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.task_listbox.configure(yscrollcommand=scrollbar.set)

        self.details_text = tk.Text(parent, height=6, font=("Inter", 12), state="disabled", wrap="word", bg="#f9fafb", relief="flat")
        self.details_text.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        action_frame = tk.Frame(parent, bg="#ffffff")
        action_frame.grid(row=3, column=0, pady=20)
        ttk.Button(action_frame, text="Delete Task", command=self.delete_task, style="TButton").grid(row=0, column=0, padx=10)
        ttk.Button(action_frame, text="Refresh", command=self.load_tasks, style="TButton").grid(row=0, column=1, padx=10)

        self.load_tasks()

    def load_categories(self):
        """Load categories into the combobox"""
        try:
            categories = self.controller.get_categories()
            self.category_combobox['values'] = [cat['name'] for cat in categories]
            self.category_combobox.set("None")
            self.categories = {cat['name']: cat['id'] for cat in categories}
        except Exception as e:
            messagebox.showerror("Load Categories Error", f"Failed to load categories: {str(e)}")
            self.category_combobox['values'] = ["None"]
            self.categories = {"None": None}

    def load_categories_list(self):
        """Load categories into the listbox"""
        try:
            categories = self.controller.get_categories()
            for item in self.category_listbox.get_children():
                self.category_listbox.delete(item)
            self.category_data = categories
            for cat in categories:
                self.category_listbox.insert("", tk.END, values=(cat['name'],))
        except Exception as e:
            messagebox.showerror("Load Categories Error", f"Failed to load categories: {str(e)}")
            self.category_data = []

    def load_users(self):
        """Load users into the listbox"""
        try:
            users = self.controller.get_all_users()
            for item in self.user_listbox.get_children():
                self.user_listbox.delete(item)
            self.user_data = users
            for user in users:
                self.user_listbox.insert("", tk.END, values=(f"{user['username']} ({user['email']})",))
        except Exception as e:
            messagebox.showerror("Load Users Error", f"Failed to load users: {str(e)}")
            self.user_data = []

    def load_tasks(self):
        """Load tasks into the listbox"""
        try:
            self.tasks = self.controller.get_tasks_by_user(self.user_id)
            for item in self.task_listbox.get_children():
                self.task_listbox.delete(item)
            for task in self.tasks:
                due_date = task['due_date'] or "No Due Date"
                self.task_listbox.insert("", tk.END, values=(task['task_name'], task['priority'], due_date))
            self.clear_details()
        except Exception as e:
            messagebox.showerror("Load Tasks Error", f"Failed to load tasks: {str(e)}")
            self.tasks = []

    def show_task_details(self, event):
        """Show details of the selected task"""
        selection = self.task_listbox.selection()
        if not selection:
            return
        index = self.task_listbox.index(selection[0])
        task = self.tasks[index]
        details = (
            f"Task: {task['task_name']}\n"
            f"Description: {task['description'] or 'None'}\n"
            f"Due Date: {task['due_date'] or 'None'}\n"
            f"Priority: {task['priority']}\n"
            f"Category: {self.get_category_name(task['category_id']) or 'None'}\n"
            f"Created: {task['created_at']}"
        )
        self.details_text.config(state="normal")
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)
        self.details_text.config(state="disabled")

    def get_category_name(self, category_id):
        """Get category name by ID"""
        if not category_id:
            return None
        for name, cid in self.categories.items():
            if cid == category_id:
                return name
        return None

    def add_category(self):
        """Add a new category"""
        name = self.category_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a category name.")
            return
        try:
            result = self.controller.add_category(name)
            messagebox.showinfo("Success", result)
            self.category_name_entry.delete(0, tk.END)
            self.load_categories_list()
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Add Category Error", f"Failed to add category: {str(e)}")

    def delete_category(self):
        """Delete the selected category"""
        selection = self.category_listbox.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a category to delete.")
            return
        index = self.category_listbox.index(selection[0])
        category_id = self.category_data[index]['id']
        try:
            self.controller.delete_category(category_id)
            messagebox.showinfo("Success", "Category deleted successfully.")
            self.load_categories_list()
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Delete Category Error", f"Failed to delete category: {str(e)}")

    def delete_user(self):
        """Delete the selected user"""
        selection = self.user_listbox.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a user to delete.")
            return
        index = self.user_listbox.index(selection[0])
        user_id = self.user_data[index]['id']
        if user_id == self.user_id:
            messagebox.showwarning("Permission Error", "You cannot delete your own account.")
            return
        try:
            self.controller.delete_user(user_id)
            messagebox.showinfo("Success", "User deleted successfully.")
            self.load_users()
        except Exception as e:
            messagebox.showerror("Delete User Error", f"Failed to delete user: {str(e)}")

    def add_task(self):
        """Add a new task"""
        task_name = self.task_name_entry.get().strip()
        description = self.description_entry.get().strip()
        due_date = self.due_date_entry.get()
        priority = self.priority_combobox.get()
        category_name = self.category_combobox.get()

        if not task_name or not description or not due_date:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        try:
            category_id = self.categories.get(category_name, None)
            result = self.controller.add_task(
                user_id=self.user_id,
                task_name=task_name,
                description=description,
                due_date=due_date,
                priority=priority,
                category_id=category_id
            )
            messagebox.showinfo("Success", result)
            self.load_tasks()
            self.clear_inputs()
        except Exception as e:
            messagebox.showerror("Add Task Error", f"Failed to add task: {str(e)}")

    def delete_task(self):
        """Delete the selected task"""
        selection = self.task_listbox.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return
        index = self.task_listbox.index(selection[0])
        task_id = self.tasks[index]['id']
        try:
            self.controller.delete_task(task_id)
            messagebox.showinfo("Success", "Task deleted successfully.")
            self.load_tasks()
        except Exception as e:
            messagebox.showerror("Delete Task Error", f"Failed to delete task: {str(e)}")

    def clear_inputs(self):
        """Clear all input fields"""
        self.task_name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.due_date_entry.set_date(None)
        self.priority_combobox.set("Medium")
        self.category_combobox.set("None")

    def clear_details(self):
        """Clear task details text"""
        self.details_text.config(state="normal")
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state="disabled")

    def logout(self):
        """Handle logout action"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerUI(root, user_id=1)
    root.mainloop()