from busca import buscar_livros
from dados import livros

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

teste_busca_por_titulo()
teste_busca_por_autor()
teste_busca_por_editora()
teste_busca_sem_resultados()
teste_busca_vazia()