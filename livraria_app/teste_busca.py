from busca import buscar_livros, listar_unidades_disponiveis, obter_estoque, consultar_estoque_por_unidade

def teste_busca_por_titulo():
    resultado = buscar_livros('Harry') # busca por título
    assert len(resultado) > 0
    encontrou = False
    for livro in resultado:
        if "Harry Potter" in livro["titulo"]:
                encontrou = True
    assert encontrou == True

def teste_busca_por_autor():
    resultado = buscar_livros('Rowling')
    assert len(resultado) > 0
    encontrou = False
    for livro in resultado:
        if "Rowling" in livro["autor"]:
            encontrou = True
    assert encontrou == True

def teste_busca_por_editora():
    resultado = buscar_livros('Rocco')
    assert len(resultado) > 0
    encontrou = False
    for livro in resultado:
        if "Rocco" in livro["editora"]:
            encontrou = True
    assert encontrou == True

def teste_busca_sem_resultados():
    resultado = buscar_livros('livroQueNaoExiste')
    assert len(resultado) == 0

def teste_busca_vazia():
    resultado = buscar_livros("")
    assert resultado == "erro"

def teste_disponibilidade():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    estoque = livro["estoque"]
    for loja, quantidade in estoque.items():
        assert isinstance(quantidade, int)
        assert quantidade >= 0

def teste_quantidade_por_unidade():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    estoque = obter_estoque(livro)
    assert len(estoque) > 0
    for nome_loja, quantidade_disponivel in estoque.items():
        assert isinstance(quantidade_disponivel, int)
        assert quantidade_disponivel >= 0

def teste_filtrar_unidades_disponiveis():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    unidades = listar_unidades_disponiveis(livro)
    for loja in unidades:
        quantidade = livro["estoque"][loja] # Pega a quantidade de exemplares da loja específica
        assert quantidade > 0

def teste_unidades_ordenadas_por_estoque():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    unidades = listar_unidades_disponiveis(livro)
    quantidades = []
    for loja in unidades:
        quantidade = livro["estoque"][loja]
        quantidades.append(quantidade)
    for i in range(len(quantidades) - 1):
        assert quantidades[i] >= quantidades[i + 1] # garantindo que a lista esteja ordenada

def teste_filtrar_por_unidade():
    resultado = buscar_livros("Harry")
    livro = resultado[0]
    unidade_escolhida = 'Loja Centro' # bd mockado
    quantidade = consultar_estoque_por_unidade(livro, unidade_escolhida)
    assert isinstance(quantidade, int)
    assert quantidade > 0

teste_busca_por_titulo()
teste_busca_por_autor()
teste_busca_por_editora()
teste_busca_sem_resultados()
teste_busca_vazia()
teste_disponibilidade()
teste_quantidade_por_unidade()
teste_filtrar_unidades_disponiveis()
teste_unidades_ordenadas_por_estoque()
teste_filtrar_por_unidade()