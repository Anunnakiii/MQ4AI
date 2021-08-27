import json
import time
from MQ_Manager import MQ
from GPU_Info import GPU_Info

if __name__ == '__main__':
    # Load config file
    with open('./CONFIG.json', 'r') as f:
        _config = json.load(f)
        print(_config)
    # Set config
    try:
        HOST = _config['host']
        PORT = _config['port']
        USER = _config['user']
        PASSWORD = _config['password']
        EXCHANGE = _config['exchange']
        QUEUE = _config['queue']
        ROUTING_KEY = _config['routing_key']
    except Exception as e:
        print(f"Set Config Failed: {e}")
        exit(1)

    # Init MQ
    ai_mq = MQ(HOST, PORT, USER, PASSWORD, QUEUE, ROUTING_KEY, EXCHANGE)
    gpu_mq = MQ(HOST, PORT, USER, PASSWORD, "gpu", "gpu", EXCHANGE)
    gpu_info = GPU_Info(gpu_mq)
    gpu_info.start()
    # Test - send
    msg = json.dumps(
        {"TIME": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "TYPE": "Str/Json", "DATA": "TEST - Message"})
    ai_mq.send(msg)
    # Run
    try:
        ai_mq.rece("ai")
    except KeyboardInterrupt as ki:
        print("Exit")
        exit(1)
