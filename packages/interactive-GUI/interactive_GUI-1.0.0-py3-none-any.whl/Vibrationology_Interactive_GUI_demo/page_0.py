from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
from tkinter import *
import os


# 主界面
class page_0(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("振动模拟")
        self.createWidget()

    def createWidget(self):
        from page_1 import page_1
        from page_2 import page_2
        from page_3 import page_3
        from page_4 import page_4
        lab = Label(self, text="请选择您要进行的模拟", font=("Consolas", 20))
        lab.place(relx=0.28, rely=0.1)
        btn_1 = Button(text="简谐振动", font=("Consolas", 18), width=30,
                       command=lambda: self.master.switch_frame(page_1))
        btn_1.place(relx=0.18, rely=0.24)
        btn_2 = Button(text="非简谐振动", font=("Consolas", 18), width=30,
                       command=lambda: self.master.switch_frame(page_2))
        btn_2.place(relx=0.18, rely=0.38)
        btn_3 = Button(text="傅里叶变换", font=("Consolas", 18), width=30,
                       command=lambda: self.master.switch_frame(page_3))
        btn_3.place(relx=0.18, rely=0.66)
        btn_4 = Button(text="单摆与混沌运动", font=("Consolas", 18), width=30,
                       command=lambda: self.master.switch_frame(page_4))
        btn_4.place(relx=0.18, rely=0.52)
        quitBtn = Button(text="退出", font=("Consolas", 16), command=lambda: self.master.destroy(), width=15)
        quitBtn.place(relx=0.35, rely=0.8)

        def relative_to_absolute(relative_path):
            # 获取当前脚本文件所在目录的路径
            current_directory = os.path.dirname(__file__)
            # 结合相对路径和当前目录，生成绝对路径
            absolute_path = os.path.join(current_directory, relative_path)
            return absolute_path

        global spring
        spring_path = relative_to_absolute("Spring oscillator.gif")
        spring = PhotoImage(file=spring_path)
        lab_spring = Label(image=spring)
        lab_spring.place(relx=0.02, rely=0.05)

        global bai
        bai_path = relative_to_absolute("Simple pendulum.gif")
        bai = PhotoImage(file=bai_path)
        lab_bai = Label(image=bai)
        lab_bai.place(relx=0.8, rely=0.02)

