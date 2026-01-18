import tkinter

def tela_nonogram(matriz_resolvida, titulo):
    """
    Cria uma janela e desenha o nonograma baseado na matriz
    0 = Branco, 1 = Preto
    """
    TAMANHO_CELULA = 20  
    
    janela = tkinter.Tk()
    janela.title(titulo)
    
    linhas = len(matriz_resolvida)
    colunas = len(matriz_resolvida[0])
    largura_tela = colunas * TAMANHO_CELULA
    altura_tela = linhas * TAMANHO_CELULA
    
    canvas = tkinter.Canvas(janela, width=largura_tela, height=altura_tela)
    canvas.pack()

    for r in range(linhas):
        for c in range(colunas):
            valor = matriz_resolvida[r][c]
            
            x1 = c * TAMANHO_CELULA
            y1 = r * TAMANHO_CELULA
            x2 = x1 + TAMANHO_CELULA
            y2 = y1 + TAMANHO_CELULA

            cor = "black" if valor == 1 else "white"

            canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="gray")

    janela.mainloop()