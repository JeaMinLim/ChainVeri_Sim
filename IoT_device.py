import json
import requests
from netifaces import interfaces, ifaddresses, AF_INET

class DeviceInfo:
    def __init__(self):
        self.model_name = []
        self.firmware_version = []
        self.firmware_hash = []
        self.UUID = []
        self.trader_ip = []
        self.trader_port = []
        self.device_ip = []
        self.device_port = []

        _iface = interfaces()
        _iface.remove(u'lo')
        _iface = ', '.join(_iface)
        _tmp = [i['addr'] for i in ifaddresses(_iface).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        self.device_ip = ', '.join(_tmp)



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # set default config
    # firmware
    parser.add_argument('-tip', '--tip', help='Trader`s ip address ', default='127.0.0.1')
    parser.add_argument('-tp', '--tport', help='Trader`s port number', default=5000, type=int)
    parser.add_argument('-m', '--model', default='JML_MK1', help='IoT device model name')
    parser.add_argument('-s', '--sender', help='UUID of IoT device', default='83765f2d-49c8-4d74-95b2-2486116e7101')
    parser.add_argument('-f', '--firmware_hash', help='Hash value of firmware', default='773c839d24cf91c394aca6f1b9cd40da')
    parser.add_argument('-v', '--version', help='firmware version in string', default='Ubuntu 17.10')
    parser.add_argument('-ip', '--ip', help='This device IP', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='This device port number', default=5100, type=int)

    args = parser.parse_args()

    device = DeviceInfo()

    device.trader_ip = args.tip
    device.trader_port = args.tport
    device.model_name = args.model
    device.UUID = args.sender
    device.firmware_hash = args.firmware_hash
    device.firmware_version = args.version

    print("IoT node information")
    print("\t MODEL: " + device.model_name)
    print("\t SENDER(IoT device) UUID: " + device.UUID)
    print("\t FIRMWARE HASH: " + device.firmware_hash)
    print("\t FIRMWARE VERSION:" + device.firmware_version)
    print("\t IP address: " + device.device_ip)

    print("Connection check")
    trader_url = "http://" + device.trader_ip + ":" + str(device.trader_port) + "/nodes/device"
    print("\t URL: " + trader_url)

    # must fix port number
    data = {
        'ip': device.device_ip,
        'port': '111',
        'UUID': device.UUID,
    }

    print(json.dumps(data))

    response = requests.post(trader_url, json=data)
    if response.ok:
        print(response.text)
