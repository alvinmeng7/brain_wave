# 导入工具包
import numpy as np
import matplotlib.pyplot as plt

import mne
from mne import find_events, Epochs, compute_covariance, make_ad_hoc_cov
from mne.datasets import sample
from mne.simulation import (simulate_sparse_stc, simulate_raw,
                            add_noise, add_ecg, add_eog)
%matplotlib
auto

data_path = sample.data_path()
raw_fname = data_path + '/MEG/sample/sample_audvis_raw.fif'
fwd_fname = data_path + '/MEG/sample/sample_audvis-meg-eeg-oct-6-fwd.fif'

# 加载真实数据作为模板
raw = mne.io.read_raw_fif(raw_fname)
raw.set_eeg_reference(projection=True



# 生成偶极子时间序列
# 设置偶极子的数量
n_dipoles = 4
# 每个epoch或者event的时间窗口长度
epoch_duration = 2.
# 谐波数
n = 0
# 随机状态（可复制）
rng = np.random.RandomState(0)


def data_fun(times):
    """产生时间交错的正弦波，谐波为10Hz"""
    global n
    n_samp = len(times)
    window = np.zeros(n_samp)
    start, stop = [int(ii * float(n_samp) / (2 * n_dipoles))
                   for ii in (2 * n, 2 * n + 1)]
    window[start:stop] = 1.
    n += 1
    data = 25e-9 * np.sin(2. * np.pi * 10. * n * times)
    data *= window
    return data


times = raw.times[:int(raw.info['sfreq'] * epoch_duration)]
fwd = mne.read_forward_solution(fwd_fname)
src = fwd['src']
stc = simulate_sparse_stc(src, n_dipoles=n_dipoles, times=times,
                          data_fun=data_fun, random_state=rng)
# look at our source data
fig, ax = plt.subplots(1)
ax.plot(times, 1e9 * stc.data.T)
ax.set(ylabel='Amplitude (nAm)', xlabel='Time (sec)')
mne.viz.utils.plt_show()


"""
得到模拟原始数据并绘制
模拟原始数据
"""
raw_sim = simulate_raw(raw.info, [stc] * 10, forward=fwd, cov=None,
                       verbose=True)
cov = make_ad_hoc_cov(raw_sim.info)
add_noise(raw_sim, cov, iir_filter=[0.2, -0.2, 0.04], random_state=rng)
add_ecg(raw_sim, random_state=rng)
add_eog(raw_sim, random_state=rng)
raw_sim.plot()
plt.show()



"""
绘制诱发数据
"""
events = find_events(raw_sim)  # only 1 pos, so event number == 1
epochs = Epochs(raw_sim, events, 1, tmin=-0.2, tmax=epoch_duration)
cov = compute_covariance(epochs, tmax=0., method='empirical',
                         verbose='error')  # quick calc
evoked = epochs.average()
evoked.plot_white(cov, time_unit='s')
plt.show()