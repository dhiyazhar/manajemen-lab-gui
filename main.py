import os
import csv
import customtkinter
from side_menu import *
from penggunaan import *
from peralatan import *
from user import User

customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("blue") 


# Inheritance dari library customtkinter dimana window aplikasi dibuat dengan meng-inherit
# kelas customtkinter.CTk 

class App(customtkinter.CTk): 
    def __init__(self):
        super().__init__()
        self.title("Manajemen Lab RPL")
        self.geometry(f"{1100}x{580}")
        
        self.cek_file_dir()
    
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.side_menu = SideBar(self, self.switch_frame)
        
        self.main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.welcome_frame = self.welcome_frame()
        self.penggunaan_frame = Penggunaan(self.main_frame)
        self.peralatan_frame = Peralatan(self.main_frame)
        self.user_frame = User(self.main_frame)

        self.frames = {
            "welcome": self.welcome_frame,
            "penggunaan": self.penggunaan_frame,
            "peralatan": self.peralatan_frame,
            "user": self.user_frame
        }

        for frame in self.frames.values():
            if hasattr(frame, 'hide'):
                frame.hide()
            else:
                frame.grid_remove()

        self.current_frame = None
        self.switch_frame("welcome")

    def welcome_frame(self):
        frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        label = customtkinter.CTkLabel(frame, text="Selamat Datang", font=customtkinter.CTkFont(size=60, weight='bold'))
        label.place(relx=0.5, rely=0.5, anchor="center")
        return frame

    def switch_frame(self, frame_name):
        new_frame = self.frames[frame_name]

        if self.current_frame == new_frame:
            return

        if self.current_frame:
            if hasattr(self.current_frame, 'hide'):
                self.current_frame.hide()
            else:
                self.current_frame.grid_remove()

        if hasattr(new_frame, 'show'):
            new_frame.show()
        else:
            new_frame.grid(row=0, column=0, sticky="nsew")

        self.current_frame = new_frame
        
    def cek_file_dir(self):
        
        data_path = "./data/" 
        
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            
            files = {
                    "penggunaan_lab.csv": ["Tanggal", "Kelas", "Dosen", "Penanggung Jawab", "Deskripsi", "Penggunaan"],
                    "peralatan_lab.csv": ["ID", "Nama", "Status", "Jumlah"],
                    "user.csv": ["Nama", "Status", "Jabatan"]
                    }
            
            for file_name, fields in files.items():
                file_path = os.path.join(data_path, file_name)
                
                with open(file_path, 'w', newline='') as file: 
                    writer = csv.writer(file)
                    writer.writerow(fields)
                
        else:
            print("Folder dan File sudah ada.")     
            
            
        
        
        
         
    

app = App()
app.mainloop()