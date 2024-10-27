from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import json
import os
import tempfile
import random
import string
import math


DATABASE_FILE = "ids_database.db"


app = Flask(__name__)

# Route pour la page d'accueil avec tri, filtrage et pagination
@app.route('/')
def index():
    section = request.args.get('section', '')  # Par défaut, section est vide
    search = request.args.get('search', '').strip()
    sort_column = request.args.get('sort')
    sort_order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))
    items_per_page = 10  # Nombre d'éléments par page

    conn = sqlite3.connect("ids_database.db")
    cursor = conn.cursor()

    # Construire la requête SQL avec filtre et tri
    query = "SELECT id, section, data FROM ids WHERE 1=1"
    params = []

    # Appliquer le filtre section uniquement si une section est spécifiée et différente de "Toutes"
    if section and section != "Toutes":
        query += " AND section = ?"
        params.append(section)

    if search:
        query += " AND data LIKE ?"
        params.append(f"%{search}%")

    # Ajouter le tri si spécifié
    if sort_column:
        query += f" ORDER BY json_extract(data, '$.{sort_column}') {sort_order}"

    # Exécuter la requête pour obtenir le nombre total d'éléments
    cursor.execute(query, params)
    total_items = len(cursor.fetchall())
    total_pages = math.ceil(total_items / items_per_page)

    # Ajouter la pagination à la requête SQL
    offset = (page - 1) * items_per_page
    query += f" LIMIT {items_per_page} OFFSET {offset}"

    cursor.execute(query, params)
    ids = cursor.fetchall()
    conn.close()

    # Parse les données JSON pour chaque ligne récupérée
    ids_data = []
    for id, section, data in ids:
        data_dict = json.loads(data)  # Convertir les données JSON en dictionnaire
        data_dict.update({"id": id, "section": section})  # Ajouter l'ID et la section
        ids_data.append(data_dict)

    return render_template(
        "index.html",
        ids=ids_data,
        selected_section=section,
        sort_column=sort_column,
        sort_order=sort_order,
        current_page=page,
        total_pages=total_pages
    )

# Route pour l'export JSON d'une section
@app.route('/export/<section>', methods=['GET'])
def export_section(section):
    if not section:
        return "Veuillez spécifier une section à exporter", 400

    conn = sqlite3.connect("ids_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, data FROM ids WHERE section = ?", (section,))
    data = cursor.fetchall()
    conn.close()

    export_data = [{"id": row[0], **json.loads(row[1])} for row in data]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{section}_export.json", mode='w', encoding='utf-8') as temp_file:
        json.dump(export_data, temp_file, ensure_ascii=False, indent=4)
        temp_file_path = temp_file.name

    return send_file(temp_file_path, as_attachment=True, download_name=f"{section}_export.json", mimetype='application/json')

# Route pour ajouter un nouvel ID
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        section = request.form['section']
        data = {key: request.form[key] for key in request.form if key != 'section'}
        new_id = ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=3)) + ''.join(random.choices(string.ascii_uppercase, k=3))

        conn = sqlite3.connect("ids_database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ids (id, section, data) VALUES (?, ?, ?)", (new_id, section, json.dumps(data)))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template("add.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

