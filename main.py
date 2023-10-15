
import customtkinter as ctk
from PIL import Image

class App(ctk.CTk):

    def __init__(self):

        super().__init__()
        self.geometry("300x360")
        self.title("Scenery sommelier")

        # ---- Frame ----
        self.frame_main = ctk.CTkFrame(self, bg_color="white")
        self.frame_main.pack(expand=True)

        # ---- Widgets ----
        # button
        self.upload_button = ctk.CTkButton(self.frame_main, text="Select image", command=self.upload_image)
        self.upload_button.pack()

        # image
        self.img = Image.open("img/suits_dining_scene.jpg")
        my_image = ctk.CTkImage(
            light_image=self.img,
            # size=(self.winfo_screenheight, self.winfo_screenwidth)
            size = tuple(item * 0.2 for item in self.img.size)
        )
        image_label = ctk.CTkLabel(self, image=my_image, text="")  # display image with a CTkLabel
        image_label.pack()

    def upload_image(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg")]) 
        print(file_path)

    


if __name__ == "__main__":

    ctk.set_appearance_mode("Dark")
    app = App()
    app.mainloop()