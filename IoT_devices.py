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
    parser.add_argument('-p', '--host', default='127.0.0.1', help='trader host ')
    args = parser.parse_args()
    trader_host = args.host

    app.run(host=trader_host)