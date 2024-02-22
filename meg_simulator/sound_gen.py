import numpy as np
import sounddevice as sd
import time

import random
import time

import os
import numpy as np
import mne

import neo
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, AggOperations


def fetch_sample_data_from_mne():

    sample_data_folder = mne.datasets.sample.data_path()  # 下载数据

    # 找到文件地址
    sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                        'sample_audvis_filt-0-40_raw.fif')

    # read_raw_fif显示文件中的数据信息，信息的意思是关于环境降噪的
    raw = mne.io.read_raw_fif(sample_data_raw_file)

    print(raw)
    return raw


def fetch_fake_eeg():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    data = board.get_board_data(20000)
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
    # demo for downsampling, it just aggregates data
    return data[1]


def main():
    fs = 16000 # 采样率
    f = 331 # 音频频率Hz
    length = 500 #时长s
    myarray1 = np.arange(fs * length) # 用numpy生成2000Hz的正弦波
    myarray1 = 1 * np.sin(2 * np.pi * f / fs * myarray1)
    print('wanmait.com显示数组内容:',myarray1)

    myarray = myarray1
    sd.play(myarray, fs) #播放
    time.sleep(length)

def gen_multi_freq_wave():
    fs = 16000  # 采样率
    f = 12  # 音频频率Hz
    length = 200  # 时长s
    myarray = np.arange(fs * length)  # 用numpy生成2000Hz的正弦波
    myarray = np.sin(2 * np.pi * f / fs * myarray)

    freqs = [511]

    for i in range(100):
        num = random.randint(1, 511)
        freqs.append(num)

    for freq in freqs:
        myarraytmp = np.arange(fs * length)
        myarraytmp = 100 * np.sin(2 * np.pi * freq / fs * myarraytmp)
        myarray += myarraytmp

    myarray = np.random.normal(myarray, 0.1)
    sd.play(myarray, fs)  # 播/≥放
    print(len(myarray))
    time.sleep(length)

if __name__ == '__main__':
    raw = fetch_sample_data_from_mne()
    max_time = 2000
    picks = mne.pick_types(raw.info, meg=True, exclude='bads')
    t_idx = raw.time_as_index([0., max_time])
    data, times = raw[picks, t_idx[0]:t_idx[1]]

    data = data * 1e11

    print("time length", len(times))
    #fs = 16000
    #eeg_array = raw
    sample_rate = 1200
    wave = np.repeat(data[0].T, 8)
    print("period time length:", len(wave)/sample_rate)

    #plt.plot(times, data[0].T)
    #plt.title("Sample channels")
    #plt.show()

    sd.play(wave, sample_rate)  # 播放
    time.sleep(len(wave)/sample_rate)
    print("done")