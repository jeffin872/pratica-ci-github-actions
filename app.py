from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"mensagem": "Bem-vindo a API FastOrder!"})


@app.route('/api/status')
def status():
    return jsonify({"status": "operacional", "servico": "FastOrder-Web"})


# Missao 5.1 - Rota /api/soma
# Recebe dois parametros via Query String (?a=2&b=3)
# e retorna um JSON no formato {"resultado": 5}
@app.route('/api/soma')
def soma():
    # Os parametros da URL chegam sempre como String,
    # entao precisamos converter para numero.
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return jsonify({
            "erro": "Informe os parametros numericos a e b. Ex: ?a=2&b=3"
        }), 400

    resultado = a + b

    # Se o resultado for inteiro (ex: 15.0), devolve 15
    if resultado.is_integer():
        resultado = int(resultado)

    return jsonify({"resultado": resultado})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
