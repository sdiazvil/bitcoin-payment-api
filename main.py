from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class BitcoinTransaction(BaseModel):
    sender: str
    receiver: str
    amount: float
    transaction_id: str

@app.post("/receive-bitcoin")
async def receive_bitcoin(transaction: BitcoinTransaction):
    # Aquí podrías implementar la lógica para manejar la transacción de Bitcoin
    # Asegúrate de validar la autenticidad y la integridad de la transacción
    
    # Ejemplo de validación simple: solo imprime la información de la transacción
    print(f"Transacción de Bitcoin recibida: {transaction}")
    
    # Puedes agregar más lógica aquí, como almacenar la transacción en una base de datos, etc.
    
    return {"status": "Transacción de Bitcoin recibida exitosamente"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)