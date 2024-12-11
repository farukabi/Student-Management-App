import sqlite3
from tkinter import ttk
from tkinter import messagebox as msg
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt

class mainpage(ctk.CTkToplevel):
    def __init__(self, parent, language="tr"):
        super().__init__()
        self.parent = parent
        self.language = language  # Use the passed language
        self.translations = {
            "de": {
                "main_page": "Startseite",
                "student_registration": "Studentenregistrierung",
                "grade_entry": "Noteneingabe",
                "attendance_entry": "Anwesenheitseingabe",
                "report": "Bericht",
                "new_registration": "Neue Registrierung",
                "first_name": "Vorname",
                "last_name": "Nachname",
                "number": "Nummer",
                "grade": "Note",
                "date": "Datum",
                "save": "Speichern",
                "error_fill_all_fields": "Bitte alle Felder ausfüllen!",
                "success_student_saved": "Student erfolgreich gespeichert!",
                "error_student_exists": "Diese Studentennummer ist bereits registriert!",
                "grades": "Noten",
                "attendance": "Anwesenheit",
                "date_format": "Datum (YYYY-MM-DD)",
                "student_not_found": "Student nicht gefunden!",
                "success_saved": "Erfolgreich gespeichert!",
                "grade_saved": "Note erfolgreich gespeichert!",
                "attendance_saved": "Anwesenheit erfolgreich gespeichert!",
                "delete": "Löschen",
                "update": "Aktualisieren",
                "export": "Exportieren",
                "graph": "Diagramm erstellen"
            },

            "en": {
                "main_page": "Main Page",
                "student_registration": "Student Registration",
                "grade_entry": "Grade Entry",
                "attendance_entry": "Attendance Entry",
                "report": "Report",
                "new_registration": "New Registration",
                "first_name": "First Name",
                "last_name": "Last Name",
                "number": "Number",
                "grade": "Grade",
                "date": "Date",
                "save": "Save",
                "error_fill_all_fields": "Please fill out all fields!",
                "success_student_saved": "Student registered successfully!",
                "error_student_exists": "This student number already exists!",
                "grades": "Grades",
                "attendance": "Attendance",
                "date_format": "Date (YYYY-MM-DD)",
                "student_not_found": "Student not found!",
                "success_saved": "Saved successfully!",
                "grade_saved": "Grade saved successfully!",
                "attendance_saved": "Attendance saved successfully!",
                "delete": "Delete",
                "update": "Update",
                "export": "Export",
                "graph": "Generate Graph"

            }
        }
        self.title(self.translate("main_page"))
        self.geometry("300x300+150+150")
        self.create_widgets()
        self.create_layout()
        self.init_db()

    def translate(self, key):
        return self.translations[self.language].get(key, key)

    def update_language(self, lang):
        self.language = lang
        self.refresh_ui()

    def refresh_ui(self):
        self.label.config(text=self.translate("main_page"))
        self.button1.config(text=self.translate("student_registration"))
        self.button2.config(text=self.translate("grade_entry"))
        self.button3.config(text=self.translate("attendance_entry"))
        self.button4.config(text=self.translate("report"))
        self.title(self.translate("main_page"))

    def init_db(self):
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            student_number TEXT UNIQUE NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number TEXT NOT NULL,
            grade TEXT NOT NULL,
            FOREIGN KEY (student_number) REFERENCES students(student_number))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (student_number) REFERENCES students(student_number))''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text=self.translate("main_page"), font=("Arial", 15))
        self.button1 = ctk.CTkButton(self, text=self.translate("student_registration"), command=self.student_reg)
        self.button2 = ctk.CTkButton(self, text=self.translate("grade_entry"), command=self.not_giris)
        self.button3 = ctk.CTkButton(self, text=self.translate("attendance_entry"), command=self.devamsizlik_girisi)
        self.button4 = ctk.CTkButton(self, text=self.translate("report"), command=self.show_report)

    def create_layout(self):
        self.label.pack(pady=(20, 0))
        self.button1.pack(pady=(20, 0))
        self.button2.pack(pady=(20, 0))
        self.button3.pack(pady=(20, 0))
        self.button4.pack(pady=(20, 0))

    def student_reg(self):
        self.win2 = ctk.CTkToplevel(self)
        self.win2.title(self.translate("student_registration"))
        self.win2.geometry("300x300")

        def close(event=None):
            self.win2.destroy()

        self.win2.bind("<Escape>", close)
        # Create a CTkFrame container
        container = ctk.CTkFrame(self.win2, corner_radius=10)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # First Name Label and Entry
        ctk.CTkLabel(container, text=self.translate("first_name"),fg_color=("green","red"),corner_radius=20).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry1 = ctk.CTkEntry(container, placeholder_text=self.translate("first_name"))
        entry1.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Last Name Label and Entry
        ctk.CTkLabel(container, text=self.translate("last_name"),fg_color=("green","red"),corner_radius=20).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry2 = ctk.CTkEntry(container, placeholder_text=self.translate("last_name"))
        entry2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Student Number Label and Entry
        ctk.CTkLabel(container, text=self.translate("number"),fg_color=("green","red"),corner_radius=20).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry3 = ctk.CTkEntry(container, placeholder_text=self.translate("number"))
        entry3.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Save Student Function
        def save_student(event=None):
            first_name = entry1.get().strip()
            last_name = entry2.get().strip()
            student_number = entry3.get().strip()

            if not first_name or not last_name or not student_number:
                msg.showerror(title="Error", message=self.translate("error_fill_all_fields"), icon="error")
                return

            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO students (first_name, last_name, student_number) VALUES (?, ?, ?)",
                               (first_name, last_name, student_number))
                conn.commit()
                msg.showinfo(title="Success", message=self.translate("success_student_saved"), icon="info")
                entry1.delete(0, ctk.END)
                entry2.delete(0, ctk.END)
                entry3.delete(0, ctk.END)
            except sqlite3.IntegrityError:
                msg.showerror(title="Error", message=self.translate("error_student_exists"), icon="error")
            finally:
                conn.close()

        # Save Button
        btn1 = ctk.CTkButton(container, text=self.translate("save"), command=save_student)
        btn1.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        self.win2.bind("<Return>", save_student)  # Bind Enter key to save action
        self.win2.grab_set()

    def not_giris(self):
        # Create a new top-level window
        self.win3 = ctk.CTkToplevel(self)
        self.win3.title(self.translate("grade_entry"))
        self.win3.geometry("300x300")
        self.win3.grab_set()
        # Create a CTkFrame container
        container = ctk.CTkFrame(self.win3, corner_radius=10)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Label and Entry for Student Number
        ctk.CTkLabel(container, text=self.translate("number"),fg_color=("green","red"),corner_radius=20).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry1 = ctk.CTkEntry(container, placeholder_text=self.translate("number"))
        entry1.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Label and Entry for Grade
        ctk.CTkLabel(container, text=self.translate("grade"),fg_color=("green","red"),corner_radius=20).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry2 = ctk.CTkEntry(container, placeholder_text=self.translate("grade"))
        entry2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Save Grade Function
        def save_grade(event=None):
            student_number = entry1.get().strip()
            grade = entry2.get().strip()

            if not student_number or not grade:
                msg.showerror(title="Error", message=self.translate("error_fill_all_fields"), icon="error")
                return

            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_number = ?", (student_number,))
            student = cursor.fetchone()

            if student:
                cursor.execute("INSERT INTO grades (student_number, grade) VALUES (?, ?)", (student_number, grade))
                conn.commit()
                msg.showinfo(title="Success", message=self.translate("grade_saved"), icon="info")
                entry1.delete(0, ctk.END)
                entry2.delete(0, ctk.END)
            else:
                msg.showerror(title="Error", message=self.translate("student_not_found"), icon="error")
            conn.close()

        # Save Button
        btn2 = ctk.CTkButton(container, text=self.translate("save"), command=save_grade)
        btn2.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Bind Enter key to save action
        self.win3.bind("<Return>", save_grade)
        def close(event=None):
            self.win3.destroy()
        self.win3.bind("<Escape>", close)
    def devamsizlik_girisi(self):
        # Create a new top-level window
        self.win4 = ctk.CTkToplevel(self)
        self.win4.title(self.translate("attendance_entry"))
        self.win4.geometry("350x300")
        self.win4.grab_set()
        def close (event=None):
            self.win4.destroy()

        self.win4.bind("<Escape>", close)
        # Create a CTkFrame container
        container = ctk.CTkFrame(self.win4, corner_radius=10)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Label and Entry for Student Number
        ctk.CTkLabel(container, text=self.translate("number"),fg_color=("green","red"),corner_radius=20).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry1 = ctk.CTkEntry(container, placeholder_text=self.translate("number"))
        entry1.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Label and Entry for Date
        ctk.CTkLabel(container, text=self.translate("date_format"),fg_color=("green","red"),corner_radius=20).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        entry2 = ctk.CTkEntry(container, placeholder_text=self.translate("date_format"))
        entry2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Save Attendance Function
        def save_attendance(event=None):
            student_number = entry1.get().strip()
            date = entry2.get().strip()

            if not student_number or not date:
                msg.showerror(title="Error", message=self.translate("error_fill_all_fields"), icon="error")
                return

            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_number = ?", (student_number,))
            student = cursor.fetchone()

            if student:
                cursor.execute("INSERT INTO attendance (student_number, date) VALUES (?, ?)", (student_number, date))
                conn.commit()
                msg.showinfo(title="Success", message=self.translate("attendance_saved"), icon="info")
                entry1.delete(0, ctk.END)
                entry2.delete(0, ctk.END)
            else:
               msg.showerror(title="Error", message=self.translate("student_not_found"), icon="error")
            conn.close()

        # Save Button
        btn3 = ctk.CTkButton(container, text=self.translate("save"), command=save_attendance)
        btn3.grid(row=2, column=0, columnspan=2, padx=10, pady=10,sticky="w")

        # Bind Enter key to save action
        self.win4.bind("<Return>", save_attendance)

    def show_report(self):
        # Create a new top-level window
        self.win5 = ctk.CTkToplevel(self)
        self.win5.geometry("800x400")
        self.win5.title(self.translate("report"))
        self.win5.grab_set()
        # Create a CTkFrame container
        container = ctk.CTkFrame(self.win5, corner_radius=10)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Create a CTkTreeview for displaying data
        tree = ttk.Treeview(container, columns=("Numara", "Ad Soyad", "Notlar", "Devamsızlık"), show="headings")
        tree.heading("Numara", text=self.translate("number"))
        tree.heading("Ad Soyad", text=f"{self.translate('first_name')} {self.translate('last_name')}")
        tree.heading("Notlar", text=self.translate("grades"))
        tree.heading("Devamsızlık", text=self.translate("attendance"))
        tree.pack(fill="both", expand=True)
        def close(event=None):
            self.win5.destroy()
        self.win5.bind("<Escape>",close)
        # Load data from the database
        def load_data():
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT 
                    s.student_number, 
                    s.first_name || ' ' || s.last_name AS full_name,
                    COALESCE(g.grades, '') AS grades,
                    COALESCE(a.attendance, '') AS attendance
                FROM 
                    students s
                LEFT JOIN 
                    (SELECT student_number, GROUP_CONCAT(grade, ', ') AS grades 
                     FROM grades 
                     GROUP BY student_number) g ON s.student_number = g.student_number
                LEFT JOIN 
                    (SELECT student_number, GROUP_CONCAT(date, ', ') AS attendance 
                     FROM attendance 
                     GROUP BY student_number) a ON s.student_number = a.student_number
            ''')

            rows = cursor.fetchall()
            for i in tree.get_children():
                tree.delete(i)  # Clear existing data
            for row in rows:
                tree.insert("", "end", values=row)

            conn.close()
            return rows  # Return data for export

        data = load_data()  # Load data and store it for exporting

        # Delete selected record
        def delete_record():
            selected_item = tree.selection()
            if not selected_item:
                msg.showerror(title="Error", message=self.translate("student_not_found"), icon="error")
                return

            record = tree.item(selected_item)["values"]
            student_number = record[0]

            confirm = msg.askyesno("Confirm", f"Do you want to delete the record for student {student_number}?")
            if not confirm:
                return

            try:
                conn = sqlite3.connect('school.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE student_number = ?", (student_number,))
                cursor.execute("DELETE FROM grades WHERE student_number = ?", (student_number,))
                cursor.execute("DELETE FROM attendance WHERE student_number = ?", (student_number,))
                conn.commit()
                conn.close()

                load_data()  # Refresh the table
                msg.showinfo(title="Success", message=f"Record for student {student_number} deleted successfully!")
            except Exception as e:
                msg.showerror(title="Error", message=f"An error occurred: {e}", icon="error")

        # Update selected record
        def update_record():
            selected_item = tree.selection()
            if not selected_item:
                msg.showerror(title="Error", message=self.translate("student_not_found"), icon="error")
                return

            record = tree.item(selected_item)["values"]
            student_number = record[0]

            update_window = ctk.CTkToplevel(self.win5)
            update_window.title(f"Update Record - {student_number}")
            update_window.geometry("400x600")

            container = ctk.CTkFrame(update_window, corner_radius=10)
            container.pack(side="top", fill="both", expand=True, padx=10, pady=10)

            # First Name
            ctk.CTkLabel(container, text=self.translate("first_name")).grid(row=0, column=0, padx=10, pady=10)
            entry1 = ctk.CTkEntry(container)
            entry1.grid(row=0, column=1, padx=10, pady=10)
            entry1.insert(0, record[1].split()[0])  # Pre-fill with current data

            # Last Name
            ctk.CTkLabel(container, text=self.translate("last_name")).grid(row=1, column=0, padx=10, pady=10)
            entry2 = ctk.CTkEntry(container)
            entry2.grid(row=1, column=1, padx=10, pady=10)
            entry2.insert(0, record[1].split()[1])  # Pre-fill with current data

            # Grades
            ctk.CTkLabel(container, text=self.translate("grades")).grid(row=2, column=0, padx=10, pady=10)
            grades_entry = ctk.CTkEntry(container)
            grades_entry.grid(row=2, column=1, padx=10, pady=10)
            grades_entry.insert(0, record[2])  # Pre-fill with current grades

            # Attendance Section
            ctk.CTkLabel(container, text=self.translate("attendance")).grid(row=3, column=0, padx=10, pady=10)

            attendance_frame = ctk.CTkScrollableFrame(container, corner_radius=10)
            attendance_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
            attendance_dates = record[3].split(",") if record[3] else []
            attendance_widgets = []

            # Populate attendance dates as editable entries
            for date in attendance_dates:
                date_entry = ctk.CTkEntry(attendance_frame)
                date_entry.insert(0, date.strip())
                date_entry.pack(fill="x", padx=5, pady=2)
                attendance_widgets.append(date_entry)

            # Add new date entry
            def add_date():
                new_date_entry = ctk.CTkEntry(attendance_frame, placeholder_text=self.translate("date_format"))
                new_date_entry.pack(fill="x", padx=5, pady=2)
                attendance_widgets.append(new_date_entry)

            # Save updates
            def save_update():
                first_name = entry1.get().strip()
                last_name = entry2.get().strip()
                grades_input = grades_entry.get().strip()
                updated_dates = [entry.get().strip() for entry in attendance_widgets if entry.get().strip()]

                if not first_name or not last_name or not grades_input:
                    msg.showerror(title="Error", message=self.translate("error_fill_all_fields"), icon="error")
                    return

                try:
                    # Validate grades as integers
                    grades_list = [int(grade.strip()) for grade in grades_input.split(",") if grade.strip()]
                    if any(grade < 0 or grade > 100 for grade in grades_list):
                        raise ValueError("Grades out of range (0-100).")

                    # Validate attendance dates only if there are any
                    if updated_dates:
                        pd.to_datetime(updated_dates, format="%Y-%m-%d")
                except ValueError as e:
                    msg.showerror(title="Error", message=str(e), icon="error")
                    return

                try:
                    conn = sqlite3.connect('school.db')
                    cursor = conn.cursor()

                    # Update student details
                    cursor.execute(
                        "UPDATE students SET first_name = ?, last_name = ? WHERE student_number = ?",
                        (first_name, last_name, student_number)
                    )

                    # Clear and insert updated grades
                    cursor.execute("DELETE FROM grades WHERE student_number = ?", (student_number,))
                    for grade in grades_list:
                        cursor.execute("INSERT INTO grades (student_number, grade) VALUES (?, ?)",
                                       (student_number, grade))

                    # Clear and insert updated attendance if not empty
                    cursor.execute("DELETE FROM attendance WHERE student_number = ?", (student_number,))
                    if updated_dates:  # Only insert attendance if there are dates
                        for date in updated_dates:
                            cursor.execute("INSERT INTO attendance (student_number, date) VALUES (?, ?)",
                                           (student_number, date))

                    conn.commit()
                    conn.close()

                    load_data()  # Refresh data
                    update_window.destroy()
                    msg.showinfo(title="Success", message=f"Record updated successfully for {student_number}!")
                except Exception as e:
                    msg.showerror(title="Error", message=f"An error occurred: {e}", icon="error")

            # Buttons for adding attendance dates and saving changes
            ctk.CTkButton(container, text=self.translate("add_date"), command=add_date).grid(row=4, column=0, padx=10,
                                                                                             pady=10)
            ctk.CTkButton(container, text=self.translate("save"), command=save_update).grid(row=4, column=1, padx=10,
                                                                                            pady=10)
        # Export data to Excel
        def export_to_excel():
            if not data:
                msg.showerror(title="Error", message="No data to export!", icon="error")
                return

            df = pd.DataFrame(data, columns=["Student Number", "Full Name", "Grades", "Attendance"])
            filename = "Student_Report.xlsx"
            df.to_excel(filename, index=False)
            msg.showinfo(title="Success", message=f"Data exported to {filename}!")

        # Generate Grade Chart
        def generate_grade_chart():
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT s.student_number, s.first_name || ' ' || s.last_name AS full_name,
                       AVG(CAST(g.grade AS FLOAT)) AS avg_grade
                FROM students s
                LEFT JOIN grades g ON s.student_number = g.student_number
                GROUP BY s.student_number
                HAVING avg_grade IS NOT NULL
            ''')

            chart_data = cursor.fetchall()
            conn.close()

            if not chart_data:
                msg.showerror(title="Error", message="No grades available for chart generation!",
                                  icon="error")
                return

            # Prepare data for plotting
            student_names = [row[1] for row in chart_data]
            avg_grades = [row[2] for row in chart_data]

            # Plotting
            plt.figure(figsize=(10, 6))
            plt.bar(student_names, avg_grades, alpha=0.7)
            plt.xlabel('Student Names')
            plt.ylabel('Average Grades')
            plt.title('Average Grades by Student')
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()

        # Buttons for Delete, Update, Export, and Chart
        btn_frame = ctk.CTkFrame(self.win5)
        btn_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(btn_frame, text=self.translate("delete"), command=delete_record).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.translate("update"), command=update_record).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.translate("export"), command=export_to_excel).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.translate("graph"), command=generate_grade_chart).pack(side="left", padx=5)




