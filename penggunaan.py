import customtkinter

class Penggunaan(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init(master, self.content_frame, fg_color="transparent", **kwargs)
    
        self.label = customtkinter.CTkLabel(self, text="Penggunaan", font=customtkinter.CTkFont(size=40))
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        


    

