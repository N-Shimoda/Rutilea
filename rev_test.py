import tkinter as tk

# ボタンがクリックされたときに実行される関数
def display_text():
    label.config(text="入力されたテキスト: " + input_text.get())  # ラベルにテキストを表示

# メインウィンドウの作成
root = tk.Tk()
root.title("テキスト表示アプリ")

# 入力欄の作成
input_text = tk.StringVar()  # テキスト変数を作成

# ラベルの作成
label = tk.Label(root, text="ここにテキストが表示されます")
label.pack(pady=10)

# 入力欄の作成
entry = tk.Entry(root, textvariable=input_text)
entry.pack(pady=5)

# ボタンの作成
button = tk.Button(root, text="表示", command=display_text)
button.pack(pady=5)

# ウィンドウを表示
root.mainloop()