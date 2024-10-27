import sqlite3
import json

# Connexion à la base de données
conn = sqlite3.connect("ids_database.db")
cursor = conn.cursor()

# Fonction pour insérer les données dans la base
def insert_data(data, section, id_key):
    for item in data:
        id_value = item.get(id_key)
        data_json = json.dumps(item)  # Convertir tout l'objet en JSON brut
        cursor.execute("""
            INSERT OR REPLACE INTO ids (id, section, data) 
            VALUES (?, ?, ?)
        """, (id_value, section, data_json))
    conn.commit()

# Fonction pour importer les données
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

# Exécution de l'importation
import_all_data()
conn.close()
print("Données importées avec succès.")
