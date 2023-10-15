import customtkinter as ctk
from PIL import Image, ImageTk

# カスタムTkinterウィンドウを作成
root = ctk.CTk()
root.title("画像表示アプリ")

# 画像ファイルのパス
image_path = "/Users/naoki/github/Rutilea/img/suits_characters.jpg"

def display_image():
    # 画像を開く
    image = Image.open(image_path)

    # 画像をTkinter PhotoImageに変換
    tk_image = ImageTk.PhotoImage(image)

    # 画像を表示するカスタムTkinterウィジェットを作成
    image_widget = ctk.CTkImage(root, light_image=tk_image)
    image_widget.pack()

# 画像を表示するボタンを作成
display_button = ctk.CTkButton(root, text="画像表示", command=display_image)
display_button.pack()

root.mainloop()