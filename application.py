from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, select, update, delete
from sqlalchemy.orm import relationship, sessionmaker, Session, mapped_column, declarative_base
from sqlalchemy import create_engine
import os, dotenv, requests, datetime, json, math, subprocess, re, glob
from datetime import datetime

dotenv.load_dotenv()
BDD_URL=os.getenv('DATABASE_URL')

# Connection à la BDD
engine = create_engine(BDD_URL, echo=True)
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
        
    def read_file(no):
        '''Méthode pour lire les fichiers et créer des objets Facture'''
        with Session(engine) as session:  # Création d'une session de base de données
            query = select(Facture).where(Facture.no==no)  # Construction de la requête SQL pour récupérer une Facture
            res = session.execute(query).scalar()  # Exécution de la requête et récupération du résultat
            if not res:  # Si aucune Facture n'existe avec le numéro spécifié
                #fac = Facture(no=no, total=0.0)  # Création d'un objet Facture avec un total initial de 0
                with open(f"static/{no}.pngqr.txt", "r") as qrcode:  # Ouverture du fichier contenant le code QR
                    contenuqrcode = qrcode.read()  # Lecture du contenu du fichier
                    contenuqrcode = contenuqrcode.split("\n")  # Séparation par les sauts de ligne
                    contenuqrcode.remove("")  # Suppression des lignes vides
                    print(contenuqrcode)  # Affichage du contenu du code QR
                    id =int(contenuqrcode[2])
                    cat =contenuqrcode[3]
                with open(f"static/{no}.png.txt", "r") as facture:  # Ouverture du fichier contenant les détails de la facture
                    contenufacture = facture.read()  # Lecture du contenu du fichier
                    contenufacture = contenufacture.split("\n")  # Séparation par les sauts de ligne
                    contenufacture.remove("")  # Suppression des lignes vides
                    print(contenufacture)  # Affichage du contenu de la facture
                    total = float(contenufacture[-2].split(" ")[1])  # Extraction du total et conversion en float
                    print(total)
                    dt = datetime.strptime(contenufacture[1].split("date ")[1], "%Y-%m-%d %H:%M:%S")  # Extraction de la date et conversion en datetime
                    print(dt)
                    name=contenufacture[2]
                fac = Facture(no=no, total=total, dt=dt)  # Création de l'objet Facture avec les détails extraits
                session.add(fac)  # Ajout de la Facture à la session
                session.commit()  # Validation des changements dans la base de données
            else :
                print (f"La facture {no} existe déjà")
            #return fac  # Retour de l'objet Facture, créé à partir des informations des fichiers TXT


    
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

# Exemple : 
# if __name__=="__main__":
#     print('DATABASE_URL=', BDD_URL)
#     with Session(engine) as session:
#         #query=delete(Facture)
#         #session.execute(query)
#         #query=delete(Client)
#         #session.execute(query)
#         #session.commit() pour effacer les clients et les factures qui sont déjà dans la BDD.

#         client = Client(id=1, name="Essai", adr="Ici")
#         print(client)
#         session.add(client)
#         session.commit()
        
#         query=select(Client).where(Client.id==1)
#         print(query)
#         client = session.execute(query).scalar()
#         print(client)

#         fac=Facture(no="FAC_2024-0000", total=0.0)
#         fac.client_r=client
#         session.add(fac)
#         session.commit()

#         query=select(Client)
#         clients = session.execute(query).all()
#         print(clients)
#         for row in clients:
#             client=row[0]
#             print(client, client.facture_r)



Facture.read_file("FAC_2019_0002-521208")




# dans bash rm ocr.SQLite
