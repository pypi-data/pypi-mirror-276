from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
from tkinter import *


# 非简谐振动界面
class page_2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("非简谐振动")
        self.createWidget()

    def createWidget(self):
        from page2_n import page2_1,page2_2
        from page_0 import page_0
        lab = Label(self, text="请选择您要进行的模拟", font=("Consolas", 20))
        lab.place(relx=0.28, rely=0.2)
        btn_1 = Button(text="阻尼振动", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page2_1))
        btn_1.place(relx=0.21, rely=0.4)
        btn_2 = Button(text="受迫振动", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page2_2))
        btn_2.place(relx=0.21, rely=0.6)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_0),
                           width=15)
        returnBtn.place(relx=0.36, rely=0.85)

