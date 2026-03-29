from livraria_app.dados import livros, reservas

def buscar_livros(termo_busca):
    if termo_busca == "":
        return "erro"
    resultados = []
    for livro in livros:
        if (termo_busca.lower() in livro["titulo"].lower()
            or termo_busca.lower() in livro["autor"].lower()
            or termo_busca.lower() in livro["editora"].lower()
        ):
            resultados.append(livro)
    return resultados

def listar_unidades_disponiveis(livro):
    unidades_disponiveis = []

    # Filtrar unidades com estoque > 0
    for loja, quantidade in livro["estoque"].items():
        if quantidade > 0:
            unidades_disponiveis.append((loja, quantidade))

    # Ordenar por quantidade (decrescente)
    unidades_disponiveis.sort(key=lambda item: item[1], reverse=True)

    # Retornar apenas os nomes das lojas
    resultado = []
    for loja, quantidade in unidades_disponiveis:
        resultado.append(loja)
    return resultado

def obter_estoque(livro):
    return livro['estoque']

def consultar_estoque_por_unidade(livro, unidade):
    estoque = obter_estoque(livro) # desenvolvida acima
    return estoque[unidade]

def realizar_reserva(livro, unidade, usuario=None, data=None): # Cria uma reserva do livro em uma unidade específica, registra na lista global e gera o QR Code mínimo.
    reserva = {
        'livro_id': livro['id'],
        'unidade': unidade,
        'status': 'reservado',
        'usuario': usuario, # impl. futuras
        'data': data
    }
    # Gera QR Code
    reserva['qr_code'] = gerar_qr_code(reserva)
    # Registra a reserva
    reservas.append(reserva)
    return reserva

def gerar_qr_code(reserva): # retorna uma string representando o QR Code mínimo da reserva. Não depedende de bibliotecas externas (bom para MVP)
    # RESERVA-{livro_id}-{unidade}
    qr_code = f"RESERVA-{reserva['livro_id']}-{reserva['unidade'].replace(' ', '').upper()}"
    return qr_code