import cv2
import numpy as np
from dados import GABARITO, questoes_coordenadas

# Parâmetros gerais
ARQUIVO_IMAGEM = 'cartao3.jpg'
NUM_QUESTOES = 50
fator_zoom = 1.0
zoom_incremento = 0.01
angulo = 0
deslocamento_vertical = 0
deslocamento_horizontal = 0
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
        preenchidos = []  # Lista para armazenar as alternativas marcadas
        maior_preto = 0

        # Verifica as alternativas de cada questão
        for j, (x, y, w, h) in enumerate(questao_coordenadas):
            regiao = imagem_binaria[y:y+h, x:x+w]
            num_pretos = cv2.countNonZero(regiao)

            # Se a quantidade de pixels pretos for significativa, considera como marcada
            if num_pretos > maior_preto:
                maior_preto = num_pretos
                preenchidos = [j]  # Marca a alternativa encontrada
            elif num_pretos == maior_preto:
                preenchidos.append(j)  # Caso haja mais de uma alternativa marcada

        alternativas_marcadas[i] = preenchidos[0] if len(preenchidos) == 1 else -1  # Se mais de uma alternativa estiver marcada, marca como erro

        alternativa_certa = ord(gabarito[i]) - ord('A')

        if alternativas_marcadas[i] != -1:
            if alternativas_marcadas[i] == alternativa_certa:
                nota += 1  # Conta como certa
            print(f'Questão {i + 1}: Alternativa marcada: {chr(alternativas_marcadas[i] + ord("A"))}')
        else:
            print(f'Questão {i + 1}: Nenhuma alternativa válida ou mais de uma marcada.')

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

# Controle de rotação, zoom e deslocamento
coordenadas_cantos = [
    (40, 25, 26),  # Superior esquerdo
    (imagem_cortada.shape[1] - 48, 29, 26),  # Superior direito
    (40, imagem_cortada.shape[0] - 61, 26),  # Inferior esquerdo
    (imagem_cortada.shape[1] - 50, imagem_cortada.shape[0] - 58, 26)  # Inferior direito
]

while True:
    # Aplica a rotação
    rotacao_matriz = cv2.getRotationMatrix2D((imagem_cortada.shape[1] // 2, imagem_cortada.shape[0] // 2), angulo, fator_zoom)
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
    elif tecla == ord('w'):  # Tecla para zoom in
        fator_zoom += zoom_incremento
    elif tecla == ord('s'):  # Tecla para zoom out
        fator_zoom -= zoom_incremento
    elif tecla == ord('i'):
        deslocamento_vertical -= 2
    elif tecla == ord('k'):
        deslocamento_vertical += 2
    elif tecla == ord('j'):
        deslocamento_horizontal -= 2
    elif tecla == ord('l'):
        deslocamento_horizontal += 2

cv2.destroyAllWindows()
