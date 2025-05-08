import tkinter as tk
from view.TaskManagerUI import TaskManagerUI
from view.auth_ui import AuthUI



def main():
    root = tk.Tk()
    app = TaskManagerUI(root)
    root.mainloop()

if __name__ == "__main__":
     root = tk.Tk()
     app = AuthUI(root)
     root.mainloop()
