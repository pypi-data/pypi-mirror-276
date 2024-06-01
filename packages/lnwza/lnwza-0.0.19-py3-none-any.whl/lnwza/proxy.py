import json
import os


def _write_file(config_proxy):
    with open(config_proxy_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(config_proxy, indent=4))


def _read_read():
    with open(config_proxy_path, 'r', encoding='utf-8') as f:
        config_proxy = json.loads(f.read())
    return config_proxy


def get():
    config_proxy = _read_read()
    for k, v in config_proxy.items():
        print(f'{k} = {v}')


def set(key, value):
    config_proxy = _read_read()
    config_proxy[key] = value
    _write_file(config_proxy)


def reset():
    # config_proxy = {
    #     "used_proxy": False,
    #     "proxy_host": None,
    #     "proxy_port": None,
    #     "proxy_user": None,
    #     "proxy_pass": None,
    # }
    config_proxy = {
        "used_proxy": True,
        "proxy_host": "150.61.8.70",
        "proxy_port": 10080,
        "proxy_user": "agyc026730",
        "proxy_pass": "op90-==="
    }
    _write_file(config_proxy)


dir = os.path.dirname(__file__)
config_proxy_path = os.path.join(dir, 'config_proxy.json')

if 'config_proxy.json' not in os.listdir(dir):
    reset()

config_proxy = _read_read()
proxy_host = config_proxy["proxy_host"]
proxy_port = config_proxy["proxy_port"]
proxy_user = config_proxy["proxy_user"]
proxy_pass = config_proxy["proxy_pass"]
proxy_link = f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
