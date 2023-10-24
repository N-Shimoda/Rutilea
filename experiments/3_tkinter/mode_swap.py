import tkinter as tk
from tkinter import ttk

def toggle_dark_mode():
    # ダークモードとライトモードのテーマを切り替える
    if current_theme.get() == "light":
        current_theme.set("dark")
        root.tk_setPalette(background='#2E2E2E', foreground='#FFFFFF')
    else:
        current_theme.set("light")
        root.tk_setPalette(background='', foreground='')

# アプリの初期化
root = tk.Tk()
root.title("Dark Mode / Light Mode")

current_theme = tk.StringVar()
current_theme.set("light")  # 初期状態はライトモード

# ダークモードとライトモードのテーマを作成
style = ttk.Style()
style.theme_create("dark", parent="default", settings={
    "TButton": {"configure": {"background": '#2E2E2E', "foreground": '#FFFFFF'}}
})
style.theme_use("dark")

# ライトモードのテーマを作成
style.theme_create("light", parent="default", settings={})
style.theme_use("light")

# ダークモードとライトモードを切り替えるボタン
theme_button = ttk.Button(root, text="Toggle Dark Mode / Light Mode", command=toggle_dark_mode)
theme_button.pack(pady=20)

root.mainloop()
