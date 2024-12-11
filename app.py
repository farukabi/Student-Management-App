
import customtkinter as ctk
import tkinter as tk
import sqlite3
import mainpage
from tkinter import messagebox as msg

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

class FirstPage(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title('SMP')
        self.geometry("400x500")
        self.resizable(False, False)
        self._set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.language = "en"
        self.translations = {
            "de": {
                "login": "Anmelden",
                "username_label": "Benutzername",
                "password_label": "Passwort",
                "login_button": "Anmelden",
                "register_label": "Kein Konto?",
                "register_button": "Registrieren",
                "login_error": "Benutzername und Passwort sind erforderlich!",
                "invalid_credentials": "Ungültiger Benutzername oder Passwort",
                "register_error": "Bitte füllen Sie alle Felder aus!",
                "register_success": "Registrierung erfolgreich erstellt!",
                "username_taken": "Dieser Benutzername ist bereits vergeben!",
                "language_menu": "Sprache",
                "settings_menu": "Einstellungen",
                "change_theme": "Design ändern",
                "german": "Deutsch",
                "english": "Englisch"
            },
            "en": {
                "login": "Login",
                "username_label": "Username",
                "password_label": "Password",
                "login_button": "Login",
                "register_label": "Don't Have an Account?",
                "register_button": "Register",
                "login_error": "Username and password are required!",
                "invalid_credentials": "Invalid username or password",
                "register_error": "Please fill out all fields!",
                "register_success": "Registration successful!",
                "username_taken": "This username is already taken!",
                "language_menu": "Language",
                "settings_menu": "Settings",
                "change_theme": "Change Theme",
                "german": "German",
                "english": "English"
            }
        }
        self.create_widgets()
        self.layout_widgets()
        self.create_menu()
        self.bind('<Return>', self.login)
        init_db()
        self.mainloop()

    def translate(self, key):
        return self.translations[self.language].get(key, key)

    def update_language(self, lang):
        self.language = lang
        self.refresh_ui()

    def change_appearance(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")
    def refresh_ui(self):
        self.title_label.configure(text=self.translate("login"))
        self.label1.configure(text=self.translate("username_label"))
        self.entry1.configure(placeholder_text=self.translate("username_label"))
        self.label2.configure(text=self.translate("password_label"))
        self.entry2.configure(placeholder_text=self.translate("password_label"))
        self.button1.configure(text=self.translate("login_button"))
        self.label3.configure(text=self.translate("register_label"))
        self.button2.configure(text=self.translate("register_button"))
        self.menubar.entryconfig(2,label=self.translate("settings_menu"))
        self.menubar.entryconfig(1, label=self.translate("language_menu"))
        self.settings_menu.entryconfig(0, label=self.translate("change_theme"))
        self.language_menu.entryconfig(0, label=self.translate("german"))
        self.language_menu.entryconfig(1, label=self.translate("english"))

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text=self.translate("login"), font=("Arial", 24, "bold"))
        self.label1 = ctk.CTkLabel(self, text=self.translate("username_label"), font=("Helvetica", 16),fg_color=("orange", "green"),corner_radius=20)
        self.entry1 = ctk.CTkEntry(self, placeholder_text=self.translate("username_label"), font=("Helvetica", 14), width=300)
        self.label2 = ctk.CTkLabel(self, text=self.translate("password_label"), font=("Helvetica", 16),fg_color=("orange", "green"),corner_radius=20)
        self.entry2 = ctk.CTkEntry(self, placeholder_text=self.translate("password_label"), show="*", font=("Helvetica", 14), width=300)
        self.button1 = ctk.CTkButton(self, text=self.translate("login_button"), command=self.login, font=("Helvetica", 14), width=150)

        self.separator = ctk.CTkLabel(self, text="―" * 30, text_color="gray")

        self.label3 = ctk.CTkLabel(self, text=self.translate("register_label"), font=("Helvetica", 14))
        self.button2 = ctk.CTkButton(self, text=self.translate("register_button"), command=self.register, font=("Helvetica", 14), width=150)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Helvetica", 12))

    def layout_widgets(self):
        self.title_label.pack(pady=(20, 10))
        self.label1.pack(pady=(10, 5))
        self.entry1.pack(pady=(0, 15))
        self.label2.pack(pady=(10, 5))
        self.entry2.pack(pady=(0, 15))
        self.button1.pack(pady=(10, 20))
        self.error_label.pack(pady=(5, 5))
        self.separator.pack(pady=(20, 10))
        self.label3.pack(pady=(5, 5))
        self.button2.pack(pady=(10, 20))

    def create_menu(self):
        self.menubar = tk.Menu(self)
        self.configure(menu=self.menubar)

        self.language_menu = tk.Menu(self.menubar, tearoff=False)
        self.language_menu.add_command(label="German", command=lambda: self.update_language("de"))
        self.language_menu.add_command(label="English", command=lambda: self.update_language("en"))

        self.settings_menu = tk.Menu(self.menubar, tearoff=False)
        self.settings_menu.add_command(label=self.translate("change_theme"), command=self.change_appearance)

        self.menubar.add_cascade(menu=self.language_menu, label=self.translate("language_menu"))
        self.menubar.add_cascade(menu=self.settings_menu, label=self.translate("settings_menu"))

    def login(self, event=None):
        username = self.entry1.get()
        password = self.entry2.get()

        if not username or not password:
            self.error_label.configure(text=self.translate("login_error"))
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.error_label.configure(text="")
            try:
                self.withdraw()  # Hide the login window
                mainpage.mainpage(parent=self, language=self.language)  # Pass `language` to `mainpage`
            except Exception as e:
                msg.showerror("Error", f"Main page could not open: {e}")
        else:
            self.error_label.configure(text=self.translate("invalid_credentials"))
            self.entry1.delete(0, ctk.END)
            self.entry2.delete(0, ctk.END)

    def register(self):
        username = self.entry1.get()
        password = self.entry2.get()

        if not username or not password:
            msg.showerror("Error", self.translate("register_error"))
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            msg.showinfo("Success", self.translate("register_success"))
            self.entry1.delete(0, ctk.END)
            self.entry2.delete(0, ctk.END)
        except sqlite3.IntegrityError:
            msg.showerror("Error", self.translate("username_taken"))
        finally:
            conn.close()

app=FirstPage()
