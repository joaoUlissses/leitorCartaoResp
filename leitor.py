import cv2
import numpy as np
from dados import GABARITO, questoes_coordenadas

# Parâmetros gerais
ARQUIVO_IMAGEM = 'cartao3.jpg'
NUM_QUESTOES = 50


alternativas_marcadas = [-1] * NUM_QUESTOES


def preprocessar_imagem(imagem):
    """Pré-processa a imagem para binarização."""
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    imagem_cinza = cv2.medianBlur(imagem_cinza, 5)
    _, imagem_binaria = cv2.threshold(imagem_cinza, 150, 255, cv2.THRESH_BINARY_INV)
    return imagem_binaria

def desenhar_retangulos(imagem, coordenadas):
    """Desenha retângulos fixos na tela."""
    for (x, y, w, h) in coordenadas:
        cv2.rectangle(imagem, (x, y), (x + w, y + h), (255, 255, 255), 2)
    return imagem

def desenhar_quadrados_cantos(imagem, coordenadas_cantos):
    """Desenha quadrados nos cantos especificados."""
    for (x, y, tamanho) in coordenadas_cantos:
        cv2.rectangle(imagem, (x, y), (x + tamanho-15, y + tamanho-15), (255, 0, 255), 1)
    return imagem

def calcular_nota(imagem_binaria, questoes_coordenadas, gabarito):
    """Calcula a nota com base nas alternativas marcadas."""
    nota = 0
    for i, questao_coordenadas in enumerate(questoes_coordenadas):
        preenchido = -1
        maior_preto = 0

        for j, (x, y, w, h) in enumerate(questao_coordenadas):
            regiao = imagem_binaria[y:y+h, x:x+w]
            num_pretos = cv2.countNonZero(regiao)

            if num_pretos > maior_preto:
                maior_preto = num_pretos
                preenchido = j

        alternativas_marcadas[i] = preenchido
        alternativa_certa = ord(gabarito[i]) - ord('A')

        if preenchido != -1:
            print(f'Questão {i + 1}: Alternativa marcada: {chr(preenchido + ord("A"))}')
        else:
            print(f'Questão {i + 1}: Nenhuma alternativa marcada.')

        if preenchido == alternativa_certa:
            nota += 1

    return nota

def desenhar_resultados(imagem, questoes_coordenadas, alternativas_marcadas, gabarito):
    """Desenha os resultados na imagem."""
    for i, questao_coordenadas in enumerate(questoes_coordenadas):
        for j, (x, y, w, h) in enumerate(questao_coordenadas):
            cor = (0, 255, 0) if j == alternativas_marcadas[i] else (0, 0, 255)
            cv2.rectangle(imagem, (x, y), (x+w, y+h), cor, 2)
    return imagem

# Carrega a imagem
imagem = cv2.imread(ARQUIVO_IMAGEM)
if imagem is None:
    print(f"Erro ao carregar a imagem: {ARQUIVO_IMAGEM}")
    exit()

# Recorte da imagem (ajustar conforme necessário)
altura, largura = imagem.shape[:2]
inicio_corte = int(altura * 0.3)
fim_corte = int(altura * 0.9)
imagem_cortada = imagem[inicio_corte:fim_corte, 0:largura]

# Pré-processa a imagem cortada
imagem_binaria = preprocessar_imagem(imagem_cortada)

# Controle de rotação e deslocamento
angulo = 0
deslocamento_vertical = 0
deslocamento_horizontal = 0

coordenadas_cantos = [
    (40, 25, 26),  # Superior esquerdo
    (imagem_cortada.shape[1] - 48, 29, 26),  # Superior direito
    (40, imagem_cortada.shape[0] - 61, 26),  # Inferior esquerdo
    (imagem_cortada.shape[1] - 50, imagem_cortada.shape[0] - 58, 26)  # Inferior direito
]

while True:
    # Aplica a rotação
    rotacao_matriz = cv2.getRotationMatrix2D((imagem_cortada.shape[1] // 2, imagem_cortada.shape[0] // 2), angulo, 1)
    imagem_rotacionada = cv2.warpAffine(imagem_binaria, rotacao_matriz, (imagem_cortada.shape[1], imagem_cortada.shape[0]))

    # Aplica os deslocamentos na imagem
    imagem_rotacionada = np.roll(imagem_rotacionada, deslocamento_vertical, axis=0)
    imagem_rotacionada = np.roll(imagem_rotacionada, deslocamento_horizontal, axis=1)

    # Cria uma cópia da imagem para exibição
    imagem_exibicao = imagem_rotacionada.copy()

    # Desenha retângulos **fixos** na tela (sem relação com a imagem)
    for questao_coordenadas in questoes_coordenadas:
        imagem_exibicao = desenhar_retangulos(imagem_exibicao, questao_coordenadas)

    # Desenha os quadrados nos cantos
    imagem_exibicao = desenhar_quadrados_cantos(imagem_exibicao, coordenadas_cantos)

    # Exibe a imagem ajustada
    cv2.imshow("Imagem com Retângulos Fixos", imagem_exibicao)
    tecla = cv2.waitKey(30)

    if tecla == ord('q'): 
        nota = calcular_nota(imagem_rotacionada, questoes_coordenadas, GABARITO)
        print(f"Nota final: {nota}/{NUM_QUESTOES}")

        imagem_resultado = desenhar_resultados(imagem_cortada, questoes_coordenadas, alternativas_marcadas, GABARITO)
        cv2.imshow("Resultados", imagem_resultado)
        cv2.imwrite("resultado.jpg", imagem_resultado)
        break
    elif tecla == ord('a'):
        angulo += 2
    elif tecla == ord('d'):
        angulo -= 2
    elif tecla == ord('i'):
        deslocamento_vertical -= 2
    elif tecla == ord('k'):
        deslocamento_vertical += 2
    elif tecla == ord('j'):
        deslocamento_horizontal -= 2
    elif tecla == ord('l'):
        deslocamento_horizontal += 2

cv2.destroyAllWindows()
