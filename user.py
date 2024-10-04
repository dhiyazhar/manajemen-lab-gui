import os
import csv
import customtkinter
import tkinter.ttk as ttk
from penggunaan import Button, CustomTreeviewStyle

class User(customtkinter.CTkFrame): 
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.file_path = "./data/user.csv"

        self.grid_columnconfigure(0, weight=1)  # Biar label memenuhi horizontal
        self.grid_rowconfigure(1, weight=1) # Button frame tidak perlu melar

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 0)) 
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="kolom") 

        self.b_add_user = Button(self.button_frame, text="Tambah User") 
        self.b_delete_user = Button(self.button_frame, text="Hapus User")
        self.b_edit_user = Button(self.button_frame, text="Edit User")

        self.b_add_user.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 
        self.b_delete_user.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 
        self.b_edit_user.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.user_table_frame = customtkinter.CTkFrame(self)
        self.user_table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Buat Treeview di dalam tabel_pengguna_frame
        self.table_wrapper = customtkinter.CTkFrame(self.user_table_frame)
        self.table_wrapper.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.user_table = ttk.Treeview(self.table_wrapper, style="Treeview", selectmode="browse")
        self.user_table['show'] = 'headings'
        self.user_table.pack(fill="both", expand=True)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        style = CustomTreeviewStyle()
        self.load_data()
        

    def hide(self):
        self.grid_remove()
        
    def load_data(self):
        self.user_table.delete(*self.user_table.get_children())
        
        try: 
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file) 
                print(reader.fieldnames)
                self.user_table['columns'] = tuple(reader.fieldnames)
                
                max_width = {col: len(col) for col in reader.fieldnames}
                for row in reader: 
                    for col in reader.fieldnames:
                        max_width[col] = max(max_width[col], len(str(row[col])))
                        
                file.seek(0)
                reader = csv.DictReader(file)
                
                total_width = sum(max_width.values())
                for col in reader.fieldnames:
                    width_ratio = max_width[col] / total_width
                    
                    if col == 'No':
                        self.user_table.column(col, width=50, stretch=False)
                    elif col == 'Status':
                        self.user_table.column(col, width=80, stretch=False)
                    else:
                        self.user_table.column(col, width=int(width_ratio * 800), stretch=True)
                    self.user_table.heading(col, text=col.title())
                
                for row in reader:
                    self.user_table.insert("", "end", values=tuple(row.values()))

        except FileNotFoundError:
            print(f"File {self.file_path} tidak ditemukan.")
                        
                

