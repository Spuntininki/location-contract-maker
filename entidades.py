from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime

# Cria uma instância do engine para o banco de dados SQLite


engine = create_engine('sqlite:///entities.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



class PersonManipulator:

    @staticmethod
    def create_person(person, nome, cpf, rg):
        person = person(nome=nome, cpf=cpf, rg=rg)
        session.add(person)
        session.commit()
        return person

    @staticmethod
    def get_person_by_id(person, id):
        person = session.query(person).get(id)
        return person

    @staticmethod
    def get_persons(person):
        person = session.query(person).all()
        return person
    
    @staticmethod
    def update_person(person, id, nome, cpf, rg):
        person = session.query(person).get(id)
        if person:
            person.nome = nome
            person.cpf = cpf
            person.rg = rg
            session.commit()
        return person

    @staticmethod
    def delete_person(person, id):
        person = session.query(person).get(id)
        if person:
            session.delete(person)
            session.commit()
        return person

class addressManipulator:


    @staticmethod
    def create_address(address_name, address_number, complement, neighborhood, city, state, cep):
        address = Address(Address_name=address_name, Address_number=address_number, complement=complement, \
                         neighborhood=neighborhood, city=city, state=state, cep=cep)
        session.add(address)
        session.commit()
        return address

    @staticmethod
    def get_address_by_id(id):
        address = session.query(Address).get(id)
        return address

    @staticmethod
    def get_all_address():
        address = session.query(Address).all()
        return address
    
    @staticmethod
    def update_address(id, address_name, address_number, complement, neighborhood, city, state):
        address = session.query(Address).get(id)
        if address:
            address.Address_name = address_name
            address.Address_number = address_number
            address.complement = complement
            address.neighborhood = neighborhood
            address.city  = city
            address.state = state
            session.commit()
        return address

    @staticmethod
    def delete_address(id):
        address = session.query(Address).get(id)
        if address:
            session.delete(address)
            session.commit()
        return address
    
    @staticmethod
    def get_full_address_string(address):
        return f'{address.Address_name}, Nº {address.Address_number}, {address.complement}, {address.neighborhood}, {address.city} - {address.state}'
    

class Owner(Base):
    __tablename__ = 'Owner'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    rg = Column(String)

class Renter(Base):
    __tablename__ = 'Renter'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    rg = Column(String)

class Address(Base):
    __tablename__ = 'Address'
    id = Column(Integer, primary_key=True)
    Address_name = Column(String)
    Address_number = Column(String)
    complement = Column(String)
    neighborhood = Column(String)
    city = Column(String)
    state = Column(String)
    cep = Column(String)

class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('Owner.id'))
    renter_id = Column(Integer, ForeignKey('Renter.id'))
    address_id = Column(Integer, ForeignKey('Address.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    created_date = Column(DateTime)

    # Define a relação com as tabelas Renter e Address
    owner = relationship('Owner', back_populates='contracts')
    renter = relationship('Renter', back_populates='contracts')
    address = relationship('Address', back_populates='contracts')    
    


    


Base.metadata.create_all(engine)
#print(addressManipulator().get_full_address_string(addressManipulator().create_address(address_name='Rua Osman da costa Pino', address_number=44, complement='casa 2', neighborhood='Jardim Carumbé', city='São Paulo', state='SP')))
#print(PersonManipulator.create_person(Renter, nome='Billy', cpf='123', rg='123'))
#addressManipulator().create_address(address_name='Rua Sebastião da Rocha pita', address_number=168, complement='casa 7', neighborhood='Vila nina', city='São Paulo', state='SP')
#PersonManipulator.create_person(Owner, nome='Laurindo Figueiredo Moreira', cpf='25142887549', rg='174227917')