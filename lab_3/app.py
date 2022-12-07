import customtkinter
from btree import BTree


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.tree = BTree(25)

        self.title("B-Tree DBMS")
        self.geometry("1080x720")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        self.searh_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=("#EBEBEC", "#212325"))
        self.searh_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.searh_frame.grid(row=0, column=0, sticky="nsew")

        customtkinter.CTkLabel(self.searh_frame, width=60, text="Key:").grid(row=0, column=0, padx=10, pady=10)

        self.search_key_v = customtkinter.StringVar(value="")
        self.search_key = customtkinter.CTkEntry(self.searh_frame, textvariable=self.search_key_v, width=80)
        self.search_key.grid(row=0, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(self.searh_frame, width=80, text="Value:").grid(row=0, column=2, padx=10, pady=10)

        self.search_value_v = customtkinter.StringVar(value="")
        self.search_value = customtkinter.CTkEntry(self.searh_frame, textvariable=self.search_value_v, width=200, state="disabled")
        self.search_value.grid(row=0, column=3, padx=10, pady=10)

        customtkinter.CTkButton(self.searh_frame, text="Search!", command=self.search).grid(row=0, column=4, padx=10, pady=10)


        self.input_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.input_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.input_frame.grid(row=1, column=0, sticky="nsew")

        customtkinter.CTkLabel(self.input_frame, width=60, text="Key:").grid(row=0, column=0, padx=10, pady=10)

        self.insert_key_v = customtkinter.StringVar(value="")
        self.insert_key = customtkinter.CTkEntry(self.input_frame, textvariable=self.insert_key_v, width=80)
        self.insert_key.grid(row=0, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(self.input_frame, width=80, text="Value:").grid(row=0, column=2, padx=10, pady=10)

        self.insert_value_v = customtkinter.StringVar(value="")
        self.insert_value = customtkinter.CTkEntry(self.input_frame, textvariable=self.insert_value_v, width=200)
        self.insert_value.grid(row=0, column=3, padx=10, pady=10)

        customtkinter.CTkButton(self.input_frame, text="Insert!", command=self.insert).grid(row=0, column=4, padx=10, pady=10)


        self.edit_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=("#EBEBEC", "#212325"))
        self.edit_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.edit_frame.grid(row=2, column=0, sticky="nsew")

        customtkinter.CTkLabel(self.edit_frame, width=60, text="Key:").grid(row=0, column=0, padx=10, pady=10)

        self.edit_key_v = customtkinter.StringVar(value="")
        self.edit_key = customtkinter.CTkEntry(self.edit_frame, textvariable=self.edit_key_v, width=80)
        self.edit_key.grid(row=0, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(self.edit_frame, width=80, text="Value:").grid(row=0, column=2, padx=10, pady=10)

        self.edit_value_v = customtkinter.StringVar(value="")
        self.edit_value = customtkinter.CTkEntry(self.edit_frame, textvariable=self.edit_value_v, width=200)
        self.edit_value.grid(row=0, column=3, padx=10, pady=10)

        customtkinter.CTkButton(self.edit_frame, text="Edit!", command=self.edit).grid(row=0, column=4, padx=10, pady=10)


        self.delete_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.delete_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.delete_frame.grid(row=3, column=0, sticky="nsew")

        customtkinter.CTkLabel(self.delete_frame, width=60, text="Key:").grid(row=0, column=0, padx=10, pady=10)

        self.delete_key_v = customtkinter.StringVar(value="")
        self.delete_key = customtkinter.CTkEntry(self.delete_frame, textvariable=self.delete_key_v, width=80)
        self.delete_key.grid(row=0, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(self.delete_frame, width=80, text="Value:").grid(row=0, column=2, padx=10, pady=10)

        self.delete_value_v = customtkinter.StringVar(value="")
        self.delete_value = customtkinter.CTkEntry(self.delete_frame, textvariable=self.delete_value_v, width=200, state="disabled")
        self.delete_value.grid(row=0, column=3, padx=10, pady=10)

        customtkinter.CTkButton(self.delete_frame, text="Delete!", command=self.delete).grid(row=0, column=4, padx=10, pady=10)

        customtkinter.CTkLabel(self, width=40, text="Log:").grid(row=4, column=0, sticky="W")
        self.logbox = customtkinter.CTkTextbox(self, text_font=("Arial", 7))
        self.logbox.grid(row=5, column=0, sticky="nsew", padx=10)

        customtkinter.CTkLabel(self, width=60, text="Schema:").grid(row=6, column=0, sticky="W")
        self.schema = customtkinter.CTkTextbox(self, text_font=("Arial", 8))
        self.schema.grid(row=7, column=0, sticky="nsew", padx=10, pady=(0, 20))

    def search(self):
        try:
            self.log(f"Search:\tKey: {self.search_key_v.get()}")
            r = self.tree.search(int(self.search_key_v.get()))
            if r:
                self.search_value_v.set(r)
                self.log("\nSuccessfull")
            else:
                self.search_value_v.set("")
                self.log("\nKey is not found")
        except Exception:
            self.log("\nError")

    def insert(self):
        try:
            self.log(f"Insert:\tKey: {self.insert_key_v.get()}\tValue: {self.insert_value_v.get()}")
            if self.tree.search(int(self.insert_key_v.get())):
                self.log("\nKey is already in tree")
            else:
                self.tree.insert((int(self.insert_key_v.get()), *self.insert_value_v.get().split(" ")))
                self.update_schema()
                self.log("\nSuccessfull")
                self.insert_value_v.set("")
                self.insert_key_v.set("")
        except Exception:
            self.log("\nError")

    def edit(self):
        try:
            self.log(f"Edit:\tKey: {self.edit_key_v.get()}\tNew value: {self.edit_value_v.get()}")
            if self.tree.edit((int(self.edit_key_v.get()), *self.edit_value_v.get().split(" "))):
                self.log("\nSuccessfull")
                self.edit_value_v.set("")
            else:
                self.log("\nKey is not in tree")
        except Exception:
            self.log("\nError")

    def delete(self):
        try:
            self.log(f"Delete\tKey: {self.delete_key_v.get()}")
            if self.tree.delete(int(self.delete_key_v.get())):
                self.log("\nSuccessfull")
                self.delete_key_v.set("")
                self.update_schema()
            else:
                self.log("\nKey is not in tree")
        except Exception:
            self.log("\nError")

    def log(self, s):
        self.logbox.insert("0.0", s + "\n")

    def update_schema(self):
        self.schema.delete('0.0', "end")
        self.schema.insert("end", self.tree)
