import io

owner_data = {
    "nome": "LAURINDO FIGUEIREDO MOREIRA",
    "cpf": "251.428.875-49",
    "rg": "17.422.791-7",
}
renter_data = {
    "nome": "VANESSA QUINTINO NASCIMENTO SANTOS",
    "cpf": "359.162.608-22",
    "rg": "41.905.286-0",
}

location_data = {
    "logradouro": "RUA OSMAN DA COSTA PINO, Nº 42, CASA 4 - JARDIM CARUMBÉ - SÃO PAULO - SP",
    "valor": 700,
    "deposito": "2 meses",
    "data_assinatura": "10/12/2022",
    "data_vencimento": "10/12/2024",
    "data_pagamento": "10"

}


template_string = f'''
<strong>{owner_data["nome"]}</strong>, <strong>(CPF) {owner_data["cpf"]}</strong>, Cédula de identidade <strong>{owner_data["rg"]}</strong> doravante denominado LOCADOR(A) 

<strong>{renter_data["nome"]}</strong> (CPF) <strong>{renter_data["cpf"]}</strong>, Cédula de identidade <strong>{renter_data["rg"]}</strong> doravante denominado LOCATÁRIO(A)  

Celebram o presente contrato de locação residencial, com as cláusulas e condições seguintes: 

O LOCADOR cede para locação residencial ao LOCATÁRIO, um salão comercial, na <strong>{location_data["logradouro"]}</strong> 

A locação destina-se ao uso exclusivo como residência e domicilio do LOCATÁRIO. 

O prazo de locação é de 02 (dois) anos, iniciando-se em 08 de julho de 2022 e terminando em 08 de julho de 2024, limite de tempo em que o imóvel objeto do presente deverá ser restituído independentemente de qualquer notificação ou interpelação sob pena de caracterizar infração contratual. 

O aluguel mensal será de R$ 900,00 (Novecentos reais) e deverá ser pago até a data de seu vencimento, todo dia 08 de cada mês do mês seguinte ao vencido, no local do endereço do LOCADOR ou outro que o mesmo venha a designar. 

Obs. (foi dado dois meses de depósito) 


'''

html_file = open('./contract_html_exibition.txt', 'r', encoding='utf-8')
# print(html_file.read())
# html_file.write(template_string)
html_file.close()
