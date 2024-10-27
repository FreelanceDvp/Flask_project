import json
import os
import sqlite3

# Configuration des chemins
image_folder_path = '/Users/edouard/DATA_ID/static/images'  # Chemin vers le dossier contenant toutes les images
db_path = 'ids_database.db'  # Chemin vers la base de données SQLite

# Connexion à la base de données
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fonction pour associer les images aux entrées de la base de données
def update_image_urls():
    # 1. Mise à jour pour les conseils
    cursor.execute("SELECT id, data FROM ids WHERE section = 'Conseils'")
    conseils = cursor.fetchall()
    for id_, data_json in conseils:
        data = json.loads(data_json)
        image_name = data.get("mapping_images")
        if image_name:
            image_path = find_image_path(image_name)
            if image_path:
                data['image_url'] = image_path
                cursor.execute("UPDATE ids SET data = ? WHERE id = ?", (json.dumps(data), id_))
    
    # 2. Mise à jour pour les plantes
    cursor.execute("SELECT id, data FROM ids WHERE section = 'Plantes'")
    plantes = cursor.fetchall()
    for id_, data_json in plantes:
        data = json.loads(data_json)
        image_name = data.get("id_images")
        if image_name:
            image_path = find_image_path(image_name)
            if image_path:
                data['image_url'] = image_path
                cursor.execute("UPDATE ids SET data = ? WHERE id = ?", (json.dumps(data), id_))

    # 3. Mise à jour pour les événements
    cursor.execute("SELECT id, data FROM ids WHERE section = 'Événements'")
    events = cursor.fetchall()
    for id_, data_json in events:
        data = json.loads(data_json)
        image_name = data.get("id_images")
        if image_name:
            image_path = find_image_path(image_name)
            if image_path:
                data['image_url'] = image_path
                cursor.execute("UPDATE ids SET data = ? WHERE id = ?", (json.dumps(data), id_))

    # 4. Mise à jour pour les maladies (plusieurs images possibles)
    cursor.execute("SELECT id, data FROM ids WHERE section = 'Maladies'")
    maladies = cursor.fetchall()
    for id_, data_json in maladies:
        data = json.loads(data_json)
        image_names = data.get("images", [])
        image_urls = [find_image_path(name) for name in image_names if find_image_path(name)]
        if image_urls:
            data['image_url'] = image_urls  # On stocke une liste de chemins d'image
            cursor.execute("UPDATE ids SET data = ? WHERE id = ?", (json.dumps(data), id_))

    # 5. Mise à jour pour les lieux
    cursor.execute("SELECT id, data FROM ids WHERE section = 'Lieux'")
    lieux = cursor.fetchall()
    for id_, data_json in lieux:
        data = json.loads(data_json)
        image_name = data.get("imageName")
        if image_name:
            image_path = find_image_path(image_name)
            if image_path:
                data['image_url'] = image_path
                cursor.execute("UPDATE ids SET data = ? WHERE id = ?", (json.dumps(data), id_))

    # Sauvegarder toutes les mises à jour
    conn.commit()

# Fonction pour trouver le chemin de l'image dans le dossier d'images
def find_image_path(image_name):
    extensions = ['.jpeg', '.jpg', '.png']
    for ext in extensions:
        image_path = os.path.join('/static/images', f"{image_name}{ext}")
        if os.path.exists(os.path.join(image_folder_path, f"{image_name}{ext}")):
            return image_path
    return None

# Exécuter la mise à jour
update_image_urls()
conn.close()
print("Champs image_url mis à jour avec succès.")
