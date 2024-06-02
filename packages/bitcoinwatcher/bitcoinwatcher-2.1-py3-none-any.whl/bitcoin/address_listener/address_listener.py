import os
from abc import ABC, abstractmethod

from bitcoinlib.transactions import Transaction
from ordipool.ordipool.mempoolio import Mempool

from bitcoin.models.address_tx_data import AddressTxData
from bitcoin.tx_listener.abstract_tx_listener import AbstractTxListener
from bitcoin.utils.constants import default_host
from bitcoin.utils.tx_address_data_extractor import DefaultTxAddressDataExtractor, MempoolTxAddressDataExtractor


class AbstractAddressListener(AbstractTxListener, ABC):
    DECIMAL_SCALE = 5
    host = os.environ.get("RPC_HOST", default_host)
    base_url = f"http://{host}:3006/api"
    mempool = Mempool(base_url=base_url)
    default_tx_extractor = DefaultTxAddressDataExtractor()
    mempool_tx_extractor = MempoolTxAddressDataExtractor(mempool)

    def __init__(self, addresses_to_listen: {str}):
        self.addresses_to_listen = addresses_to_listen

    @abstractmethod
    def consume(self, tx_hex, subscribed_address, address_tx_data: [AddressTxData]):
        pass

    def filter_address_tx_data(self, address_tx_data: [AddressTxData]) -> [str]:
        filtered_address_tx_data = list(filter(lambda x: x.address in self.addresses_to_listen and x.address != "",
                                               address_tx_data))
        # get all address
        return list(set((map(lambda x: x.address, filtered_address_tx_data))))

    def on_tx(self, tx: Transaction):
        # get all address in the inputs and outputs along with the amount
        if tx.coinbase:
            return
        address_tx_data = self.default_tx_extractor.extract(tx)
        # filter the address we are interested in
        addresses_for_events = self.filter_address_tx_data(address_tx_data)
        if len(addresses_for_events) == 0:
            return
        # get the address tx data from mempool for full details if any address matches
        try:
            address_tx_data = self.mempool_tx_extractor.extract(tx)
        except Exception as e:
            print(f"Error in getting mempool tx data, taking defaults: {e}")
            address_tx_data = address_tx_data

        for address in addresses_for_events:
            self.consume(tx_hex=tx.raw_hex(), subscribed_address=address, address_tx_data=address_tx_data)
