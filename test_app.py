import pytest
from app import app


# Cria um cliente de teste falso para nao precisarmos subir o servidor real
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_status_code(client):
    resposta = client.get('/')
    assert resposta.status_code == 200


def test_home_mensagem(client):
    resposta = client.get('/')
    dados = resposta.get_json()
    assert dados['mensagem'] == "Bem-vindo a API FastOrder!"


def test_status(client):
    resposta = client.get('/api/status')
    assert resposta.status_code == 200
    assert resposta.get_json()['status'] == "operacional"


# Missao 6.1 - Teste da rota /api/soma
def test_soma(client):
    resposta = client.get('/api/soma?a=10&b=5')
    assert resposta.status_code == 200
    assert resposta.get_json()['resultado'] == 15


def test_soma_decimais(client):
    resposta = client.get('/api/soma?a=1.5&b=2.5')
    assert resposta.status_code == 200
    assert resposta.get_json()['resultado'] == 4


def test_soma_parametro_invalido(client):
    resposta = client.get('/api/soma?a=abc&b=5')
    assert resposta.status_code == 400


def test_soma_parametro_ausente(client):
    resposta = client.get('/api/soma?a=5')
    assert resposta.status_code == 400
