
from bit import PrivateKeyTestnet
from fastapi import HTTPException

from models import BitcoinReception, BitcoinTransaction, TxInput
from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

wif = config["WIF"]
my_key = PrivateKeyTestnet(wif)


def send_bitcoin_to_wallet(transaction: BitcoinTransaction):
    print('usd: '+my_key.get_balance('usd'))
    print('btc: '+my_key.get_balance('btc'))
    
    #Send BTC to wallet
    wallet_to = transaction.receiver
    amount = transaction.amount
    currency = 'usd'
    balance = my_key.get_balance('usd')
    
    if amount > float(balance):
        raise HTTPException(status_code=404, detail="No hay suficientes fondos para completar la transacción.")
    else:
        try:
            #send bitcoins to wallet
            tx_hash = my_key.send([(wallet_to, amount, currency)])
            #print tx hash
            print(tx_hash)
            return {f"hash transacción: {tx_hash}"}
        except HTTPException as e:
            print(f"Error general: {e}")


def check_bitcoin_received(transaction: BitcoinReception):
    transacciones = my_key.get_transactions()
    print("Transacciones:")
    print(transacciones)
    for tx in transacciones:
        if tx == transaction.tx_hash:
            print("Transacción encontrada")
            return {f"transacción encontrada: {tx}"}
        else:
            return  {"Transacción no encontrada"}
    

def check_confirmed_tx(data: TxInput):
    url = f"https://api.blockcypher.com/v1/btc/test3/txs/{data.txid}"
    response = requests.get(url).json()
    if "confirmed" in response:
        return {"message": f"La transacción {data.txid} ha sido confirmada el {response['confirmed']}"}
    else:
        return {"message": f"La transacción {data.txid} no ha sido confirmada o no existe"}