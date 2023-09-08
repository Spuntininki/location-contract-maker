from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.units import inch
import re
from entidades import PersonManipulator, addressManipulator, Owner, Renter
from datetime import datetime


def formatar_cpf(string_numeros):
    
    numeros = re.sub(r'\D', '', string_numeros)
    
    if len(numeros) != 11:
        return "Formato inválido. A string deve conter 11 dígitos numéricos."
    
    cpf_formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    
    return cpf_formatado

def formatar_rg(string_numerica):
    # Remover caracteres não numéricos da string
    numeros = re.sub(r'\D', '', string_numerica)
    
    # Verificar se a string possui pelo menos 8 dígitos numéricos
    if len(numeros) < 8:
        return "Formato inválido. A string deve conter pelo menos 8 dígitos numéricos."
    
    # Formatar o RG com pontos e traços
    rg_formatado = f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}-{numeros[8]}"
    rg_formatado = f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}-{numeros[8]}"
    
    return rg_formatado

def get_full_date_description(string_date='', today=False):
    
    STRING_DESC_OF_MONTHS = {
        1:'janeiro',
        2:'fevereiro',
        3: 'março',
        4: 'abril',
        5: 'maio',
        6:'junho',
        7:'julho',
        8:'agosto',
        9:'setembro',
        10:'outubro',
        11:'novembro',
        12:'dezembro'
        }
    if not today:        
        date = datetime.strptime(string_date, '%Y-%m-%d')
        return f'{str(date.day).zfill(2)} de {str(STRING_DESC_OF_MONTHS[date.month]).zfill(2)} de {date.year}'
    else:
        date = datetime.now()
        return f'{str(date.day).zfill(2)} de {str(STRING_DESC_OF_MONTHS[date.month]).zfill(2)} de {date.year}'

def numero_por_extenso(numero):
    unidades = ['zero', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove']
    especiais = ['dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove']
    dezenas = ['vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
    centenas = ['cem', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']
    milhares = ['mil', 'milhão', 'bilhão', 'trilhão', 'quatrilhão', 'quintilhão', 'sextilhão', 'septilhão', 'octilhão', 'nonilhão', 'decilhão', 'undecilhão', 'dodecilhão']
    
    numero = int(numero)
    if numero >= 0 and numero < 10:
        return unidades[numero]
    elif numero >= 10 and numero < 20:
        return especiais[numero - 10]
    elif numero >= 20 and numero < 100:
        dezena = dezenas[numero // 10 - 2]
        unidade = unidades[numero % 10]
        if numero % 10 == 0:
            return dezena
        else:
            return f"{dezena} e {unidade}"
    elif numero >= 100 and numero < 1000:
        centena = centenas[numero // 100]
        dezena = numero % 100
        if dezena == 0:
            return centena
        else:
            return f"{centena} e {numero_por_extenso(dezena)}"
    elif numero >= 1000 and numero < 1_000_000:
        n = str(numero)
        tamanho = len(n)
        if tamanho % 3 != 0:
            n = n.zfill(tamanho + (3 - (tamanho % 3)))
            tamanho = len(n)
        parte_extenso = []
        for i in range(0, tamanho, 3):
            segmento = int(n[i:i+3])
            if segmento != 0:
                extenso = numero_por_extenso(segmento)
                if i != 0:
                    extenso = f"{extenso} {milhares[i//3]}"
                parte_extenso.append(extenso)
        return ", ".join(parte_extenso)

    return "Número não suportado"


    

def create_contract(owner_id, renter_id, address_id, start_date, end_date):
    doc = SimpleDocTemplate("meu_contrato.pdf", pagesize=letter)

    person_maker = PersonManipulator()
    address_maker = addressManipulator()

    owner = person_maker.get_person_by_id(Owner, owner_id)
    renter = person_maker.get_person_by_id(Renter, renter_id)
    address = address_maker.get_full_address_string(address_maker.get_address_by_id(address_id))

    owner_cpf = formatar_cpf(owner.cpf)
    owner_rg = formatar_rg(owner.rg)
    renter_cpf = formatar_cpf(renter.cpf)
    renter_rg = formatar_rg(renter.rg)

    start_date_string_description = get_full_date_description(start_date)
    end_date_string_description = get_full_date_description(end_date)

    # Defina os estilos para diferentes partes do contrato
    styles = getSampleStyleSheet()
    style_title = styles['Title']
    style_paragraph = styles['Normal']
    estilo_assinatura = ParagraphStyle(
        'Assinatura',
        parent=style_paragraph,
        spaceAfter=30,
        alignment=0
    )

    test_style= ParagraphStyle(
        'Test',
        parent=style_paragraph,
        alignment=4
    )

   
    content = []


    title = Paragraph("CONTRATO DE LOCAÇÃO", style_title)
    content.append(title)

    #owner_name = 'Laurindo Figueiredo Moreira'
    #client_name = 'Fernando Leite Da Silva'

    #RUA SEBASTIÃO DA ROCHA PITA, Nº 168, CASA 2 – VILA NINA - SÃO PAULO – SP
    paragraphs = [ 
        f'<b>{owner.nome.upper()}, (CPF) {owner_cpf},</b> Cédula de identidade <b>{owner_rg}</b> doravante denominado <b>LOCADOR(A)</b>',
        f'<b>{renter.nome.upper()} (CPF) {renter_cpf}</b>, Cédula de identidade <b>{renter_rg}</b> doravante denominado <b>LOCATÁRIO(A)</b>',
        'Celebram o presente contrato de locação residencial, com as cláusulas e condições seguintes:',
        f'O <b>LOCADOR</b> cede para locação residencial ao <b>LOCATÁRIO</b>, um salão comercial, na <b>{address}</b>. A locação destina-se ao uso exclusivo como residência e domicílio do <b>LOCATÁRIO</b>.',
        f'O prazo de locação é de <b>02 (dois) anos</b>, iniciando-se em <b>{start_date_string_description}</b> e terminando em <b>{end_date_string_description}</b>, limite de tempo em que o imóvel objeto do presente deverá ser restituído independentemente de qualquer notificação ou interpelação sob pena de caracterizar infração contratual.',
        'O aluguel mensal será de <b>R$ 600,00 (Seiscentos reais)</b> e deverá ser pago até a data de seu vencimento, todo dia <b>30 de cada mês</b> do mês seguinte ao vencido, no local do endereço do <b>LOCADOR</b> ou outro que o mesmo venha a designar.',
        '<b>Obs. (foi dado um mês de depósito)</b>',
        'A impontualidade acarretará juros moratórios na base de 1% (um por cento) ao mês calculado sobre o valor do aluguel. O atraso superior a 30 (trinta) dias implicará em correção monetária do valor do aluguel e encargos de cobrança correspondentes a 10% (dez por cento) do valor assim corrigido.'
        'O pagamento de qualquer dos aluguéis não implica em renúncia do direito de cobrança de eventuais diferenças de aluguéis, de encargos ou impostos que oportunamente não tiverem sidos lançados nos respectivos recibos.',
        'O aluguel será reajustado anualmente pela variação do <b>ÍNDICE</b> (exemplo: IGP-M, INPC-IBGE, etc.). Entretanto, se em virtude de lei subsequente vier a ser admitida a correção e periodicidade inferior a prevista na legislação vigente à época de sua celebração, que é anual, concordam as partes desde já e em caráter irrevogável que a correção do aluguel e o seu indexador passará automaticamente a ser feito no menor prazo que for permitido pela lei posterior e pelo maior índice vigente dentre os permitidos pelo Governo Federal e que venha a refletir a variação do período.',
        'Havendo prorrogação tácita ou expressa do presente contrato o mesmo será reajustado a preço de mercado sem qualquer relação com o patamar aqui pactuado a ser estabelecido pelo <b>LOCADOR</b>, que poderá ainda estipular, de comum acordo com o <b>LOCATÁRIO</b>, o índice de reajuste e periodicidade.',
        'Nas cobranças judiciais e extrajudiciais de alugueis em atraso os mesmos serão acrescidos de juros de mora, atualização monetária e honorários advocatícios, na base de 20% ( vinte por cento ) sendo que qualquer recebimento feitos pela <b>LOCADOR</b> fora dos prazos e condições convencionais neste contrato, será havido como mera tolerância e não induzirá novação bem como resgate de recibos posteriores não significará quitação de aluguéis e outras obrigações contratuais deixadas de quitar nas épocas certas.',
        'O imóvel da presente locação destina-se ao uso exclusivo como residência e domicilio do <b>LOCATÁRIO</b>, conforme cláusula 2, não sendo permitida a transferência, sublocação, cessão ou empréstimo no todo ou em parte, sem a prévia e expressa autorização do <b>LOCADOR</b>.',
        'Além do aluguel são de responsabilidade do <b>LOCATÁRIO</b> as despesas com consumo de luz, água, esgoto, seguro contra incêndio, imposto predial e todas as demais taxas ou impostos, tributos municipais e encargos da locação, que venham a incidir sobre o imóvel, inclusive taxa de condomínio, que deverão ser pagas diretamente pela mesma, o qual ficará obrigada a apresentar os comprovantes de quitação juntamente com o pagamento do aluguel.',
        'O <b>LOCATÁRIO</b> declara neste ato tomar conhecimento da existência de regras estabelecidas na <b>CONVENÇÃO DE CONDOMÍNIOS</b> e compromete-se a respeitá-las e cumpri-las, juntamente com seus familiares e prepostos, sob pena de rescisão contratual.',
        'Encerrada a locação a entrega das chaves só será processada mediante exibição ao <b>LOCADOR</b>, dos comprovantes de quitação das despesas e encargos da locação referidos nas cláusulas anteriores, inclusive corte final de luz.',
        'Fica facultado ao <b>LOCADOR</b> ou ao seu representante legal vistoriar o imóvel sempre que julgar necessário.',
        'O <b>LOCATÁRIO</b> se obriga, sob pena de cometer infração contratual, a comunicar por escrito ao <b>LOCADOR</b>, com antecipação mínima de 30 (trinta) dias, a sua intenção de devolver o imóvel antes do prazo aqui previsto.',
        'O <b>LOCATÁRIO</b> assume o compromisso de solicitar ao <b>LOCADOR</b> uma vistoria 30 (trinta) dias antes de desocupar o imóvel para ser constatado o estado de conservação do mesmo.',
        'Quaisquer modificações no imóvel locadas só poderão ser feitas com expressa autorização do <b>LOCADOR</b>. Aderem ao mesmo as benfeitorias sejam elas úteis, necessárias ou voluntárias independentes de sua natureza, não cabendo direito de indenização, retenção, compensação ou reembolso.',
        'Fica convencionado que a parte que infringir o presente contrato em qualquer dos seus termos, se sujeita ao pagamento em benefício da outra, da multa contratual correspondente a 1 (uma) vez o valor do aluguel vigente à época da infração, tantas vezes forem as infrações praticadas, sem prejuízo da resolução contratual e demais comunicações previstas neste instrumento.',
        'Se o <b>LOCATÁRIO</b> vier a usar da faculdade que lhe confere o contido no artigo 4º da Lei n º 8.245/1991 e devolver o imóvel antes do vencimento do prazo ajustado, pagará a multa compensatória equivalente a 02 (duas) vezes o valor do aluguel vigente, reduzido proporcionalmente ao tempo do contrato já cumprido.',
        'Permanecendo o <b>LOCATÁRIO</b> no imóvel após o prazo de desocupação voluntária nos casos de denúncia condicionada, pagará ele o aluguel pena que vier a ser arbitrado na notificação premonitória na forma de que dispõe o artigo 575 do Novo Código Civil Brasileiro, o mesmo ocorrendo no caso de mútuo acordo nos termos do artigo 9, inciso I da Lei n º 8.245/1991, quando a desocupação não se verificar na data convencionada.',
        'No caso do imóvel ser posto à venda, o <b>LOCATÁRIO</b> declara que não possui interesse em sua aquisição, renunciando expressamente ao eventual direito de preferência e autoriza desde já, a visita de interessados, em horários previamente convencionados.',
        'O <b>LOCATÁRIO</b> declara, para todos os fins e efeitos de direito, que recebe o imóvel locado em condições plenas de uso, em perfeito estado de conservação, higiene e limpeza, obrigando-se e comprometendo-se a devolvê-lo em iguais condições, independentemente de qualquer aviso ou notificação prévia, e qualquer que seja o motivo da devolução, sob pena de incorrer nas cominações previstas neste contrato ou estipuladas em lei, além da obrigação de indenizar por danos ou prejuízos decorrentes da inobservância desta obrigação, salvo as deteriorações decorrentes de uso normal do imóvel.',
        'Elegem as partes o foro do domicílio do <b>LOCADOR</b>, para dirimir quaisquer dúvidas oriundas do presente contrato, renunciando a qualquer outro por mais privilegiado que seja.',
        f'<b>São Paulo, {get_full_date_description(today=True)}</b>'
    

        ]
    
    for paragraphText in paragraphs:
        content.append(Paragraph(paragraphText, test_style))
        
   
    content.append(Spacer(height=0.5*inch, width=0.5*inch))

    #assinatura = Paragraph("______________________", estilo_assinatura)

    data = [
        ["LOCATÁRIO", "LOCADOR"],
        ["______________________", "______________________"],
        [owner.nome, renter.nome],
        ["Data", "Data"]
    ]

    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        #('BACKGROUND', (0, 0), (-1, 0), '#DDDDDD'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        #('BACKGROUND', (0, 1), (-1, -1), '#EEEEEE'),
        ('TEXTCOLOR', (0, 1), (-1, -1), '#000000'),
        ('LEFTPADDING', (1, 0), (1, -1), 140),
    ])


    table = Table(data)
    table.setStyle(style)
    
    content.append(table)
    


    # Gera o documento PDF
    doc.build(content)



