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
        _tmp = [i['addr'] for i in ifaddresses(_iface).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        self.device_ip = ', '.join(_tmp)
        # create UUID for IoT device
        self.UUID = str(uuid4())
        self.resDevice_ip = []
        self.resDevice_port = []
        self.resUUID = []


def _getLogger(_logName, _logDir, _logSize=500 * 1024, _logCount=4):
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


logPrefix = "1ST"
logger = _getLogger('IoTdevice', './log')

device = DeviceInfo()

app = Flask(__name__)


app.route('/verification/result', methods=['POST'])
def verification_resutl():
    return


@app.route('/verification/exchange', methods=['POST'])
def exchainge_vinfo():
    return


@app.route('/verification/info', methods=['GET'])
def verificaiton_info():
    # trigger verification process
    # caller should be REST API client(POSTMAN, cURL eta)
    logger.info("verification")

    # exchange V-INFO(Verification-related information)
    response = {
        'trader': {
            'ip': device.trader_ip,
            'port': device.trader_port
        },
        'requester': {
            'ip': device.device_ip,
            'port': device.device_port
        },
        'responder': {
            'ip': device.resDevice_ip,
            'port': device.resDevice_port,
        }
    }
    return jsonify(response), 201


@app.route('/connect', methods=['POST'])
def connect_device():
    # send connection result to IoT device
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['ip', 'port', 'UUID']
    if not all(k in values for k in required):
        return 'Missing values', 400

    device.resDevice_ip = values.get('ip')
    device.resDevice_port = values.get('port')
    device.resUUID = values.get('UUID')

    response = {
        'message': 'connection established',
        'ip': device.device_ip,
        'port': device.device_port,
        'UUID': device.UUID,
    }
    return jsonify(response), 201


def connect_to_device(self, _ip, _port):
    logger.info("Connection check to %s:%s" % (_ip, _port) )
    _url = "http://" + _ip + ":" + str(_port) + "/connect"

    _data = {
        'ip': device.device_ip,
        'port': device.device_port,
        'UUID': device.UUID,
    }

    response = requests.post(_url, json=_data)

    return response


def triggerVerification(self, _IP, _PORT):
    logger.info("send V-INFO to the other IoT device")
    _url = "http://" + _IP + ":" + _PORT + "/connect/device"

    vinfo = {
        'ip': device.device_ip,
        'port': device.device_port,
        'UUID': device.UUID,
    }
    logger.info("send V-INFO to the other IoT device")
    response = requests.post(_url, json=data)
    logger.info("send V-INFO to the other IoT device")
    if response.ok:
        values = request.get_json()
        required = ['ip', 'port', 'UUID']
        if not all(k in values for k in required):
            return 'Missing values', 400
        logger.info("send V-INFO to the other IoT device")
        device.resDevice_ip = values.get('ip')
        device.resDevice_port = values.get('port')
        device.resUUID = values.get('UUID')
        logger.info("\t V-INFO: revices V-NFO")
        logger.info("\t V-INFO: ip \tport \tUUID")
        logger.info("\t\t: %s, %s, $%s " % (device.resDevice_ip, device.resDevice_port, device.resDevice_UUID))

    else:
        logger.info("can not find other IoT device")


def log_device_info():
    # print current device Info
    logger.info("IoT node information: %s" % logPrefix)
    logger.info("\t MODEL: " + device.model_name)
    logger.info("\t SENDER(IoT device) UUID: " + device.UUID)
    logger.info("\t FIRMWARE HASH: " + device.firmware_hash)
    logger.info("\t FIRMWARE VERSION:" + device.firmware_version)
    logger.info("\t IP address: " + device.device_ip)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # set default config
    # firmware
    parser.add_argument('-tip', '--tip', help='Trader`s ip address ', default='127.0.0.1')
    parser.add_argument('-tp', '--tport', help='Trader`s port number', default=5000, type=int)
    parser.add_argument('-m', '--model', default='JML_MK1', help='IoT device model name')
    # parser.add_argument('-s', '--sender', help='UUID of IoT device', default='83765f2d-49c8-4d74-95b2-2486116e7101')
    parser.add_argument('-f', '--firmware_hash', help='Hash value of firmware',
                        default='773c839d24cf91c394aca6f1b9cd40da')
    parser.add_argument('-v', '--version', help='firmware version in string', default='Ubuntu 17.10')
    parser.add_argument('-ip', '--ip', help='This device IP', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='This device port number', default=5100, type=int)

    args = parser.parse_args()

    device.trader_ip = args.tip
    device.trader_port = args.tport
    device.model_name = args.model
    device.device_port = args.port
    device.firmware_hash = args.firmware_hash
    device.firmware_version = args.version

    logger.info("Connection test with Trader")
    response = connect_to_device(device, device.trader_ip, device.trader_port)

    if response.ok:
        try:
            logPrefix = "1ST"
            app.run(host='0.0.0.0', port=device.device_port)
            logger.info("Start IoT device %s: listen %s:%s" % (logPrefix, '0.0.0.0', device.device_port))
            log_device_info()

        except:
            print("You are not the first device")
            device.device_port = device.device_port + 1

            logger.info("Connection test with First IoT device")
            device.resDevice_ip = '127.0.0.01'
            device.resDevice_port = 5100
            response = connect_to_device(device, device.device_ip, device.trader_port)

            app.run(host='0.0.0.0', port=device.device_port)
            logPrefix = '2ND:'
            logger.info("Start IoT device %s: listen %s:%s" % (logPrefix, '0.0.0.0', device.device_port))
            log_device_info()
    else:
        print("connection test fail")
