# -*- coding: utf-8 -*-
'''
------------------------------------------------
    File Name:         GPU_Info
    Author:            wanJ
    Date:              2021/8/27
    Description:       获取显卡状态
------------------------------------------------
'''

from threading import Thread
import pynvml


class GPU_Info():
    def __init__(self):
        pynvml.nvmlInit()
        self.deviceCount = pynvml.nvmlDeviceGetCount()  # 几块显卡

    def gpu_info(self):
        while True:
            for i in range(self.deviceCount):
                self.get_gpu_state(i)

    def get_gpu_state(self, index):
        handle = pynvml.nvmlDeviceGetHandleByIndex(index)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        print(f'Decive: {index}, {gpu_name}, \
                可用显存: {meminfo.free / 1024 ** 2}, \
                已用显存: {meminfo.used / 1024 ** 2}, \
                总显存: {meminfo.total / 1024 ** 2}')
        return index, gpu_name, meminfo.free / 1024 ** 2, meminfo.used / 1024 ** 2, meminfo.total / 1024 ** 2

    def start(self):  # 创建线程
        gpu_info_thread = Thread(target=self.gpu_info)
        gpu_info_thread.start()  # 启动线程
