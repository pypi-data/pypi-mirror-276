from matplotlib import rcParams

rcParams['font.family'] = 'Microsoft YaHei'

from scipy.signal import square
from scipy.fftpack import fft, ifft, fftfreq
import numpy as np
import matplotlib.pyplot as plt


from vpython import *
from tkinter import *








# 阻尼振动的傅里叶分解
class page3_1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("阻尼振动的傅里叶分解")
        self.createWidget()

    def start(self):
        m = float(self.ask_m.get())
        c = float(self.ask_gama.get())
        k = float(self.ask_k.get())
        span = float(self.ask_t.get())
        sr = float(self.ask_sr.get())

        # 设置参数
        dt = 0.001

        N = int(1 / dt * span)

        x0 = 1.0
        v0 = 0.0

        # 定义函数计算斜率
        def f(x, v):
            return v, -c / m * v - k / m * x

        # 使用龙格-库塔法求解微分方程
        def rk4_step(x, v, dt):
            k1x, k1v = f(x, v)
            k2x, k2v = f(x + 0.5 * dt * k1x, v + 0.5 * dt * k1v)
            k3x, k3v = f(x + 0.5 * dt * k2x, v + 0.5 * dt * k2v)
            k4x, k4v = f(x + dt * k3x, v + dt * k3v)
            x_new = x + dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x)
            v_new = v + dt / 6.0 * (k1v + 2 * k2v + 2 * k3v + k4v)
            return x_new, v_new

        # 数值求解
        num_steps = int(span / dt)
        t = np.linspace(0, span, N, endpoint=False)
        x_values = np.zeros(num_steps)
        v_values = np.zeros(num_steps)
        x_values[0] = x0
        v_values[0] = v0

        for i in range(1, num_steps):
            x_values[i], v_values[i] = rk4_step(x_values[i - 1], v_values[i - 1], dt)

        # 生成时间数组
        t = np.linspace(0, span, N, endpoint=False)

        # 位移傅里叶
        X = fft(x_values)
        X_norm = abs(X) * 2 / N
        freq = fftfreq(N, 1 / sr)

        top_freq_indices = np.argsort(-X_norm)[:50]  # 获取幅度最高频率的索引
        keep_freq_50 = np.zeros_like(X_norm)
        keep_freq_50[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:10]  # 获取幅度最高频率的索引
        keep_freq_10 = np.zeros_like(X_norm)
        keep_freq_10[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:3]  # 获取幅度最高频率的索引
        keep_freq_3 = np.zeros_like(X_norm)
        keep_freq_3[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        # 逆傅里叶变换
        g_ifft_50 = ifft(X * keep_freq_50)
        g_ifft_10 = ifft(X * keep_freq_10)
        g_ifft_3 = ifft(X * keep_freq_3)

        # 画图
        fig, ax = plt.subplots(2, 2, figsize=(15, 8))
        # 高斯脉冲时域图
        ax[0, 0].plot(t, x_values)
        ax[0, 0].set_title('阻尼运动位移的傅里叶分解')
        ax[0, 0].set_xlabel('Time (s)')
        ax[0, 0].set_ylabel('Amplitude')
        ax[0, 0].grid()

        # ifft
        ax[0, 1].plot(t, g_ifft_50.real, color='#FF0000', label="保留前50个谐波")
        ax[0, 1].plot(t, g_ifft_10.real, color='#FFB7DD', label="保留前10个谐波")
        ax[0, 1].plot(t, g_ifft_3.real, color='#00FF7F', label="保留前3个谐波")
        ax[0, 1].set_title('Ifft')
        ax[0, 1].set_xlabel('Time (s)')
        ax[0, 1].set_ylabel('Amplitude')
        ax[0, 1].legend(loc='upper right')
        ax[0, 1].grid()

        # 频谱图
        ax[1, 0].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b')
        ax[1, 0].set_xlabel('Freq (HZ)')
        ax[1, 0].set_ylabel('FFT Amplitude')
        ax[1, 1].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b', label='傅里叶分解的数值解')
        ax[1, 1].set_xlabel('Freq (HZ)')
        ax[1, 1].set_ylabel('FFT Amplitude')
        ax[1, 1].set_xlim(-0.01 * sr, 0.01 * sr)
        ax[1, 1].legend()

        # 速度傅里叶
        X = fft(v_values)
        X_norm = abs(X) * 2 / N
        freq = fftfreq(N, 1 / sr)

        top_freq_indices = np.argsort(-X_norm)[:50]  # 获取幅度最高频率的索引
        keep_freq_50 = np.zeros_like(X_norm)
        keep_freq_50[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:10]  # 获取幅度最高频率的索引
        keep_freq_10 = np.zeros_like(X_norm)
        keep_freq_10[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:3]  # 获取幅度最高频率的索引
        keep_freq_3 = np.zeros_like(X_norm)
        keep_freq_3[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        # 逆傅里叶变换
        g_ifft_50 = ifft(X * keep_freq_50)
        g_ifft_10 = ifft(X * keep_freq_10)
        g_ifft_3 = ifft(X * keep_freq_3)

        # 画图
        fig, ax = plt.subplots(2, 2, figsize=(15, 8))
        # 高斯脉冲时域图
        ax[0, 0].plot(t, v_values)
        ax[0, 0].set_title('阻尼运动速度的傅里叶分解')
        ax[0, 0].set_xlabel('Time (s)')
        ax[0, 0].set_ylabel('Amplitude')
        ax[0, 0].grid()

        # ifft
        ax[0, 1].plot(t, g_ifft_50.real, color='#FF0000', label="保留前50个谐波")
        ax[0, 1].plot(t, g_ifft_10.real, color='#FFB7DD', label="保留前10个谐波")
        ax[0, 1].plot(t, g_ifft_3.real, color='#00FF7F', label="保留前3个谐波")
        ax[0, 1].set_title('Ifft')
        ax[0, 1].set_xlabel('Time (s)')
        ax[0, 1].set_ylabel('Amplitude')
        ax[0, 1].legend(loc='upper right')
        ax[0, 1].grid()

        # 频谱图
        ax[1, 0].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b')
        ax[1, 0].set_xlabel('Freq (HZ)')
        ax[1, 0].set_ylabel('FFT Amplitude')
        ax[1, 1].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b', label='傅里叶分解的数值解')
        ax[1, 1].set_xlabel('Freq (HZ)')
        ax[1, 1].set_ylabel('FFT Amplitude')
        ax[1, 1].set_xlim(-0.01 * sr, 0.01 * sr)
        ax[1, 1].legend()

        plt.show()

    def createWidget(self):


        from page_3 import page_3


        # 提示
        lab_t = Label(self, text="演示时长t:", font=("Consolas", 16))
        lab_t.place(relx=0.26, rely=0.05)
        lab_gama = Label(self, text="阻尼系数r(临界阻尼为:2√km):", font=("Consolas", 16))
        lab_gama.place(relx=0.26, rely=0.20)
        lab_k = Label(self, text="弹性系数k:", font=("Consolas", 16))
        lab_k.place(relx=0.26, rely=0.35)
        lab_m = Label(self, text="请输入物体质量m:", font=("Consolas", 16))
        lab_m.place(relx=0.26, rely=0.5)
        lab_sr = Label(self, text="请输入采样率sr:", font=("Consolas", 16))
        lab_sr.place(relx=0.26, rely=0.65)

        # 输入框
        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.26, rely=0.13)
        self.ask_gama = Entry(self, font=("Consolas", 16), width=25)
        self.ask_gama.place(relx=0.26, rely=0.28)
        self.ask_k = Entry(self, font=("Consolas", 16), width=25)
        self.ask_k.place(relx=0.26, rely=0.43)
        self.ask_m = Entry(self, font=("Consolas", 16), width=25)
        self.ask_m.place(relx=0.26, rely=0.58)
        self.ask_sr = Entry(self, font=("Consolas", 16), width=25)
        self.ask_sr.place(relx=0.26, rely=0.73)
        lab = Label(self, text="时间过长会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.8, rely=0.8)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_3))
        returnBtn.place(relx=0.15, rely=0.8)


# 方波的傅里叶分解
class page3_2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("方波的傅里叶分解")
        self.createWidget()

    def start(self):
        sr = float(self.ask_sr.get())
        span = float(self.ask_t.get())
        A = float(self.ask_A.get())
        omega = float(self.ask_omega.get())
        # 设置参数
        N = int(sr * span)

        # 生成时间数组
        t = np.linspace(0, span, N, endpoint=False)

        original = A * square(2 * np.pi * omega * t, duty=0.5)
        X = fft(original)
        X_norm = abs(X) * 2 / N
        freq = fftfreq(N, 1 / sr)

        top_freq_indices = np.argsort(-X_norm)[:50]  # 获取幅度最高频率的索引
        keep_freq_50 = np.zeros_like(X_norm)
        keep_freq_50[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:10]  # 获取幅度最高频率的索引
        keep_freq_10 = np.zeros_like(X_norm)
        keep_freq_10[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:3]  # 获取幅度最高频率的索引
        keep_freq_3 = np.zeros_like(X_norm)
        keep_freq_3[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        # 逆傅里叶变换
        g_ifft_50 = ifft(X * keep_freq_50)
        g_ifft_10 = ifft(X * keep_freq_10)
        g_ifft_3 = ifft(X * keep_freq_3)

        # 画图
        fig, ax = plt.subplots(2, 2, figsize=(15, 8))
        # 高斯脉冲时域图
        ax[0, 0].plot(t, original)
        ax[0, 0].set_title('方波')
        ax[0, 0].set_xlabel('Time (s)')
        ax[0, 0].set_ylabel('Amplitude')
        ax[0, 0].grid()

        # ifft
        ax[0, 1].plot(t, g_ifft_50.real, color='#FF0000', label="保留前50个谐波")
        ax[0, 1].plot(t, g_ifft_10.real, color='#FFB7DD', label="保留前10个谐波")
        ax[0, 1].plot(t, g_ifft_3.real, color='#00FF7F', label="保留前3个谐波")
        ax[0, 1].set_title('Ifft')
        ax[0, 1].set_xlabel('Time (s)')
        ax[0, 1].set_ylabel('Amplitude')
        ax[0, 1].legend(loc='upper right')
        ax[0, 1].grid()

        # 频谱图
        ax[1, 0].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b')
        ax[1, 0].set_xlabel('Freq (HZ)')
        ax[1, 0].set_ylabel('FFT Amplitude')
        ax[1, 1].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b')
        ax[1, 1].set_xlabel('Freq (HZ)')
        ax[1, 1].set_ylabel('FFT Amplitude')
        ax[1, 1].set_xlim(-100 * omega, 100 * omega)

        plt.show()

    def createWidget(self):

        from page_3 import page_3

        # 提示
        lab_t = Label(self, text="演示时长t:", font=("Consolas", 16))
        lab_t.place(relx=0.26, rely=0.07)
        lab_A = Label(self, text="振幅A:", font=("Consolas", 16))
        lab_A.place(relx=0.26, rely=0.23)
        lab_sr = Label(self, text="采样率sr:", font=("Consolas", 16))
        lab_sr.place(relx=0.26, rely=0.39)
        lab_omega = Label(self, text="方波频率omega:", font=("Consolas", 16))
        lab_omega.place(relx=0.26, rely=0.55)

        # 输入框
        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.26, rely=0.15)
        self.ask_A = Entry(self, font=("Consolas", 16), width=25)
        self.ask_A.place(relx=0.26, rely=0.31)
        self.ask_sr = Entry(self, font=("Consolas", 16), width=25)
        self.ask_sr.place(relx=0.26, rely=0.47)
        self.ask_omega = Entry(self, font=("Consolas", 16), width=25)
        self.ask_omega.place(relx=0.26, rely=0.63)
        lab = Label(self, text="采样率过大会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.8, rely=0.75)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_3))
        returnBtn.place(relx=0.15, rely=0.75)


# 三角波的傅里叶分解
class page3_3(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("三角波的傅里叶分解")
        self.createWidget()

    def start(self):
        sr = float(self.ask_sr.get())
        span = float(self.ask_t.get())
        A = float(self.ask_A.get())
        omega = float(self.ask_omega.get())

        # 生成三角波信号
        def triangle_wave(freq, amplitude):
            triangle = amplitude * (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1)
            return triangle

        # 设置参数
        N = int(sr * span)

        # 生成时间数组
        t = np.linspace(0, span, N, endpoint=False)

        tr = triangle_wave(omega, A)
        X = fft(tr)
        X_norm = abs(X) * 2 / N
        freq = fftfreq(N, 1 / sr)

        top_freq_indices = np.argsort(-X_norm)[:50]  # 获取幅度最高频率的索引
        keep_freq_50 = np.zeros_like(X_norm)
        keep_freq_50[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:10]  # 获取幅度最高频率的索引
        keep_freq_10 = np.zeros_like(X_norm)
        keep_freq_10[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:3]  # 获取幅度最高频率的索引
        keep_freq_3 = np.zeros_like(X_norm)
        keep_freq_3[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        # 逆傅里叶变换
        g_ifft_50 = ifft(X * keep_freq_50)
        g_ifft_10 = ifft(X * keep_freq_10)
        g_ifft_3 = ifft(X * keep_freq_3)

        # 画图
        fig, ax = plt.subplots(2, 2, figsize=(15, 8))
        # 高斯脉冲时域图
        ax[0, 0].plot(t, tr)
        ax[0, 0].set_title('三角波')
        ax[0, 0].set_xlabel('Time (s)')
        ax[0, 0].set_ylabel('Amplitude')
        ax[0, 0].grid()

        # ifft
        ax[0, 1].plot(t, g_ifft_50.real, color='#FF0000', label="保留前50个谐波")
        ax[0, 1].plot(t, g_ifft_10.real, color='#FFB7DD', label="保留前10个谐波")
        ax[0, 1].plot(t, g_ifft_3.real, color='#00FF7F', label="保留前3个谐波")
        ax[0, 1].set_title('Ifft')
        ax[0, 1].set_xlabel('Time (s)')
        ax[0, 1].set_ylabel('Amplitude')
        ax[0, 1].legend(loc='upper right')
        ax[0, 1].grid()

        # 频谱图
        ax[1, 0].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b')
        ax[1, 0].set_xlabel('Freq (HZ)')
        ax[1, 0].set_ylabel('FFT Amplitude')
        ax[1, 1].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b')
        ax[1, 1].set_xlabel('Freq (HZ)')
        ax[1, 1].set_ylabel('FFT Amplitude')
        ax[1, 1].set_xlim(-omega * 20, omega * 20)

        plt.show()

    def createWidget(self):

        from page_3 import page_3

        # 提示
        lab_t = Label(self, text="演示时长t:", font=("Consolas", 16))
        lab_t.place(relx=0.26, rely=0.07)
        lab_A = Label(self, text="振幅A:", font=("Consolas", 16))
        lab_A.place(relx=0.26, rely=0.23)
        lab_sr = Label(self, text="采样率sr:", font=("Consolas", 16))
        lab_sr.place(relx=0.26, rely=0.39)
        lab_omega = Label(self, text="三角波频率omega:", font=("Consolas", 16))
        lab_omega.place(relx=0.26, rely=0.55)

        # 输入框
        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.26, rely=0.15)
        self.ask_A = Entry(self, font=("Consolas", 16), width=25)
        self.ask_A.place(relx=0.26, rely=0.31)
        self.ask_sr = Entry(self, font=("Consolas", 16), width=25)
        self.ask_sr.place(relx=0.26, rely=0.47)
        self.ask_omega = Entry(self, font=("Consolas", 16), width=25)
        self.ask_omega.place(relx=0.26, rely=0.63)
        lab = Label(self, text="采样率过大会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.8, rely=0.75)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_3))
        returnBtn.place(relx=0.15, rely=0.75)


# 高斯脉冲的傅里叶分解
class page3_4(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("高斯脉冲的傅里叶分解")
        self.createWidget()

    def start(self):
        sr = float(self.ask_sr.get())
        span = float(self.ask_t.get())
        A = float(self.ask_A.get())
        sd = float(self.ask_sd.get())

        def gp(sd, A):
            return A * np.exp(-(t ** 2 / (2 * sd ** 2)) / ((2 * np.pi) ** 0.5 * sd))

        # 设置参数
        N = int(sr * span)

        # 生成时间数组
        t = np.linspace(-span / 2, span / 2, N, endpoint=False)

        g = gp(sd, A)
        X = fft(g)
        X_norm = abs(X) * 2 / N
        freq = fftfreq(N, 1 / sr)

        top_freq_indices = np.argsort(-X_norm)[:50]  # 获取幅度最高频率的索引
        keep_freq_50 = np.zeros_like(X_norm)
        keep_freq_50[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:10]  # 获取幅度最高频率的索引
        keep_freq_10 = np.zeros_like(X_norm)
        keep_freq_10[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        top_freq_indices = np.argsort(-X_norm)[:3]  # 获取幅度最高频率的索引
        keep_freq_3 = np.zeros_like(X_norm)
        keep_freq_3[top_freq_indices] = 1  # 设置这些频率对应的索引为1

        # 逆傅里叶变换
        g_ifft_50 = ifft(X * keep_freq_50)
        g_ifft_10 = ifft(X * keep_freq_10)
        g_ifft_3 = ifft(X * keep_freq_3)

        # 画图
        fig, ax = plt.subplots(2, 2, figsize=(15, 8))
        # 高斯脉冲时域图
        ax[0, 0].plot(t, g)
        ax[0, 0].set_title('高斯脉冲')
        ax[0, 0].set_xlabel('Time (s)')
        ax[0, 0].set_ylabel('Amplitude')
        ax[0, 0].grid()

        # ifft
        ax[0, 1].plot(t, g_ifft_50.real, color='#FF0000', label="保留前50个谐波")
        ax[0, 1].plot(t, g_ifft_10.real, color='#FFB7DD', label="保留前10个谐波")
        ax[0, 1].plot(t, g_ifft_3.real, color='#00FF7F', label="保留前3个谐波")
        ax[0, 1].set_title('Ifft')
        ax[0, 1].set_xlabel('Time (s)')
        ax[0, 1].set_ylabel('Amplitude')
        ax[0, 1].legend(loc='upper right')
        ax[0, 1].grid()

        # 频谱图
        ax[1, 0].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b')
        ax[1, 0].set_xlabel('Freq (HZ)')
        ax[1, 0].set_ylabel('FFT Amplitude')
        ax[1, 1].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b', label='傅里叶分解的数值解')
        ax[1, 1].set_xlabel('Freq (HZ)')
        ax[1, 1].set_ylabel('FFT Amplitude')
        ax[1, 1].set_xlim(-1 / sd, 1 / sd)
        ax[1, 1].legend()

        plt.show()

    def createWidget(self):

        from page_3 import page_3

        # 提示
        lab_t = Label(self, text="演示时长t:", font=("Consolas", 16))
        lab_t.place(relx=0.26, rely=0.07)
        lab_A = Label(self, text="振幅A:", font=("Consolas", 16))
        lab_A.place(relx=0.26, rely=0.23)
        lab_sr = Label(self, text="采样率sr:", font=("Consolas", 16))
        lab_sr.place(relx=0.26, rely=0.39)
        lab_sd = Label(self, text="高斯脉冲标准差sd:", font=("Consolas", 16))
        lab_sd.place(relx=0.26, rely=0.55)

        # 输入框
        self.ask_t = Entry(self, font=("Consolas", 16), width=25)
        self.ask_t.place(relx=0.26, rely=0.15)
        self.ask_A = Entry(self, font=("Consolas", 16), width=25)
        self.ask_A.place(relx=0.26, rely=0.31)
        self.ask_sr = Entry(self, font=("Consolas", 16), width=25)
        self.ask_sr.place(relx=0.26, rely=0.47)
        self.ask_sd = Entry(self, font=("Consolas", 16), width=25)
        self.ask_sd.place(relx=0.26, rely=0.63)
        lab = Label(self, text="采样率过大会导致运算量变大,如点击开始后没反应请耐心等待", font=("Consolas", 10)).place(
            rely=0.95, relx=0.20)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.8, rely=0.75)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_3))
        returnBtn.place(relx=0.15, rely=0.75)


# 拍的分解
class page3_5(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("拍的傅里叶分解")
        self.createWidget()

    def start(self):
        A1 = float(self.ask_A1.get())
        A2 = float(self.ask_A2.get())
        span = float(self.ask_t.get())
        phi1 = float(self.ask_phi1.get()) * pi
        phi2 = float(self.ask_phi2.get()) * pi
        omega1 = float(self.ask_omega1.get()) * pi
        omega2 = float(self.ask_omega2.get()) * pi
        sr = float(self.ask_sr.get())
        x1 = []
        x2 = []
        pai1 = []
        pai2 = []

        # 设置参数
        N = int(sr * span)

        # 生成时间数组
        t = np.linspace(0, span, N, endpoint=False)

        for t_ in t:
            x1_ = A1 * cos(omega1 * t_ + phi1)
            x2_ = A2 * cos(omega2 * t_ + phi2)
            pai1_ = (A1 + A2) * cos((omega2 - omega1) / 2 * t_ + (phi2 - phi1) / 2)
            pai2_ = -(A1 + A2) * cos((omega2 - omega1) / 2 * t_ + (phi2 - phi1) / 2)
            x1.append(x1_)
            x2.append(x2_)
            pai1.append(pai1_)
            pai2.append(pai2_)
        x = [sum(pair) for pair in zip(x1, x2)]
        X = fft(x)
        X_norm = abs(X) * 2 / N
        freq = fftfreq(N, 1 / sr)

        # 画图
        fig, ax = plt.subplots(1, 2, figsize=(16, 7))
        # 高斯脉冲时域图
        ax[0].plot(t, x, color="#FF0000")
        ax[0].plot(t, pai1, color="#00FFFF")
        ax[0].plot(t, pai2, color="#00FFFF")
        ax[0].set_title('拍')
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel('Amplitude')
        ax[0].grid()

        # 频域图
        ax[1].stem(freq, X_norm, 'b', markerfmt=' ', basefmt='-b', label='傅里叶分解数值解')
        ax[1].set_title('FFT')
        ax[1].set_xlabel('Freq')
        ax[1].set_ylabel('Amplitude')
        ax[1].legend(loc='upper right')
        ax[1].grid()
        ax[1].legend()

        plt.show()

    def createWidget(self):

        from page_3 import page_3

        # 提示
        lab_t = Label(self, text="展示时间:", font=("Consolas", 14))
        lab_t.place(relx=0.12, rely=0.05)
        lab_A1 = Label(self, text="振幅A1:", font=("Consolas", 14))
        lab_A1.place(relx=0.12, rely=0.15)
        lab_A2 = Label(self, text="振幅A2:", font=("Consolas", 14))
        lab_A2.place(relx=0.12, rely=0.25)
        lab_omega1 = Label(self, text="角频率omega1(π):", font=("Consolas", 14))
        lab_omega1.place(relx=0.12, rely=0.35)
        lab_omega2 = Label(self, text="角频率omega2(π):", font=("Consolas", 14))
        lab_omega2.place(relx=0.12, rely=0.45)
        lab_phi1 = Label(self, text="初相Phi1(π):", font=("Consolas", 14))
        lab_phi1.place(relx=0.12, rely=0.55)
        lab_phi2 = Label(self, text="初相Phi2(π):", font=("Consolas", 14))
        lab_phi2.place(relx=0.12, rely=0.65)
        lab_sr = Label(self, text="采样率sr:", font=("Consolas", 14))
        lab_sr.place(relx=0.12, rely=0.75)

        # 输入框
        self.ask_t = Entry(self, font=("Consolas", 14), width=25)
        self.ask_t.place(relx=0.4, rely=0.05)
        self.ask_A1 = Entry(self, font=("Consolas", 14), width=25)
        self.ask_A1.place(relx=0.4, rely=0.15)
        self.ask_A2 = Entry(self, font=("Consolas", 14), width=25)
        self.ask_A2.place(relx=0.4, rely=0.25)
        self.ask_omega1 = Entry(self, font=("Consolas", 14), width=25)
        self.ask_omega1.place(relx=0.4, rely=0.35)
        self.ask_omega2 = Entry(self, font=("Consolas", 14), width=25)
        self.ask_omega2.place(relx=0.4, rely=0.45)
        self.ask_phi1 = Entry(self, font=("Consolas", 14), width=25)
        self.ask_phi1.place(relx=0.4, rely=0.55)
        self.ask_phi2 = Entry(self, font=("Consolas", 14), width=25)
        self.ask_phi2.place(relx=0.4, rely=0.65)
        self.ask_sr = Entry(self, font=("Consolas", 14), width=25)
        self.ask_sr.place(relx=0.4, rely=0.75)
        lab = Label(self, text="展示时间过长会导致运算量变大,如点击开始后没反应请耐心等待",
                    font=("Consolas", 10)).place(rely=0.95, relx=0.20)

        # 开始退出键
        startBtn = Button(self, text="开始", font=("Consolas", 14), command=self.start)
        startBtn.place(relx=0.8, rely=0.85)
        returnBtn = Button(text="返回", font=("Consolas", 14), command=lambda: self.master.switch_frame(page_3))
        returnBtn.place(relx=0.15, rely=0.85)

