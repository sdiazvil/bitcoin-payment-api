
from bit import PrivateKeyTestnet
from fastapi import HTTPException

from models import BitcoinTransaction, TxInput
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


def check_bitcoin_received(transaction: TxInput):
    transacciones = my_key.get_transactions()
    print("Transacciones:")
    print(transacciones)
    for tx in transacciones:
        if tx == transaction.txid:
            print("Transacción encontrada")
            return {f"transacción encontrada: {tx}"}
    

def check_confirmed_tx(data: TxInput):
    base_url = config["URL"]
    url = f"{base_url}{data.txid}"
    response = requests.get(url).json()
    if "confirmed" in response:
        confirmations = response['confirmations']
        if confirmations == 1:
            confirmations_message = "1 confirmación"
        if confirmations == 0:
            confirmations_message = "0 confirmaciones"
        if confirmations > 1:
            confirmations_message = f"{confirmations} confirmaciones"
        return {"message": f"La transacción {data.txid} ha sido confirmada el {response['confirmed']} y tiene {confirmations_message}"}
    else:
        return {"message": f"La transacción {data.txid} no ha sido confirmada o no existe"}
