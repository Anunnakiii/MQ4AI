"""
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
                       2.序列化发送的数据对象
                       3.实时发送GPU信息到消息队列
------------------------------------------------
"""

import json
import time
from MQ_Manager import MQ
from threading import Thread
import pynvml


class GPU_Info():
    def __init__(self, gpu_mq: MQ):
        self.gpu_mq = gpu_mq
        pynvml.nvmlInit()
        self.deviceCount = pynvml.nvmlDeviceGetCount()

    def gpu_info(self):
        while True:
            gpus_info = dict()
            for i in range(self.deviceCount):
                gpu_index = f"GPU{i}"
                gpus_info[gpu_index] = self.get_gpu_state(i)
            self.gpu_mq.send(json.dumps(gpus_info))
            time.sleep(1)

    def get_gpu_state(self, index):
        gpu_info = dict()
        handle = pynvml.nvmlDeviceGetHandleByIndex(index)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        # print(f'Decive: {index}, {gpu_name}, \
        #         可用显存: {meminfo.free / 1024 ** 2}, \
        #         已用显存: {meminfo.used / 1024 ** 2}, \
        #         总显存: {meminfo.total / 1024 ** 2}')
        gpu_info["GPU_Name"] = gpu_name.decode()
        gpu_info["Free_Mem"] = meminfo.free / 1024 ** 2
        gpu_info["Used_Mem"] = meminfo.used / 1024 ** 2
        gpu_info["Total_Mem"] = meminfo.total / 1024 ** 2
        return gpu_info

    def start(self):  # 创建线程
        gpu_info_thread = Thread(target=self.gpu_info)
        gpu_info_thread.start()  # 启动线程
