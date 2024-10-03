import os
import customtkinter
from penggunaan import Button

class User(customtkinter.CTkFrame): 
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)  # Biar label memenuhi horizontal
        self.grid_rowconfigure(1, weight=1) # Button frame tidak perlu melar

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 0)) 
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="kolom") 

        self.b_tambah_pengguna = Button(self.button_frame, text="Tambah Penggunaan") 
        self.b_hapus_pengguna = Button(self.button_frame, text="Hapus Penggunaan")
        self.b_edit_pengguna = Button(self.button_frame, text="Edit Penggunaan")

        self.b_tambah_pengguna.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 
        self.b_hapus_pengguna.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 
        self.b_edit_pengguna.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.tabel_pengguna_frame = customtkinter.CTkFrame(self)
        self.tabel_pengguna_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Buat Treeview di dalam tabel_pengguna_frame
        self.tabel_wrapper = customtkinter.CTkFrame(self.tabel_pengguna_frame)
        self.tabel_wrapper.pack(fill="both", expand=True, padx=20, pady=20)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        self.grid_remove()

