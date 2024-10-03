import customtkinter
import tkinter.ttk as ttk

class Button(customtkinter.CTkButton):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, font=customtkinter.CTkFont(size=15), **kwargs)


class Penggunaan(customtkinter.CTkFrame):
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

        self.tabel = ttk.Treeview(self.tabel_wrapper, columns=("Nama", "Usia"), show="headings")
        self.tabel.pack(fill="both", expand=True)

        self.tabel.heading("Nama", text="Nama")
        self.tabel.heading("Usia", text="Usia")


        self.tabel.insert("", "end", values=("Andi", 20))
        self.tabel.insert("", "end", values=("Budi", 25))


    def show(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        style = ttk.Style()

        style.theme_use("default")

        # Configure the Treeview colors
        style.configure("Treeview",
                        background=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                        foreground=customtkinter.ThemeManager.theme["CTkLabel"]["text_color"][1],
                        fieldbackground=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                        bordercolor=customtkinter.ThemeManager.theme["CTkFrame"]["border_color"][1],
                        borderwidth=0)

        # Configure the Treeview heading
        style.configure("Treeview.Heading",
                        background=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"][1],
                        foreground=customtkinter.ThemeManager.theme["CTkLabel"]["text_color"][1],
                        relief="flat")

        style.map("Treeview.Heading",
                relief=[('active', 'groove'), ('pressed', 'sunken')])

        # Configure selection colors
        style.map("Treeview",
                background=[('selected', customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][1])],
                foreground=[('selected', customtkinter.ThemeManager.theme["CTkButton"]["text_color"][1])])


    def hide(self):
        self.grid_remove()





    

