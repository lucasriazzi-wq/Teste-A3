LIVRO = {
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "isbn": "9788535914849",
    "ano_publicacao": 1899,
    "quantidade_total": 2,
}


def criar_livro(client, **extra):
    r = client.post("/livros", json={**LIVRO, **extra})
    assert r.status_code == 201, r.text
    return r.json()


def criar_usuario(client, email="maria@email.com"):
    r = client.post("/usuarios", json={"nome": "Maria Silva", "email": email})
    assert r.status_code == 201, r.text
    return r.json()


# ---------------- livros ----------------
def test_cadastrar_e_buscar_livro(client):
    livro = criar_livro(client)
    assert livro["quantidade_disponivel"] == 2
    r = client.get(f"/livros/{livro['id']}")
    assert r.status_code == 200
    assert r.json()["titulo"] == "Dom Casmurro"


def test_buscar_por_titulo_e_autor(client):
    criar_livro(client)
    criar_livro(client, titulo="O Alienista", isbn="9788525406958", autor="Machado de Assis")
    criar_livro(client, titulo="Capitães da Areia", isbn="9788535914850", autor="Jorge Amado")

    assert len(client.get("/livros").json()) == 3
    assert len(client.get("/livros", params={"autor": "machado"}).json()) == 2
    por_titulo = client.get("/livros", params={"titulo": "alien"}).json()
    assert [l["titulo"] for l in por_titulo] == ["O Alienista"]


def test_livro_inexistente_retorna_404(client):
    assert client.get("/livros/999").status_code == 404
    assert client.put("/livros/999", json=LIVRO).status_code == 404
    assert client.delete("/livros/999").status_code == 404


def test_dados_invalidos_retornam_400(client):
    r = client.post("/livros", json={"titulo": "", "autor": "X"})
    assert r.status_code == 400
    assert r.json()["erro"] == "Dados inválidos."


def test_isbn_duplicado_retorna_400(client):
    criar_livro(client)
    assert client.post("/livros", json=LIVRO).status_code == 400


def test_atualizar_livro(client):
    livro = criar_livro(client)
    r = client.put(f"/livros/{livro['id']}", json={**LIVRO, "titulo": "Novo Título", "quantidade_total": 5})
    assert r.status_code == 200
    assert r.json()["titulo"] == "Novo Título"
    assert r.json()["quantidade_disponivel"] == 5


def test_remover_livro(client):
    livro = criar_livro(client)
    assert client.delete(f"/livros/{livro['id']}").status_code == 200
    assert client.get(f"/livros/{livro['id']}").status_code == 404


# ---------------- empréstimos ----------------
def test_fluxo_emprestimo_e_devolucao(client):
    livro = criar_livro(client, quantidade_total=1)
    usuario = criar_usuario(client)

    r = client.post("/emprestimos", json={"livro_id": livro["id"], "usuario_id": usuario["id"]})
    assert r.status_code == 201
    emprestimo = r.json()
    assert emprestimo["data_devolucao"] is None
    assert client.get(f"/livros/{livro['id']}").json()["quantidade_disponivel"] == 0

    # sem exemplares -> 400
    r = client.post("/emprestimos", json={"livro_id": livro["id"], "usuario_id": usuario["id"]})
    assert r.status_code == 400

    # livro com empréstimo em aberto não pode ser removido
    assert client.delete(f"/livros/{livro['id']}").status_code == 400

    r = client.put(f"/emprestimos/{emprestimo['id']}/devolucao")
    assert r.status_code == 200
    assert r.json()["data_devolucao"] is not None
    assert client.get(f"/livros/{livro['id']}").json()["quantidade_disponivel"] == 1

    # devolver duas vezes -> 400
    assert client.put(f"/emprestimos/{emprestimo['id']}/devolucao").status_code == 400


def test_emprestimo_com_livro_ou_usuario_inexistente(client):
    livro = criar_livro(client)
    usuario = criar_usuario(client)
    assert client.post("/emprestimos", json={"livro_id": 999, "usuario_id": usuario["id"]}).status_code == 404
    assert client.post("/emprestimos", json={"livro_id": livro["id"], "usuario_id": 999}).status_code == 404
    assert client.get("/emprestimos/999").status_code == 404
    assert client.put("/emprestimos/999/devolucao").status_code == 404


def test_listar_emprestimos_ativos(client):
    livro = criar_livro(client)
    usuario = criar_usuario(client)
    e1 = client.post("/emprestimos", json={"livro_id": livro["id"], "usuario_id": usuario["id"]}).json()
    client.post("/emprestimos", json={"livro_id": livro["id"], "usuario_id": usuario["id"]})
    client.put(f"/emprestimos/{e1['id']}/devolucao")
    assert len(client.get("/emprestimos").json()) == 2
    assert len(client.get("/emprestimos", params={"apenas_ativos": True}).json()) == 1


# ---------------- usuários ----------------
def test_email_duplicado_e_invalido(client):
    criar_usuario(client)
    assert client.post("/usuarios", json={"nome": "Outra", "email": "maria@email.com"}).status_code == 400
    assert client.post("/usuarios", json={"nome": "X", "email": "invalido"}).status_code == 400
    assert client.get("/usuarios/999").status_code == 404


# ---------------- erro 500 ----------------
def test_erro_interno_retorna_500(client):
    from app.main import app

    @app.get("/_teste-erro")
    def _erro():
        raise RuntimeError("falha simulada")

    r = client.get("/_teste-erro")
    assert r.status_code == 500
    assert r.json() == {"erro": "Erro interno do servidor."}
