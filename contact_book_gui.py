import tkinter as tk
from tkinter import messagebox, simpledialog
from contact_book import load_contacts, save_contacts


class ContactBookGUI:
    """Pastel‑themed contact‑book GUI with create / read / update / delete."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("1000x500")
        self.root.configure(bg="#fcefee")  # overall pastel background

        # Load existing data
        self.contacts = load_contacts()

        # Build UI
        self._create_widgets()

    # ─────────────────────────────────────────────────────────────────────────────
    #  WIDGETS
    # ─────────────────────────────────────────────────────────────────────────────
    def _create_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#fcefee")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Buttons
        btn_add = tk.Button(
            main_frame,
            text="Add Contact",
            command=self.add_contact,
            width=50,
            bg="#e5d4ed",
        )
        btn_view = tk.Button(
            main_frame,
            text="View Contacts",
            command=self.view_contacts,
            width=50,
            bg="#d6eaf8",
        )
        btn_search = tk.Button(
            main_frame,
            text="Search Contacts",
            command=self.search_contact,
            width=50,
            bg="#fdebd0",
        )
        btn_update = tk.Button(
            main_frame,
            text="Update Contact",
            command=self.update_contact,
            width=50,
            bg="#d4efdf",
        )
        btn_delete = tk.Button(
            main_frame,
            text="Delete Contact",
            command=self.delete_contact,
            width=50,
            bg="#f9e79f",
        )
        btn_exit = tk.Button(
            main_frame, text="Exit", command=self.root.quit, width=20, bg="#f5b7b1"
        )

        # Layout
        for b in (btn_add, btn_view, btn_search, btn_update, btn_delete, btn_exit):
            b.pack(pady=5)

        # Text area
        self.text_display = tk.Text(main_frame, height=45, width=400, bg="#fef9e7")
        self.text_display.pack(pady=10)

    # ─────────────────────────────────────────────────────────────────────────────
    #  CRUD FUNCTIONS
    # ─────────────────────────────────────────────────────────────────────────────
    def add_contact(self):
        """Collect fields in a single pastel form (Toplevel)."""

        form = tk.Toplevel(self.root)
        form.title("Add Contact")
        form.geometry("300x250")
        form.configure(bg="#fef6fb")
        form.resizable(False, False)
        form.grab_set()  # modal

        # Field helpers
        def _label(text):
            return tk.Label(form, text=text, bg="#fef6fb")

        _label("Name:").pack(pady=(15, 5))
        name_entry = tk.Entry(form, width=30)
        name_entry.pack()

        _label("Phone:").pack(pady=5)
        phone_entry = tk.Entry(form, width=30)
        phone_entry.pack()

        _label("Email:").pack(pady=5)
        email_entry = tk.Entry(form, width=30)
        email_entry.pack()

        def submit():
            name, phone, email = (
                name_entry.get().strip(),
                phone_entry.get().strip(),
                email_entry.get().strip(),
            )

            if not name or not phone or not email:
                messagebox.showerror("Error", "All fields are required.", parent=form)
                return

            self.contacts.append({"name": name, "phone": phone, "email": email})
            save_contacts(self.contacts)
            messagebox.showinfo("Success", f"{name} has been added!", parent=form)
            form.destroy()
            self.view_contacts()

        tk.Button(form, text="Save Contact", command=submit, bg="#d8e2dc", width=20).pack(
            pady=15
        )

    # ─────────────────────────────────────────────────────────────────────────────
    def view_contacts(self):
        self.text_display.delete(1.0, tk.END)
        if not self.contacts:
            self.text_display.insert(tk.END, "No contacts found!")
            return
        for i, c in enumerate(self.contacts, 1):
            self.text_display.insert(
                tk.END,
                f"{i}. {c['name']}\n   Phone: {c['phone']}\n   Email: {c['email']}\n\n",
            )

    # ─────────────────────────────────────────────────────────────────────────────
    def search_contact(self):
        term = simpledialog.askstring("Search Contacts", "Enter name to search:")
        if not term:
            return
        matches = [c for c in self.contacts if term.lower() in c["name"].lower()]
        self.text_display.delete(1.0, tk.END)
        if not matches:
            self.text_display.insert(tk.END, "No matching contacts found!")
            return
        self.text_display.insert(tk.END, f"Found {len(matches)} contact(s):\n\n")
        for c in matches:
            self.text_display.insert(
                tk.END, f"Name: {c['name']}\nPhone: {c['phone']}\nEmail: {c['email']}\n\n"
            )

    # ─────────────────────────────────────────────────────────────────────────────
    def update_contact(self):
        name = simpledialog.askstring("Update Contact", "Enter name of contact to update:")
        if not name:
            return
        for c in self.contacts:
            if c["name"].lower() == name.lower():
                new_phone = simpledialog.askstring(
                    "Update Contact", "Enter new phone:", initialvalue=c["phone"]
                )
                new_email = simpledialog.askstring(
                    "Update Contact", "Enter new email:", initialvalue=c["email"]
                )
                if new_phone:
                    c["phone"] = new_phone.strip()
                if new_email:
                    c["email"] = new_email.strip()
                save_contacts(self.contacts)
                messagebox.showinfo("Success", f"{name}'s contact has been updated!")
                self.view_contacts()
                return
        messagebox.showerror("Error", "Contact not found!")

    # ─────────────────────────────────────────────────────────────────────────────
    def delete_contact(self):
        name = simpledialog.askstring("Delete Contact", "Enter name of contact to delete:")
        if not name:
            return
        for i, c in enumerate(self.contacts):
            if c["name"].lower() == name.lower():
                if messagebox.askyesno("Confirm Delete", f"Delete {name}?"):
                    self.contacts.pop(i)
                    save_contacts(self.contacts)
                    messagebox.showinfo("Deleted", f"{name} has been deleted!")
                    self.view_contacts()
                return
        messagebox.showerror("Error", "Contact not found!")


if __name__ == "__main__":
    root = tk.Tk()
    ContactBookGUI(root)
    root.mainloop()
