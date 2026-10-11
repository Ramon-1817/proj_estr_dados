# GERA PASSOS DA ORDENAÇÃO

def gerar_passos_ordenacao(lista):

    vetor = lista.copy()

    comparacoes = 0
    deslocamentos = 0

    n = len(vetor)

    # ESTADIO INICIAL

    yield{
        "tipo": "inicio",
        "vetor": vetor.copy(),
        "comparacoes": comparacoes,
        "deslocamentos": deslocamentos,
        "i": None,
        "j": None,
        "chave": None,
        "buraco": None,
        "comparar_indice": None,
        "ordenado_ate": 0,
        "linha": None,
        "mensagem": "Iniciando Ordenação..."
}

# ORDENAÇÃO

    for i in range(1, n):

        chave = vetor[i]

        j = i - 1

        buraco = i

        # Mostra a seleção da chave

        yield {
            "tipo": "selecionar",
            "vetor": vetor.copy(),
            "comparacoes": comparacoes,
            "deslocamentos": deslocamentos,
            "i": i,
            "j": j,
            "chave": chave,
            "buraco": buraco,
            "comparar_indice": None,
            "ordenado_ate": i - 1,
            "linha": 2,
            "mensagem": f"Chave Selecionada: {chave}"
        }

        while j >= 0:

            comparacoes += 1

            resultado = vetor[j] > chave

            yield {
                "tipo": "comparar",
                "vetor": vetor.copy(),
                "comparacoes": comparacoes,
                "deslocamentos": deslocamentos,
                "i": i,
                "j": j,
                "chave": chave,
                "buraco": buraco,
                "comparar_indice": j,
                "ordenado_ate": i - 1,
                "linha": 4,
                "mensagem": f"Comparando: {vetor[j]} > {chave} -> {resultado}"
            }

            if vetor[j] > chave:

                numero_deslocado = vetor[j]

                vetor[j + 1] = vetor[j]

                deslocamentos += 1

                buraco = j

                yield {
                    "tipo": "deslocar",
                    "vetor": vetor.copy(),
                    "comparacoes": comparacoes,
                    "deslocamentos": deslocamentos,
                    "i": i,
                    "j": j,
                    "chave": chave,
                    "buraco": buraco,
                    "comparar_indice": j,
                    "ordenado_ate": i - 1,
                    "linha": 5,
                    "mensagem": f"Deslocando {numero_deslocado} para a direita"
                }

                j -= 1

            else:

                break

        # Insere a chave no espaço encontrado

        vetor[j + 1] = chave

        yield {
            "tipo": "inserir",
            "vetor": vetor.copy(),
            "comparacoes": comparacoes,
            "deslocamentos": deslocamentos,
            "i": i,
            "j": j + 1,
            "chave": chave,
            "buraco": None,
            "comparar_indice": None,
            "ordenado_ate": i,
            "linha": 7,
            "mensagem": f"Inserindo {chave} na posição {j + 1}"
        }

    yield {
        "tipo": "fim",
        "vetor": vetor.copy(),
        "comparacoes": comparacoes,
        "deslocamentos": deslocamentos,
        "i": None,
        "j": None,
        "chave": None,
        "buraco": None,
        "comparar_indice": None,
        "ordenado_ate": n - 1,
        "linha": None,
        "mensagem": "Ordenação Concluída!"
    }