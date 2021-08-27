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
        print('Decive: {0}, {1}, 可用显存: {2}, 已用显存: {3}, 总显存: {4}'.format(index, gpu_name, meminfo.free / 1024 ** 2,
                                                                        meminfo.used / 1024 ** 2,
                                                                        meminfo.total / 1024 ** 2))
        return index, gpu_name, meminfo.free / 1024 ** 2, meminfo.used / 1024 ** 2, meminfo.total / 1024 ** 2

    def start(self):  # 创建线程
        gpu_info_thread = Thread(target=self.gpu_info)
        gpu_info_thread.start()  # 启动线程


if __name__ == '__main__':
    gpu = GPU_Info()
    gpu.start()
