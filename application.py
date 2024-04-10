from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, select, update, delete
from sqlalchemy.orm import relationship, sessionmaker, Session, mapped_column, declarative_base
from sqlalchemy import create_engine
import os, dotenv, requests, datetime, json, math, subprocess, re, glob

dotenv.load_dotenv()
BDD_URL=os.getenv('DATABASE_URL')

# Connection à la BDD
engine = create_engine(BDD_URL) # , echo=True
# classe de base dont no objets ORM vont dériver
Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id  = Column(Integer, primary_key=True)
    name = Column(String)
    adr = Column(String)
    cat = Column(String)
    # 'factures' permet d'accéder aux factures (1..N) du clients
    facture_r = relationship("Facture", back_populates="client_r")
    def __str__(this):
        return f"CLIENT [{this.id}] {this.name} ({this.adr})"

class Facture(Base):
    __tablename__ = 'factures'
    no = Column(String, primary_key=True)
    dt = Column(DateTime)
    total = Column(Float)
    # client_id est la FK
    client_id = mapped_column(ForeignKey("clients.id"))
    # 'client' permet d'accéder au client lié à la facture
    client_r = relationship("Client", back_populates="facture_r")
    commander_r = relationship("Commandes", back_populates="facturation_r")
    def __str__(this):
        return f"factures [{this.id}] {this.name} ({this.adr})"
    
class Commandes (Base):
    __tablename__ = 'commande'
    facture_no  = Column(String, ForeignKey ("factures.no") ,primary_key=True)
    produit_name = Column(String, ForeignKey ("produits.name") , primary_key=True)
    idx = Column(Integer)
    qty = Column(Integer)
    produits_r = relationship("Produit", back_populates="commande_r")
    facturation_r = relationship("Facture", back_populates="commander_r")
    def __str__(this):
        return f"commandes [{this.id}] {this.name} ({this.adr})"

class Produit (Base):
    __tablename__ = 'produits'
    name  = Column(String, primary_key=True)
    price = Column(Integer)
    commande_r = relationship("Commandes", back_populates="produits_r")
    def __str__(this):
        return f"produit [{this.id}] {this.name} ({this.adr})"
    
# ------------------------------------------------------------

# Cette commande crée dans la BDD les tables correspondantes
Base.metadata.create_all(bind=engine)


if __name__=="__main__":
    print('DATABASE_URL=', BDD_URL)
    with Session(engine) as session:
        #query=delete(Facture)
        #session.execute(query)
        #query=delete(Client)
        #session.execute(query)
        #session.commit() pour effacer les clients et les factures qui sont déjà dans la BDD.


        client = Client(id=1, name="Essai", adr="Ici")
        print(client)
        session.add(client)
        session.commit()
        

        query=select(Client).where(Client.id==1)
        print(query)
        client = session.execute(query).scalar()
        print(client)

        fac=Facture(no="FAC_2024-0000", total=0.0)
        fac.client_r=client
        session.add(fac)
        session.commit()

        query=select(Client)
        clients = session.execute(query).all()
        print(clients)
        for row in clients:
            client=row[0]
            print(client, client.facture_r)

    





# dans bash rm ocr.SQLite
