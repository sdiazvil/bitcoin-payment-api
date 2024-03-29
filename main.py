from fastapi import FastAPI, HTTPException
import uvicorn
from models import BitcoinTransaction, TxInput

from transaction import check_bitcoin_received, check_confirmed_tx, send_bitcoin_to_wallet

app = FastAPI(
    title="Bitcoin transaction microservice",
    version="1.0",
    description="A simple API server to transfer btc in testnet"
    )

@app.post("/send-bitcoin")
def send_bitcoin(transaction: BitcoinTransaction):
    try:
        response = send_bitcoin_to_wallet(transaction)
        return response
    except HTTPException as e:
        return {"error": f"Error: {e.status_code}, {e.detail}"}
    except Exception as e:
        return {"error": f"Error desconocido: {str(e)}"}

@app.post("/received-bitcoin")
def received_bitcoin(transaction: TxInput):
    try:
        response = check_bitcoin_received(transaction)
        return response
    except HTTPException as e:
        return {"error": f"Error: {e.status_code}, {e.detail}"}
    except Exception as e:
        return {"error": f"Error desconocido: {str(e)}"}

@app.post("/check-received-bitcoin")
def check_received_bitcoin(transaction: TxInput):
    try:
        response = check_confirmed_tx(transaction)
        return response
    except HTTPException as e:
        # Manejar la excepción HTTPException
        return {"error": f"Error: {e.status_code}, {e.detail}"}
    except Exception as e:
        # Manejar otras excepciones
        return {"error": f"Error desconocido: {str(e)}"}
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)