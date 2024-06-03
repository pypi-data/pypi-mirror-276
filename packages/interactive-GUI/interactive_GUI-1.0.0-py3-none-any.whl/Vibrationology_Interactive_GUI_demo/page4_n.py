from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
import numpy as np
from vpython import *
from tkinter import *


# 角谐振动
class page4_1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("角谐振动")
        self.running = False
        self.createWidget()

    def start(self):
        self.running = True
        t = 0.0
        t_end = float(self.ask_t.get())  # 时间
        g = 9.8  # 重力加速度
        xl = float(self.ask_l.get())  # 摆长
        dt = 0.01  # 时间步长
        theta = float(self.ask_theat.get()) * pi  # 初始角度
        omiga = 0.  # 初始角速度
        n = int(t_end / dt)  # 迭代次数
        ThetaT0 = []  # 存储角度
        OmigaT0 = []  # 存储角速度
        Time0 = []  # 存储时间

        # 进行迭代计算
        for i in range(n):
            # 使用四阶龙格-库塔法进行数值解求解
            xk1 = -(g / xl) * theta
            xl1 = omiga
            xk2 = -(g / xl) * (theta + dt / 2. * xl1)
            xl2 = omiga + dt / 2. * xk1
            xk3 = -(g / xl) * (theta + dt / 2. * xl2)
            xl3 = omiga + dt / 2. * xk2
            xk4 = -(g / xl) * (theta + dt * xl3)
            xl4 = omiga + dt * xk3

            # 计算下一个时间步的角度和角速度
            omiga = omiga + dt / 6. * (xk1 + 2 * xk2 + 2 * xk3 + xk4)
            theta = theta + dt / 6. * (xl1 + 2 * xl2 + 2 * xl3 + xl4)
            t = t + dt

            ThetaT0.append(theta)
            OmigaT0.append(omiga)
            Time0.append(t)

        if self.running:
            s1 = canvas(title="角谐振动", width=700, height=494.5, background=color.black, center=vector(0, 0, 0), x=0,
                        y=0, align="left")
            base = box(pos=vector(0, 0.5 * xl, 0), size=vec(0.5 * xl, 0.01 * xl, 0.5 * xl))
            ball = sphere(pos=vec(-xl * sin(theta), 0.5 * xl - xl * cos(theta), 0), radius=0.05 * xl, color=color.cyan,
                          shininess=0.6)
            rod = cylinder(pos=base.pos, axis=ball.pos - base.pos, radius=0.005 * xl, color=color.white, opacity=0.8)
            g1 = graph(width=600, height=400, title="θ_t", xtitle="t(s)", ytitle="θ(rad)", align="left")
            g2 = graph(width=600, height=400, title="θ_ω", xtitle="θ(rad)", ytitle="ω(rad)", align="left")
            theat_t = gcurve(graph=g1, color=color.red)
            theat_omega = gcurve(graph=g2, color=color.green)

            s2 = canvas(width=500, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 4, 0), text="角谐运动的演示", color=color.green, box=False, height=25)
            lab_l = label(canvas=s2, pos=vec(0, 1, 0), text=f"l={self.ask_l.get()}m", color=color.green, box=False,
                          height=20)
            lab_theta = label(canvas=s2, pos=vec(0, -1, 0), text=f"θ={self.ask_theat.get()}π", color=color.green,
                              box=False, height=20)

            for i in range(n):
                rate(int(1 / dt))
                ball.pos = vec(-xl * sin(ThetaT0[i]), 0.5 * xl - xl * cos(ThetaT0[i]), 0)
                rod.axis = ball.pos - base.pos
                theat_t.plot(Time0[i], ThetaT0[i])
                theat_omega.plot(ThetaT0[i], OmigaT0[i])
                self.update()

    def createWidget(self):
        from page_4 import page_4
        lab_t = Label(self, text="演示时长t:", font=("Consolas", 16))
        lab_t.place(relx=0.25, rely=0.15)
        lab_l = Label(self, text="摆长l:", font=("Consolas", 16))
        lab_l.place(relx=0.25, rely=0.35)
        lab_theat = Label(self, text="初始角度theat(π):", font=("Consolas", 16))
        lab_theat.place(relx=0.25, rely=0.55)

        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.25, rely=0.25)
        self.ask_l = Entry(self, font=("Consolas", 16), width=25)
        self.ask_l.place(relx=0.25, rely=0.45)
        self.ask_theat = Entry(self, font=("Consolas", 16), width=25)
        self.ask_theat.place(relx=0.25, rely=0.65)

        start_btn = Button(self, text="开始", font=("Consolas", 16), command=self.start)
        start_btn.place(relx=0.75, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_4))
        returnBtn.place(relx=0.15, rely=0.8)
        lab = Label(self, text="时间过长会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)


# 大角度单摆
class page4_2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("大角度单摆")
        self.running = False
        self.createWidget()

    def start(self):
        self.running = True
        t = 0.0
        t_end = float(self.ask_t.get())  # 时间
        g = 9.8  # 重力加速度
        xl = float(self.ask_l.get())  # 摆长
        dt = 0.02  # 时间步长
        theta = float(self.ask_theat.get()) * pi  # 初始角度
        omiga = 0.  # 初始角速度
        n = int(t_end / dt)  # 迭代次数
        ThetaT0 = []  # 存储角度
        OmigaT0 = []  # 存储角速度
        Time0 = []  # 存储时间

        for i in range(n):
            xk1 = -(g / xl) * sin(theta)
            xl1 = omiga
            xk2 = -(g / xl) * sin(theta + dt / 2. * xl1)
            xl2 = omiga + dt / 2. * xk1
            xk3 = -(g / xl) * sin(theta + dt / 2. * xl2)
            xl3 = omiga + dt / 2. * xk2
            xk4 = -(g / xl) * sin(theta + dt * xl3)
            xl4 = omiga + dt * xk3

            omiga = omiga + dt / 6. * (xk1 + 2. * xk2 + 2. * xk3 + xk4)
            theta = theta + dt / 6. * (xl1 + 2. * xl2 + 2. * xl3 + xl4)
            t = t + dt
            ThetaT0.append(theta)
            OmigaT0.append(omiga)
            Time0.append(t)

        if self.running:
            s1 = canvas(title="大角度单摆", width=700, height=494.5, background=color.black, center=vector(0, 0, 0),
                        x=0, y=0, align='left')
            base = box(pos=vector(0, 0.5 * xl, 0), size=vec(0.5 * xl, 0.01 * xl, 0.5 * xl))
            ball = sphere(pos=vec(-xl * sin(theta), 0.5 * xl - xl * cos(theta), 0), radius=0.05 * xl, color=color.cyan,
                          shininess=0.6)
            rod = cylinder(pos=base.pos, axis=ball.pos - base.pos, radius=0.005 * xl, color=color.white, opacity=0.8)
            g1 = graph(width=600, height=400, title="θ_t", xtitle="t(s)", ytitle="θ(rad)", align="left")
            g2 = graph(width=600, height=400, title="θ_ω", xtitle="θ(rad)", ytitle="ω(rad)", align="left")
            theat_t = gcurve(graph=g1, color=color.red)
            theat_omega = gcurve(graph=g2, color=color.green)

            s2 = canvas(width=500, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 4, 0), text="大角度单摆的演示", color=color.green, box=False,
                           height=25)
            lab_l = label(canvas=s2, pos=vec(0, 1, 0), text=f"l={self.ask_l.get()}m", color=color.green, box=False,
                          height=20)
            lab_theta = label(canvas=s2, pos=vec(0, -1, 0), text=f"θ={self.ask_theat.get()}π", color=color.green,
                              box=False, height=20)

            for i in range(n):
                rate(1 / dt)
                ball.pos = vec(-xl * sin(ThetaT0[i]), 0.5 * xl - xl * cos(ThetaT0[i]), 0)
                rod.axis = ball.pos - base.pos
                theat_t.plot(Time0[i], ThetaT0[i])
                theat_omega.plot(ThetaT0[i], OmigaT0[i])
                self.update()

    def createWidget(self):
        from page_4 import page_4
        lab_t = Label(self, text="演示时长t:", font=("Consolas", 16))
        lab_t.place(relx=0.25, rely=0.15)
        lab_l = Label(self, text="摆长l:", font=("Consolas", 16))
        lab_l.place(relx=0.25, rely=0.35)
        lab_theat = Label(self, text="初始角度theat(π):", font=("Consolas", 16))
        lab_theat.place(relx=0.25, rely=0.55)

        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.25, rely=0.25)
        self.ask_l = Entry(self, font=("Consolas", 16), width=25)
        self.ask_l.place(relx=0.25, rely=0.45)
        self.ask_theat = Entry(self, font=("Consolas", 16), width=25)
        self.ask_theat.place(relx=0.25, rely=0.65)

        start_btn = Button(self, text="开始", font=("Consolas", 16), command=self.start)
        start_btn.place(relx=0.75, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_4))
        returnBtn.place(relx=0.15, rely=0.8)
        lab = Label(self, text="时间过长会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)


# 阻尼单摆
class page4_3(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("阻尼单摆")
        self.running = False

        self.createWidget()

    def start(self):
        self.running = True
        t = 0.0
        t_end = float(self.ask_t.get())
        g = 9.8
        xl = float(self.ask_l.get())
        k = float(self.ask_k.get())  # 临界阻尼k = 2√g/l
        dt = 0.02
        theta = float(self.ask_theat.get()) * pi
        omiga = 0.
        n = int(t_end / dt)

        ThetaT0 = []
        OmigaT0 = []
        Time0 = []
        for i in range(n):
            xk1 = -(g / xl) * theta - k * omiga
            xl1 = omiga
            xk2 = -(g / xl) * (theta + dt / 2. * xl1) - k * (omiga + dt / 2. * xk1)
            xl2 = omiga + dt / 2. * xk1
            xk3 = -(g / xl) * (theta + dt / 2. * xl2) - k * (omiga + dt / 2. * xk2)
            xl3 = omiga + dt / 2. * xk2
            xk4 = -(g / xl) * (theta + dt * xl3) - k * (omiga + dt * xk3)
            xl4 = omiga + dt * xk3

            omiga = omiga + dt / 6. * (xk1 + 2 * xk2 + 2 * xk3 + xk4)
            theta = theta + dt / 6. * (xl1 + 2 * xl2 + 2 * xl3 + xl4)
            t = t + dt
            ThetaT0.append(theta)
            OmigaT0.append(omiga)
            Time0.append(t)

        if self.running:
            s1 = canvas(title="阻尼单摆", width=700, height=494.5, background=color.black, center=vector(0, 0, 0), x=0,
                        y=0, align='left')

            base = box(pos=vector(0, 0.5 * xl, 0), size=vec(0.5 * xl, 0.01 * xl, 0.5 * xl))
            ball = sphere(pos=vec(-xl * sin(theta), 0.5 * xl - xl * cos(theta), 0), radius=0.05 * xl, color=color.cyan,
                          shininess=0.6)
            rod = cylinder(pos=base.pos, axis=ball.pos - base.pos, radius=0.005 * xl, color=color.white, opacity=0.8)
            g1 = graph(width=500, height=400, title="θ_t", xtitle="t(s)", ytitle="θ(rad)", align="left")
            g2 = graph(width=500, height=400, title="θ_ω", xtitle="θ(rad)", ytitle="ω(rad)", align="left")
            theat_t = gcurve(graph=g1, color=color.red)
            theat_omega = gcurve(graph=g2, color=color.green)

            s2 = canvas(width=500, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 4, 0), text="阻尼单摆的演示", color=color.green, box=False, height=25)
            lab_l = label(canvas=s2, pos=vec(0, 1, 0), text=f"l={self.ask_l.get()}m", color=color.green, box=False,
                          height=20)
            lab_theta = label(canvas=s2, pos=vec(0, -1, 0), text=f"θ={self.ask_theat.get()}π", color=color.green,
                              box=False, height=20)
            lab_gama = label(canvas=s2, pos=vec(0, -3, 0), text=f"r={self.ask_k.get()}", color=color.green, box=False,
                             height=20)

            for i in range(n):
                rate(1 / dt)
                ball.pos = vec(-xl * sin(ThetaT0[i]), 0.5 * xl - xl * cos(ThetaT0[i]), 0)
                rod.axis = ball.pos - base.pos
                theat_t.plot(Time0[i], ThetaT0[i])
                theat_omega.plot(ThetaT0[i], OmigaT0[i])
                self.update()

    def createWidget(self):
        from page_4 import page_4
        lab_t = Label(self, text="演示时间t:", font=("Consolas", 16))
        lab_t.place(relx=0.25, rely=0.05)
        lab_l = Label(self, text="摆长l:", font=("Consolas", 16))
        lab_l.place(relx=0.25, rely=0.23)
        lab_theat = Label(self, text="初始角度theat(π):", font=("Consolas", 16))
        lab_theat.place(relx=0.25, rely=0.41)
        lab_theat = Label(self, text="阻尼系数r(临界阻尼:2√g/l):", font=("Consolas", 16))
        lab_theat.place(relx=0.25, rely=0.59)

        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.25, rely=0.14)
        self.ask_l = Entry(self, font=("Consolas", 16), width=25)
        self.ask_l.place(relx=0.25, rely=0.32)
        self.ask_theat = Entry(self, font=("Consolas", 16), width=25)
        self.ask_theat.place(relx=0.25, rely=0.50)
        self.ask_k = Entry(self, font=("Consolas", 16), width=25)
        self.ask_k.place(relx=0.25, rely=0.68)

        start_btn = Button(self, text="开始", font=("Consolas", 16), command=self.start)
        start_btn.place(relx=0.75, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_4))
        returnBtn.place(relx=0.15, rely=0.8)
        lab = Label(self, text="时间过长会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)


# 受迫单摆
class page4_4(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("受迫单摆")
        self.running = False
        self.createWidget()

    def start(self):
        self.running = True
        t = 0.0
        t_end = float(self.ask_t.get())
        g = 9.8
        xl = float(self.ask_l.get())
        k = float(self.ask_k.get())
        F = float(self.ask_f.get())
        W = (g / xl) ** 0.5
        dt = 0.02
        theta = float(self.ask_theat.get()) * pi
        omiga = 0.
        n = int(t_end / dt)
        ThetaT0 = []
        OmigaT0 = []
        Time0 = []
        for i in range(n):
            xk1 = -(g / xl) * theta - k * omiga + F * sin(W * t)
            xl1 = omiga
            xk2 = -(g / xl) * (theta + dt / 2. * xl1) - k * (omiga + dt / 2. * xk1) + F * sin(W * t)
            xl2 = omiga + dt / 2. * xk1
            xk3 = -(g / xl) * (theta + dt / 2. * xl2) - k * (omiga + dt / 2. * xk2) + F * sin(W * t)
            xl3 = omiga + dt / 2. * xk2
            xk4 = -(g / xl) * (theta + dt * xl3) - k * (omiga + dt * xk3) + F * sin(W * t)
            xl4 = omiga + dt * xk3

            omiga = omiga + dt / 6. * (xk1 + 2 * xk2 + 2 * xk3 + xk4)
            theta = theta + dt / 6. * (xl1 + 2 * xl2 + 2 * xl3 + xl4)
            t = t + dt
            ThetaT0.append(theta)
            OmigaT0.append(omiga)
            Time0.append(t)

        if self.running:
            s1 = canvas(title="受迫单摆", width=700, height=494.5, background=color.black, center=vector(0, 0, 0), x=0,
                        y=0, align='left')
            base = box(pos=vector(0, 0.5 * xl, 0), size=vec(0.5 * xl, 0.01 * xl, 0.5 * xl))
            ball = sphere(pos=vec(-xl * sin(theta), 0.5 * xl - xl * cos(theta), 0), radius=0.05 * xl, color=color.cyan,
                          shininess=0.6)
            rod = cylinder(pos=base.pos, axis=ball.pos - base.pos, radius=0.005 * xl, color=color.white, opacity=0.8)
            g1 = graph(width=600, height=400, title="θ_t", xtitle="t(s)", ytitle="θ(rad)", align="left")
            g2 = graph(width=600, height=400, title="θ_ω", xtitle="θ(rad)", ytitle="ω(rad)", align="left")
            theat_t = gcurve(graph=g1, color=color.red)
            theat_omega = gcurve(graph=g2, color=color.green)

            s2 = canvas(width=500, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 4, 0), text="受迫单摆的演示", color=color.green, box=False, height=25)
            lab_l = label(canvas=s2, pos=vec(0, 1, 0), text=f"l={self.ask_l.get()}m", color=color.green, box=False,
                          height=20)
            lab_theta = label(canvas=s2, pos=vec(0, -1, 0), text=f"θ={self.ask_theat.get()}π", color=color.green,
                              box=False, height=20)
            lab_gama = label(canvas=s2, pos=vec(0, -3, 0), text=f"r={self.ask_k.get()}", color=color.green, box=False,
                             height=20)
            lab_gama = label(canvas=s2, pos=vec(0, -5, 0), text=f"r={self.ask_f.get()}sin({W:.2f}t)N",
                             color=color.green, box=False, height=20)

            for i in range(n):
                rate(1 / dt)
                ball.pos = vec(-xl * sin(ThetaT0[i]), 0.5 * xl - xl * cos(ThetaT0[i]), 0)
                rod.axis = ball.pos - base.pos
                theat_t.plot(Time0[i], ThetaT0[i])
                theat_omega.plot(ThetaT0[i], OmigaT0[i])
                self.update()

    def createWidget(self):
        from page_4 import page_4
        lab_t = Label(self, text="演示时间t:", font=("Consolas", 14))
        lab_t.place(relx=0.27, rely=0.05)
        lab_l = Label(self, text="摆长l:", font=("Consolas", 14))
        lab_l.place(relx=0.27, rely=0.19)
        lab_theat = Label(self, text="初始角度theat(π):", font=("Consolas", 14))
        lab_theat.place(relx=0.27, rely=0.33)
        lab_k = Label(self, text="阻尼系数r:", font=("Consolas", 14))
        lab_k.place(relx=0.27, rely=0.47)
        lab_f = Label(self, text="策动力F:", font=("Consolas", 14))
        lab_f.place(relx=0.27, rely=0.61)

        self.ask_t = Entry(self, font=("Consolas", 14), width=25)
        self.ask_t.place(relx=0.27, rely=0.12)
        self.ask_l = Entry(self, font=("Consolas", 14), width=25)
        self.ask_l.place(relx=0.27, rely=0.26)
        self.ask_theat = Entry(self, font=("Consolas", 14), width=25)
        self.ask_theat.place(relx=0.27, rely=0.40)
        self.ask_k = Entry(self, font=("Consolas", 14), width=25)
        self.ask_k.place(relx=0.27, rely=0.54)
        self.ask_f = Entry(self, font=("Consolas", 14), width=25)
        self.ask_f.place(relx=0.27, rely=0.68)

        start_btn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        start_btn.place(relx=0.75, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_4))
        returnBtn.place(relx=0.15, rely=0.8)
        lab = Label(self, text="时间过长会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)


# 混沌运动
class page4_5(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("混沌运动")
        self.running = False
        self.createWidget()

    def start(self):
        self.running = True
        t = 0.0
        t_end = float(self.ask_t.get())
        g = 9.8
        xl = float(self.ask_l.get())
        k = float(self.ask_k.get())
        F = float(self.ask_f.get())
        W = float(self.ask_omega.get())
        dt = 0.02
        theta = float(self.ask_theat.get()) * pi
        omiga = 0.
        n = int(t_end / dt)

        ThetaT0 = []
        OmigaT0 = []
        Time0 = []
        for i in range(n):
            xk1 = -(g / xl) * sin(theta) - k * omiga + F * sin(W * t)
            xl1 = omiga
            xk2 = -(g / xl) * sin(theta + dt / 2. * xl1) - k * (omiga + dt / 2. * xk1) + F * sin(W * t)
            xl2 = omiga + dt / 2. * xk1
            xk3 = -(g / xl) * sin(theta + dt / 2. * xl2) - k * (omiga + dt / 2. * xk2) + F * sin(W * t)
            xl3 = omiga + dt / 2. * xk2
            xk4 = -(g / xl) * sin(theta + dt * xl3) - k * (omiga + dt * xk3) + F * sin(W * t)
            xl4 = omiga + dt * xk3

            omiga = omiga + dt / 6. * (xk1 + 2 * xk2 + 2 * xk3 + xk4)
            theta = theta + dt / 6. * (xl1 + 2 * xl2 + 2 * xl3 + xl4)

            if (theta > pi):
                theta = theta - 2 * pi
            if (theta < -pi):
                theta = theta + 2 * pi

            t = t + dt
            ThetaT0.append(theta)
            OmigaT0.append(omiga)
            Time0.append(t)

        if self.running:
            s1 = canvas(title="阻尼单摆", width=700, height=490, background=color.black, center=vector(0, 0, 0), x=0,
                        y=0, align='left')
            base = box(pos=vector(0, 0, 0), size=vec(0.5 * xl, 0.01 * xl, 0.5 * xl))
            ball = sphere(pos=vec(-xl * sin(theta), -xl * cos(theta), 0), radius=0.05 * xl, color=color.cyan,
                          shininess=0.6)
            rod = cylinder(pos=base.pos, axis=ball.pos - base.pos, radius=0.005 * xl, color=color.white, opacity=0.8)
            g1 = graph(width=600, height=400, title="θ_t", xtitle="t(s)", ytitle="θ(rad)", align="left")
            g2 = graph(width=600, height=400, title="θ_ω", xtitle="θ(rad)", ytitle="ω(rad)", align="left")
            theat_t = gcurve(graph=g1, color=color.red)
            theat_omega = gcurve(graph=g2, color=color.green)

            s2 = canvas(width=500, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 4, 0), text="混沌运动的0演示", color=color.green, box=False, height=25)
            lab_l = label(canvas=s2, pos=vec(0, 1, 0), text=f"l={self.ask_l.get()}m", color=color.green, box=False,
                          height=20)
            lab_theta = label(canvas=s2, pos=vec(0, -1, 0), text=f"θ={self.ask_theat.get()}π", color=color.green,
                              box=False, height=20)
            lab_gama = label(canvas=s2, pos=vec(0, -3, 0), text=f"r={self.ask_k.get()}", color=color.green, box=False,
                             height=20)
            lab_F = label(canvas=s2, pos=vec(0, -5, 0), text=f"r={self.ask_f.get()}sin({self.ask_omega.get()}t)N",
                          color=color.green, box=False, height=20)

            for i in range(n):
                rate(1 / dt)
                ball.pos = vec(-xl * sin(ThetaT0[i]), -xl * cos(ThetaT0[i]), 0)
                rod.axis = ball.pos - base.pos
                theat_t.plot(Time0[i], ThetaT0[i])
                theat_omega.plot(ThetaT0[i], OmigaT0[i])
                self.update()

    def createWidget(self):
        from page_4 import page_4
        lab_t = Label(self, text="演示时长t:", font=("Consolas", 14))
        lab_t.place(relx=0.27, rely=0.05)
        lab_l = Label(self, text="摆长l:", font=("Consolas", 14))
        lab_l.place(relx=0.27, rely=0.17)
        lab_theat = Label(self, text="初始角度theat(π):", font=("Consolas", 14))
        lab_theat.place(relx=0.27, rely=0.29)
        lab_k = Label(self, text="阻尼系数r:", font=("Consolas", 14))
        lab_k.place(relx=0.27, rely=0.41)
        lab_f = Label(self, text="策动力F(F=Asin(ωt)):", font=("Consolas", 14))
        lab_f.place(relx=0.27, rely=0.53)
        lab_omega = Label(self, text="策动力频率ω:", font=("Consolas", 14))
        lab_omega.place(relx=0.27, rely=0.65)

        self.ask_t = Entry(self, font=("Consolas", 14), width=25)
        self.ask_t.place(relx=0.27, rely=0.11)
        self.ask_l = Entry(self, font=("Consolas", 14), width=25)
        self.ask_l.place(relx=0.27, rely=0.23)
        self.ask_theat = Entry(self, font=("Consolas", 14), width=25)
        self.ask_theat.place(relx=0.27, rely=0.35)
        self.ask_k = Entry(self, font=("Consolas", 14), width=25)
        self.ask_k.place(relx=0.27, rely=0.47)
        self.ask_f = Entry(self, font=("Consolas", 14), width=25)
        self.ask_f.place(relx=0.27, rely=0.59)
        self.ask_omega = Entry(self, font=("Consolas", 14), width=25)
        self.ask_omega.place(relx=0.27, rely=0.71)

        start_btn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        start_btn.place(relx=0.75, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_4))
        returnBtn.place(relx=0.15, rely=0.8)
        lab = Label(self, text="时间过长会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)


# 倍周期分叉
class page4_6(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("倍周期分叉")
        self.createWidget()

    def start(self):
        import pylab as pl
        g = 9.8
        xl = float(self.ask_l.get())
        q = float(self.ask_q.get())
        F_start = float(self.ask_F_start.get())
        F_end = float(self.ask_F_end.get())
        theat_0 = float(self.ask_theat.get()) * pi
        W = float(self.ask_W.get())
        n = int(10000 * (F_end - F_start))

        dt = 0.04
        twopi = 2 * np.pi
        ThetaT0 = []
        F0 = []

        for F in np.arange(F_start, F_end, 0.01):
            theta = theat_0
            omiga = 0.
            t = 0.0
            for i in range(n):
                xk1 = -(g / xl) * np.sin(theta) - q * omiga + F * np.sin(W * t)
                xl1 = omiga
                xk2 = -(g / xl) * np.sin(theta + dt / 2. * xl1) - q * (omiga + dt / 2. * xk1) + F * np.sin(
                    W * (t + dt / 2))
                xl2 = omiga + dt / 2. * xk1
                xk3 = -(g / xl) * np.sin(theta + dt / 2. * xl2) - q * (omiga + dt / 2. * xk2) + F * np.sin(
                    W * (t + dt / 2))
                xl3 = omiga + dt / 2. * xk2
                xk4 = -(g / xl) * np.sin(theta + dt * xl3) - q * (omiga + dt * xk3) + F * np.sin(W * (t + dt))
                xl4 = omiga + dt * xk3

                omiga = omiga + dt / 6. * (xk1 + 2 * xk2 + 2 * xk3 + xk4)
                theta = theta + dt / 6. * (xl1 + 2 * xl2 + 2 * xl3 + xl4)

                if (theta > np.pi):
                    theta = theta - np.pi * 2.
                if (theta < -np.pi):
                    theta = theta + np.pi * 2.
                t = t + dt

                if abs(W * t / twopi - int(W * t / twopi + 1.0e-6)) < 0.005 and t > 99.9:
                    ThetaT0.append(theta)
                    F0.append(F)
        fig = pl.figure(figsize=(8, 5))
        pl.plot(F0, ThetaT0, 'r.', linewidth=0.1, ms=3.0)

        pl.ylabel(r'Theta', fontsize=20)
        pl.xlabel(r'F', fontsize=20)

        pl.show()

    def createWidget(self):
        from page_4 import page_4
        lab_F_start = Label(self, text="策动力最小值F_min:", font=("Consolas", 14))
        lab_F_start.place(relx=0.27, rely=0.03)
        lab_F_end = Label(self, text="策动力最大值F_max:", font=("Consolas", 14))
        lab_F_end.place(relx=0.27, rely=0.15)
        lab_W = Label(self, text="策动力频率omega", font=("Consolas", 14))
        lab_W.place(relx=0.27, rely=0.27)
        lab_l = Label(self, text="摆长l:", font=("Consolas", 14))
        lab_l.place(relx=0.27, rely=0.39)
        lab_theat = Label(self, text="初始角度theat(π):", font=("Consolas", 14))
        lab_theat.place(relx=0.27, rely=0.51)
        lab_q = Label(self, text="阻力f:", font=("Consolas", 14))
        lab_q.place(relx=0.27, rely=0.63)

        self.ask_F_start = Entry(self, font=("Consolas", 14), width=25)
        self.ask_F_start.place(relx=0.27, rely=0.09)
        self.ask_F_end = Entry(self, font=("Consolas", 14), width=25)
        self.ask_F_end.place(relx=0.27, rely=0.21)
        self.ask_W = Entry(self, font=("Consolas", 14), width=25)
        self.ask_W.place(relx=0.27, rely=0.33)
        self.ask_l = Entry(self, font=("Consolas", 14), width=25)
        self.ask_l.place(relx=0.27, rely=0.45)
        self.ask_theat = Entry(self, font=("Consolas", 14), width=25)
        self.ask_theat.place(relx=0.27, rely=0.57)
        self.ask_q = Entry(self, font=("Consolas", 14), width=25)
        self.ask_q.place(relx=0.27, rely=0.69)

        start_btn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        start_btn.place(relx=0.75, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_4))
        returnBtn.place(relx=0.15, rely=0.8)
        lab = Label(self, text="策动力范围过大会导致运算量变大,如点击开始后没反应请耐心等待",
                    font=("Consolas", 10)).place(rely=0.95, relx=0.18)

