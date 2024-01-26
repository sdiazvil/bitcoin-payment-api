
from bit import PrivateKeyTestnet
from fastapi import HTTPException

from models import BitcoinReception, BitcoinTransaction
from dotenv import dotenv_values

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
    # También puedes verificar las transacciones
    transacciones = my_key.get_transactions()
    print("Transacciones:")
    print(transacciones)
    for tx in transacciones:
        if tx == transaction.tx_hash:
            print("Transacción encontrada")
            return {f"transacción encontrada: {tx}"}
        else:
            return  {"Transacción no encontrada"}
