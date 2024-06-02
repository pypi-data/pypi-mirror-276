import os

import zmq
from bitcoinlib.transactions import Transaction

from bitcoin.tx_listener.abstract_tx_listener import AbstractTxListener
from bitcoin.utils.constants import default_host, default_port


class ZMQTXListener:
    socket = None

    def __init__(self, tx_listener: AbstractTxListener):
        rpc_host = os.environ.get("RPC_HOST", default_host)
        self.zmq_url = f"tcp://{rpc_host}:{default_port}"
        self.tx_listener = tx_listener
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        self.socket = socket

    def start(self):
        connections = self.socket.connect(self.zmq_url)
        print(f"Connected to {connections}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
        while True:
            topic, body, seq = self.socket.recv_multipart()
            tx = Transaction.parse(body, strict=False)
            self.tx_listener.on_tx(tx)

    def stop(self):
        self.socket.close()
        self.socket = None
