# https://office54.net/python/tkinter/background-gradation-frame

import tkinter as tk
root = tk.Tk()
root.geometry("500x300")
root.title('グラデーション')

x_place=0
color_changer=200

for i in range(5):
    c=str(224499+color_changer)
    tk.Frame(root,width=100,height=300,bg="#"+c).place(x=x_place,y=0)
    x_place=x_place+100
    color_changer=color_changer+1000

root.mainloop()