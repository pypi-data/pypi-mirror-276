from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
from vpython import *
from tkinter import *


# 阻尼
class page2_1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("阻尼振动")
        self.running = False

        # 初始化振动物体的状态
        self.pos0 = vector(5, 0, 0)  # 初始位置
        self.v0 = vector(0, 0, 0)  # 初始速度

        self.createWidget()

    def start(self):
        self.running = True
        t = 0
        dt = 0.01
        t_end = float(self.ask_t.get())
        k = float(self.ask_k.get())
        beta = float(self.ask_beta.get())
        m = float(self.ask_m.get())

        def a(ball_pos, v, k, gamma, m):
            x = ball_pos - spring.pos
            spring_force = -k * x
            damping_force = -beta * v
            net_force = spring_force + damping_force
            acceleration = net_force / m
            return acceleration

        if self.running:
            s1 = canvas(width=800, height=494, center=vec(0, 0, 0), background=color.black, align='left')
            # 创建一个球体作为振动物体
            ball = sphere(pos=self.pos0, radius=0.5, color=color.cyan)
            # 创建一个弹簧
            spring = helix(pos=vector(0, 0, 0), axis=ball.pos - vector(0, 0, 0), radius=0.3, coils=10, thickness=0.1,
                           color=color.white)
            # 图像
            graph_x = graph(title='位移与时间的关系', width=500, height=400, xtitle='时间/t', ytitle='位移/m',
                            xmax=t_end, xmin=0, align="left")
            xt = gcurve(graph=graph_x, color=color.red, label='位移')
            graph_v = graph(title='速度与时间的关系', width=500, height=400, xtitle='时间/t', ytitle='速度/(m/s)',
                            xmin=0, xmax=t_end, align="left")
            vt = gcurve(graph=graph_v, color=color.red, label='速度')
            graph_a = graph(title='加速度与时间的关系', width=500, height=400, xtitle='时间/t',
                            ytitle='加速度/(m/(s*s))', xmin=0, xmax=t_end, align="left")
            at = gcurve(graph=graph_a, color=color.red, label='加速度')
            # 创造X，Y方向的坐标轴
            X = arrow(pos=vec(-10, 0, 0), axis=vec(20, 0, 0), shaftwidth=0.2, label="X", color=color.white)
            Y = arrow(pos=vec(0, -10, 0), axis=vec(0, 20, 0), shaftwidth=0.2, label="Y", color=color.white)

            s2 = canvas(width=700, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 3, 0), text="阻尼振动的演示", color=color.green, box=False, height=25)
            lab_k = label(canvas=s2, pos=vec(0, 1, 0), text=f"k={self.ask_k.get()}N/m", color=color.green, box=False,
                          height=20)
            lab_beta = label(canvas=s2, pos=vec(0, 0, 0), text=f"r={self.ask_beta.get()}", color=color.green, box=False,
                             height=20)
            lab_m = label(canvas=s2, pos=vec(0, -1, 0), text=f"m={self.ask_m.get()}kg", color=color.green, box=False,
                          height=20)

            # 计算阻尼振动的运动
            while t < t_end:  # 模拟时间为10秒
                rate(int(1 / dt))  # 控制动画的帧率
                # 计算k1
                a1 = a(ball.pos, self.v0, k, gamma, m)
                v1 = self.v0 + a1 * dt
                x1 = v1 * dt

                # 计算k2
                a2 = a(ball.pos + 1 / 2 * x1, self.v0 + 1 / 2 * a1 * dt, k, gamma, m)
                v2 = self.v0 + a2 * dt
                x2 = v2 * dt

                # 计算k3
                a3 = a(ball.pos + 0.5 * x2, self.v0 + 0.5 * a2 * dt, k, gamma, m)
                v3 = self.v0 + a3 * dt
                x3 = v3 * dt

                # 计算k4
                a4 = a(ball.pos + x3, self.v0 + a3 * dt, k, gamma, m)
                v4 = self.v0 + a4 * dt
                x4 = v4 * dt

                # 更新位置和速度
                ball.pos += (x1 + 2 * x2 + 2 * x3 + x4) / 6
                self.v0 += (a1 + 2 * a2 + 2 * a3 + a4) / 6 * dt
                ball_a = (a1 + 2 * a2 + 2 * a3 + a4) / 6

                # 插入图标
                xt.plot(t, ball.pos.x)
                vt.plot(t, self.v0.x)
                at.plot(t, ball_a.x)
                # 更新弹簧的位置
                spring.axis = ball.pos - spring.pos
                t += dt
                self.update()

    def createWidget(self):
        from page_2 import page_2
        # 提示
        lab_t = Label(self, text="演示时长t", font=("Consolas", 16))
        lab_t.place(relx=0.25, rely=0.08)
        lab_beta = Label(self, text="阻尼系数r(临界阻尼为:2√km)", font=("Consolas", 16))
        lab_beta.place(relx=0.25, rely=0.24)
        lab_k = Label(self, text="弹簧常数k", font=("Consolas", 16))
        lab_k.place(relx=0.25, rely=0.40)
        lab_m = Label(self, text="物体质量m", font=("Consolas", 16))
        lab_m.place(relx=0.25, rely=0.56)

        # 输入框
        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.25, rely=0.16)
        self.ask_beta = Entry(self, font=("Consolas", 16), width=25)
        self.ask_beta.place(relx=0.25, rely=0.32)
        self.ask_k = Entry(self, font=("Consolas", 16), width=25)
        self.ask_k.place(relx=0.25, rely=0.48)
        self.ask_m = Entry(self, font=("Consolas", 16), width=25)
        self.ask_m.place(relx=0.25, rely=0.64)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.75, rely=0.75)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_2))
        returnBtn.place(relx=0.15, rely=0.75)


# 受迫振动
class page2_2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("受迫振动")
        self.running = False

        self.createWidget()

    def createWidget(self):
        from page_2 import page_2
        # 提示
        lab_t = Label(self, text="演示时长t:", font=("Consolas", 16))
        lab_t.place(relx=0.26, rely=0.03)
        lab_cedongli = Label(self, text="策动力(形如:Hcos(ωt)):", font=("Consolas", 16))
        lab_cedongli.place(relx=0.26, rely=0.17)
        lab_gama = Label(self, text="阻尼系数r:", font=("Consolas", 16))
        lab_gama.place(relx=0.26, rely=0.38)
        lab_k = Label(self, text="弹性系数k:", font=("Consolas", 16))
        lab_k.place(relx=0.26, rely=0.52)
        lab_m = Label(self, text="物体质量m:", font=("Consolas", 16))
        lab_m.place(relx=0.26, rely=0.66)
        lab_H = Label(self, text="H:", font=("Consolas", 16))
        lab_H.place(relx=0.22, rely=0.233)
        lab_w = Label(self, text="ω:", font=("Consolas", 16))
        lab_w.place(relx=0.22, rely=0.303)

        # 输入框
        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.26, rely=0.1)
        self.ask_H = Entry(self, font=("Consolas", 16), width=25)
        self.ask_H.place(relx=0.26, rely=0.24)
        self.ask_omega = Entry(self, font=("Consolas", 16), width=25)
        self.ask_omega.place(relx=0.26, rely=0.31)
        self.ask_gama = Entry(self, font=("Consolas", 16), width=25)
        self.ask_gama.place(relx=0.26, rely=0.45)
        self.ask_k = Entry(self, font=("Consolas", 16), width=25)
        self.ask_k.place(relx=0.26, rely=0.59)
        self.ask_m = Entry(self, font=("Consolas", 16), width=25)
        self.ask_m.place(relx=0.26, rely=0.73)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.8, rely=0.82)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_2))
        returnBtn.place(relx=0.15, rely=0.82)

    def start(self):
        self.running = True
        t_end = 20
        H = 20
        omega = 2
        gama = 2
        k = 1
        pos0 = vector(1, 0, 0)  # 初始位置
        v0 = vector(0, 0, 0)  # 初始速度
        F0 = vec(0, 0, 0)
        F0.x = H

        t_end = float(self.ask_t.get())
        H = float(self.ask_H.get())
        omega = float(self.ask_omega.get())
        gama = float(self.ask_gama.get())
        k = float(self.ask_k.get())
        m = float(self.ask_m.get())
        dt = 0.01
        t = 0

        def a(ball_pos, v, k, gamma, m, omega, F0, t):
            x = ball_pos - spring.pos
            spring_force = -k * x
            damping_force = -gamma * v
            Fp = F0 * cos(omega * t)
            net_force = spring_force + damping_force + Fp
            acceleration = net_force / m
            return acceleration

        # 创建基础设施
        s1 = canvas(width=800, height=494, center=vec(0, 0, 0), background=color.black, align="left")
        ball = sphere(pos=pos0, radius=0.5, color=color.cyan)
        spring = helix(pos=vector(0, 0, 0), axis=ball.pos - vector(0, 0, 0), radius=0.3, coils=8, thickness=0.1,
                       color=color.white)
        X = arrow(pos=vec(-10, 0, 0), axis=vec(20, 0, 0), shaftwidth=0.2, label="X", color=color.white)
        Y = arrow(pos=vec(0, -10, 0), axis=vec(0, 20, 0), shaftwidth=0.2, label="Y", color=color.white)

        # 创建图像
        graph_x = graph(title='位移与时间的关系', width=500, height=400, xtitle='时间/t', ytitle='位移/m', xmax=t_end,
                        xmin=0, align="left")
        xt = gcurve(graph=graph_x, color=color.red, label='位移')
        graph_v = graph(title='速度与时间的关系', width=500, height=400, xtitle='时间/t', ytitle='速度/(m/s)', xmin=0,
                        xmax=t_end, align="left")
        vt = gcurve(graph=graph_v, color=color.red, label='速度')
        graph_a = graph(title='加速度与时间的关系', width=500, height=400, xtitle='时间/t', ytitle='加速度/(m/(s*s))',
                        xmin=0, xmax=t_end, align="left")
        at = gcurve(graph=graph_a, color=color.red, label='加速度')

        s2 = canvas(width=700, height=494.5, background=color.black, align="left")
        lanb_1 = label(canvas=s2, pos=vec(0, 3, 0), text="受迫振动的演示", color=color.green, box=False, height=25)
        lab_k = label(canvas=s2, pos=vec(0, 1, 0), text=f"k={self.ask_k.get()}N/m", color=color.green, box=False,
                      height=20)
        lab_gama = label(canvas=s2, pos=vec(0, 0, 0), text=f"r={self.ask_gama.get()}", color=color.green, box=False,
                         height=20)
        lab_m = label(canvas=s2, pos=vec(0, -1, 0), text=f"m={self.ask_m.get()}kg", color=color.green, box=False,
                      height=20)
        lab_F = label(canvas=s2, pos=vec(0, -2, 0), text=f"F={self.ask_H.get()}cos({self.ask_omega.get()}t)N",
                      color=color.green, box=False, height=20)

        if self.running:
            while t <= t_end:
                rate(int(1 / dt))  # 控制动画的帧率

                # 计算k1
                a1 = a(ball.pos, v0, k, gama, m, omega, F0, t)
                v1 = v0 + a1 * dt
                x1 = v1 * dt

                # 计算k2
                a2 = a(ball.pos + 1 / 2 * x1, v0 + 1 / 2 * a1 * dt, k, gama, m, omega, F0, t + dt / 2)
                v2 = v0 + a2 * dt
                x2 = v2 * dt

                # 计算k3
                a3 = a(ball.pos + 0.5 * x2, v0 + 0.5 * a2 * dt, k, gama, m, omega, F0, t + dt / 2)
                v3 = v0 + a3 * dt
                x3 = v3 * dt

                # 计算k4
                a4 = a(ball.pos + x3, v0 + a3 * dt, k, gama, m, omega, F0, t + dt)
                v4 = v0 + a4 * dt
                x4 = v4 * dt

                # 更新位置和速度
                ball.pos += (x1 + 2 * x2 + 2 * x3 + x4) / 6
                v0 += (a1 + 2 * a2 + 2 * a3 + a4) / 6 * dt
                ball_a = (a1 + 2 * a2 + 2 * a3 + a4) / 6

                # 插入图标
                xt.plot(t, ball.pos.x)
                vt.plot(t, v0.x)
                at.plot(t, ball_a.x)

                # 更新弹簧的位置
                spring.axis = ball.pos - spring.pos
                t += dt  # 更新时间
                self.update()

