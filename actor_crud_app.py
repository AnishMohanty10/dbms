import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Database connection configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "MovieProduction",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


class ActorCRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MovieProduction - Actor Management System")
        self.root.geometry("820x620")
        self.root.minsize(750, 550)

        # Style configuration
        self.setup_styles()

        # Build UI layout
        self.create_widgets()

        # Initial read of existing data
        self.read_records()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Global fonts and colors
        style.configure(".", font=("Helvetica", 11))
        style.configure("TLabel", font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), foreground="#1e293b")
        style.configure("SubHeader.TLabel", font=("Helvetica", 10), foreground="#64748b")
        style.configure("Card.TFrame", background="#f8fafc", relief="solid", borderwidth=1)

        # Button styles
        style.configure("Create.TButton", font=("Helvetica", 10, "bold"), background="#10b981", foreground="white")
        style.configure("Read.TButton", font=("Helvetica", 10, "bold"), background="#3b82f6", foreground="white")
        style.configure("Update.TButton", font=("Helvetica", 10, "bold"), background="#f59e0b", foreground="white")
        style.configure("Delete.TButton", font=("Helvetica", 10, "bold"), background="#ef4444", foreground="white")
        style.configure("Clear.TButton", font=("Helvetica", 10), background="#6b7280", foreground="white")

    def create_widgets(self):
        main_container = ttk.Frame(self.root, padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header_frame, text="Actor Database Manager", style="Header.TLabel").pack(anchor=tk.W)
        ttk.Label(header_frame, text="Connected to MySQL: MovieProduction.ACTOR", style="SubHeader.TLabel").pack(anchor=tk.W)

        # Form Frame (Inputs)
        form_frame = ttk.LabelFrame(main_container, text=" Actor Information ", padding=15)
        form_frame.pack(fill=tk.X, pady=(0, 15))

        labels = ["Actor ID:", "Actor Name:", "Gender:", "Nationality:", "Fee ($):"]
        self.entries = {}

        for i, text in enumerate(labels):
            field_name = text.replace(":", "").replace(" ($)", "").replace(" ", "_")
            lbl = ttk.Label(form_frame, text=text, width=14, anchor=tk.W)
            lbl.grid(row=i, column=0, padx=5, pady=4, sticky=tk.W)

            entry = ttk.Entry(form_frame, width=45)
            entry.grid(row=i, column=1, padx=5, pady=4, sticky=tk.EW)
            self.entries[field_name] = entry

        form_frame.columnconfigure(1, weight=1)

        # Buttons Frame
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(0, 15))

        btn_create = ttk.Button(button_frame, text="➕ Create", style="Create.TButton", command=self.create_record)
        btn_create.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)

        btn_read = ttk.Button(button_frame, text="🔄 Read (Refresh)", style="Read.TButton", command=self.read_records)
        btn_read.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)

        btn_update = ttk.Button(button_frame, text="✏️ Update", style="Update.TButton", command=self.update_record)
        btn_update.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)

        btn_delete = ttk.Button(button_frame, text="🗑️ Delete", style="Delete.TButton", command=self.delete_record)
        btn_delete.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)

        btn_clear = ttk.Button(button_frame, text="🧹 Clear Fields", style="Clear.TButton", command=self.clear_fields)
        btn_clear.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)

        # Records Display Frame (Listbox)
        list_frame = ttk.LabelFrame(main_container, text=" Actor Records ", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Header row for the listbox
        header_text = f"{'ID':<10} | {'Name':<25} | {'Gender':<12} | {'Nationality':<20} | {'Fee ($)':<12}"
        header_label = tk.Label(
            list_frame,
            text=header_text,
            font=("Courier", 11, "bold"),
            bg="#e2e8f0",
            fg="#1e293b",
            anchor="w",
            padx=6,
            pady=4,
        )
        header_label.pack(fill=tk.X)

        # Listbox with Scrollbars
        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack(fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(listbox_container, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(listbox_container, orient=tk.HORIZONTAL)

        self.record_listbox = tk.Listbox(
            listbox_container,
            font=("Courier", 11),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            activestyle="none",
            selectbackground="#93c5fd",
            selectforeground="#1e293b",
            relief="flat",
            highlightthickness=1,
            highlightcolor="#cbd5e1",
        )

        scrollbar_y.config(command=self.record_listbox.yview)
        scrollbar_x.config(command=self.record_listbox.xview)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.record_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Selecting a row populates entry fields
        self.record_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Helvetica", 9),
            bg="#f1f5f9",
            fg="#475569",
            padx=10,
            pady=3,
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Internal cache of retrieved rows for easy selection handling
        self.cached_records = []

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries["Actor_ID"].focus_set()
        self.status_var.set("Form cleared.")

    def validate_inputs(self, check_all=True):
        actor_id_str = self.entries["Actor_ID"].get().strip()
        name = self.entries["Actor_Name"].get().strip()
        gender = self.entries["Gender"].get().strip()
        nationality = self.entries["Nationality"].get().strip()
        fee_str = self.entries["Fee"].get().strip()

        if not actor_id_str:
            messagebox.showwarning("Validation Error", "Actor_ID is required.")
            self.entries["Actor_ID"].focus_set()
            return None

        try:
            actor_id = int(actor_id_str)
        except ValueError:
            messagebox.showwarning("Validation Error", "Actor_ID must be a valid integer.")
            self.entries["Actor_ID"].focus_set()
            return None

        fee = None
        if fee_str:
            try:
                fee = float(fee_str)
            except ValueError:
                messagebox.showwarning("Validation Error", "Fee must be a valid number.")
                self.entries["Fee"].focus_set()
                return None

        if check_all and not name:
            messagebox.showwarning("Validation Error", "Actor Name is required.")
            self.entries["Actor_Name"].focus_set()
            return None

        return {
            "Actor_ID": actor_id,
            "ActorName": name,
            "Gender": gender,
            "Nationality": nationality,
            "Fee": fee,
        }

    def create_record(self):
        data = self.validate_inputs(check_all=True)
        if not data:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO ACTOR (Actor_ID, ActorName, Gender, Nationality, Fee)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (data["Actor_ID"], data["ActorName"], data["Gender"], data["Nationality"], data["Fee"]),
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", f"Actor record {data['Actor_ID']} created successfully!")
            self.status_var.set(f"Record with ID {data['Actor_ID']} inserted.")
            self.clear_fields()
            self.read_records()
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to create record:\n{err}")
            self.status_var.set("Error during record creation.")

    def read_records(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Actor_ID, ActorName, Gender, Nationality, Fee FROM ACTOR ORDER BY Actor_ID ASC")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            self.record_listbox.delete(0, tk.END)
            self.cached_records = rows

            for row in rows:
                actor_id = row[0]
                name = row[1] if row[1] is not None else ""
                gender = row[2] if row[2] is not None else ""
                nationality = row[3] if row[3] is not None else ""
                fee = f"{row[4]:.2f}" if row[4] is not None else "0.00"

                formatted_line = f"{str(actor_id):<10} | {name:<25} | {gender:<12} | {nationality:<20} | {fee:<12}"
                self.record_listbox.insert(tk.END, formatted_line)

            self.status_var.set(f"Loaded {len(rows)} records from database.")
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to read records:\n{err}")
            self.status_var.set("Error fetching records.")

    def update_record(self):
        data = self.validate_inputs(check_all=True)
        if not data:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                UPDATE ACTOR
                SET ActorName = %s, Gender = %s, Nationality = %s, Fee = %s
                WHERE Actor_ID = %s
            """
            cursor.execute(
                query,
                (data["ActorName"], data["Gender"], data["Nationality"], data["Fee"], data["Actor_ID"]),
            )
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            conn.close()

            if affected == 0:
                messagebox.showwarning("Warning", f"No record found with Actor_ID = {data['Actor_ID']}.")
                self.status_var.set(f"Actor_ID {data['Actor_ID']} not found.")
            else:
                messagebox.showinfo("Success", f"Actor record {data['Actor_ID']} updated successfully!")
                self.status_var.set(f"Record {data['Actor_ID']} updated.")
                self.read_records()
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to update record:\n{err}")
            self.status_var.set("Error during record update.")

    def delete_record(self):
        actor_id_str = self.entries["Actor_ID"].get().strip()
        if not actor_id_str:
            messagebox.showwarning("Warning", "Please specify an Actor_ID to delete.")
            self.entries["Actor_ID"].focus_set()
            return

        try:
            actor_id = int(actor_id_str)
        except ValueError:
            messagebox.showwarning("Validation Error", "Actor_ID must be a valid integer.")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete Actor with ID {actor_id}?",
        )
        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ACTOR WHERE Actor_ID = %s", (actor_id,))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            conn.close()

            if affected == 0:
                messagebox.showwarning("Warning", f"No record found with Actor_ID = {actor_id}.")
                self.status_var.set(f"Actor_ID {actor_id} not found.")
            else:
                messagebox.showinfo("Success", f"Actor record {actor_id} deleted successfully!")
                self.status_var.set(f"Record {actor_id} deleted.")
                self.clear_fields()
                self.read_records()
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to delete record:\n{err}")
            self.status_var.set("Error during record deletion.")

    def on_listbox_select(self, event):
        selection = self.record_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index < len(self.cached_records):
            record = self.cached_records[index]
            self.clear_fields()
            self.entries["Actor_ID"].insert(0, str(record[0]))
            if record[1] is not None:
                self.entries["Actor_Name"].insert(0, str(record[1]))
            if record[2] is not None:
                self.entries["Gender"].insert(0, str(record[2]))
            if record[3] is not None:
                self.entries["Nationality"].insert(0, str(record[3]))
            if record[4] is not None:
                self.entries["Fee"].insert(0, str(record[4]))
            self.status_var.set(f"Selected Actor_ID: {record[0]}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ActorCRUDApp(root)
    root.mainloop()
