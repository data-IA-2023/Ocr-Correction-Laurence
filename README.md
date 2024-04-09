# Ocr-Correction-Laurence

OCR_API : Clé Api

VISION_KEY : Clé vision
VISION_ENDPOINT: Clé vision
DATABASE_URL=sqlite:///ocr.sqlite 
DISCORD_OCR : Lien vers discord

# dans l'environnement :
pip install -r requirements.txt

# dans le fichier du projet :
Env/Scripts/activate

# dans l'environnement :
 uvicorn controller:app --port 3000 --host 0.0.0.0 --reload
 # Page internet :
 http://localhost:3000/

 # Docker :
docker build -t ocr-correction-laurence .
docker run -p 3000:3000 -e MYVAR=XXX --name ocr-correction-laurence ocr-correction-laurence

# pour supprimer le conteneur du docker :
docker rm ocr-correction-laurence
### aller sur le site, F5, puis revenir sous VSc pour voir la réponse

# Mettre docker image sous Azure : 
docker run -it ocr-correction-laurence
docker login conteneurlb.azurecr.io 
docker tag ocr-correction-laurence conteneurlb.azurecr.io/ocr-correction-laurence
docker push conteneurlb.azurecr.io/ocr-correction-laurence
# pour récupérer l image d azure : 
docker pull conteneurlb.azurecr.io/ocr-correction-laurence 
