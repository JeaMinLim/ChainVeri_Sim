import json
import logging
import logging.handlers

import os
import requests
from uuid import uuid4
from flask import Flask, jsonify, request
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
        # get IoT device`s IP address
        _iface = interfaces()
        _iface.remove(u'lo')
        _iface = ', '.join(_iface)
        _tmp = [i['addr'] for i in ifaddresses(_iface).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        self.device_ip = ', '.join(_tmp)
        # create UUID for IoT device
        self.UUID = str(uuid4())


def _getLogger(_logName, _logDir, _logSize=500*1024, _logCount=4):
    if not os.path.exists(_logDir):
        os.makedirs(_logDir)
    _logfile = '%s/%s.log' % (_logDir, _logName)
    _logLevel = logging.INFO
    _logger = logging.getLogger(_logName)
    _logger.setLevel(_logLevel)
    if _logger.handlers is not None and len(_logger.handlers) >= 0:
        for handler in _logger.handlers:
            _logger.removeHandler(handler)
            _logger.handlers = []
        _loghandler = logging.handlers.RotatingFileHandler(_logfile, maxBytes=_logSize, backupCount=_logCount)
        _formatter = logging.Formatter('[%(asctime)s] %(message)s')
        _loghandler.setFormatter(_formatter)
        _logger.addHandler(_loghandler)

        return _logger


logger = _getLogger('IoTdevice', './log')

app = Flask(__name__)


@app.route('/connect/device', methods=['POST'])
def connect_device():
    # send connection result to IoT device
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['ip', 'port', 'UUID']
    if not all(k in values for k in required):
        return 'Missing values', 400

    device_uuid = values.get('UUID')

    response = {
        'message': 'connected',
        'my_UUID': device.UUID,
        'your_UUID': device_uuid,
    }
    return jsonify(response), 201


def connetOther(self, _IP, _PORT):
    print("Connect to IoT device")
    _url = "http://" + _IP + ":" + _PORT + "/connect/device"

    data = {
        'ip': device.device_ip,
        'port': device.device_port,
        'UUID': device.UUID,
    }

    response = requests.post(_url, json=data)
    if response.ok:
        print(response)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # set default config
    # firmware
    parser.add_argument('-tip', '--tip', help='Trader`s ip address ', default='127.0.0.1')
    parser.add_argument('-tp', '--tport', help='Trader`s port number', default=5000, type=int)
    parser.add_argument('-m', '--model', default='JML_MK1', help='IoT device model name')
    #parser.add_argument('-s', '--sender', help='UUID of IoT device', default='83765f2d-49c8-4d74-95b2-2486116e7101')
    parser.add_argument('-f', '--firmware_hash', help='Hash value of firmware', default='773c839d24cf91c394aca6f1b9cd40da')
    parser.add_argument('-v', '--version', help='firmware version in string', default='Ubuntu 17.10')
    parser.add_argument('-ip', '--ip', help='This device IP', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='This device port number', default=5100, type=int)

    args = parser.parse_args()

    device = DeviceInfo()

    device.trader_ip = args.tip
    device.trader_port = args.tport
    device.model_name = args.model
    device.device_port = args.port
    device.firmware_hash = args.firmware_hash
    device.firmware_version = args.version

    #logger.info("IoT node information")
    #print("IoT node information")
    #print("\t MODEL: " + device.model_name)
    #print("\t SENDER(IoT device) UUID: " + device.UUID)
    #print("\t FIRMWARE HASH: " + device.firmware_hash)
    #print("\t FIRMWARE VERSION:" + device.firmware_version)
    #print("\t IP address: " + device.device_ip)

    print("Connection check")
    trader_url = "http://" + device.trader_ip + ":" + str(device.trader_port) + "/connect/device"
    print("\t Trader check URL: " + trader_url)

    data = {
        'ip': device.device_ip,
        'port': device.device_port,
        'UUID': device.UUID,
    }
    response = requests.post(trader_url, json=data)
    if response.ok:
        try:
            logPrefix = "1ST"
            logger.info("Start IoT device %s: listen %s:%s" % (logPrefix, '0.0.0.0', device.device_port))
            app.run(host='0.0.0.0', port=device.device_port)
        except:
            print("You are not the first device")
            device.device_port = device.device_port + 1
            # minimum handshake
            connetOther(device, device.device_ip, str(device.device_port - 1))
            logPrefix = '2ND:'
            logger.info("Start IoT device : listen %s:%s" % ('0.0.0.0', device.device_port))
            app.run(host='0.0.0.0', port=device.device_port)
    else:
        print("connection test fail")