from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from contractGenerator import create_contract

app = FastAPI()

@app.get('/get-contract')
async def generate_contract(owner_id, renter_id, address_id):
    create_contract(owner_id, renter_id, address_id)
    return FileResponse('meu_contrato.pdf', media_type="application/pdf")