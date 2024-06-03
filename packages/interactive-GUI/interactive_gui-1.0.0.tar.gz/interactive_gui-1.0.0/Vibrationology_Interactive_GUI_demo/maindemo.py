from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
from tkinter import *
from page_0 import page_0


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.current_frame = None
        self.switch_frame(page_0)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.geometry("600x500+500+200")


if __name__ == "__main__":
    app = App()
    app.mainloop()
