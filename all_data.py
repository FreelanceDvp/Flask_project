import json
import random
import string
from generate_id import app, db, IDS  # Assure-toi que 'generate_id' est le nom correct de ton fichier principal Flask

# Configuration de la base de données PostgreSQL directement dans le script
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:iPFNYhFxLndfgavAPKYgfDcDwFifwknr@junction.proxy.rlwy.net:27748/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Fonction pour générer un identifiant unique au format ABC123DEF
def generate_unique_id():
    while True:
        # Générer l'ID au format 3 lettres - 3 chiffres - 3 lettres
        id_value = ''.join(random.choices(string.ascii_uppercase, k=3)) + \
                   ''.join(random.choices(string.digits, k=3)) + \
                   ''.join(random.choices(string.ascii_uppercase, k=3))
        
        # Vérifier si l'ID existe déjà dans la base de données
        if not db.session.get(IDS, id_value):
            return id_value  # Retourner cet ID uniquement s'il est unique

# Fonction pour insérer les données dans la base de données PostgreSQL via SQLAlchemy
def insert_data(data, section, id_key):
    for item in data:
        # Utiliser l'id donné ou générer un id unique si non fourni
        id_value = item.get(id_key) or generate_unique_id()
        data_json = json.dumps(item)  # Convertir l'objet en JSON brut

        # Vérifier l'existence et mettre à jour ou ajouter un nouvel enregistrement
        existing_item = db.session.get(IDS, id_value)
        if existing_item:
            existing_item.section = section
            existing_item.data = data_json
        else:
            new_item = IDS(id=id_value, section=section, data=data_json)
            db.session.add(new_item)

    # Committer tous les ajouts et les mises à jour
    db.session.commit()

# Fonction pour importer toutes les données
def import_all_data():
    # Import des plantes
    with open("/Users/edouard/Documents/PlantCreation/PlantCreation/mesplantes.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if isinstance(data, dict) and "plantes" in data:
            data = data["plantes"]
        insert_data(data, "Plantes", "id_plantes")

    # Import des maladies
    with open("/Users/edouard/Documents/PlantCreation/PlantCreation/maladies.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        insert_data(data, "Maladies", "id_maladie")

    # Import des conseils
    with open("/Users/edouard/Documents/PlantCreation/PlantCreation/conseilsPlanres2.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        insert_data(data, "Conseils", "id_conseils")

    # Import des événements
    with open("/Users/edouard/Documents/PlantCreation/PlantCreation/events.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if isinstance(data, dict) and "events" in data:
            data = data["events"]
        insert_data(data, "Événements", "id_event")

    # Import des lieux
    with open("/Users/edouard/Documents/PlantCreation/PlantCreation/MapLocation.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        insert_data(data, "Lieux", "id_lieux")

# Exécution de l'importation des données
with app.app_context():
    import_all_data()
    print("Données importées avec succès.")
