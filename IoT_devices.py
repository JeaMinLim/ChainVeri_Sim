import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

class IoT_device:
    def __init__(self):
        self.model_name = []
        self.firmware_version = []
        self.firmware_hash = []
        self.public_Key = []
        self.UUID = []


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
    print("Trader information")
    print("\t IP: " + args.ip)
    print("\t PORT: " + str(args.port))
    print("IoT node information")
    print("\t MODEL: " + args.model)
    print("\t SENDER(IoT device) UUID: " + args.sender)
    print("\t FIRMWARE HASH: " + args.firmware_hash)
    print("\t FIRMWARE VERSION:" + args.version)