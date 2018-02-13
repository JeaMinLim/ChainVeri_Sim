import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request
import socket

class device_info:
    def __init__(self):
        self.model_name = []
        self.firmware_version = []
        self.firmware_hash = []
        self.UUID = []
        self.trader_ip = []
        self.trader_port = []

    def request_verification(self, other_ip, other_port):
        """
        request verification process to other IoT devices

        :param other_ip: other IoT device IP address
        :param other_port: other IoT device port number
        :return: True if valid, False if not
        """
        request_url = "http://" + other_ip + ":" + str(other_port) + "/verification/request"
        response = requests.get(trader_url)




if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-ip', '--ip', help='Trader`s ip address ', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='Trader`s port number', default=5000, type=int)
    parser.add_argument('-m', '--model', default='JML_MK1', help='IoT device model name')
    parser.add_argument('-s', '--sender', help='UUID of IoT device', default='83765f2d-49c8-4d74-95b2-2486116e7101')
    parser.add_argument('-f', '--firmware_hash', help='Hash value of firmware', default='773c839d24cf91c394aca6f1b9cd40da')
    parser.add_argument('-v', '--version', help='firmware version in string', default='Ubuntu 17.10')

    args = parser.parse_args()

    device_info.trader_ip = args.ip
    device_info.trader_port = args.port
    device_info.model_name = args.model
    device_info.UUID = args.sender
    device_info.firmware_hash = args.firmware_hash
    device_info.firmware_version = args.version

    print("Trader information")
    trader_url = "http://" + device_info.trader_ip + ":" + str(device_info.trader_port) + "/information/you"

    response = requests.get(trader_url)
    print(response.text)

    print("\t URL: " + trader_url)
    print("IoT node information")
    print("\t MODEL: " + device_info.model_name)
    print("\t SENDER(IoT device) UUID: " + device_info.UUID)
    print("\t FIRMWARE HASH: " + device_info.firmware_hash)
    print("\t FIRMWARE VERSION:" + device_info.firmware_version)
    device_ip = socket.gethostbyname(socket.gethostname())
    print("\t IP address: " + device_ip)

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5100, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
