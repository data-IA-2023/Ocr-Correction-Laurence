print("start modele")
# Note : Appli « MVC » FastAPI 

import os
import dotenv
import pprint


dotenv.load_dotenv()
env_var = os. environ

print("------- Variable de l'environnement de Laurence ---------")
pprint.pprint(dict(env_var), width=1)
