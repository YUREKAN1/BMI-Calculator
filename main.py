
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from bmi_calculator import calculate_bmi, classify_bmi
from database import DatabaseManager
from charts import show_bmi_chart


class BMICalculatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("650x760")
        self.root.resizable(False, False)
        self.root.configure(bg="#F4F7F6")

        self.db = None
        self.users = {}
        self.current_bmi = None
        self.current_weight = None
        self.current_height = None
        self.calculated_user_id = None

        self.setup_styles()

        try:
            self.db = DatabaseManager()
        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not initialize the database:\n{error}"
            )
            self.root.destroy()
            return

        self.create_widgets()
        self.load_users()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TButton",
            font=("Arial", 10, "bold"),
            padding=8
        )

        style.configure(
            "TEntry",
            padding=7,
            font=("Arial", 11)
        )

        style.configure(
            "TCombobox",
            padding=7,
            font=("Arial", 11)
        )

        style.configure(
            "Treeview",
            font=("Arial", 9),
            rowheight=27
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 9, "bold")
        )

    def create_widgets(self):

        tk.Label(
            self.root,
            text="BMI Calculator",
            font=("Arial", 24, "bold"),
            bg="#F4F7F6",
            fg="#263238"
        ).pack(pady=(18, 3))

        tk.Label(
            self.root,
            text="Calculate and track your Body Mass Index",
            font=("Arial", 10),
            bg="#F4F7F6",
            fg="#607D8B"
        ).pack(pady=(0, 15))

        # User selection
        user_frame = tk.Frame(
            self.root,
            bg="white",
            padx=18,
            pady=12,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        user_frame.pack(padx=30, fill="x")

        tk.Label(
            user_frame,
            text="Select User",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#37474F"
        ).pack(anchor="w")

        user_row = tk.Frame(user_frame, bg="white")
        user_row.pack(fill="x", pady=(6, 0))

        self.user_combo = ttk.Combobox(
            user_row,
            state="readonly",
            font=("Arial", 10)
        )
        self.user_combo.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        self.user_combo.bind(
            "<<ComboboxSelected>>",
            self.on_user_selected
        )

        tk.Button(
            user_row,
            text="+ Add User",
            command=self.add_user,
            font=("Arial", 9, "bold"),
            bg="#1976D2",
            fg="white",
            activebackground="#1565C0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7
        ).pack(side="right")

        # BMI inputs
        input_frame = tk.Frame(
            self.root,
            bg="white",
            padx=22,
            pady=15,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        input_frame.pack(padx=30, pady=12, fill="x")

        tk.Label(
            input_frame,
            text="Weight (kg)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#37474F"
        ).pack(anchor="w")

        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.pack(fill="x", pady=(5, 12))

        tk.Label(
            input_frame,
            text="Height (m)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#37474F"
        ).pack(anchor="w")

        self.height_entry = ttk.Entry(input_frame)
        self.height_entry.pack(fill="x", pady=(5, 15))

        self.weight_entry.bind(
            "<KeyRelease>",
            self.invalidate_result
        )
        self.height_entry.bind(
            "<KeyRelease>",
            self.invalidate_result
        )

        tk.Button(
            input_frame,
            text="Calculate BMI",
            command=self.calculate,
            font=("Arial", 10, "bold"),
            bg="#2E8B57",
            fg="white",
            activebackground="#246B45",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=9
        ).pack(fill="x")

        # BMI result
        self.result_frame = tk.Frame(
            self.root,
            bg="#F4F7F6"
        )
        self.result_frame.pack(pady=(5, 8))

        self.bmi_label = tk.Label(
            self.result_frame,
            text="Your BMI will appear here",
            font=("Arial", 15, "bold"),
            bg="#F4F7F6",
            fg="#455A64"
        )
        self.bmi_label.pack(pady=3)

        self.category_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg="#F4F7F6"
        )
        self.category_label.pack(pady=3)

        # Record and chart actions
        action_frame = tk.Frame(
            self.root,
            bg="#F4F7F6"
        )
        action_frame.pack(pady=(0, 12))

        self.save_button = tk.Button(
            action_frame,
            text="Save Record",
            command=self.save_record,
            font=("Arial", 10, "bold"),
            bg="#1976D2",
            fg="white",
            activebackground="#1565C0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=8,
            state="disabled"
        )
        self.save_button.pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="View BMI Trend",
            command=self.view_bmi_trend,
            font=("Arial", 10, "bold"),
            bg="#6A5ACD",
            fg="white",
            activebackground="#5848B5",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=8
        ).pack(side="left", padx=5)

        # BMI history
        history_frame = tk.Frame(
            self.root,
            bg="white",
            padx=12,
            pady=10,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        history_frame.pack(
            padx=30,
            pady=(0, 10),
            fill="both",
            expand=True
        )

        tk.Label(
            history_frame,
            text="BMI History",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#263238"
        ).pack(anchor="w", pady=(0, 8))

        columns = (
            "date",
            "weight",
            "height",
            "bmi",
            "category"
        )

        self.history_table = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            height=5
        )

        self.history_table.heading("date", text="Date")
        self.history_table.heading("weight", text="Weight")
        self.history_table.heading("height", text="Height")
        self.history_table.heading("bmi", text="BMI")
        self.history_table.heading("category", text="Category")

        self.history_table.column(
            "date", width=165, anchor="center"
        )
        self.history_table.column(
            "weight", width=85, anchor="center"
        )
        self.history_table.column(
            "height", width=85, anchor="center"
        )
        self.history_table.column(
            "bmi", width=65, anchor="center"
        )
        self.history_table.column(
            "category", width=105, anchor="center"
        )

        # Category colours in history
        self.history_table.tag_configure(
            "Underweight",
            foreground="#C47A00"
        )
        self.history_table.tag_configure(
            "Normal",
            foreground="#2E8B57"
        )
        self.history_table.tag_configure(
            "Overweight",
            foreground="#E67E22"
        )
        self.history_table.tag_configure(
            "Obese",
            foreground="#D32F2F"
        )

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_table.yview
        )

        self.history_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.history_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

        # Clear button
        tk.Button(
            self.root,
            text="Clear",
            command=self.clear_fields,
            font=("Arial", 9),
            bg="#CFD8DC",
            fg="#263238",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=6
        ).pack(pady=(0, 5))

        tk.Label(
            self.root,
            text="BMI is a screening measure, not a diagnosis.",
            font=("Arial", 8),
            bg="#F4F7F6",
            fg="#78909C"
        ).pack(side="bottom", pady=8)

    def load_users(self, selected_user_id=None):

        try:
            user_rows = self.db.get_users()

            self.users = {
                row["name"]: row["id"]
                for row in user_rows
            }

            names = list(self.users.keys())
            self.user_combo["values"] = names

            if selected_user_id is not None:
                selected_name = next(
                    (
                        name for name, user_id in self.users.items()
                        if user_id == selected_user_id
                    ),
                    None
                )

                if selected_name:
                    self.user_combo.set(selected_name)
                else:
                    self.user_combo.set("")

            elif names and not self.user_combo.get():
                self.user_combo.current(0)

            self.refresh_history()

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load users:\n{error}"
            )

    def add_user(self):

        name = simpledialog.askstring(
            "Add User",
            "Enter the user's name:",
            parent=self.root
        )

        if name is None:
            return

        name = name.strip()

        if not name:
            messagebox.showerror(
                "Input Error",
                "User name cannot be empty."
            )
            return

        try:
            user_id = self.db.add_user(name)

            self.load_users(selected_user_id=user_id)
            self.invalidate_result()

            messagebox.showinfo(
                "Success",
                f"User '{name}' added successfully."
            )

        except ValueError as error:
            messagebox.showerror("User Error", str(error))

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not add user:\n{error}"
            )

    def get_selected_user_id(self):

        selected_name = self.user_combo.get()

        if not selected_name:
            return None

        return self.users.get(selected_name)

    def on_user_selected(self, event=None):

        self.invalidate_result()
        self.refresh_history()

    def refresh_history(self):

        for item in self.history_table.get_children():
            self.history_table.delete(item)

        user_id = self.get_selected_user_id()

        if user_id is None:
            return

        try:
            records = self.db.get_bmi_history(user_id)

            # Newest records first
            for record in reversed(records):

                date = record["recorded_at"].replace("T", " ")

                bmi = float(record["bmi"])
                category = classify_bmi(bmi)

                self.history_table.insert(
                    "",
                    "end",
                    values=(
                        date,
                        f'{record["weight"]:.2f} kg',
                        f'{record["height"]:.2f} m',
                        f'{bmi:.2f}',
                        category
                    ),
                    tags=(category,)
                )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load BMI history:\n{error}"
            )

    def view_bmi_trend(self):

        user_id = self.get_selected_user_id()

        if user_id is None:
            messagebox.showwarning(
                "Select User",
                "Please select a user to view their BMI trend."
            )
            return

        try:
            records = self.db.get_bmi_history(user_id)
            user_name = self.user_combo.get()

            show_bmi_chart(
                parent=self.root,
                records=records,
                user_name=user_name
            )

        except Exception as error:
            messagebox.showerror(
                "Chart Error",
                f"Could not display BMI trend:\n{error}"
            )

    def invalidate_result(self, event=None):

        self.current_bmi = None
        self.current_weight = None
        self.current_height = None
        self.calculated_user_id = None

        self.save_button.config(state="disabled")

    def calculate(self):

        weight_text = self.weight_entry.get().strip()
        height_text = self.height_entry.get().strip()

        if not weight_text or not height_text:
            messagebox.showerror(
                "Input Error",
                "Please enter both weight and height."
            )
            return

        try:
            weight = float(weight_text)
            height = float(height_text)

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter valid numeric values."
            )
            return

        try:
            bmi = calculate_bmi(weight, height)
            category = classify_bmi(bmi)

        except ValueError as error:
            messagebox.showerror(
                "Input Error",
                str(error)
            )
            return

        category_colors = {
            "Underweight": "#E69500",
            "Normal": "#2E8B57",
            "Overweight": "#E67E22",
            "Obese": "#D32F2F"
        }

        color = category_colors.get(category, "#263238")

        self.bmi_label.config(
            text=f"Your BMI: {bmi:.2f}",
            fg="#263238"
        )

        self.category_label.config(
            text=f"Category: {category}",
            fg=color
        )

        self.current_bmi = bmi
        self.current_weight = weight
        self.current_height = height
        self.calculated_user_id = self.get_selected_user_id()

        if self.calculated_user_id is not None:
            self.save_button.config(state="normal")
        else:
            self.save_button.config(state="disabled")

    def save_record(self):

        user_id = self.get_selected_user_id()

        if user_id is None:
            messagebox.showwarning(
                "Select User",
                "Please add or select a user before saving."
            )
            return

        if self.current_bmi is None:
            messagebox.showwarning(
                "Calculate First",
                "Please calculate BMI before saving."
            )
            return

        if user_id != self.calculated_user_id:
            messagebox.showwarning(
                "User Changed",
                "The selected user has changed.\n"
                "Please calculate BMI again before saving."
            )
            return

        try:
            self.db.save_bmi_record(
                user_id=user_id,
                weight=self.current_weight,
                height=self.current_height,
                bmi=self.current_bmi
            )

            messagebox.showinfo(
                "Success",
                "BMI record saved successfully!"
            )

            self.refresh_history()
            self.invalidate_result()

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not save BMI record:\n{error}"
            )

    def clear_fields(self):

        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)

        self.bmi_label.config(
            text="Your BMI will appear here",
            fg="#455A64"
        )

        self.category_label.config(text="")

        self.invalidate_result()


if __name__ == "__main__":

    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
