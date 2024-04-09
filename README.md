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
