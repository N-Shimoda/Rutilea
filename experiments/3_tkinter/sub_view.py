import time
import threading
import tkinter
from tkinter import ttk

class TimerButton(tkinter.Button):
    def __init__(self, root):
        super().__init__(
            root,
            text="start",
            width=15,
            command=self.start_timer,
        )
    
    def start_timer(self):
        #サブウィンドウ
        self.sub = tkinter.Toplevel()
        
        #プログレスバー
        self.p = ttk.Progressbar(self.sub, mode="indeterminate", )
        self.p.pack()
        self.p.start()

        #タイマー開始
        self.thread = threading.Thread(target=self.timer)
        self.thread.start()

    def timer(self):
        #タイマー
        i = 0
        while i < 10:
            time.sleep(1)
            i += 1

        self.p.stop()       #プログレスバー停止
        self.sub.destroy()  #サブウィンドウ削除


if __name__ == "__main__":
    root = tkinter.Tk()

    b= TimerButton(root)
    b.pack()

    root.mainloop()