from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
from tkinter import *


# 简谐振动界面
class page_1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("简谐振动")
        self.createWidget()

    def createWidget(self):
        from page1_n import page1_1,page1_2,page1_3,page1_4,page1_5
        from page_0 import page_0
        lab = Label(self, text="请选择您要进行的模拟", font=("Consolas", 20))
        lab.place(relx=0.28, rely=0.1)
        btn_1 = Button(text="简谐振动的演示(旋转矢量法)", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page1_1))
        btn_1.place(relx=0.21, rely=0.23)
        btn_2 = Button(text="简谐振动的合成(同向同频)", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page1_2))
        btn_2.place(relx=0.21, rely=0.36)
        btn_3 = Button(text="简谐振动的演示(同向不同频)", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page1_3))
        btn_3.place(relx=0.21, rely=0.49)
        btn_4 = Button(text="简谐振动的合成(方向垂直同频)", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page1_4))
        btn_4.place(relx=0.21, rely=0.62)
        btn_5 = Button(text="简谐振动的合成(方向垂直不同频)", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page1_5))
        btn_5.place(relx=0.21, rely=0.75)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_0),
                           width=15)
        returnBtn.place(relx=0.36, rely=0.85)
