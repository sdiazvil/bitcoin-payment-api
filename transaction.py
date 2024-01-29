
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


def check_bitcoin_tx(transaction: BitcoinReception):
    transacciones = my_key.get_transactions()
    print("Transacciones:")
    print(transacciones)
    for tx in transacciones:
        if tx == transaction.tx_hash:
            print("Transacción encontrada")
            return {f"transacción encontrada: {tx}"}
        
def check_confirmed_tx(data: TxInput):
    # Construir la URL de la API de BlockCypher para consultar el estado de la transacción
    url = f"https://api.blockcypher.com/v1/btc/test3/txs/{data.txid}"
    # Hacer una petición GET a la URL y obtener la respuesta en formato JSON
    response = requests.get(url).json()
    # Verificar si la respuesta contiene el campo "confirmed"
    if "confirmed" in response:
        # Devolver un mensaje indicando que la transacción ha sido confirmada y la fecha de confirmación
        return {"message": f"La transacción {data.txid} ha sido confirmada el {response['confirmed']}"}
    else:
        # Devolver un mensaje indicando que la transacción no ha sido confirmada o no existe
        return {"message": f"La transacción {data.txid} no ha sido confirmada o no existe"}