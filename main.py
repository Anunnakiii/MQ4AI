import json
import time
from MQ_Manager import MQ
from GPU_Info import GPU_Info
from utils import *

if __name__ == '__main__':
    try:
        AI_HOST, AI_PORT, AI_USER, AI_PASSWORD, AI_QUEUE, AI_ROUTING_KEY, AI_EXCHANGE, AI_R_QUEUE, AI_R_EXCHANGE = load_config(
            "./AI_CONFIG.json")
        GPU_HOST, GPU_PORT, GPU_USER, GPU_PASSWORD, GPU_QUEUE, GPU_ROUTING_KEY, GPU_EXCHANGE, GPU_R_QUEUE, GPU_R_EXCHANGE = load_config(
            "./GPU_CONFIG.json")
    except Exception as e:
        print("Load config failed")
        exit(1)
    # Init MQ
    ai_mq = MQ(AI_HOST, AI_PORT, AI_USER, AI_PASSWORD, AI_QUEUE, AI_ROUTING_KEY, AI_EXCHANGE, AI_R_EXCHANGE, AI_R_QUEUE)
    gpu_mq = MQ(GPU_HOST, GPU_PORT, GPU_USER, GPU_PASSWORD, GPU_QUEUE, GPU_ROUTING_KEY, GPU_EXCHANGE, GPU_R_EXCHANGE,
                GPU_R_QUEUE)
    gpu_info = GPU_Info(gpu_mq)
    # gpu_info.start()
    # Test - send
    msg = json.dumps(
        {"TIME": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "TYPE": "Str/Json", "DATA": "TEST - Message"})
    ai_mq.send(msg)
    # Run
    try:
        ai_mq.rece()
    except KeyboardInterrupt as ki:
        print("Exit")
        exit(1)
