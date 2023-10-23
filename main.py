
import customtkinter as ctk
import tkinter as tk
import webbrowser
import urllib.request
from PIL import Image
import threading
import json
from src.spotify import search_spotify
from src.visual_LLM import image_to_text

class App(ctk.CTk):

    def __init__(self):

        # ---- Debugging ----
        self.verbose = True
        self.i = 0

        # ---- Root ----
        super().__init__()
        self.geometry("500x750")
        self.title("Music from image")

        # ---- Variables ----
        self.picture_file = Image.open("/Users/naoki/Desktop/img/suits_dining_scene.jpg")
        self.pad_size = 14
        self.corner_radius = 18
        self.font_family = "Helvetica"
        self.picture_img = None     # for avoiding initial error when activating App.

        # setting initial music as '勇者 by YOASOBI' 
        self.spotify_result = [
            {
                'artwork_url': 'https://i.scdn.co/image/ab67616d0000b273a9f9b6f07b43009f5b0216dc',
                'track_name': '勇者',
                'track_url': 'https://open.spotify.com/track/4LjIQmt1t6NjpM0tpttzjo',
                'album_url': 'https://open.spotify.com/album/6L7pjBfP49dh1WYDmHngOO',
                'artist_name': 'YOASOBI',
                'artist_url': 'https://open.spotify.com/artist/64tJ2EAv1R6UaZqc4iOCyj'
            }
        ]

        # ---- Children ----
        self.create_menubar()
        self.create_frames()
        self.create_widgets()

    
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
        self.frame_main = ctk.CTkFrame(self)
        self.frame_main.pack(expand=True, fill="both")

        # ---- RIGHT frame ----
        self.frame_top = GradientFrame(self.frame_main, "black", "orange")
        self.frame_middle = ctk.CTkFrame(self.frame_main, fg_color="white")
        self.frame_bottom = ctk.CTkFrame(self.frame_main, fg_color="green")

        self.frame_top.pack(expand=True, fill="both")
        self.frame_middle.pack(fill="x")
        self.frame_bottom.pack(fill="x")

        # for resizing image
        self.frame_top.bind("<Configure>", self._configure_Cb)
    

    def create_widgets(self):

        # destroy current objects
        frames = [obj for obj in self.frame_main.winfo_children() if type(obj)==ctk.CTkFrame or type(obj)==GradientFrame]  # list of frames
        for frame in frames:
            children = frame.winfo_children()
            for obj in children:
                obj.destroy()

        self.create_top_widgets()
        self.create_middle_widgets()
        self.create_bottom_widgets()


    def create_top_widgets(self):

        # display image with a CTkLabel
        self.picture_img = ctk.CTkImage(
            light_image=self.picture_file,
            size = self._resized_image_size(),
        )
        image_label = ctk.CTkLabel(
            self.frame_top,
            image=self.picture_img,
            text="",
            corner_radius=self.corner_radius,
            fg_color="black",
            bg_color="yellow"
        )
        image_label.pack(expand=True, padx=self.pad_size, pady=self.pad_size)

        change_button = ctk.CTkButton(
            self.frame_top,
            text="Refresh image",
            image=ctk.CTkImage(
                Image.open("/Users/naoki/github/Rutilea/img/refresh.jpg"),
                size=(36,30),
            ),
            command=self._upload_image,
        )
        change_button.pack(padx=self.pad_size, pady=self.pad_size)


    def create_middle_widgets(self):

        if self.verbose:
            pretty_dict = json.dumps(self.spotify_result, indent=4, sort_keys=True)
            print("Current Spotify results ({} items):".format( len(self.spotify_result)) )
            print(pretty_dict)

        # ---- Tabview ----
        self.tabview = ctk.CTkTabview(self.frame_middle)
        self.tabview.pack(padx=self.pad_size, pady=self.pad_size)

        if self.spotify_result == []:   # case when no tracks found
            self.tabview.add("Music 1")
            label = ctk.CTkLabel(self.tabview.tab("Music 1"), text="Sorry, LLM or Spotify did not work well.\nPlease try again.")
            label.pack()
        else:
            for i in range(len(self.spotify_result)):
                self.tabview.add("Music {}".format(i+1))
        
        self.tabview.set("Music 1")
        self.tabview.pack(fill="x")

        # ---- Music View ----
        for result in self.spotify_result:
            i = self.spotify_result.index(result)

            # download artwork
            dst_path = "img/artwork_{}.jpg".format(i)
            urllib.request.urlretrieve(result["artwork_url"], dst_path)
            self.album_file = Image.open(dst_path)

            # create widgets in each tabs
            music_view = MusicView(
                master=self.tabview.tab("Music {}".format(i+1)),
                album_file=self.album_file,
                spotify_result=result
            )
            music_view.pack()


    def create_bottom_widgets(self):
        # ---- BOTTOM frame ----
        label = ctk.CTkLabel(self.frame_bottom, text="Powered by Spotify")
        label.pack()


    def _upload_image(self):

        # Ask the user to choose an image file
        file_path = ctk.filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg"), ("画像ファイル", "*.png")]) 
        print(file_path)

        if file_path:
            self.picture_file = Image.open(file_path)

            # Show waiting view in GUI
            self.sub = ProcessingWindow()
            self.update()

            # Select appropriate music with LLM
            thread = threading.Thread(target=self._update_music(file_path))
            thread.start()

            self.create_widgets()

    
    def _update_music(self, file_path):

        if self.verbose:
            print("processing!")

        # Suggest some music which fits to the atmosphere of given image
        music_list = image_to_text(file_path)

        self.spotify_result = []

        if len(music_list) > 0:     # LLM could suggest at least 1 piece of music

            # Search suggeted musics in Spotify
            for music in music_list:
                result = search_spotify(music)
                if result is not None:
                    self.spotify_result.append(result)
                else:
                    print(colorize('"No music found in Spotify for "{}"'.format(music), 31))

        else:
            # LLM could not suggest any music
            print(colorize("LLM could not suggest music. View updation cancelled.", 31))

        # Destroy processing view
        self.sub.progress_bar.stop()
        self.sub.destroy()


    def _resized_image_size(self) -> tuple:
        """
        イメージを何倍に縮小・拡大して表示するかを求める関数。リサイズされた画像のサイズを返す。
        """        
        image_width, image_height = self.picture_file.size
        self.update_idletasks()     # for avoiding initial error that window size loaded as (1,1)
        window_width = self.frame_top.winfo_width()
        window_height = self.frame_top.winfo_height()

        scale = min(window_width/image_width, window_height/image_height)
        if self.verbose:
            print("image size: {}".format(self.picture_file.size))
            print("window size: {}".format((window_width, window_height)))
            print("resizing image (scale = {})".format(scale))

        # time.sleep(0.001)

        return (scale*image_width, scale*image_height)


    def _configure_Cb(self, e):
        # update the size of image
        if self.picture_img is not None:
            self.picture_img.configure(size=self._resized_image_size())
            if self.verbose:
                self.i += 1
                print("{}th Configure Callback".format(self.i))

        # update gradient
        self.frame_top._draw_gradient(e)


class MusicView(ctk.CTkFrame):
    
    def __init__(self, master=None, album_file=None, spotify_result=None):

        super().__init__(master)

        self.verbose = True
        self.pad_size = 14
        self.corner_radius = 18
        self.font_family = "Helvetica"

        self.spotify_result = spotify_result
        self.album_file = album_file

        self.create_widgets()

    
    def create_widgets(self):

        # ---- Album artwork ----
        self.album_img = ctk.CTkImage(
            light_image=self.album_file,
            size=(160,160)
        )
        album_artwork = ctk.CTkLabel(
            self,
            image=self.album_img,
            text="",
            corner_radius=self.corner_radius,
            fg_color="black"
        )

        # ---- Name of track & artist ----
        title_label = ctk.CTkLabel(
            self,
            text=self.spotify_result["track_name"],
            font=ctk.CTkFont(family=self.font_family, size=20),
            text_color="black",
            anchor="w"
        )
        artist_label = ctk.CTkLabel(
            self,
            text=self.spotify_result["artist_name"],
            font=ctk.CTkFont(family=self.font_family),
            text_color="black",
            anchor="w"
        )

        # Spotify button
        self.spotify_button = ctk.CTkButton(
            self,
            text="Spotify",
            command=self._open_spotify,
        )

        album_artwork.pack(side="left", padx=self.pad_size, pady=self.pad_size)
        title_label.pack(anchor="w")
        artist_label.pack(anchor="w")
        self.spotify_button.pack(anchor="w")


    def _open_spotify(self):
        if self.verbose:
            print("Opening Spotify...")
        webbrowser.open(url=self.spotify_result["track_url"])


class GradientFrame(tk.Canvas):
    
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, color1="red", color2="black", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")


class ProcessingWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.title("Notice")

        # ---- geometry ----
        width=300
        height=200
        x_pos = self.master.winfo_width()//2 - width//2
        y_pos =  self.master.winfo_height()//2 - height//2
        self.geometry("{}x{}+{}+{}".format(width, height, x_pos, y_pos))

        # set as modal window
        self.grab_set()        # モーダルにする
        self.focus_set()       # フォーカスを新しいウィンドウをへ移す
        self.transient(self.master)   # タスクバーに表示しない

        self.label = ctk.CTkLabel(self, text="LLM Processing...")
        self.label.pack(padx=20, pady=20)

        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress_bar.pack()
        self.progress_bar.start()


def colorize(text, color_code):
    # see https://www.python.ambitious-engineer.com/archives/3721 for color selection
    return f"\033[{color_code}m{text}\033[0m"


if __name__ == "__main__":

    # ctk.set_appearance_mode("Dark")
    app = App()
    app.mainloop()