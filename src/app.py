import tkinter as tk
from tkinter import ttk, messagebox
from auth import login, get_buildkey
from fetch_data import get_books, get_chapters, get_problems
from solve_problems import solve_problem
import logging

class AutoBookzApp:
    """
    AutoBookzApp is the main class for the AutoBooks project. It provides a GUI interface
    for automating the completion of zyBooks activity assignments.

    Attributes:
        root: The root Tkinter window.
        books: A list of books retrieved after user login.
        current_book: The currently selected book.
        current_chapters: A list of currently selected chapters.
        token: Authentication token after successful login.
        buildkey: Build key retrieved after login.
    """

    def __init__(self, root):
        """
        Initializes the AutoBookzApp with the root window, sets up the GUI elements,
        and initializes the necessary attributes.
        """
        self.root = root
        self.root.title("AutoBookz")
        self.root.geometry("800x600")

        # Apply a theme and colors for consistent styling
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TButton', background='#007bff', foreground='white', font=('Arial', 12), padding=6)
        self.style.map('TButton', background=[('active', '#0056b3')])
        self.style.configure('TProgressbar', thickness=20, troughcolor='#d6d6d6', background='#007bff')

        # Create the menu bar, widgets, and status bar
        self.create_menus()
        self.create_widgets()
        self.create_status_bar()

        # Initialize data structures to store books and chapters
        self.books = []
        self.current_book = None
        self.current_chapters = []

    def create_menus(self):
        """
        Creates the menu bar with 'File' and 'Help' menus.
        Provides options to save/load data and access the 'About' dialog.
        """
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # File menu for save/load functionality and exit option
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Load", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help menu to show 'About' dialog
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Troubleshoot", command=self.show_faq)

    def create_widgets(self):
        """
        Creates the main widgets for the application, including tabs for
        login, chapters selection, and problem-solving.
        """
        # Tab Control for switching between different sections of the app
        self.tab_control = ttk.Notebook(self.root)
        self.login_tab = ttk.Frame(self.tab_control)
        self.chapters_tab = ttk.Frame(self.tab_control)
        self.problems_tab = ttk.Frame(self.tab_control)

        # Add tabs to the control
        self.tab_control.add(self.login_tab, text='Login')
        self.tab_control.add(self.chapters_tab, text='Chapters')
        self.tab_control.add(self.problems_tab, text='Problems')
        self.tab_control.pack(expand=1, fill='both')

        # Initialize the widgets for each tab
        self.create_login_widgets()
        self.create_chapters_widgets()
        self.create_problems_widgets()

    def create_login_widgets(self):
        """
        Creates the widgets in the 'Login' tab for user authentication.
        Includes input fields for email and password, a login button, and a show password option.
        """
        # Email Entry
        self.email_label = ttk.Label(self.login_tab, text="Email:")
        self.email_label.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        self.email_entry = ttk.Entry(self.login_tab, width=50)
        self.email_entry.grid(column=1, row=0, padx=10, pady=10)

        # Password Entry
        self.password_label = ttk.Label(self.login_tab, text="Password:")
        self.password_label.grid(column=0, row=1, padx=10, pady=10, sticky='W')
        self.password_entry = ttk.Entry(self.login_tab, show="*", width=50)
        self.password_entry.grid(column=1, row=1, padx=10, pady=10)

        # Show Password Checkbox
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(self.login_tab, text="Show Password",
                                                   variable=self.show_password_var,
                                                   command=self.toggle_password_visibility)
        self.show_password_check.grid(column=1, row=2, padx=10, pady=10, sticky='W')

        # Login Button
        self.login_button = ttk.Button(self.login_tab, text="Login", command=self.login)
        self.login_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    def create_chapters_widgets(self):
        """
        Creates the widgets in the 'Chapters' tab for displaying and selecting
        chapters from the selected zyBook.
        """
        # Label for Chapters Listbox
        self.chapters_label = ttk.Label(self.chapters_tab, text="Chapters:")
        self.chapters_label.grid(column=0, row=0, padx=10, pady=10, sticky='W')

        # Listbox for displaying chapters
        self.chapters_listbox = tk.Listbox(self.chapters_tab, selectmode=tk.MULTIPLE, width=70, height=10)
        self.chapters_listbox.grid(column=1, row=0, padx=10, pady=10)

        # Load Chapters Button
        self.load_chapters_button = ttk.Button(self.chapters_tab, text="Load Chapters", command=self.load_chapters)
        self.load_chapters_button.grid(column=1, row=1, padx=10, pady=10)

    def create_problems_widgets(self):
        """
        Creates the widgets in the 'Problems' tab for displaying and selecting
        problems from the selected chapters.
        """
        # Label for Problems Listbox
        self.problems_label = ttk.Label(self.problems_tab, text="Problems:")
        self.problems_label.grid(column=0, row=0, padx=10, pady=10, sticky='W')

        # Listbox for displaying problems
        self.problems_listbox = tk.Listbox(self.problems_tab, selectmode=tk.MULTIPLE, width=70, height=10)
        self.problems_listbox.grid(column=1, row=0, padx=10, pady=10)

        # Load Problems Button
        self.load_problems_button = ttk.Button(self.problems_tab, text="Load Problems", command=self.load_problems)
        self.load_problems_button.grid(column=1, row=1, padx=10, pady=10)

        # Progress Bar for showing problem-solving progress
        self.progress = ttk.Progressbar(self.problems_tab, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

        # Text box for displaying results
        self.result_text = tk.Text(self.problems_tab, height=10, width=70, wrap=tk.WORD, font=('Arial', 12))
        self.result_text.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    def create_status_bar(self):
        """
        Creates a status bar at the bottom of the application window
        to display status messages.
        """
        self.status_bar = ttk.Label(self.root, text="Ready", anchor='w', relief='sunken', padding=(10, 2))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message):
        """
        Updates the text displayed on the status bar.

        Args:
            message: The status message to display.
        """
        self.status_bar.config(text=message)

    def toggle_password_visibility(self):
        """
        Toggles the visibility of the password entry field based on the
        state of the 'Show Password' checkbox.
        """
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def login(self):
        """
        Handles the login process by retrieving the email and password from the
        input fields, authenticating the user, and fetching available zyBooks.
        """
        email = self.email_entry.get()
        password = self.password_entry.get()
        try:
            # Authenticate the user using the login function from the auth module
            result = login(email, password)
            self.token = result['session']['auth_token']
            self.buildkey = get_buildkey()
            user_id = result['user']['user_id']

            # Fetch the user's books and update the chapters list
            self.books = get_books(self.token, user_id)
            self.update_books_list()
        except Exception as e:
            # Log any errors and display them to the user
            logging.error(f'Error: {e}')
            messagebox.showerror("Error", str(e))

    def update_books_list(self):
        """
        Updates the chapters listbox with the available zyBooks for the logged-in user.
        Only books where the user has a 'Student' role are listed.
        """
        self.chapters_listbox.delete(0, tk.END)
        for book in self.books:
            if book['user_zybook_role'] == 'Student':
                self.chapters_listbox.insert(tk.END, book['zybook_code'])

    def load_chapters(self):
        """
        Loads chapters for the selected zyBooks and displays them in the problems listbox.
        """
        selected_books = [self.chapters_listbox.get(i) for i in self.chapters_listbox.curselection()]
        self.current_chapters = []
        self.problems_listbox.delete(0, tk.END)
        for zybook_code in selected_books:
            chapters = get_chapters(self.token, zybook_code)
            for term in chapters:
                for chapter in term['chapters']:
                    chapter_number = chapter['number']
                    self.current_chapters.append((zybook_code, chapter_number))
                    self.problems_listbox.insert(tk.END, f"Zybook: {zybook_code}, Chapter: {chapter_number}")

    def load_problems(self):
        """
        Loads problems for the selected chapters and displays them in the results text box.
        """
        selected_chapters = [self.problems_listbox.get(i) for i in self.problems_listbox.curselection()]
        self.result_text.delete(1.0, tk.END)
        for item in selected_chapters:
            zybook_code, chapter_number = self.parse_chapter_string(item)
            for chapter in self.current_chapters:
                if chapter[0] == zybook_code and chapter[1] == chapter_number:
                    sections = get_problems(self.token, zybook_code, chapter_number, 1)  # Assume section 1
                    for problem in sections['section']['content_resources']:
                        self.result_text.insert(tk.END, f"Problem ID: {problem['id']}, Type: {problem['type']}\n")

    def parse_chapter_string(self, chapter_string):
        """
        Parses a string representation of a chapter to extract the zyBook code and chapter number.

        Args:
            chapter_string: The string representation of a chapter.

        Returns:
            A tuple (zybook_code, chapter_number).
        """
        parts = chapter_string.split(", ")
        zybook_code = parts[0].split(": ")[1]
        chapter_number = int(parts[1].split(": ")[1])
        return zybook_code, chapter_number

    def save_data(self):
        """
        Placeholder for save functionality.
        """
        pass

    def load_data(self):
        """
        Placeholder for load functionality.
        """
        pass

    def show_about(self):
        messagebox.showinfo("About AutoBookz", "AutoBookz v1.0\nDeveloped by Bryce McLeod")

    def show_faq(self):
        messagebox.showinfo("Troubleshooting", "Did you try turning it off and on again?")

if __name__ == "__main__":
    # Create the root Tkinter window and run the AutoBookz application
    root = tk.Tk()
    app = AutoBookzApp(root)
    root.mainloop()
