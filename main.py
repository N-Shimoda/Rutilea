
import customtkinter as ctk

class App(ctk.CTk):

    def __init__(self):

        super().__init__()
        self.geometry("300x360")
        self.title("Scenery sommelier")

        self.window = ctk.CTkFrame(self, bg_color="white")
        self.window.pack(expand=True)

        self.upload_button = ctk.CTkButton(self.window, text="Select image", command=self.upload_image)
        self.upload_button.pack()

    def upload_image(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("画像ファイル","*.jpg")]) 
        print(file_path)


if __name__ == "__main__":

    # ctk.set_appearance_mode("Dark")
    app = App()
    app.mainloop()