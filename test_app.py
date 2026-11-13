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


def test_soma(client):
    resposta = client.get('/api/soma?a=10&b=5')
    assert resposta.status_code == 200
    assert resposta.get_json()['resultado'] == 15


def test_soma_parametro_invalido(client):
    resposta = client.get('/api/soma?a=abc&b=5')
    assert resposta.status_code == 400


# ---------- Feature Flag: FEATURE_DESCONTO_PROMO ----------

# Teste 1: com a flag desativada, a rota retorna 403
def test_desconto_desativado_por_padrao(client, monkeypatch):
    # Sem a variavel de ambiente, a flag fica DESLIGADA
    monkeypatch.delenv("FEATURE_DESCONTO_PROMO", raising=False)
    resposta = client.get('/api/desconto?valor=100&porcentagem=15')
    assert resposta.status_code == 403
    assert resposta.get_json()['flag_status'] is False


def test_desconto_desativado_explicito(client, monkeypatch):
    monkeypatch.setenv("FEATURE_DESCONTO_PROMO", "false")
    resposta = client.get('/api/desconto?valor=100&porcentagem=15')
    assert resposta.status_code == 403


# Teste 2: com a flag ativada, a rota funciona e retorna 200
def test_desconto_ativado(client, monkeypatch):
    monkeypatch.setenv("FEATURE_DESCONTO_PROMO", "true")
    resposta = client.get('/api/desconto?valor=100&porcentagem=15')
    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados['valor_final'] == 85.0


def test_desconto_porcentagem_padrao(client, monkeypatch):
    monkeypatch.setenv("FEATURE_DESCONTO_PROMO", "true")
    resposta = client.get('/api/desconto?valor=100')
    assert resposta.status_code == 200
    assert resposta.get_json()['valor_final'] == 90.0


def test_desconto_ativado_valor_invalido(client, monkeypatch):
    monkeypatch.setenv("FEATURE_DESCONTO_PROMO", "true")
    resposta = client.get('/api/desconto?valor=abc')
    assert resposta.status_code == 400


def test_desconto_ativado_valor_negativo(client, monkeypatch):
    monkeypatch.setenv("FEATURE_DESCONTO_PROMO", "true")
    resposta = client.get('/api/desconto?valor=-5')
    assert resposta.status_code == 400


def test_status_mostra_estado_da_flag(client, monkeypatch):
    monkeypatch.setenv("FEATURE_DESCONTO_PROMO", "true")
    ligada = client.get('/api/status').get_json()
    assert ligada['flags']['desconto_promo'] is True

    monkeypatch.setenv("FEATURE_DESCONTO_PROMO", "false")
    desligada = client.get('/api/status').get_json()
    assert desligada['flags']['desconto_promo'] is False