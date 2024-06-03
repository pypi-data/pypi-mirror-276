from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
from vpython import *
from tkinter import *


# 简谐运动的演示
class page1_1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("简谐振动的演示（旋转矢量法）")
        self.running = False
        self.create_widgets()

    def exit(self):
        self.running = False
        self.master.destroy()

    def create_widgets(self):
        from page_1 import page_1
        # 创建entry组件并赋值
        Label(self, text="振幅A:", font=("Consolas", 16)).place(relx=0.25, rely=0.05)
        Label(self, text="角频率ω(π):", font=("Consolas", 16)).place(relx=0.25, rely=0.23)
        Label(self, text="初相位φ(π):", font=("Consolas", 16)).place(relx=0.25, rely=0.41)
        Label(self, text="持续时间t:", font=("Consolas", 16)).place(relx=0.25, rely=0.59)

        self.A_entry = Entry(self, font=("Consolas", 16), width=25)
        self.A_entry.place(relx=0.25, rely=0.14)
        self.omega_entry = Entry(self, font=("Consolas", 16), width=25)
        self.omega_entry.place(relx=0.25, rely=0.32)
        self.phi_entry = Entry(self, font=("Consolas", 16), width=25)
        self.phi_entry.place(relx=0.25, rely=0.50)
        self.t_end_entry = Entry(self, font=("Consolas", 16), width=25)
        self.t_end_entry.place(relx=0.25, rely=0.68)

        # 开始键和退出键
        self.start_button = Button(self, text="开始", font=("Consolas", 14), command=self.start_simulation)
        self.start_button.place(relx=0.8, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_1))
        returnBtn.place(relx=0.1, rely=0.8)

    def start_simulation(self):
        self.running = True
        self.A = float(self.A_entry.get())
        self.omega = float(self.omega_entry.get()) * pi
        self.phi = float(self.phi_entry.get()) * pi
        self.t_end = float(self.t_end_entry.get())
        t = 0
        dt = 0.01

        s1 = canvas(width=800, height=494.5, color=color.black, align="left")
        g1 = graph(width=500, height=340, scroll=True, xmin=0, xmax=self.t_end, align='left', xtitle='时间(s)',
                   ytitle='位移(m)')
        g2 = graph(width=500, height=340, scroll=True, xmin=0, xmax=self.t_end, align='left', xtitle='时间(s)',
                   ytitle='速度(m/s)')
        g3 = graph(width=500, height=340, scroll=True, xmin=0, xmax=self.t_end, align='left', xtitle='时间(s)',
                   ytitle='加速度(m/s^2)')
        x_plot = gcurve(graph=g1, color=color.red, label="x")
        v_plot = gcurve(graph=g2, color=color.green, label="v")
        a_plot = gcurve(graph=g3, color=color.blue, label="a")

        ball = sphere(pos=vec(self.A * cos(self.phi), self.A * cos(self.phi), 0), radius=0.2 * self.A, color=color.cyan)
        ball2 = sphere(pos=vec(ball.pos.x, 0, 0), radius=0.3, color=ball.color)
        r = ring(pos=vec(0, 0, 0), radius=self.A, thickness=ball.radius * 0.15, color=ball.color, axis=vector(0, 0, 1))
        v = self.A * vector(-self.omega * sin(self.omega * t + self.phi), self.omega * cos(self.omega * t + self.phi),
                            0)
        v_axis = arrow(pos=ball.pos, axis=v * 0.3, shaftwidth=ball.radius * 0.1, color=color.green)
        x_axis = arrow(pos=ball.pos, axis=-ball.pos, shaftwidth=ball.radius * 0.1, color=color.red)
        X = arrow(pos=vec(-self.A * 1.5, 0, 0), axis=vec(self.A * 3, 0, 0), shaftwidth=0.1, title="X",
                  color=color.white)
        Y = arrow(pos=vec(0, -self.A * 1.5, 0), axis=vec(0, self.A * 3, 0), shaftwidth=0.1, title="Y",
                  color=color.white)

        # 创建白线对象
        self.line = curve(pos=[ball.pos, ball2.pos], radius=0.05, color=ball.color)

        s2 = canvas(width=700, height=494.5, background=color.black, align="left")
        lanb_1 = label(canvas=s2, pos=vec(0, 7, 0), text="简谐运动的旋转矢量法演示", color=color.green, box=False,
                       height=25)
        lab_A = label(canvas=s2, pos=vec(0, 1, 0), text=f"A={self.A_entry.get()}", color=color.green, box=False,
                      height=20)
        lab_omega = label(canvas=s2, pos=vec(0, -1, 0), text=f"ω={self.omega_entry.get()}π", color=color.green,
                          box=False, height=20)
        lab_phi = label(canvas=s2, pos=vec(0, -3, 0), text=f"φ={self.phi_entry.get()}π", color=color.green, box=False,
                        height=20)

        if self.running:
            while t <= self.t_end:
                rate(int(1 / dt))
                t += dt
                x = self.A * vector(cos(self.omega * t + self.phi), sin(self.omega * t + self.phi), 0)
                v = self.A * vector(-self.omega * sin(self.omega * t + self.phi),
                                    self.omega * cos(self.omega * t + self.phi), 0)
                a = self.A * vector(-self.omega ** 2 * cos(self.omega * t + self.phi),
                                    -self.omega ** 2 * sin(self.omega * t + self.phi), 0)
                ball.pos = x
                ball2.pos.x = x.x
                v_axis.pos = ball.pos
                v_axis.axis = v * 0.3
                x_axis.pos = ball.pos
                x_axis.axis = -ball.pos

                # 更新白线的位置
                self.line.modify(0, pos=ball.pos)
                self.line.modify(1, pos=ball2.pos)

                x_plot.plot(t, x.x)
                v_plot.plot(t, v.x)
                a_plot.plot(t, a.x)
                self.update()


# 同向同频
class page1_2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.running = False
        self.master.title("简谐振动的合成(同向同频)")

        self.dt = 0.01
        self.t = 0

        self.create_widgets()  # 创建界面部件

    def start(self):
        self.running = True
        A1 = float(self.entry1.get())
        A2 = float(self.entry2.get())
        phi1 = float(self.entry3.get()) * pi
        phi2 = float(self.entry4.get()) * pi
        omega = float(self.entry5.get()) * pi
        t_end = float(self.entry6.get())

        if self.running:
            # 创建三个球体和箭头
            s1 = canvas(width=800, height=494, center=vec(0, 0, 0), background=color.black, align="left")
            self.ball1 = sphere(radius=max(A1, A2) * 0.1, color=color.cyan, opacity=0.8)
            self.ball2 = sphere(radius=max(A1, A2) * 0.1, color=color.green, opacity=0.8)
            self.ball3 = sphere(radius=max(A1, A2) * 0.1, color=color.magenta, opacity=0.8)

            self.v1_axis = arrow(shaftwidth=self.ball1.radius * 0.2, color=self.ball1.color)
            self.x1_axis = arrow(shaftwidth=self.ball1.radius * 0.2, color=self.ball1.color)
            self.v2_axis = arrow(shaftwidth=self.ball2.radius * 0.2, color=self.ball2.color)
            self.x2_axis = arrow(shaftwidth=self.ball2.radius * 0.2, color=self.ball2.color)
            self.v3_axis = arrow(shaftwidth=self.ball3.radius * 0.2, color=self.ball3.color)
            self.x3_axis = arrow(shaftwidth=self.ball3.radius * 0.2, color=self.ball3.color)

            # 创建 X、Y 轴和环
            self.X = arrow(pos=vec(-max(A1, A2) * 1.5, 0, 0), axis=vec(3 * max(A2, A1), 0, 0),
                           shaftwidth=min(A1, A2) * 0.1, label="X", color=color.white)
            self.Y = arrow(pos=vec(0, -max(A1, A2) * 1.5, 0), axis=vec(0, 3 * max(A2, A1), 0),
                           shaftwidth=min(A1, A2) * 0.1, label="Y", color=color.white)
            self.r = ring(pos=vec(0, 0, 0), radius=max(A1, A2), thickness=max(A1, A2) * 0.05, color=color.white,
                          axis=vec(0, 0, 1))

            # 添加连接球1和球3的白线
            self.line1 = curve(pos=[self.ball1.pos, self.ball3.pos], color=color.white, radius=self.ball3.radius * 0.05)

            # 添加连接球2和球3的白线
            self.line2 = curve(pos=[self.ball2.pos, self.ball3.pos], color=color.white, radius=self.ball3.radius * 0.05)

            # 创建三个图形窗口和图形曲线
            self.graph = graph(width=500, height=400, scroll=True, xmin=0, xmax=t_end, xtitle='时间(s)',
                               ytitle='位移(m)/速度(m/s)', title="ball3", align="left")
            self.x_plot = gcurve(graph=self.graph, color=color.red, label="x")
            self.v_plot = gcurve(graph=self.graph, color=color.yellow, label="v")

            self.graph1 = graph(width=500, height=400, scroll=True, xmin=0, xmax=t_end, xtitle='时间(s)',
                                ytitle='位移(m)/速度(m/s)', title="ball1", align="left")
            self.x1_plot = gcurve(graph=self.graph1, color=color.red, label="x")
            self.v1_plot = gcurve(graph=self.graph1, color=color.green, label="v")

            self.graph2 = graph(width=500, height=400, scroll=True, xmin=0, xmax=t_end, xtitle='时间(s)',
                                ytitle='位移(m)/速度(m/s)', title="ball2", align="left")
            self.x2_plot = gcurve(graph=self.graph2, color=color.orange, label="x")
            self.v2_plot = gcurve(graph=self.graph2, color=color.blue, label="v")

            s2 = canvas(width=700, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 7, 0), text="同向同频的简谐运动的合成旋转矢量法演示",
                           color=color.green, box=False, height=25)
            lab_A1 = label(canvas=s2, pos=vec(0, 3, 0), text=f"A1={self.entry1.get()}", color=color.green, box=False,
                           height=20)
            lab_A2 = label(canvas=s2, pos=vec(0, 1, 0), text=f"A2={self.entry2.get()}", color=color.green, box=False,
                           height=20)
            lab_omega = label(canvas=s2, pos=vec(0, -1, 0), text=f"ω={self.entry5.get()}π", color=color.green,
                              box=False, height=20)
            lab_phi1 = label(canvas=s2, pos=vec(0, -3, 0), text=f"φ1={self.entry3.get()}π", color=color.green,
                             box=False, height=20)
            lab_phi2 = label(canvas=s2, pos=vec(0, -5, 0), text=f"φ2={self.entry4.get()}π", color=color.green,
                             box=False, height=20)

            while self.t <= t_end:
                rate(int(1 / self.dt))

                # 计算球1和球2的位置和速度
                x1 = A1 * vec(cos(omega * self.t + phi1), sin(omega * self.t + phi1), 0)
                v1 = A1 * vec(-omega * sin(omega * self.t + phi1), omega * cos(omega * self.t + phi1), 0)

                x2 = A2 * vec(cos(omega * self.t + phi2), sin(omega * self.t + phi2), 0)
                v2 = A2 * vec(-omega * sin(omega * self.t + phi2), omega * cos(omega * self.t + phi2), 0)

                # 更新球1的位置、速度及箭头
                self.ball1.pos = x1
                self.v1_axis.pos = self.ball1.pos
                self.v1_axis.axis = v1 * 0.2
                self.x1_axis.pos = x1
                self.x1_axis.axis = -x1

                # 更新球2的位置、速度及箭头
                self.ball2.pos = x2
                self.v2_axis.pos = self.ball2.pos
                self.v2_axis.axis = v2 * 0.2
                self.x2_axis.pos = x2
                self.x2_axis.axis = -x2

                # 绘制球1和球2的位移和速度图像
                self.x1_plot.plot(self.t, x1.x)
                self.v1_plot.plot(self.t, v1.x)

                self.x2_plot.plot(self.t, x2.x)
                self.v2_plot.plot(self.t, v2.x)

                # 计算并绘制球1和球2合成后的位移
                self.x = x1 + x2
                self.v = v1 + v2
                self.x_plot.plot(self.t, self.x.x)
                self.v_plot.plot(self.t, self.v.x)

                # 更新球3的位置、速度及箭头
                self.ball3.pos = x1 + x2
                self.v3_axis.pos = self.ball3.pos
                self.v3_axis.axis = self.v * 0.2
                self.x3_axis.pos = self.x
                self.x3_axis.axis = -self.x

                # 更新连接球1和球3的白线的位置
                self.line1.modify(0, self.ball1.pos)
                self.line1.modify(1, self.ball3.pos)

                # 更新连接球2和球3的白线的位置
                self.line2.modify(0, self.ball2.pos)
                self.line2.modify(1, self.ball3.pos)
                self.t += self.dt
                self.update()

    def create_widgets(self):
        from page_1 import page_1
        # 创建标签和输入框，用于输入振幅、相位、角频率和总时间
        self.label1 = Label(self, text="振幅A1:", font=("Consolas", 16))
        self.label1.place(relx=0.15, rely=0.1)
        self.entry1 = Entry(self, font=("Consolas", 16), width=20)
        self.entry1.place(relx=0.42, rely=0.1)

        self.label2 = Label(self, text="振幅A2:", font=("Consolas", 16))
        self.label2.place(relx=0.15, rely=0.22)
        self.entry2 = Entry(self, font=("Consolas", 16), width=20)
        self.entry2.place(relx=0.42, rely=0.22)

        self.label3 = Label(self, text="初相phi1(π):", font=("Consolas", 16))
        self.label3.place(relx=0.15, rely=0.34)
        self.entry3 = Entry(self, font=("Consolas", 16), width=20)
        self.entry3.place(relx=0.42, rely=0.34)

        self.label4 = Label(self, text="初相phi2(π):", font=("Consolas", 16))
        self.label4.place(relx=0.15, rely=0.46)
        self.entry4 = Entry(self, font=("Consolas", 16), width=20)
        self.entry4.place(relx=0.42, rely=0.46)

        self.label5 = Label(self, text="角频率omega(π):", font=("Consolas", 16))
        self.label5.place(relx=0.15, rely=0.58)
        self.entry5 = Entry(self, font=("Consolas", 16), width=20)
        self.entry5.place(relx=0.42, rely=0.58)

        self.label6 = Label(self, text="演示时长t:", font=("Consolas", 16))
        self.label6.place(relx=0.15, rely=0.7)
        self.entry6 = Entry(self, font=("Consolas", 16), width=20)
        self.entry6.place(relx=0.42, rely=0.7)

        # 创建开始和退出按钮
        self.start_button = Button(self.master, text="开始", font=("Consolas", 16), command=self.start)
        self.start_button.place(relx=0.8, rely=0.8)

        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_1))
        returnBtn.place(relx=0.2, rely=0.8)


# 同向不同频
class page1_3(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("简谐振动的演示(同向不同频)")
        self.running = False
        self.create_widgets()

    def start(self):
        self.running = True
        A1 = float(self.entry1.get())
        A2 = float(self.entry2.get())
        phi1 = float(self.entry3.get()) * pi
        phi2 = float(self.entry4.get()) * pi
        omega1 = float(self.entry5.get()) * pi
        omega2 = float(self.entry6.get()) * pi
        t_end = float(self.entry7.get())

        if self.running:
            scene = canvas(width=800, height=494, center=vec(0, 0, 0), background=color.black, align='left')
            self.graph = graph(width=500, height=400, scroll=True, xmin=0, xmax=t_end, xtitle='时间(s)',
                               ytitle='位移(m)/速度(m/s)', title="拍的合成", align="left")
            self.x_plot = gcurve(graph=self.graph, color=color.magenta, label="x")

            self.pai1 = gcurve(graph=self.graph, color=vec(0, 1, 1))
            self.pai2 = gcurve(graph=self.graph, color=vec(0, 1, 1))

            self.graph1 = graph(width=500, height=400, scroll=True, xmin=0, xmax=t_end, xtitle='时间(s)',
                                ytitle='位移(m)/速度(m/s)', title="球1", align="left")
            self.x1_plot = gcurve(graph=self.graph1, color=color.red, label="x")
            self.v1_plot = gcurve(graph=self.graph1, color=color.green, label="v")

            self.graph2 = graph(width=500, height=400, scroll=True, xmin=0, xmax=t_end, xtitle='时间(s)',
                                ytitle='位移(m)/速度(m/s)', title="球2", align="left")
            self.x2_plot = gcurve(graph=self.graph2, color=color.orange, label="x")
            self.v2_plot = gcurve(graph=self.graph2, color=color.blue, label="v")

            self.ball1 = sphere(radius=max(A1, A2) * 0.1, color=color.cyan, opacity=0.8)
            self.ball2 = sphere(radius=max(A1, A2) * 0.1, color=color.green, opacity=0.8)
            self.ball3 = sphere(radius=max(A1, A2) * 0.1, color=color.magenta, opacity=0.8)

            self.v1_axis = arrow(shaftwidth=self.ball1.radius * 0.2, color=self.ball1.color)
            self.x1_axis = arrow(shaftwidth=self.ball1.radius * 0.2, color=self.ball1.color)
            self.v2_axis = arrow(shaftwidth=self.ball2.radius * 0.2, color=self.ball2.color)
            self.x2_axis = arrow(shaftwidth=self.ball2.radius * 0.2, color=self.ball2.color)
            self.v3_axis = arrow(shaftwidth=self.ball3.radius * 0.2, color=self.ball3.color)
            self.x3_axis = arrow(shaftwidth=self.ball3.radius * 0.2, color=self.ball3.color)

            self.X = arrow(pos=vec(-max(A1, A2) * 1.5, 0, 0), axis=vec(3 * max(A2, A1), 0, 0),
                           shaftwidth=min(A1, A2) * 0.1, label="X", color=color.white)
            self.Y = arrow(pos=vec(0, -max(A1, A2) * 1.5, 0), axis=vec(0, 3 * max(A2, A1), 0),
                           shaftwidth=min(A1, A2) * 0.1, label="Y", color=color.white)
            self.r = ring(pos=vec(0, 0, 0), radius=max(A1, A2), thickness=max(A1, A2) * 0.05, color=color.white,
                          axis=vec(0, 0, 1))

            # 添加球和球之间的白色线条
            self.line1 = curve(pos=[self.ball1.pos, self.ball3.pos], color=color.white, radius=self.ball3.radius * 0.05)
            self.line2 = curve(pos=[self.ball2.pos, self.ball3.pos], color=color.white, radius=self.ball3.radius * 0.05)

            s2 = canvas(width=700, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 7, 0), text="同向不同频的简谐运动的合成旋转矢量法演示",
                           color=color.green, box=False, height=25)
            lab_A1 = label(canvas=s2, pos=vec(0, 3, 0), text=f"A1={self.entry1.get()}", color=color.green, box=False,
                           height=20)
            lab_A2 = label(canvas=s2, pos=vec(0, 1, 0), text=f"A2={self.entry2.get()}", color=color.green, box=False,
                           height=20)
            lab_omega1 = label(canvas=s2, pos=vec(0, -1, 0), text=f"ω1={self.entry5.get()}π", color=color.green,
                               box=False, height=20)
            lab_omega2 = label(canvas=s2, pos=vec(0, -3, 0), text=f"ω2={self.entry6.get()}π", color=color.green,
                               box=False, height=20)
            lab_phi1 = label(canvas=s2, pos=vec(0, -5, 0), text=f"φ1={self.entry3.get()}π", color=color.green,
                             box=False, height=20)
            lab_phi2 = label(canvas=s2, pos=vec(0, -7, 0), text=f"φ2={self.entry4.get()}π", color=color.green,
                             box=False, height=20)

            t = 0
            dt = 0.01
            while t <= t_end:
                rate(int(1 / dt))

                # 计算位置和速度
                x1 = A1 * vec(cos(omega1 * t + phi1), sin(omega1 * t + phi1), 0)
                v1 = A1 * vec(-omega1 * sin(omega1 * t + phi1), omega1 * cos(omega1 * t + phi1), 0)

                x2 = A2 * vec(cos(omega2 * t + phi2), sin(omega2 * t + phi2), 0)
                v2 = A2 * vec(-omega2 * sin(omega2 * t + phi2), omega2 * cos(omega2 * t + phi2), 0)

                # 更新球的位置
                self.ball1.pos = x1
                self.v1_axis.pos = self.ball1.pos
                self.v1_axis.axis = v1 * 0.2
                self.x1_axis.pos = x1
                self.x1_axis.axis = -x1

                self.ball2.pos = x2
                self.v2_axis.pos = self.ball2.pos
                self.v2_axis.axis = v2 * 0.2
                self.x2_axis.pos = x2
                self.x2_axis.axis = -x2

                self.p1 = (A1 + A2) * cos((omega2 - omega1) / 2 * t + (phi2 - phi1) / 2)
                self.p2 = -(A1 + A2) * cos((omega2 - omega1) / 2 * t + (phi2 - phi1) / 2)

                # 更新图表
                self.x1_plot.plot(t, x1.x)
                self.v1_plot.plot(t, v1.x)

                self.x2_plot.plot(t, x2.x)
                self.v2_plot.plot(t, v2.x)

                self.x = x1 + x2
                self.x_plot.plot(t, self.x.x)

                self.pai1.plot(t, self.p1)
                self.pai2.plot(t, self.p2)

                self.ball3.pos = x1 + x2
                self.v3 = v1 + v2
                self.v3_axis.pos = self.ball3.pos
                self.v3_axis.axis = self.v3 * 0.2
                self.x3_axis.pos = x1 + x2
                self.x3_axis.axis = -(x1 + x2)

                # 更新球1和球3之间的线条位置
                self.line1.modify(0, self.ball1.pos)
                self.line1.modify(1, self.ball3.pos)

                # 更新球2和球3之间的线条位置
                self.line2.modify(0, self.ball2.pos)
                self.line2.modify(1, self.ball3.pos)
                t += dt
                self.update()

    def create_widgets(self):
        from page_1 import page_1
        self.label1 = Label(self, text="振幅A1:", font=("Consolas", 16))
        self.label1.place(relx=0.12, rely=0.1)
        self.entry1 = Entry(self, width=20, font=("Consolas", 16))
        self.entry1.place(relx=0.43, rely=0.1)

        self.label2 = Label(self, text="振幅A2:", font=("Consolas", 16))
        self.label2.place(relx=0.12, rely=0.2)
        self.entry2 = Entry(self, width=20, font=("Consolas", 16))
        self.entry2.place(relx=0.43, rely=0.2)

        self.label3 = Label(self, text="初相phi1(π):", font=("Consolas", 16))
        self.label3.place(relx=0.12, rely=0.3)
        self.entry3 = Entry(self, width=20, font=("Consolas", 16))
        self.entry3.place(relx=0.43, rely=0.3)

        self.label4 = Label(self, text="初相phi2(π):", font=("Consolas", 16))
        self.label4.place(relx=0.12, rely=0.4)
        self.entry4 = Entry(self, width=20, font=("Consolas", 16))
        self.entry4.place(relx=0.43, rely=0.4)

        self.label5 = Label(self, text="角频率omega1(π):", font=("Consolas", 16))
        self.label5.place(relx=0.12, rely=0.5)
        self.entry5 = Entry(self, width=20, font=("Consolas", 16))
        self.entry5.place(relx=0.43, rely=0.5)

        self.label6 = Label(self, text="角频率omega2(π):", font=("Consolas", 16))
        self.label6.place(relx=0.12, rely=0.6)
        self.entry6 = Entry(self, width=20, font=("Consolas", 16))
        self.entry6.place(relx=0.43, rely=0.6)

        self.label7 = Label(self, text="演示时长t:", font=("Consolas", 16))
        self.label7.place(relx=0.12, rely=0.7)
        self.entry7 = Entry(self, width=20, font=("Consolas", 16))
        self.entry7.place(relx=0.43, rely=0.7)

        # 创建开始和退出按钮
        self.start_button = Button(self.master, text="开始", font=("Consolas", 16), command=self.start)
        self.start_button.place(relx=0.8, rely=0.8)

        returnBtn = Button(text="返回", font=("Consolas", 16), command=lambda: self.master.switch_frame(page_1))
        returnBtn.place(relx=0.2, rely=0.8)


# 方向垂直频率相同
class page1_4(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("简谐振动的合成(方向垂直同频)")
        self.running = False
        self.createWidget()

    def createWidget(self):
        from page_1 import page_1
        # 标签
        lab_A1 = Label(self, text="振幅A1", font=("Consolas", 14))
        lab_A1.place(relx=0.05, rely=0.10)
        lab_A2 = Label(self, text="振幅A2", font=("Consolas", 14))
        lab_A2.place(relx=0.05, rely=0.22)
        lab_omega = Label(self, text="角频率omega(π)", font=("Consolas", 14))
        lab_omega.place(relx=0.05, rely=0.34)
        lab_phi1 = Label(self, text="初相phi1(π)", font=("Consolas", 14))
        lab_phi1.place(relx=0.05, rely=0.46)
        lab_phi2 = Label(self, text="初相phi2(π)", font=("Consolas", 14))
        lab_phi2.place(relx=0.05, rely=0.58)

        # 滑块
        self.s_A1 = Scale(self, from_=1, to=20, resolution=0.5, digits=4, sliderlength=20, width=18, length=350,
                          orient=HORIZONTAL)
        self.s_A1.place(relx=0.3, rely=0.06)
        self.s_A1.set(10)
        self.s_A2 = Scale(self, from_=1, to=20, resolution=0.5, digits=4, sliderlength=20, width=18, length=350,
                          orient=HORIZONTAL)
        self.s_A2.place(relx=0.3, rely=0.18)
        self.s_A2.set(8)
        self.s_omega = Scale(self, from_=1 / 8, to=2, resolution=1 / 8, digits=4, sliderlength=20, width=18, length=350,
                             orient=HORIZONTAL)
        self.s_omega.place(relx=0.3, rely=0.30)
        self.s_omega.set(0.5)
        self.s_phi1 = Scale(self, from_=1 / 8, to=2, resolution=1 / 8, digits=4, sliderlength=20, width=18, length=350,
                            orient=HORIZONTAL)
        self.s_phi1.place(relx=0.3, rely=0.42)
        self.s_phi1.set(0.25)
        self.s_phi2 = Scale(self, from_=1 / 8, to=2, resolution=1 / 8, digits=4, sliderlength=20, width=18, length=350,
                            orient=HORIZONTAL)
        self.s_phi2.place(relx=0.3, rely=0.54)
        self.s_phi2.set(0.5)

        # 基础参数
        self.t = 0
        self.dt = 0.01

        # 第一个简谐运动 X轴
        self.A1 = self.s_A1.get()
        self.omega1 = pi * self.s_omega.get()
        self.phi1 = pi * self.s_phi1.get()
        self.T1 = 2 * pi / self.omega1
        self.x1 = self.A1 * cos(self.omega1 * self.t + self.phi1)

        # 第二个简谐运动 Y轴
        self.A2 = self.s_A2.get()
        self.omega2 = pi * self.s_omega.get()
        self.phi2 = pi * self.s_phi2.get()
        self.T2 = 2 * pi / self.omega2
        self.x2 = self.A2 * cos(self.omega2 * self.t + self.phi2)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.8, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_1))
        returnBtn.place(relx=0.1, rely=0.8)

    def start(self):
        self.running = True
        if self.running:
            # 画表

            s1 = canvas(width=800, height=494.5, color=color.black, align="left")
            self.X = arrow(pos=vec(-20, 0, 0), axis=vec(40, 0, 0), shaftwidth=0.5, label="X", color=color.white)
            self.Y = arrow(pos=vec(0, -20, 0), axis=vec(0, 40, 0), shaftwidth=0.5, label="Y", color=color.white)

            # 和运动
            self.ball = sphere(pos=vec(self.x2, self.x1, 0), radius=2, color=color.cyan, make_trail=True, retain=500)

            self.g1 = graph(width=500, height=400, scroll=True, xmin=0, xmax=30, xtitle='时间(s)', ytitle='x方向位移',
                            title="ball1", align="left")
            self.x1_plot = gcurve(graph=self.g1, color=color.red, label="x")
            self.g2 = graph(width=500, height=400, scroll=True, xmin=0, xmax=30, xtitle='时间(s)', ytitle='y方向位移',
                            title="ball2", align="left")
            self.x2_plot = gcurve(graph=self.g2, color=color.orange, label="y")
            self.g = graph(width=500, height=400, scroll=True, xmin=-20, xmax=20, xtitle='X位移', ytitle='Y位移',
                           title="ball", align="left")
            self.x_plot = gcurve(graph=self.g, color=color.red, label="x")

            s2 = canvas(width=700, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 7, 0), text="不同向同频的简谐运动的合成旋转矢量法演示",
                           color=color.green, box=False, height=25)
            lab_A1 = label(canvas=s2, pos=vec(0, 3, 0), text=f"A1={self.s_A1.get()}", color=color.green, box=False,
                           height=20)
            lab_A2 = label(canvas=s2, pos=vec(0, 1, 0), text=f"A2={self.s_A2.get()}", color=color.green, box=False,
                           height=20)
            lab_omega = label(canvas=s2, pos=vec(0, -1, 0), text=f"ω={self.s_omega.get()}π", color=color.green,
                              box=False, height=20)
            lab_phi1 = label(canvas=s2, pos=vec(0, -3, 0), text=f"φ1={self.s_phi1.get()}π", color=color.green,
                             box=False, height=20)
            lab_phi2 = label(canvas=s2, pos=vec(0, -5, 0), text=f"φ2={self.s_phi2.get()}π", color=color.green,
                             box=False, height=20)

            while self.t <= (self.g1.xmax - self.g1.xmin) and self.running:
                rate(int(1 / self.dt))
                self.t += self.dt
                omega = self.s_omega.get() * pi
                self.x1 = self.s_A1.get() * cos(omega * self.t + self.s_phi1.get() * pi)
                self.x2 = self.s_A2.get() * cos(omega * self.t + self.s_phi2.get() * pi)
                self.ball.pos = vec(self.x1, self.x2, 0)
                self.x1_plot.plot(self.t, self.x1)
                self.x2_plot.plot(self.t, self.x2)
                self.x_plot.plot(self.ball.pos.x, self.ball.pos.y)
                self.update()


# 李萨如
class page1_5(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.running = False
        self.master.title("简谐振动的合成(方向垂直不同频)")
        self.createWidget()

    def createWidget(self):
        from page_1 import page_1
        # 标签
        lab_A1 = Label(self, text="振幅A1", font=("Consolas", 14))
        lab_A1.place(relx=0.05, rely=0.10)
        lab_A2 = Label(self, text="振幅A2", font=("Consolas", 14))
        lab_A2.place(relx=0.05, rely=0.22)
        lab_omega1 = Label(self, text="角频率omega1(π)", font=("Consolas", 14))
        lab_omega1.place(relx=0.05, rely=0.34)
        lab_omega2 = Label(self, text="角频率omega2(π)", font=("Consolas", 14))
        lab_omega2.place(relx=0.05, rely=0.46)
        lab_phi1 = Label(self, text="初相phi1(π)", font=("Consolas", 14))
        lab_phi1.place(relx=0.05, rely=0.58)
        lab_phi2 = Label(self, text="初相phi2(π)", font=("Consolas", 14))
        lab_phi2.place(relx=0.05, rely=0.70)

        # 滑块
        self.s_A1 = Scale(self, from_=1, to=20, resolution=0.5, digits=4, sliderlength=20, width=18, length=350,
                          orient=HORIZONTAL)
        self.s_A1.place(relx=0.3, rely=0.06)
        self.s_A1.set(10)
        self.s_A2 = Scale(self, from_=1, to=20, resolution=0.5, digits=4, sliderlength=20, width=18, length=350,
                          orient=HORIZONTAL)
        self.s_A2.place(relx=0.3, rely=0.18)
        self.s_A2.set(8)
        self.s_omega1 = Scale(self, from_=1 / 8, to=2, resolution=1 / 8, digits=4, sliderlength=20, width=18,
                              length=350, orient=HORIZONTAL)
        self.s_omega1.place(relx=0.3, rely=0.30)
        self.s_omega1.set(0.5)
        self.s_omega2 = Scale(self, from_=1 / 8, to=2, resolution=1 / 8, digits=4, sliderlength=20, width=18,
                              length=350, orient=HORIZONTAL)
        self.s_omega2.place(relx=0.3, rely=0.42)
        self.s_omega2.set(0.75)
        self.s_phi1 = Scale(self, from_=1 / 8, to=2, resolution=1 / 8, digits=4, sliderlength=20, width=18, length=350,
                            orient=HORIZONTAL)
        self.s_phi1.place(relx=0.3, rely=0.54)
        self.s_phi1.set(0.25)
        self.s_phi2 = Scale(self, from_=1 / 8, to=2, resolution=1 / 8, digits=4, sliderlength=20, width=18, length=350,
                            orient=HORIZONTAL)
        self.s_phi2.place(relx=0.3, rely=0.66)
        self.s_phi2.set(0.5)

        # 基础参数
        self.t = 0
        self.dt = 0.01

        # 第一个简谐运动 X轴
        self.A1 = self.s_A1.get()
        self.omega1 = pi * self.s_omega1.get()
        self.phi1 = pi * self.s_phi1.get()
        self.x1 = self.A1 * cos(self.omega1 * self.t + self.phi1)

        # 第二个简谐运动 Y轴
        self.A2 = self.s_A2.get()
        self.omega2 = pi * self.s_omega2.get()
        self.phi2 = pi * self.s_phi2.get()
        self.x2 = self.A2 * cos(self.omega2 * self.t + self.phi2)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.8, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_1))
        returnBtn.place(relx=0.1, rely=0.8)

    def start(self):
        self.running = True
        if self.running:
            # 画表
            self.g1 = graph(width=500, height=400, scroll=True, xmin=0, xmax=30, xtitle='时间(s)', ytitle='x方向位移',
                            title="ball1", align="left")
            self.x1_plot = gcurve(graph=self.g1, color=color.red, label="x")
            self.g2 = graph(width=500, height=400, scroll=True, xmin=0, xmax=30, xtitle='时间(s)', ytitle='y方向位移',
                            title="ball2", align="left")
            self.x2_plot = gcurve(graph=self.g2, color=color.orange, label="y")
            self.g = graph(width=500, height=400, scroll=True, xmin=-20, xmax=20, xtitle='X位移', ytitle='Y位移',
                           title="ball", align="left")
            self.x_plot = gcurve(graph=self.g, color=color.red, label="x")
            s1 = canvas(width=800, height=494.5, color=color.black, align="left")
            self.X = arrow(pos=vec(-20, 0, 0), axis=vec(40, 0, 0), shaftwidth=0.5, label="X", color=color.white)
            self.Y = arrow(pos=vec(0, -20, 0), axis=vec(0, 40, 0), shaftwidth=0.5, label="Y", color=color.white)

            # 和运动
            self.ball = sphere(pos=vec(self.x1, self.x2, 0), radius=2, color=color.cyan, make_trail=True, retain=500)

            s2 = canvas(width=700, height=494.5, background=color.black, align="left")
            lanb_1 = label(canvas=s2, pos=vec(0, 7, 0), text="不同向不同频的简谐运动的合成旋转矢量法演示",
                           color=color.green, box=False, height=25)
            lab_A1 = label(canvas=s2, pos=vec(0, 3, 0), text=f"A1={self.s_A1.get()}", color=color.green, box=False,
                           height=20)
            lab_A2 = label(canvas=s2, pos=vec(0, 1, 0), text=f"A2={self.s_A2.get()}", color=color.green, box=False,
                           height=20)
            lab_omega = label(canvas=s2, pos=vec(0, -1, 0), text=f"ω1={self.s_omega1.get()}π", color=color.green,
                              box=False, height=20)
            lab_omega = label(canvas=s2, pos=vec(0, -3, 0), text=f"ω2={self.s_omega2.get()}π", color=color.green,
                              box=False, height=20)
            lab_phi1 = label(canvas=s2, pos=vec(0, -5, 0), text=f"φ1={self.s_phi1.get()}π", color=color.green,
                             box=False, height=20)
            lab_phi2 = label(canvas=s2, pos=vec(0, -7, 0), text=f"φ2={self.s_phi2.get()}π", color=color.green,
                             box=False, height=20)

            while self.t <= (self.g1.xmax - self.g1.xmin) and self.running:
                rate(int(1 / self.dt))
                self.t += self.dt
                self.x1 = self.s_A1.get() * cos(self.s_omega1.get() * pi * self.t + self.s_phi1.get() * pi)
                self.x2 = self.s_A2.get() * cos(self.s_omega2.get() * pi * self.t + self.s_phi2.get() * pi)
                self.ball.pos = vec(self.x1, self.x2, 0)
                self.x1_plot.plot(self.t, self.x1)
                self.x2_plot.plot(self.t, self.x2)
                self.x_plot.plot(self.ball.pos.x, self.ball.pos.y)
                self.update()

