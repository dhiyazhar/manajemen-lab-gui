import customtkinter

class Button(customtkinter.CTkButton):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, **kwargs)

class SideBar(customtkinter.CTkFrame):
    def __init__(self, master, switch_frame_callback, **kwargs):
        super().__init__(master, width=140, corner_radius=0, **kwargs)

        self.switch_frame_callback = switch_frame_callback

        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)
        self.title_label = customtkinter.CTkLabel(self, text="MENU", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.penggunaan_button = Button(self, text="Penggunaan", command=lambda: self.switch_frame_callback("penggunaan"))
        self.penggunaan_button.grid(row=1, column=0, padx=20, pady=10)

        self.peralatan_button = Button(self, text="Peralatan", command=lambda: self.switch_frame_callback("peralatan"))
        self.peralatan_button.grid(row=2, column=0, padx=20, pady=10)

        self.user_button = Button(self, text="User", command=lambda: self.switch_frame_callback("user"))
        self.user_button.grid(row=3, column=0, padx=20, pady=10)

        

