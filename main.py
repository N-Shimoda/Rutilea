
import customtkinter as ctk
import tkinter as tk
import webbrowser
from PIL import Image

class App(ctk.CTk):

    def __init__(self):

        # ---- Debugging ----
        self.verbose = True
        self.i = 0

        # ---- Root ----
        super().__init__()
        self.geometry("560x560")
        self.title("Music from image")
        self.img = Image.open("img/suits_dining_scene.jpg")
        self.spotify_url = "https://open.spotify.com/intl-ja/track/4LjIQmt1t6NjpM0tpttzjo"  # 勇者

        self.need_resize = False
        self.bind("<Configure>", self._configure_Cb)

        # self.bind("<Enter>", self._enter_Cb)

        # ---- Children ----
        self.create_menubar()
        self.create_frames()
        self.create_left_widgets()
        self.create_right_widgets()

    
    def create_menubar(self):
        
        self.menubar = tk.Menu(self)
        self.menu_view = tk.Menu(self.menubar)
        self.menu_file = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="View", menu=self.menu_view)
        self.menubar.add_cascade(label="File", menu=self.menu_file)

        # `file`
        self.menu_file.add_command(label="Open image", command=self._upload_image, accelerator="Cmd+O")
        
        self.config(menu=self.menubar)


    def create_frames(self):

        # ---- Define LEFT & RIGHT ----
        self.frame_left = ctk.CTkFrame(self, fg_color="gray21")
        self.frame_right = ctk.CTkFrame(self)

        self.frame_left.pack(side="left", fill="y")
        self.frame_right.pack(side="right", expand=True, fill="both")

        # ---- RIGHT frame ----
        self.frame_top = ctk.CTkFrame(self.frame_right, fg_color="cyan")
        self.frame_middle = ctk.CTkFrame(self.frame_right, fg_color="white")
        self.frame_bottom = ctk.CTkFrame(self.frame_right, fg_color="green")

        self.frame_top.pack(expand=True, fill="both")
        self.frame_middle.pack(fill="x")
        self.frame_bottom.pack(fill="x")


    def create_left_widgets(self):
        # ---- LEFT frame ----
        # button
        self.upload_button = ctk.CTkButton(self.frame_left, text="+", command=self._upload_image)
        self.upload_button.pack(side="bottom", anchor="e")
    

    def create_right_widgets(self):

        # destroy current objects in RIGHT frame
        frames = [obj for obj in self.frame_right.winfo_children() if type(obj)==ctk.CTkFrame]  # list of frames
        print(len(frames))
        for frame in frames:
            children = frame.winfo_children()
            for obj in children:
                obj.destroy()

        # ---- TOP frame ----
        # display image with a CTkLabel
        self.my_image = ctk.CTkImage(
            light_image=self.img,
            size = self._resized_image_size(),
        )
        image_label = ctk.CTkLabel(
            self.frame_top,
            image=self.my_image,
            text="",
            bg_color="white"
        ) 
        image_label.pack(expand=True)

        # ---- MIDDLE frame ----
        desc_label = ctk.CTkLabel(
            self.frame_middle,
            text='Dining scene from "SUITS".',
            anchor="e"
        )
        desc_label.pack(fill="x")

        # ---- BOTTOM frame ----
        # Spotify button
        self.spotify_button = ctk.CTkButton(
            self.frame_bottom,
            text="Spotify",
            command=self._open_spotify
        )
        self.spotify_button.pack()


    def _upload_image(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg"), ("画像ファイル", "*.png")]) 
        print(file_path)

        if file_path:
            self.img = Image.open(file_path)
            self.create_right_widgets()


    def _resized_image_size(self) -> tuple:
        """
        イメージを何倍に縮小・拡大して表示するかを求める関数。リサイズされた画像のサイズを返す。
        """        
        image_width, image_height = self.img.size
        self.update_idletasks()     # for avoiding initial error that window size loaded as (1,1)
        window_width = self.frame_top.winfo_width()
        window_height = self.frame_top.winfo_height()

        scale = min(window_width/image_width, window_height/image_height)
        if self.verbose:
            print("image size: {}".format(self.img.size))
            print("window size: {}".format((window_width, window_height)))
            print("resizing image (scale = {})".format(scale))

        return (scale*image_width, scale*image_height)


    def _configure_Cb(self, e):
        # update the size of image
        self.my_image.configure(size=self._resized_image_size())
        if self.verbose:
            self.i += 1
            print("{}th Configure Callback".format(self.i))

    
    def _enter_Cb(self, e):

        if self.need_resize:
            if self.verbose:
                print("Resized")
            self.need_resize = False
            self.create_right_widgets()


    def _open_spotify(self):
        if self.verbose:
            print("Opening Spotify.")
        webbrowser.open(url=self.spotify_url)


if __name__ == "__main__":

    ctk.set_appearance_mode("Dark")
    app = App()
    app.mainloop()