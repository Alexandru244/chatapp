import tkinter as tk
from tkinter import ttk

from chat_app.settings import USER_NAME
from client.contacts import get_contacts
from client.disussion import create_new_discussion


class DiscussionList(tk.Frame):
    def __init__(self, master=None, user_id=None):
        super().__init__(master)
        master.grid(row=0, column=0, sticky="ns")
        self.master = master

        self.listbox_discussions = None
        self.new_discussion_btn = None

        self.user_id = user_id
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text=f"{USER_NAME}", font=("Arial", 12, "bold"), pady=5, bg="#121212", fg="white")
        label.pack(fill=tk.X, padx=10, pady=(10, 0))

        self.new_discussion_btn = tk.Button(
            self, text="New Chat", command=self.open_contact_popup, font=("Arial", 12, "bold"), bg="#1D3461",
            fg="white", relief=tk.FLAT
        )
        self.new_discussion_btn.pack(fill=tk.X, padx=10, pady=10)

        self.listbox_discussions = ttk.Treeview(self, selectmode="browse", columns=2)
        self.listbox_discussions.heading("#0", text="Discussions")
        self.listbox_discussions.heading("#1", text="Status")
        self.listbox_discussions.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def open_contact_popup(self):
        contact_popup = tk.Toplevel(self)
        contact_popup.title("Select a Contact")

        contact_listbox = ttk.Treeview(contact_popup, selectmode="extended")
        contact_listbox.heading("#0", text="Select a contact")

        contacts = get_contacts()
        for contact in contacts:
            contact_listbox.insert('', 'end', text=contact["name"], values=(contact["id"]))

        contact_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

        def add_selected_contact():
            selected_contacts = []
            selected_names = []
            curr_items = contact_listbox.selection()

            if curr_items:
                for i in curr_items:
                    contacts_id = contact_listbox.item(i)["values"]
                    contacts_names = contact_listbox.item(i)["text"]
                    selected_contacts.extend(contacts_id)
                    selected_names.append(contacts_names)

                group_name = group_name_entry.get("1.0", "end-1c")

                # the reload happens with websockets
                create_new_discussion(self.user_id, selected_contacts, group_name)

                contact_popup.destroy()

        group_name_label = tk.Label(contact_popup, text="Group name", font=("Arial", 12, "bold"))
        group_name_label.pack(fill=tk.X, padx=10)
        group_name_entry = tk.Text(contact_popup, height=1.2, width=5, bg="white", fg="black", font=("Arial", 12))
        group_name_entry.pack(fill=tk.X, padx=10, pady=10)

        submit_button = tk.Button(
            contact_popup, text="Submit", command=add_selected_contact, font=("Arial", 12, "bold"), bg="#1D3461",
            fg="white", relief="flat"
        )
        submit_button.pack(pady=10)