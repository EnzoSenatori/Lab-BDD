from __future__ import annotations

from pathlib import Path

from flask import Flask, request, send_from_directory

try:
    from .busca import (
        buscar_livros,
        listar_unidades_disponiveis,
        obter_estoque,
        realizar_reserva,
    )
    from .dados import livros
except ImportError:
    from busca import (  # type: ignore
        buscar_livros,
        listar_unidades_disponiveis,
        obter_estoque,
        realizar_reserva,
    )
    from dados import livros  # type: ignore

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = Flask(__name__)


def serializar_livro(livro: dict) -> dict:
    estoque = obter_estoque(livro)
    total_estoque = sum(estoque.values())
    unidades_disponiveis = listar_unidades_disponiveis(livro)

    if total_estoque == 0:
        badge = "Indisponível"
    elif total_estoque <= 2:
        badge = "Estoque limitado"
    else:
        badge = "Em estoque"

    return {
        "id": livro["id"],
        "titulo": livro["titulo"],
        "autor": livro["autor"],
        "editora": livro["editora"],
        "total_estoque": total_estoque,
        "badge": badge,
        "unidades_disponiveis": unidades_disponiveis,
    }


@app.get("/")
def index():
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.get("/styles.css")
def styles():
    return send_from_directory(str(FRONTEND_DIR), "styles.css")


@app.get("/app.js")
def script():
    return send_from_directory(str(FRONTEND_DIR), "app.js")


@app.get("/api/livros")
def api_livros():
    termo = request.args.get("termo", "").strip()

    if not termo:
        return {"error": "Digite um termo de busca."}, 400

    resultados = buscar_livros(termo)
    if resultados == "erro":
        return {"error": "Digite um termo de busca."}, 400

    return {
        "termo": termo,
        "total": len(resultados),
        "livros": [serializar_livro(livro) for livro in resultados],
    }


@app.get("/api/livros/<int:livro_id>/unidades")
def api_unidades(livro_id: int):
    livro = next((item for item in livros if item["id"] == livro_id), None)
    if livro is None:
        return {"error": "Livro não encontrado."}, 404

    estoque = obter_estoque(livro)
    unidades = [
        {
            "nome": loja,
            "quantidade": quantidade,
        }
        for loja, quantidade in sorted(
            estoque.items(), key=lambda item: item[1], reverse=True
        )
        if quantidade > 0
    ]

    return {
        "livro": serializar_livro(livro),
        "unidades": unidades,
    }


@app.post("/api/reservas")
def api_reservas():
    payload = request.get_json(silent=True) or {}

    livro_id = payload.get("livro_id")
    unidade = (payload.get("unidade") or "").strip()
    usuario = (payload.get("usuario") or "").strip() or None
    data = (payload.get("data") or "").strip() or None

    if livro_id is None or not unidade:
        return {"error": "Informe livro_id e unidade."}, 400

    try:
        livro_id = int(livro_id)
    except (TypeError, ValueError):
        return {"error": "livro_id inválido."}, 400

    livro = next((item for item in livros if item["id"] == livro_id), None)
    if livro is None:
        return {"error": "Livro não encontrado."}, 404

    estoque = obter_estoque(livro)
    if estoque.get(unidade, 0) <= 0:
        return {"error": "Unidade sem estoque disponível."}, 400

    reserva = realizar_reserva(livro, unidade, usuario=usuario, data=data)

    return {"reserva": reserva}, 201


if __name__ == "__main__":
    app.run(debug=True)