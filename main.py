import customtkinter
from side_menu import *
from penggunaan import *

class App(customtkinter.CTk): 
    def __init__(self):
        super().__init__()
        self.title("Manajemen Lab RPL")
        self.geometry(f"{1100}x{580}")
    
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.side_menu = SideBar(self, self.switch_frame)
        
        self.main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.welcome_frame = self.welcome_frame()
        self.penggunaan_frame = Penggunaan()
        self.peralatan_frame = self.create_peralatan_frame()
        self.user_frame = self.create_user_frame()

        self.current_frame = self.welcome_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def welcome_frame(self):
        frame = customtkinter.CTkFrame(self.content_frame, fg_color="transparent")
        label = customtkinter.CTkLabel(frame, text="Selamat Datang", font=customtkinter.CTkFont(size=60, weight='bold'))
        label.place(relx=0.5, rely=0.5, anchor="center")
        return frame

    # def create_penggunaan_frame(self):
    #     frame = customtkinter.CTkFrame(self.content_frame, fg_color="transparent")
    #     label = customtkinter.CTkLabel(frame, text="Penggunaan Content", font=customtkinter.CTkFont(size=40))
    #     label.place(relx=0.5, rely=0.5, anchor="center")
    #     return frame

    def create_peralatan_frame(self):
        frame = customtkinter.CTkFrame(self.content_frame, fg_color="transparent")
        label = customtkinter.CTkLabel(frame, text="Peralatan Content", font=customtkinter.CTkFont(size=40))
        label.place(relx=0.5, rely=0.5, anchor="center")
        return frame

    def create_user_frame(self):
        frame = customtkinter.CTkFrame(self.content_frame, fg_color="transparent")
        label = customtkinter.CTkLabel(frame, text="User Content", font=customtkinter.CTkFont(size=40))
        label.place(relx=0.5, rely=0.5, anchor="center")
        return frame

    def switch_frame(self, frame_name):
        # Hide the current frame
        self.current_frame.grid_forget()

        # Show the new frame
        if frame_name == "welcome":
            self.current_frame = self.welcome_frame
        elif frame_name == "penggunaan":
            self.current_frame = Penggunaan()
        elif frame_name == "peralatan":
            self.current_frame = self.peralatan_frame
        elif frame_name == "user":
            self.current_frame = self.user_frame

        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    # def create_penggunaan_frame(self):
    #     frame = customtkinter.CTkFrame(self.content_frame, fg_color="transparent")
    #     label = customtkinter.CTkLabel(frame, text="Penggunaan", font=customtkinter.CTkFont(size=40))
    #     label.pack(pady=20)
        
    #     name_label = customtkinter.CTkLabel(frame, text="Nama:")
    #     name_label.pack()
    #     name_entry = customtkinter.CTkEntry(frame)
    #     name_entry.pack()
        
    #     date_label = customtkinter.CTkLabel(frame, text="Tanggal:")
    #     date_label.pack()
    #     date_entry = customtkinter.CTkEntry(frame)
    #     date_entry.pack()
        
    #     submit_button = customtkinter.CTkButton(frame, text="Submit", command=self.submit_penggunaan)
    #     submit_button.pack(pady=20)
        
    #     return frame

    # def submit_penggunaan(self):
    #     # Add your submission logic here
    #     pass
    

app = App()
app.mainloop()