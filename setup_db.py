import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("ids_database.db")
cursor = conn.cursor()

# Création de la table pour stocker les IDs et les données en format JSON
cursor.execute("DROP TABLE IF EXISTS ids")
cursor.execute("""
    CREATE TABLE ids (
        id TEXT PRIMARY KEY,
        section TEXT,
        data TEXT
    )
""")
conn.commit()
conn.close()
print("Base de données initialisée avec une table flexible.")
