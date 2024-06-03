from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
from tkinter import *


# 傅里叶变换
class page_3(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("傅里叶变换")
        self.createWidget()

    def createWidget(self):
        from page3_n import page3_1,page3_2,page3_3,page3_4,page3_5
        from page_0 import page_0
        lab = Label(self, text="请选择您要进行的模拟", font=("Consolas", 20))
        lab.place(relx=0.28, rely=0.1)
        btn_1 = Button(text="阻尼振动的傅里叶分解", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page3_1))
        btn_1.place(relx=0.21, rely=0.23)
        btn_2 = Button(text="方波的傅里叶分解", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page3_2))
        btn_2.place(relx=0.21, rely=0.36)
        btn_2 = Button(text="三角波的傅里叶分解", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page3_3))
        btn_2.place(relx=0.21, rely=0.49)
        btn_2 = Button(text="高斯脉冲的傅里叶分解", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page3_4))
        btn_2.place(relx=0.21, rely=0.62)
        btn_2 = Button(text="拍振动的傅里叶分解", width=30, font=("Consolas", 16),
                       command=lambda: self.master.switch_frame(page3_5))
        btn_2.place(relx=0.21, rely=0.75)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_0),
                           width=15)
        returnBtn.place(relx=0.36, rely=0.85)

