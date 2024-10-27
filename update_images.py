import json
import os
from generate_id import app, db, IDS  # Importe app et db correctement depuis generate_id.py

# URL de base pour les images sur un stockage accessible (exemple)
BASE_IMAGE_URL = '/Users/edouard/DATA_ID/static/images'  # Remplace par le chemin réel

# Fonction pour associer les images aux entrées de la base de données
def update_image_urls():
    # 1. Mise à jour pour les conseils
    conseils = IDS.query.filter_by(section='Conseils').all()
    for item in conseils:
        data = json.loads(item.data)
        image_name = data.get("mapping_images")
        if image_name:
            image_path = find_image_path(image_name)
            if image_path:
                data['image_url'] = image_path
                item.data = json.dumps(data)

    # 2. Mise à jour pour les plantes
    plantes = IDS.query.filter_by(section='Plantes').all()
    for item in plantes:
        data = json.loads(item.data)
        image_name = data.get("id_images")
        if image_name:
            image_path = find_image_path(image_name)
            if image_path:
                data['image_url'] = image_path
                item.data = json.dumps(data)

    # 3. Mise à jour pour les événements
    events = IDS.query.filter_by(section='Événements').all()
    for item in events:
        data = json.loads(item.data)
        image_name = data.get("id_images")
        if image_name:
            image_path = find_image_path(image_name)
            if image_path:
                data['image_url'] = image_path
                item.data = json.dumps(data)

    # 4. Mise à jour pour les maladies (plusieurs images possibles)
    maladies = IDS.query.filter_by(section='Maladies').all()
    for item in maladies:
        data = json.loads(item.data)
        image_names = data.get("images", [])
        image_urls = [find_image_path(name) for name in image_names if find_image_path(name)]
        if image_urls:
            data['image_url'] = image_urls
            item.data = json.dumps(data)

    # 5. Mise à jour pour les lieux
    lieux = IDS.query.filter_by(section='Lieux').all()
    for item in lieux:
        data = json.loads(item.data)
        image_name = data.get("imageName")
        if image_name:
            image_path = find_image_path(image_name)
            if image_path:
                data['image_url'] = image_path
                item.data = json.dumps(data)

    # Sauvegarder toutes les mises à jour dans la base de données
    db.session.commit()

# Fonction pour construire le chemin de l'image
def find_image_path(image_name):
    extensions = ['.jpeg', '.jpg', '.png']
    for ext in extensions:
        # Construire l'URL complète de l'image
        image_path = f"{BASE_IMAGE_URL}/{image_name}{ext}"
        if os.path.exists(os.path.join('/Users/edouard/DATA_ID/static/images', f"{image_name}{ext}")):
            return image_path
    return None

# Exécuter la mise à jour
with app.app_context():  # Utiliser app.app_context() correctement ici
    update_image_urls()
    print("Champs image_url mis à jour avec succès.")
