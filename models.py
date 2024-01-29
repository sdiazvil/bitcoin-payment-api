from pydantic import BaseModel

class BitcoinTransaction(BaseModel):
    receiver: str
    amount: float
    transaction_id: str

class BitcoinReception(BaseModel):
    tx_hash: str
    amount: float
    transaction_id: str

class TxInput(BaseModel):
    txid: str