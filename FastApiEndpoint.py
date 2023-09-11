from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from contractGenerator import create_contract
from entidades import PersonManipulator, Owner, Renter
from entidades import addressManipulator
from pydantic import BaseModel
app = FastAPI()

class personPayload(BaseModel):
    name: str
    cpf: str
    rg: str

class addressPayload(BaseModel):
    address_name: str
    address_number: str
    complement: str
    neighborhood: str
    city: str
    state: str
    cep: str

@app.post('/make-Owner')
async def make_owner(person_data: personPayload):
    PersonManipulator().create_person(Owner, person_data.name, person_data.cpf, person_data.rg)
    return person_data


@app.post('/make-Renter')
async def make_owner(person_data: personPayload):
    PersonManipulator().create_person(Renter, person_data.name, person_data.cpf, person_data.rg)
    return person_data

@app.post('/make-Address')
async def make_owner(address_data: addressPayload):
    addressManipulator().create_address(address_name=address_data.address_name, address_number=address_data.address_number, complement=address_data.complement, \
                         neighborhood=address_data.neighborhood, city=address_data.city, state=address_data.state, cep=address_data.cep)
    return address_data

@app.get('/get-contract')
async def generate_contract(owner_id, renter_id, address_id, start_date, end_date, due_date, value):
    create_contract(owner_id, renter_id, address_id, start_date, end_date, due_date, value)
    #Adicionar esse header no "FileResponse" para fazer o download do arquivo pelo navegador ao invés de exibir direto.
    #headers = {
    #    "Content-Disposition": f"attachment; filename=meu_contrato.pdf"
    #}


    return FileResponse('meu_contrato.pdf', media_type="application/pdf")
