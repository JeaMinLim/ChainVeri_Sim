import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import os
import requests
from flask import Flask, jsonify, request

from datetime import datetime
import logging
import logging.handlers

class Blockchain:
    # Initalize ChainVeri Blockchain
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block['previous_hash']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'type': 1,
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, model_name, firmware_hash, version):
        """
        Creates a new verification info to go into the next mined Block

        :param sender: Address of the Sender(UUID or Public Key eta.)
        :param model_name: name of IoT device model
        :param firmware_hash: The hash value of firmware
        :param version: firmware version
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'model_name': model_name,
            'firmware_hash': firmware_hash,
            'version': version
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         
        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()


def getLogger(_logName, _logDir, _logSize=500*1024, _logCount=4):
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


logger = getLogger('trader', './log')


@app.route('/connect/device', methods=['POST'])
def connect_device():
    # send connection result to IoT device
    logger.info("\t /connect/device")
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['ip', 'port', 'UUID']
    if not all(k in values for k in required):
        return 'Missing values', 400

    device_uuid = values.get('UUID')

    response = {
        'your_UUID': device_uuid,
    }
    return jsonify(response), 201


@app.route('/information/you', methods=['GET'])
def send_information():
    # Send this Trader`s information
    logger.info("\t /information/you")
    response = {
        'trader_address': node_identifier,
    }
    return jsonify(response), 200


@app.route('/address/device', methods=['GET'])
def make_address():
    # Generate and send random identifier(UUID) for IoT devices.
    # This API is for simulations ONLY!!!!
    logger.info("\t /address/device")
    identifier = str(uuid4())

    response = {
        'identifier': identifier,
    }
    return jsonify(response), 200


@app.route('/dump', methods=['GET'])
def save_blockchain():
    # save blockchain into file
    logger.info("\t /dump")
    date = datetime.today().strftime("%Y%m%d%H%M")

    file = open("ChainVeri-" + date, 'w')
    file.write("ChainVeri Blockchain " + date + "\n")
    file.write(json.dumps(blockchain.chain, indent='\t'))

    file.close()

    # print blockchain data to client
    response = {
        'message': "Blockchain Saved",
        'index': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    logger.info("\t /mine")
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    logger.info("\t /transaction/new")
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'model_name', 'firmware_hash', 'version']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    blockchain.new_transaction(values['sender'], values['model_name'], values['firmware_hash'], values['version'])

    response = {'message': f'Transaction will be added to Block'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    logger.info("\t /chain")
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    logger.info("\t /nodes/register")
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    logger.info("\t /nodes/resolve")
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    logger.info("Start trader: listen %s:%s" % ('0.0.0.0', port))

    app.run(host='0.0.0.0', port=port)
