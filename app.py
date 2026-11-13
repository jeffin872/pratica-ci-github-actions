import os

from flask import Flask, jsonify, request

app = Flask(__name__)


def feature_desconto_ativa():
    """Feature Flag controlada por variavel de ambiente.

    Lida a CADA requisicao (e nao uma vez so na importacao), entao mudar
    FEATURE_DESCONTO_PROMO muda o comportamento sem alterar o codigo.
    """
    valor = os.getenv("FEATURE_DESCONTO_PROMO", "false")
    return valor.strip().lower() == "true"


@app.route('/')
def home():
    return jsonify({"mensagem": "Bem-vindo a API FastOrder!"})


@app.route('/api/status')
def status():
    return jsonify({
        "status": "operacional",
        "servico": "FastOrder-Web",
        "flags": {
            "desconto_promo": feature_desconto_ativa()
        }
    })


@app.route('/api/soma')
def soma():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return jsonify({
            "erro": "Informe os parametros numericos a e b. Ex: ?a=2&b=3"
        }), 400

    resultado = a + b
    if resultado.is_integer():
        resultado = int(resultado)
    return jsonify({"resultado": resultado})


# Nova Rota - Protegida pela Feature Flag
@app.route('/api/desconto')
def desconto():
    # Dark launch: a rota existe no container, mas so responde com a flag on
    if not feature_desconto_ativa():
        return jsonify({
            "erro": "Funcionalidade em construcao ou desativada "
                    "temporariamente",
            "flag_status": False
        }), 403

    try:
        valor_total = float(request.args.get('valor', 0))
        porcentagem = float(request.args.get('porcentagem', 10))

        if valor_total <= 0:
            return jsonify({"erro": "Valor deve ser maior que zero"}), 400

        valor_com_desconto = valor_total - (valor_total * (porcentagem / 100))
        return jsonify({
            "valor_original": valor_total,
            "desconto_aplicado": f"{porcentagem}%",
            "valor_final": valor_com_desconto
        })
    except (ValueError, TypeError):
        return jsonify({"erro": "Parametros de desconto invalidos"}), 400


if __name__ == '__main__':
    # Host e debug vem do ambiente: nada de debug=True nem 0.0.0.0 fixos
    # no codigo (o Bandit acusa os dois). O Dockerfile define
    # FLASK_HOST=0.0.0.0.
        app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )   