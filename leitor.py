import cv2
import numpy as np

# Parâmetros
ARQUIVO_IMAGEM = 'cartao2.jpg'
NUM_QUESTOES = 50
NUM_ALTERNATIVAS = 5
GABARITO = [
    'B', 'A', 'D', 'A', 'E', 'B', 'C', 'D', 'A', 'B',
    'A', 'C', 'C', 'E', 'D', 'B', 'E', 'C', 'A', 'E',
    'D', 'E', 'E', 'A', 'C', 'C', 'D', 'B', 'D', 'D',
    'A', 'D', 'D', 'B', 'C', 'D', 'B', 'D', 'D', 'D',
    'D', 'E', 'C', 'A', 'D', 'B', 'C', 'A', 'D', 'E'
]
#alternativas
hori=68
horiSoma=38
vert = 69
VSoma =18
TC = 18
TC2 = 19
altB = vert+VSoma
altC = vert+VSoma*2
altD = vert+VSoma*3
altE = vert+VSoma*4
linhaSoma = 12+ vert + VSoma * 6
linhaSoma2=16+ vert + VSoma * 12
linhaSoma3 = 24+vert+VSoma*18
correcao = 3

# Carrega a imagem e converte para escala de cinza
imagem = cv2.imread(ARQUIVO_IMAGEM)

# Obter altura e largura da imagem
altura, largura = imagem.shape[:2]

inicio_corte = int(altura * 0.3)
imagem_cortada = imagem[inicio_corte:altura, 0:largura]
imagem_cinza = cv2.cvtColor(imagem_cortada, cv2.COLOR_BGR2GRAY)

# Aplica um filtro para suavizar a imagem
imagem_sem_ruido = cv2.bilateralFilter(imagem_cinza, 9, 75, 75)

# Aplica um threshold para binarizar a imagem
_, imagem_binaria = cv2.threshold(imagem_sem_ruido, 150, 255, cv2.THRESH_BINARY_INV)

# Lista de coordenadas para cada questão (exemplo para as primeiras 3 questões)
# [x, y, largura, altura] para cada alternativa de uma questão
questoes_coordenadas = [
    [[hori, vert, TC2, TC], [hori, altB,TC2,TC],
      [hori, altC,TC2,TC], [hori, altD,TC2,TC],
        [hori, altE,TC2,TC]],  # Questão 1
    [[hori+horiSoma, vert, TC, TC], [hori+horiSoma, altB,TC,TC],
      [hori+horiSoma, altC,TC,TC], [hori+horiSoma, altD,TC,TC],
        [hori+horiSoma, altE,TC,TC]],  # Questão 2
    [[hori+horiSoma*2, vert, TC, TC], [hori+horiSoma*2, altB,TC,TC],
      [hori+horiSoma*2, altC,TC,TC], [hori+horiSoma*2, altD,TC,TC],
        [hori+horiSoma*2, altE,TC,TC]],  # Questão 3
    [[hori+horiSoma*3, vert, TC, TC], [hori+horiSoma*3, altB,TC,TC],
      [hori+horiSoma*3, altC,TC,TC], [hori+horiSoma*3, altD,TC,TC],
        [hori+horiSoma*3, altE,TC,TC]],  # Questão 4
    [[hori+horiSoma*4, vert, TC, TC], [hori+horiSoma*4, altB,TC,TC],
      [hori+horiSoma*4, altC,TC,TC], [hori+horiSoma*4, altD,TC,TC],
        [hori+horiSoma*4, altE,TC,TC]],  # Questão 5
    [[hori+horiSoma*5, vert, TC, TC], [hori+horiSoma*5, altB,TC,TC],
      [hori+horiSoma*5, altC,TC,TC], [hori+horiSoma*5, altD,TC,TC],
        [hori+horiSoma*5, altE,TC,TC]],  # Questão 6
    [[hori+horiSoma*6, vert, TC, TC], [hori+horiSoma*6, altB,TC,TC],
      [hori+horiSoma*6, altC,TC,TC], [hori+horiSoma*6, altD,TC,TC],
        [hori+horiSoma*6, altE,TC,TC]],  # Questão 7
    [[hori+horiSoma*7, vert, TC, TC], [hori+horiSoma*7, altB, TC, TC],
     [hori+horiSoma*7, altC, TC, TC], [hori+horiSoma*7, altD, TC, TC],
     [hori+horiSoma*7, altE, TC, TC]],  # Questão 8
    [[hori+horiSoma*8, vert, TC, TC], [hori+horiSoma*8, altB, TC, TC],
     [hori+horiSoma*8, altC, TC, TC], [hori+horiSoma*8, altD, TC, TC],
     [hori+horiSoma*8, altE, TC, TC]],  # Questão 9
    [[hori+horiSoma*9, vert, TC, TC], [hori+horiSoma*9, altB, TC, TC],
     [hori+horiSoma*9, altC, TC, TC], [hori+horiSoma*9, altD, TC, TC],
     [hori+horiSoma*9, altE, TC, TC]],  # Questão 10
    [[hori+horiSoma*10, vert, TC, TC], [hori+horiSoma*10, altB, TC, TC],
     [hori+horiSoma*10, altC, TC, TC], [hori+horiSoma*10, altD, TC, TC],
     [hori+horiSoma*10, altE, TC, TC]],  # Questão 11
    [[hori+horiSoma*11, vert, TC, TC], [hori+horiSoma*11, altB, TC, TC],
     [hori+horiSoma*11, altC, TC, TC], [hori+horiSoma*11, altD, TC, TC],
     [hori+horiSoma*11, altE, TC, TC]],  # Questão 12
    [[hori+horiSoma*12, vert, TC, TC], [hori+horiSoma*12, altB, TC, TC],
     [hori+horiSoma*12, altC, TC, TC], [hori+horiSoma*12, altD, TC, TC],
     [hori+horiSoma*12, altE, TC, TC]],  # Questão 13
    [[hori+horiSoma*13, vert, TC, TC], [hori+horiSoma*13, altB, TC, TC],
     [hori+horiSoma*13, altC, TC, TC], [hori+horiSoma*13, altD, TC, TC],
     [hori+horiSoma*13, altE, TC, TC]],  # Questão 14
    [[hori+horiSoma*14, vert, TC, TC], [hori+horiSoma*14, altB, TC, TC],
     [hori+horiSoma*14, altC, TC, TC], [hori+horiSoma*14, altD, TC, TC],
     [hori+horiSoma*14, altE, TC, TC]],  # Questão 15
#questao 16 - 30
[[hori, linhaSoma, TC2, TC], [hori, linhaSoma + VSoma, TC2, TC],
     [hori, linhaSoma + VSoma * 2, TC2, TC], [hori, linhaSoma + VSoma * 3, TC2, TC],
     [hori, linhaSoma + VSoma * 4, TC2, TC]],  # Questão 16
    [[hori + horiSoma, linhaSoma, TC, TC], [hori + horiSoma, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma, linhaSoma + VSoma * 4, TC, TC]],  # Questão 17
    [[hori + horiSoma * 2, linhaSoma, TC, TC], [hori + horiSoma * 2, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 2, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 2, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 2, linhaSoma + VSoma * 4, TC, TC]],  # Questão 18
    [[hori + horiSoma * 3, linhaSoma, TC, TC], [hori + horiSoma * 3, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 3, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 3, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 3, linhaSoma + VSoma * 4, TC, TC]],  # Questão 19
    [[hori + horiSoma * 4, linhaSoma, TC, TC], [hori + horiSoma * 4, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 4, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 4, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 4, linhaSoma + VSoma * 4, TC, TC]],  # Questão 20
    [[hori + horiSoma * 5, linhaSoma, TC, TC], [hori + horiSoma * 5, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 5, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 5, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 5, linhaSoma + VSoma * 4, TC, TC]],  # Questão 21
    [[hori + horiSoma * 6, linhaSoma, TC, TC], [hori + horiSoma * 6, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 6, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 6, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 6, linhaSoma + VSoma * 4, TC, TC]],  # Questão 22
    [[hori + horiSoma * 7- correcao, linhaSoma, TC, TC], [hori + horiSoma * 7- correcao, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 7- correcao, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 7- correcao, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 7- correcao, linhaSoma + VSoma * 4, TC, TC]],  # Questão 23
    [[hori + horiSoma * 8- correcao, linhaSoma, TC, TC], [hori + horiSoma * 8- correcao, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 8- correcao, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 8- correcao, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 8- correcao, linhaSoma + VSoma * 4, TC, TC]],  # Questão 24
    [[hori + horiSoma * 9- correcao, linhaSoma, TC, TC], [hori + horiSoma * 9- correcao, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 9- correcao, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 9- correcao, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 9- correcao, linhaSoma + VSoma * 4, TC, TC]],  # Questão 25
    [[hori + horiSoma * 10-correcao, linhaSoma, TC, TC], [hori + horiSoma * 10-correcao, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 10-correcao, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 10-correcao, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 10-correcao, linhaSoma + VSoma * 4, TC, TC]],  # Questão 26
    [[hori + horiSoma * 11-correcao, linhaSoma, TC, TC], [hori + horiSoma * 11-correcao, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 11-correcao, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 11-correcao, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 11-correcao, linhaSoma + VSoma * 4, TC, TC]],  # Questão 27
    [[hori + horiSoma * 12-correcao, linhaSoma, TC, TC], [hori + horiSoma * 12-correcao, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 12-correcao, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 12-correcao, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 12-correcao, linhaSoma + VSoma * 4, TC, TC]],  # Questão 28
    [[hori + horiSoma * 13-correcao, linhaSoma, TC, TC], [hori + horiSoma * 13-correcao, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 13-correcao, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 13-correcao, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 13-correcao, linhaSoma + VSoma * 4, TC, TC]],  # Questão 29
    [[hori + horiSoma * 14-correcao, linhaSoma, TC, TC], [hori + horiSoma * 14-correcao, linhaSoma + VSoma, TC, TC],
     [hori + horiSoma * 14-correcao, linhaSoma + VSoma * 2, TC, TC], [hori + horiSoma * 14-correcao, linhaSoma + VSoma * 3, TC, TC],
     [hori + horiSoma * 14-correcao, linhaSoma + VSoma * 4, TC, TC]],  # Questão 30
     
[[hori, linhaSoma2, TC2, TC], [hori, linhaSoma2 + VSoma, TC2, TC],
     [hori, linhaSoma2 + VSoma * 2, TC2, TC], [hori, linhaSoma2 + VSoma * 3, TC2, TC],
     [hori, linhaSoma2 + VSoma * 4, TC2, TC]],  # Questão 31

    [[hori + horiSoma, linhaSoma2, TC, TC], [hori + horiSoma, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 32

    [[hori + horiSoma * 2, linhaSoma2, TC, TC], [hori + horiSoma * 2, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 2, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 2, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 2, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 33

    [[hori + horiSoma * 3, linhaSoma2, TC, TC], [hori + horiSoma * 3, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 3, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 3, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 3, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 34

    [[hori + horiSoma * 4, linhaSoma2, TC, TC], [hori + horiSoma * 4, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 4, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 4, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 4, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 35

    [[hori + horiSoma * 5, linhaSoma2, TC, TC], [hori + horiSoma * 5, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 5, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 5, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 5, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 36

    [[hori + horiSoma * 6, linhaSoma2, TC, TC], [hori + horiSoma * 6, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 6, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 6, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 6, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 37

    [[hori + horiSoma * 7- correcao, linhaSoma2, TC, TC], [hori + horiSoma * 7- correcao, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 7- correcao, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 7- correcao, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 7- correcao, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 38

    [[hori + horiSoma * 8- correcao, linhaSoma2, TC, TC], [hori + horiSoma * 8- correcao, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 8- correcao, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 8- correcao, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 8- correcao, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 39

    [[hori + horiSoma * 9- correcao, linhaSoma2, TC, TC], [hori + horiSoma * 9- correcao, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 9- correcao, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 9- correcao, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 9- correcao, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 40

    [[hori + horiSoma * 10-correcao, linhaSoma2, TC, TC], [hori + horiSoma * 10-correcao, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 10-correcao, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 10-correcao, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 10-correcao, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 41

    [[hori + horiSoma * 11-correcao, linhaSoma2, TC, TC], [hori + horiSoma * 11-correcao, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 11-correcao, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 11-correcao, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 11-correcao, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 42

    [[hori + horiSoma * 12-correcao, linhaSoma2, TC, TC], [hori + horiSoma * 12-correcao, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 12-correcao, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 12-correcao, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 12-correcao, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 43

    [[hori + horiSoma * 13-correcao, linhaSoma2, TC, TC], [hori + horiSoma * 13-correcao, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 13-correcao, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 13-correcao, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 13-correcao, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 44
     
    [[hori + horiSoma * 14-correcao, linhaSoma2, TC, TC], [hori + horiSoma * 14-correcao, linhaSoma2 + VSoma, TC, TC],
     [hori + horiSoma * 14-correcao, linhaSoma2 + VSoma * 2, TC, TC], [hori + horiSoma * 14-correcao, linhaSoma2 + VSoma * 3, TC, TC],
     [hori + horiSoma * 14-correcao, linhaSoma2 + VSoma * 4, TC, TC]],  # Questão 45
[[hori, linhaSoma3, TC2, TC], [hori, linhaSoma3 + VSoma, TC2, TC],
     [hori, linhaSoma3 + VSoma * 2, TC2, TC], [hori, linhaSoma3 + VSoma * 3, TC2, TC],
     [hori, linhaSoma3 + VSoma * 4, TC2, TC]],  # Questão 46
    [[hori + horiSoma, linhaSoma3, TC, TC], [hori + horiSoma, linhaSoma3 + VSoma, TC, TC],
     [hori + horiSoma, linhaSoma3 + VSoma * 2, TC, TC], [hori + horiSoma, linhaSoma3 + VSoma * 3, TC, TC],
     [hori + horiSoma, linhaSoma3 + VSoma * 4, TC, TC]],  # Questão 47
    [[hori + horiSoma * 2, linhaSoma3, TC, TC], [hori + horiSoma * 2, linhaSoma3 + VSoma, TC, TC],
     [hori + horiSoma * 2, linhaSoma3 + VSoma * 2, TC, TC], [hori + horiSoma * 2, linhaSoma3 + VSoma * 3, TC, TC],
     [hori + horiSoma * 2, linhaSoma3 + VSoma * 4, TC, TC]],  # Questão 48
    [[hori + horiSoma * 3, linhaSoma3, TC, TC], [hori + horiSoma * 3, linhaSoma3 + VSoma, TC, TC],
     [hori + horiSoma * 3, linhaSoma3 + VSoma * 2, TC, TC], [hori + horiSoma * 3, linhaSoma3 + VSoma * 3, TC, TC],
     [hori + horiSoma * 3, linhaSoma3 + VSoma * 4, TC, TC]],  # Questão 49
    [[hori + horiSoma * 4, linhaSoma3, TC, TC], [hori + horiSoma * 4, linhaSoma3 + VSoma, TC, TC],
     [hori + horiSoma * 4, linhaSoma3 + VSoma * 2, TC, TC], [hori + horiSoma * 4, linhaSoma3 + VSoma * 3, TC, TC],
     [hori + horiSoma * 4, linhaSoma3 + VSoma * 4, TC, TC]],  # Questão 50
]

nota = 0

# Itera pelas questões
for i in range(NUM_QUESTOES):
    if i >= len(questoes_coordenadas):
        break  # Para evitar acessar uma questão que não foi definida nas coordenadas

    questao_coordenadas = questoes_coordenadas[i]
    preenchido = -1
    maior_preto = 0

    # Itera pelas alternativas
    for j, (x, y, w, h) in enumerate(questao_coordenadas):
        # Extrai a região da alternativa
        regiao = imagem_binaria[y:y+h, x:x+w]

        regiao_float = regiao.astype(np.float32)


        # Conta o número de pixels pretos (preenchidos)
        num_pretos = cv2.countNonZero(regiao_float)

        # Determina a alternativa mais preenchida
        if num_pretos > maior_preto:
            maior_preto = num_pretos
            preenchido = j

        # Desenha o retângulo da alternativa na imagem (opcional)
        cv2.rectangle(imagem_cinza, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Verifica a resposta
    if preenchido != -1:
        alternativa_marcada = preenchido
        alternativa_certa = ord(GABARITO[i]) - ord('A')
        print(f'Questão {i + 1}: Alternativa marcada: {chr(alternativa_marcada + ord("A"))}')

        # Verifica se a resposta está correta
        if alternativa_marcada == alternativa_certa:
            nota += 1

# Exibe a nota final
print(f'Nota final: {nota}/{NUM_QUESTOES}')

# Mostra a imagem com os retângulos desenhados
cv2.imshow('Imagem com Retângulos', imagem_cinza)
cv2.waitKey(0)
cv2.destroyAllWindows()
