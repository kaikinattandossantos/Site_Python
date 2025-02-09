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


@app.route('/result')
def search_result():
    query = request.args.get('query', '')
    return render_template("result.html", query=query)

if __name__ == '__main__':
    app.run(debug=True)
