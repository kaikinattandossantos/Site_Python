from flask import Flask, request, jsonify, render_template
from fuzzywuzzy import process
from sqlalchemy import create_engine

app = Flask(__name__)

# Conectar ao banco de dados
engine = create_engine('sqlite:///database.db')

# Simulação de temas no banco
temas = ["Python", "Java", "JavaScript", "Machine Learning", "Banco de Dados", "Inteligência Artificial"]

@app.route("/")
def index():
    return render_template("index.html")  # Renderiza o HTML


@app.route('/serching', methods=['GET'])
def search_suggestions():
    query = request.args.get('query', '').lower()

    # Buscar termos similares no banco
    suggestions = [tema for tema in temas if query in tema.lower()]

    # Correção automática
    if not suggestions:
        melhor_correcao = process.extractOne(query, temas)
        if melhor_correcao and melhor_correcao[1] > 80:  # Se for muito parecido
            suggestions.append(melhor_correcao[0])

    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
