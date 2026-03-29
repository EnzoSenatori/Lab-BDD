from flask import Flask, render_template, request, jsonify
from livraria_app.busca import buscar_livros, listar_unidades_disponiveis, realizar_reserva

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    termo = request.form.get('termo', '')
    resultados = buscar_livros(termo)
    if isinstance(resultados, str):
        return render_template('index.html', erro=resultados)
    return render_template('index.html', livros=resultados, termo=termo)

@app.route('/unidades/<int:livro_id>')
def unidades(livro_id):
    # Simulando o objeto livro para a função que você já tem
    livro_fake = {'id': livro_id}
    lista_unidades = listar_unidades_disponiveis(livro_fake)
    return jsonify(lista_unidades)

@app.route('/reservar', methods=['POST'])
def reservar():
    dados = request.json
    reserva = realizar_reserva(dados['livro_id'], dados['unidade'])
    return jsonify(reserva)

if __name__ == '__main__':
    app.run(debug=True)