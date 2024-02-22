import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.sans-serif'] = ['SimHei']
sample_rate = 22050  # 采样率
time = 5  # 波形时间


def wave_bulid(f0, amplitude_xishu=1):  # 波形生成

    w_oumiga = 2 * pi * f0
    x = np.linspace(0, time, sample_rate * time)
    y = amplitude_xishu * np.cos(w_oumiga * x)
    return x, y, f0


def to_fft(data, N=sample_rate * time):  # 转换为频域数据，并进行取半、归一化等处理
    # N=self.nframes #取样点数
    df = sample_rate / (
                N - 1)  # 每个点分割的频率 如果你采样频率是4096，你FFT以后频谱是从-2048到+2048hz（4096除以2），然后你的1024个点均匀分布，相当于4个HZ你有一个点，那个复数的模就对应了频谱上的高度
    freq = [df * n for n in range(0, N)]

    wave_data2 = data[0:N]
    fft_int = np.fft.fft(wave_data2)
    # print(N, len(data),len(wave_data2))
    c = fft_int * 2 / N  # *2能量集中化  /N归一化
    d = int(len(c) / 2)  # 对称取半
    freq = freq[:d - 1]
    fredata = abs(c[:d - 1])

    return freq, fredata


def wave_filter(y_data, fre_min=0, fre_max=11025, sample_rate=22050, time=5):  # 滤波函数
    if fre_max > sample_rate / 2:
        fre_max = sample_rate / 2
    N = int(sample_rate * time)
    freq = np.linspace(0, sample_rate, N)
    ft_y = np.fft.fft(y_data)
    n1 = np.array(np.where(freq <= fre_min)).max()
    n2 = np.array(np.where(freq >= fre_max)).min()
    ft_y[n1:n2] = 0 + 0j
    ft_y[-n2:-n1] = 0 + 0j
    y_new = np.fft.ifft(ft_y)
    return y_new


def wave_all(f0):  # 生成时域+频域波形
    x, y, f0 = wave_bulid(f0)
    fre_x, fre_y = to_fft(y)
    str_data = "y = cos(2Pi*" + str(f0) + "*t)"
    return x, y, fre_x, fre_y, str_data


# *******生成两个信号*******
f0 = [2, 30]  # 调制信号，载波信号频率
str_title = ["调制信号", "载波"]
plt.figure(figsize=(16, 10))

y3 = 1
for i in range(0, len(f0)):  # 生成f0中两个波形
    x, y, fre_x, fre_y, str_data = wave_all(f0[i])
    y3 *= y  # 调制后的信号

    plt.subplot(5, 2, i * 2 + 1)
    plt.title(str_title[i], fontdict={'weight': 'normal', 'size': 10})
    # plt.xlabel(u"Time(S)")
    plt.plot(x, y)

    plt.subplot(5, 2, i * 2 + 2)
    # plt.title(str_data+"频域",fontdict={'weight':'normal','size': 10})
    # plt.xlabel(u"Frequency")
    plt.plot(fre_x, fre_y)
    plt.xlim(0, f0[1] * 1.5)

# *******AM调制后的波形*******
fre_x, fre_y = to_fft(y3)
plt.subplot(5, 2, 5)
plt.title("AM已调波", fontdict={'weight': 'normal', 'size': 10})
# plt.xlabel(u"Time(S)")
plt.plot(x, y3)

plt.subplot(5, 2, 6)
# plt.title("AM Frc")
# plt.xlabel(u"Frequency")
plt.plot(fre_x, fre_y)
plt.xlim(0, f0[1] * 1.5)

# *******同步检波后的波形********
y4 = y3 * wave_bulid(f0[1])[1]
fre_x4, fre_y4 = to_fft(y4)

plt.subplot(5, 2, 7)
plt.title("AM同步检波", fontdict={'weight': 'normal', 'size': 10})
# plt.xlabel(u"Time(S)")
plt.plot(x, y4)

plt.subplot(5, 2, 8)
# plt.title("AM Frc")
# plt.xlabel(u"Frequency")
plt.plot(fre_x4, fre_y4)
plt.xlim(0, f0[1] * 2.5)

# *******滤波后的波形*******
y5 = wave_filter(y4, 9, )
fre_x5, fre_y5 = to_fft(y5)

plt.subplot(5, 2, 9)
plt.title("滤波后信号", fontdict={'weight': 'normal', 'size': 10})
# plt.xlabel(u"Time(S)")
plt.plot(x, y5)

plt.subplot(5, 2, 10)
# plt.title("AM Frc")
# plt.xlabel(u"Frequency")
plt.plot(fre_x5, fre_y5)
plt.xlim(0, f0[1] * 2.5)
# plt.subplots_adjust(hspace=0.4)
plt.show()