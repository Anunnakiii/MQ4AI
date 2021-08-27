# -*- coding: utf-8 -*-
'''
------------------------------------------------
    File Name:         GPU_Info
    Author:            wanJ
    Date:              2021/8/27
    Description:       获取显卡状态
------------------------------------------------
    修改记录：
    Author:            BoiWong
    Date:              2021/8/27
    Description:       1.重构部分代码
                       2.实时发送GPU信息到消息队列
------------------------------------------------
'''

from MQ_Manager import MQ
from threading import Thread
import pynvml


class GPU_Info():
    def __init__(self, gpu_mq: MQ):
        self.gpu_mq = gpu_mq
        pynvml.nvmlInit()
        self.deviceCount = pynvml.nvmlDeviceGetCount()  # 几块显卡

    def gpu_info(self):
        while True:
            for i in range(self.deviceCount):
                self.gpu_mq.send(self.get_gpu_state(i))

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
