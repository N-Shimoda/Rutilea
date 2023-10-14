
import customtkinter as ctk

class App(ctk.CTk):

    def __init__(self):

        super().__init__()
        self.geometry("300x360")

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)

        self.upload_button = ctk.CTkButton(self, text="Select image", command=self.upload_image)
        self.upload_button.pack()

    def button_callbck(self):
        print("button clicked")

    def upload_image(self):
        pass

ctk.set_appearance_mode("Dark")
app = App()
app.mainloop()