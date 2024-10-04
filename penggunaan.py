import os
import csv
from datetime import datetime
import customtkinter
import tkinter.ttk as ttk

class Penggunaan(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.file_path = "./data/penggunaan_lab.csv"
        
        self.grid_columnconfigure(0, weight=1)  # Biar label memenuhi horizontal
        self.grid_rowconfigure(1, weight=1) # Button frame tidak perlu melar

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 0)) 
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="kolom") 

        self.b_add_usage = Button(self.button_frame, text="Tambah Penggunaan") 
        self.b_delete_usage = Button(self.button_frame, text="Hapus Penggunaan")
        self.b_edit_usage = Button(self.button_frame, text="Edit Penggunaan")

        self.b_add_usage.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 
        self.b_delete_usage.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 
        self.b_edit_usage.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.usage_table_frame = customtkinter.CTkFrame(self)
        self.usage_table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.table_wrapper = customtkinter.CTkFrame(self.usage_table_frame)
        self.table_wrapper.pack(fill="both", expand=True, padx=20, pady=20)

        self.table = ttk.Treeview(self.table_wrapper, style="Treeview", selectmode="browse")
        self.table['show'] = 'headings'
        self.table.pack(fill="both", expand=True)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        style = CustomTreeviewStyle()        
        self.load_data()


    def hide(self):
        self.grid_remove()
        
    def load_data(self):
        self.table.delete(*self.table.get_children())

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.table["columns"] = tuple(reader.fieldnames)

                max_width = {col: len(col) for col in reader.fieldnames}
                for row in reader:
                    for col in reader.fieldnames:
                        if col == 'Tanggal':
                            tanggal_str = datetime.strptime(row['Tanggal'], '%Y-%m-%d').strftime('%d-%m-%Y')
                            max_width[col] = max(max_width[col], len(tanggal_str))
                        else:
                            max_width[col] = max(max_width[col], len(str(row[col])))
                            
                file.seek(0) 
                next(reader) 

                total_width = sum(max_width.values())
                for col in reader.fieldnames:
                    width_ratio = max_width[col] / total_width
                    if col == 'No':
                        self.table.column(col, width=50, stretch=False)
                    elif col == 'Tanggal':
                        self.table.column(col, width=100, stretch=False)
                    elif col in ['Kelas', 'Dosen', 'Penanggung Jawab']:
                        self.table.column(col, width=max(150, int(width_ratio * 800)), stretch=True)
                    else:
                        self.table.column(col, width=int(width_ratio * 800), stretch=True)
                    self.table.heading(col, text=col.title())

                for row in reader:
                    tanggal = datetime.strptime(row['Tanggal'], '%Y-%m-%d').strftime('%d-%m-%Y')
                    values = list(row.values())
                    values[1] = tanggal
                    self.table.insert("", "end", values=tuple(values))

                    
        except FileNotFoundError:
            print(f"File {self.filepath} tidak ditemukan.")
                
        
class CustomTreeviewStyle:
    def __init__(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.configure_treeview()

    def configure_treeview(self):
        self.style.configure("Treeview",
                            background=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                            foreground=customtkinter.ThemeManager.theme["CTkLabel"]["text_color"][1],
                            fieldbackground=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                            bordercolor=customtkinter.ThemeManager.theme["CTkFrame"]["border_color"][1],
                            borderwidth=0)

        self.style.configure("Treeview.Heading",
                            background=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"][1],
                            foreground=customtkinter.ThemeManager.theme["CTkLabel"]["text_color"][1],
                            relief="flat")

        self.style.map("Treeview.Heading",
                      relief=[('active', 'groove'), ('pressed', 'sunken')])

        self.style.map("Treeview",
                      background=[('selected', customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][1])],
                      foreground=[('selected', customtkinter.ThemeManager.theme["CTkButton"]["text_color"][1])])
        

class Button(customtkinter.CTkButton):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, font=customtkinter.CTkFont(size=15), **kwargs)
        




    

