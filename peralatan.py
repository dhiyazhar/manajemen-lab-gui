import os
import csv
import tkinter.ttk as ttk
import customtkinter
from penggunaan import Button, CustomTreeviewStyle

class Peralatan(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.file_path = "./data/peralatan_lab.csv"
        
        self.grid_columnconfigure(0, weight=1)  # Biar label memenuhi horizontal
        self.grid_rowconfigure(1, weight=1) # Button frame tidak perlu melar

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 0)) 
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="kolom") 

        self.b_add_inventory = Button(self.button_frame, text="Tambah Inventori Peralatan") 
        self.b_delete_inventory = Button(self.button_frame, text="Hapus Inventori Peralatan")
        self.b_edit_inventory = Button(self.button_frame, text="Edit Inventori Peralatan")

        self.b_add_inventory.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 
        self.b_delete_inventory.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 
        self.b_edit_inventory.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.inventory_table_frame = customtkinter.CTkFrame(self)
        self.inventory_table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.table_wrapper = customtkinter.CTkFrame(self.inventory_table_frame)
        self.table_wrapper.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.inventory_table = ttk.Treeview(self.table_wrapper, style="Treeview", selectmode="browse")
        self.inventory_table['show'] = 'headings'
        self.inventory_table.pack(fill="both", expand=True)


    def show(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        style = CustomTreeviewStyle()        
        self.load_data()
        

    def hide(self):
        self.grid_remove()
        
    def load_data(self):
        self.inventory_table.delete(*self.inventory_table.get_children())

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.inventory_table["columns"] = tuple(reader.fieldnames)

                # Hitung panjang maksimum setiap kolom (dalam pixel)
                max_width = {col: len(col) for col in reader.fieldnames}
                for row in reader:
                    for col in reader.fieldnames:
                        max_width[col] = max(max_width[col], len(str(row[col])))

                file.seek(0)
                reader = csv.DictReader(file)

                # Atur heading dan width kolom
                total_width = sum(max_width.values())
                for col in reader.fieldnames:
                    width_ratio = max_width[col] / total_width
                    if col == 'No':
                        # Set fixed width for No column
                        self.inventory_table.column(col, width=50, stretch=False)
                    elif col == 'Tanggal':
                        # Set fixed width for Tanggal column
                        self.inventory_table.column(col, width=80, stretch=False)
                    else:
                        # For other columns (like Deskripsis), adjust width proportionally
                        self.inventory_table.column(col, width=int(width_ratio * 800), stretch=True)
                    self.inventory_table.heading(col, text=col.title())

                # Masukkan data ke Treeview
                for row in reader:
                    self.inventory_table.insert("", "end", values=tuple(row.values()))

        except FileNotFoundError:
            print(f"File {self.file_path} tidak ditemukan.")   