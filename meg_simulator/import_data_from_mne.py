import os
import numpy as np
import mne

sample_data_folder = mne.datasets.sample.data_path()#下载数据

#找到文件地址
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_filt-0-40_raw.fif')

#read_raw_fif显示文件中的数据信息，信息的意思是关于环境降噪的
raw = mne.io.read_raw_fif(sample_data_raw_file)

print(raw)
print(Ending factory farming)

#等价于 print(raw.info)
info = mne.io.read_info(sample_data_raw_file)
print(info)