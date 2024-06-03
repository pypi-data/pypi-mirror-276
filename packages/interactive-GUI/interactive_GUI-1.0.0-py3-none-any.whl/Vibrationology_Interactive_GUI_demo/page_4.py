from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
from tkinter import *


# 单摆
class page_4(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("单摆")
        self.createWidget()

    def createWidget(self):
        from page_0 import page_0
        from page4_n import page4_1, page4_2, page4_3, page4_4,page4_5,page4_6
        lab = Label(self, text="请选择您要进行的模拟", font=("Consolas", 20))
        lab.place(relx=0.28, rely=0.08)
        btn_1 = Button(text="角谐运动", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page4_1))
        btn_1.place(relx=0.21, rely=0.20)
        btn_2 = Button(text="大角度单摆", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page4_2))
        btn_2.place(relx=0.21, rely=0.31)
        btn_3 = Button(text="阻尼单摆", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page4_3))
        btn_3.place(relx=0.21, rely=0.42)
        btn_4 = Button(text="受迫单摆", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page4_4))
        btn_4.place(relx=0.21, rely=0.53)
        btn_5 = Button(text="混沌运动", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page4_5))
        btn_5.place(relx=0.21, rely=0.64)
        btn_6 = Button(text="倍周期分叉", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page4_6))
        btn_6.place(relx=0.21, rely=0.75)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_0),
                           width=15)
        returnBtn.place(relx=0.36, rely=0.87)

