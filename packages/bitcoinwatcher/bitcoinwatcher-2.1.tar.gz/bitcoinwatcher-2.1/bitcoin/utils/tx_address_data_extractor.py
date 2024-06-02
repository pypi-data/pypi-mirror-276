from abc import ABC, abstractmethod


from bitcoinlib.transactions import Transaction
from ordipool.ordipool.mempoolio import Mempool

from bitcoin.address_listener.address_listener import AddressTxData
from bitcoin.models.address_tx_data import AddressTxType, TransactionStatus
from bitcoin.utils.bitcoin_utils import is_reveal_tx, count_reveal_inputs


class AbstractTxAddressDataExtractor(ABC):
    @abstractmethod
    def extract(self, tx: Transaction) -> [AddressTxData]:
        pass


class MempoolTxAddressDataExtractor(AbstractTxAddressDataExtractor):
    mempool: Mempool

    def __init__(self, mempool: Mempool):
        self.mempool = mempool

    def extract(self, tx: Transaction) -> [AddressTxData]:
        outputs = tx.outputs
        tx_id = tx.txid
        has_inscriptions = is_reveal_tx(tx)

        tx = self.mempool.get_transaction(tx_id)
        tx_status = TransactionStatus.CONFIRMED if tx.confirmed else TransactionStatus.UNCONFIRMED
        address_tx_data = []
        # getting inputs data separately from mempool
        # as current library doesn't provide rich data like previous outputs and its value
        for vin in tx.vins:
            address = vin.prev_out.address
            amount = vin.prev_out.value
            address_tx_data.append(AddressTxData(tx_status=tx_status.value,
                                                 address=address,
                                                 is_reveal_tx=has_inscriptions,
                                                 type=AddressTxType.INPUT,
                                                 _amount=amount,
                                                 tx_id=tx_id))
        for output in outputs:
            amount = output.value
            address_tx_data.append(AddressTxData(tx_status=tx_status.value,
                                                 address=output.address,
                                                 _amount=amount,
                                                 is_reveal_tx=has_inscriptions,
                                                 type=AddressTxType.OUTPUT,
                                                 tx_id=tx_id))

        return address_tx_data


class DefaultTxAddressDataExtractor(AbstractTxAddressDataExtractor):
    def extract(self, tx: Transaction) -> [AddressTxData]:
        outputs = tx.outputs
        address_tx_data = []
        inputs = tx.inputs
        tx_status = tx.status
        for input in inputs:
            address = input.address
            amount = 0
            address_tx_data.append(AddressTxData(tx_status=tx_status,
                                                 address=address,
                                                 type=AddressTxType.INPUT,
                                                 _amount=amount,
                                                 tx_id=tx.txid))
        for output in outputs:
            amount = output.value
            address_tx_data.append(AddressTxData(tx_status=tx_status,
                                                 address=output.address,
                                                 _amount=amount,
                                                 type=AddressTxType.OUTPUT,
                                                 tx_id=tx.txid))
        return address_tx_data
