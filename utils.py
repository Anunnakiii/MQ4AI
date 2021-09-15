import json


def load_config(filename):
    # Load config file
    with open(filename, 'r') as f:
        _config = json.load(f)
        print(_config)
    # Set config
    try:
        host = _config['host']
        port = _config['port']
        user = _config['user']
        password = _config['password']
        exchange = _config['exchange']
        queue = _config['queue']
        routing_key = _config['routing_key']
        r_queue = _config['r_queue']
        r_exchange = _config['r_exchange']
        return host, port, user, password, queue, routing_key, exchange, r_queue, r_exchange
    except Exception as e:
        print(f"Set Config Failed: {e}")
