from dados import livros

def buscar_livros(termo_busca):
    resultados = []
    for livro in livros:
        if (termo_busca.lower() in livro["titulo"].lower()
            or termo_busca.lower() in livro["autor"].lower()
            or termo_busca.lower() in livro["editora"].lower()
        ):
            resultados.append(livro)
    return resultados