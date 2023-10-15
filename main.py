
import customtkinter as ctk
from PIL import Image

class App(ctk.CTk):

    def __init__(self):

        # ---- Root ----
        super().__init__()
        # self.geometry("300x360")
        self.title("Scenery sommelier")
        self.img = Image.open("img/suits_dining_scene.jpg")

        # ---- Children ----
        self.create_frames()
        self.create_widgets()


    def create_frames(self):

        self.frame_left = ctk.CTkFrame(self, fg_color="white")
        self.frame_right = ctk.CTkFrame(self, fg_color="cyan")

        self.frame_left.pack(side="left", fill="y")
        self.frame_right.pack(side="right", expand=True, fill="both")
        

    def create_widgets(self):

        # destroy current objects in each frame
        frames = [obj for obj in self.winfo_children() if type(obj)==ctk.CTkFrame]  # list of frames
        for frame in frames:
            children = frame.winfo_children()
            for obj in children:
                obj.destroy()

        # ---- LEFT frame ----
        # button
        self.upload_button = ctk.CTkButton(self.frame_left, text="+", command=self._upload_image)
        self.upload_button.pack(side="bottom", anchor="e")

        # ---- RIGHT frame ----
        # image
        my_image = ctk.CTkImage(
            light_image=self.img,
            size = tuple(item * 0.2 for item in self.img.size)
        )
        image_label = ctk.CTkLabel(self.frame_right, image=my_image, text="Selected image:")    # display image with a CTkLabel
        image_label.pack(expand=True, anchor="center")


    def _upload_image(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg")]) 
        print(file_path)
        self.img = Image.open(file_path)

        self.create_widgets()


if __name__ == "__main__":

    ctk.set_appearance_mode("Dark")
    app = App()
    app.mainloop()