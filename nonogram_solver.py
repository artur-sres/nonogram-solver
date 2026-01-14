from itertools import combinations
from pysat.solvers import Glucose4


def gerar_possibilidades(tamanho, regras):
    """
    Gera todas as combinações possíveis de preenchimento para uma linha ou coluna
    
    Args:
        tamanho_linha (int)
        regras (list)
        
    Returns:
        Uma lista de listas, onde cada lista interna é uma configuração válida
    """
    
    # Caso sem regras, nenhuma célula pintada
    if not regras or regras == [0]:
        return [[0] * tamanho]

    possibilidades = [] 
    num_espacos_pintados = sum(regras)
    num_blocos = len(regras)
    # espaços livres sçao todos os espaços de células não pintadas que não sejam obrigatórios
    num_espacos_livres = tamanho - num_espacos_pintados - (num_blocos - 1) 

    # Loop que vai gerar as combinações possíveis
    for p in combinations(range(num_blocos + num_espacos_livres), num_blocos):
        linha = []
        ultimo_index = -1

        # A cada iteração vai adicionar espaços em branco antes do bloco, na primeira iteração não adiciona
        for i, valor in enumerate(p):
            espacos = valor - ultimo_index - 1 

            # Adiciona um espaço em branco OBRIGATÓRIO caso seja após um bloco
            if i > 0:
                espacos += 1

            # Adiciona espaços vazios antes de um bloco e o bloco em si
            linha.extend([0] * espacos)  
            linha.extend([1] * regras[i]) 
            ultimo_index = valor

        # Adiciona espaços vazios restantes no final da linha
        linha.extend([0] * (tamanho - len(linha))) 
        possibilidades.append(linha)

    return possibilidades


def get_id(linha, coluna, total_colunas):
    """Retorna um ID único (int) para cada célula da matriz (1 a N)."""
    return (linha * total_colunas) + coluna + 1


def add_clausulas(num_linhas, num_colunas, regras_linhas, regras_colunas):
    """
    Constrói e preenche o solver com as cláusulas

    Passos:
    1. Gerar todas as possibilidades para cada linha/coluna
    2. Criar uma variável SAT para cada "escolha"
    3. Garantir que apenas UMA permutação seja escolhida por linha/coluna
    4. Garantir que a escolha seja compatível
    """
    
    total_celulas = num_linhas * num_colunas
    prox_ID_livre = total_celulas + 1

    solver = Glucose4()

    # Adicionar clausulas de possibilidades das linhas ao solver
    for r in range(num_linhas):
        regra_atual = regras_linhas[r + 1] 
        possibilidades = gerar_possibilidades(num_colunas, regra_atual)
        # Cada possibilidade tem um ID unico
        IDs_escolhas = [] 

        # Adiciona cada possibilidade da linha ao solver
        for p in possibilidades:
            id_escolha = prox_ID_livre
            prox_ID_livre += 1
            IDs_escolhas.append(id_escolha) 

            # Verifica se cada celula da linha esta pintada ou não e adiciona ao solver
            for c, val in enumerate(p):
                cell_id = get_id(r, c, num_colunas)

                if val == 1:
                    solver.add_clause([-id_escolha, cell_id]) # Celula pintada
                else:
                    solver.add_clause([-id_escolha, -cell_id]) # Celula vazia

        solver.add_clause(IDs_escolhas) # Adiciona os IDs atribuidos as possibilidades, garantindo que pelo menos uma seja escolhida

        # Garante que o solver não escolha mais que uma das possibilidades
        for i in range(len(IDs_escolhas)):
            for j in range(i + 1, len(IDs_escolhas)):
                solver.add_clause([-IDs_escolhas[i], -IDs_escolhas[j]])


    # Repete o mesmo processo que foi feito com as linhas, mas com as colunas
    for c in range(num_colunas):
        regra_atual = regras_colunas[c + 1]
        possibilidades = gerar_possibilidades(num_linhas, regra_atual)
        IDs_escolhas = []

        for p in possibilidades:
            id_escolha = prox_ID_livre
            prox_ID_livre += 1
            IDs_escolhas.append(id_escolha)

            for r, val in enumerate(p):
                cell_id = get_id(r, c, num_colunas)

                if val == 1:
                    solver.add_clause([-id_escolha, cell_id])
                else:
                    solver.add_clause([-id_escolha, -cell_id])

        solver.add_clause(IDs_escolhas)

        for i in range(len(IDs_escolhas)):
            for j in range(i + 1, len(IDs_escolhas)):
                solver.add_clause([-IDs_escolhas[i], -IDs_escolhas[j]])
                
    return solver