import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import json
import tempfile
import random
import string
import math

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration de la base de données en utilisant SQLAlchemy avec PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Créez les tables dans la base de données si elles n'existent pas encore
with app.app_context():
    db.create_all()

# Définissez vos modèles ici (exemple de modèle)
class IDS(db.Model):
    __tablename__ = 'ids'
    id = db.Column(db.String, primary_key=True)
    section = db.Column(db.String)
    data = db.Column(db.Text)

# Créer les tables si elles n'existent pas
with app.app_context():
    db.create_all()

# Route pour la page d'accueil avec tri, filtrage et pagination
@app.route('/')
def index():
    section = request.args.get('section', '')
    search = request.args.get('search', '').strip()
    sort_column = request.args.get('sort')
    sort_order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))
    items_per_page = 10

    query = ID.query

    # Filtrage par section si spécifié
    if section and section != "Toutes":
        query = query.filter_by(section=section)
    
    # Recherche dans les données
    if search:
        query = query.filter(ID.data.like(f"%{search}%"))

    # Tri
    if sort_column:
        if sort_order == 'asc':
            query = query.order_by(db.text(f"json_extract(data, '$.{sort_column}') ASC"))
        else:
            query = query.order_by(db.text(f"json_extract(data, '$.{sort_column}') DESC"))

    # Pagination
    total_items = query.count()
    total_pages = math.ceil(total_items / items_per_page)
    ids = query.offset((page - 1) * items_per_page).limit(items_per_page).all()

    # Conversion des données JSON pour l'affichage
    ids_data = []
    for item in ids:
        data_dict = json.loads(item.data)
        data_dict.update({"id": item.id, "section": item.section})
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

    items = ID.query.filter_by(section=section).all()
    export_data = [{"id": item.id, **json.loads(item.data)} for item in items]

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

        new_item = ID(id=new_id, section=section, data=json.dumps(data))
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template("add.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
