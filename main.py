from nonogram_solver import add_clausulas, get_id
from testes import SETTINGS


# Descomente o teste que deseja executar

# nome_do_desenho = "mario" 
# nome_do_desenho = "hollow_knight" 
# nome_do_desenho = "heart" 
# nome_do_desenho = "creeper" 
nome_do_desenho = "golfinho"

configuracao = SETTINGS[nome_do_desenho]
num_linhas = configuracao["size"]["row"]
num_colunas = configuracao["size"]["column"]
regras_linhas = configuracao["rules"]["rows"]
regras_colunas = configuracao["rules"]["columns"]

solver = add_clausulas(num_linhas, num_colunas, regras_linhas, regras_colunas)

if solver.solve():
    modelo = solver.get_model()

    grid = []
    for r in range(num_linhas):
        linha_visual = ""
        for c in range(num_colunas):
            cell_id = get_id(r, c, num_colunas)

            if cell_id in modelo:
                linha_visual += "■ "
            else:
                linha_visual += ". "

        print(linha_visual)
else:
    print("Sem solução possível")