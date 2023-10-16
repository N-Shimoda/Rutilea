
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

class App(ctk.CTk):

    def __init__(self):

        # ---- Root ----
        super().__init__()
        self.geometry("560x560")
        self.title("Scenery sommelier")
        self.img = Image.open("img/suits_dining_scene.jpg")

        self.i = 0
        self.need_resize = False
        self.bind("<Configure>", self._configure_Cb)
        self.bind("<Enter>", self._enter_Cb)

        # ---- Children ----
        self.create_menubar()
        self.create_frames()
        self.create_widgets()

    
    def create_menubar(self):
        
        self.menubar = tk.Menu(self)
        self.menu_view = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="View", menu=self.menu_view)
        
        self.config(menu=self.menubar)


    def create_frames(self):

        self.frame_left = ctk.CTkFrame(self, fg_color="gray21")
        self.frame_right = ctk.CTkFrame(self)

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
            size = self._resized_image_size(),
        )
        image_label = ctk.CTkLabel(self.frame_right, image=my_image, text="")    # display image with a CTkLabel
        image_label.pack(expand=True, anchor="center")


    def _upload_image(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg"), ("画像ファイル", "*.png")]) 
        print(file_path)

        if file_path:
            self.img = Image.open(file_path)
            self.create_widgets()


    def _resized_image_size(self) -> tuple:
        """
        イメージを何倍に縮小・拡大して表示するかを求める関数。リサイズされた画像のサイズを返す。
        """        
        image_width, image_height = self.img.size
        self.update_idletasks()     # for avoiding initial error that window size loaded as (1,1)
        window_width = self.frame_right.winfo_width()
        window_height = self.frame_right.winfo_height()

        # print("image size: {}".format(self.img.size))
        # print("window size: {}".format((window_width, window_height)))

        scale = min(window_width/image_width, window_height/image_height)
        return (scale*image_width, scale*image_height)


    def _configure_Cb(self, e):
        
        if not self.need_resize:
            self.i = self.i + 1
            self.need_resize = True
            # print(type(e))
            # print(e)
            print("Callback {}".format(self.i))

    
    def _enter_Cb(self, e):

        # print(type(e))
        # print(e)

        if self.need_resize:
            print("Resized")
            self.need_resize = False
            self.create_widgets()


if __name__ == "__main__":

    ctk.set_appearance_mode("Dark")
    app = App()
    app.mainloop()