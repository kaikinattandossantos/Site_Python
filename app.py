from flask import Flask, request, jsonify, render_template
from fuzzywuzzy import process
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite chamadas do frontend

# Configuração do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Tema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

# Criar o banco de dados e adicionar temas iniciais
with app.app_context():
    db.create_all()
    
    if Tema.query.count() == 0:  # Evita duplicação
        for nome in temas:
            db.session.add(Tema(nome=nome))
        db.session.commit()

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Página de resultados (se necessário)
@app.route('/result')
def search_result():
    query = request.args.get('query', '')
    return render_template("result.html", query=query)

# Rota de busca de sugestões
@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify([])

    # Buscar todos os temas no banco de dados
    temas = [tema.nome for tema in Tema.query.all()]
    
    # Encontrar as melhores sugestões usando fuzzy matching
    resultados = process.extract(query, temas, limit=5)
    sugestoes = [resultado[0] for resultado in resultados if resultado[1] > 50]

    return jsonify(sugestoes)

if __name__ == '__main__':
    app.run(debug=True)
