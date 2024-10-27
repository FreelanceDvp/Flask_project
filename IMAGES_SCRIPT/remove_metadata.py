import os
from PIL import Image

def remove_metadata_from_images(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                # Ouvrir l'image
                image = Image.open(file_path)
                
                # Supprimer les métadonnées en copiant l'image sans info
                data = list(image.getdata())
                new_image = Image.new(image.mode, image.size)
                new_image.putdata(data)
                
                # Sauvegarder l'image sans métadonnées
                new_image.save(file_path)
                print(f"Metadonnées supprimées pour : {filename}")
            except Exception as e:
                print(f"Erreur avec l'image {filename}: {e}")

# Utiliser le script
remove_metadata_from_images('/Users/edouard/DATA_ID/static/images')