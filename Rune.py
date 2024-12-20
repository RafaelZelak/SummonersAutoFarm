import pyautogui
import cv2
import numpy as np
import os
import sys
import math
import time
import hashlib
import json
from Found import Found
from FoundClickRobot import FoundClick
from FoundOneTime import FoundOneTime
from FoundClickOneTime import FoundClickOneTime
from CalcRune import calcular_eficiencia_da_runa

def find_image_on_screen(target_image, confidence=0.7):
    """
    Procura uma imagem na tela com uma confiança definida e retorna sua posição central.
    """
    try:
        position = pyautogui.locateCenterOnScreen(target_image, confidence=confidence)
        return position
    except:
        return None

def distance(p1, p2):
    """
    Calcula a distância Euclidiana entre dois pontos.
    """
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def count_and_print_coordinates(image_to_find, search_region, confidence=0.7, min_distance=50):
    """
    Procura múltiplas ocorrências de uma imagem em uma região específica da tela.
    Imprime as coordenadas únicas de onde a imagem foi encontrada, ignorando coordenadas muito próximas.
    Retorna a quantidade de ocorrências únicas.
    """
    screenshot = pyautogui.screenshot(region=search_region)  # Tira print da região
    screen_array = np.array(screenshot)  # Converte para array do OpenCV
    screen_bgr = cv2.cvtColor(screen_array, cv2.COLOR_RGB2BGR)  # Converte para BGR

    template = cv2.imread(image_to_find, cv2.IMREAD_UNCHANGED)  # Carrega a imagem
    h, w, _ = template.shape  # Dimensões da imagem

    # Faz o match de template
    result = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= confidence)

    # Converte para lista de pontos
    points = list(zip(*locations[::-1]))

    clicked_coordinates = []  # Lista para armazenar as coordenadas clicadas
    star_count = 0  # Contador de ocorrências

    for point in points:
        # Certifique-se de que o template foi carregado corretamente
        if template is None:
            raise ValueError(f"Erro ao carregar a imagem: {image_to_find}")

        # Ajusta para as coordenadas absolutas e centraliza o clique na imagem correspondente
        template_center_x = point[0] + w // 2
        template_center_y = point[1] + h // 2
        x = template_center_x + search_region[0]
        y = template_center_y + search_region[1]

        print(f"Coordenadas ajustadas: Central ({template_center_x}, {template_center_y}) na região absoluta ({x}, {y})")

        # Verifica se a coordenada está distante o suficiente de todas as anteriores
        should_click = True
        for prev_x, prev_y in clicked_coordinates:
            if distance((x, y), (prev_x, prev_y)) < min_distance:
                should_click = False
                break

        # Se a coordenada for suficientemente distante, clica nela
        if should_click:
            pyautogui.click(x, y)  # Clica na posição centralizada
            print(f"Runa encontrada em COORD: ({x}, {y})\n")
            clicked_coordinates.append((x, y))
            time.sleep(0.3)

            # Verifica se a runa é rara e executa ações específicas
            RunaJaVendida = FoundOneTime("./img/button/RecompraBtn.png", threshold=0.8)
            if RunaJaVendida == False:
                RuneRare = FoundOneTime("./img/runes/Rare.png", threshold=0.8)
                if RuneRare:
                    print("A runa é Rara, Vendendo")
                    Vender = FoundOneTime("./img/button/VenderPriceBtn.png", threshold=0.8)
                    if Vender:
                        FoundClick("./img/button/VenderPriceBtn.png", threshold=0.8)
                    else:
                        FoundClick("./img/button/OkBtn.png", threshold=0.8)

                    star_count += 1
                    input("Pressione Enter para continuar...")
                    continue

                # Captura uma print da área acima do botão "Vender"
                vender_pos = pyautogui.locateOnScreen("./img/button/VenderPriceBtn.png", confidence=0.8)
                if vender_pos:
                    vx, vy, vw, vh = map(int, vender_pos)  # Garante que os valores sejam inteiros
                    top_region = (
                        max(0, vx - int(vw * 0.5)) + 11,  # Reduz o deslocamento para incluir mais pixels à esquerda
                        max(0, vy - int(vh * 4.5)),       # Mantém o ajuste vertical
                        int(vw * 1.5),                    # Aumenta a largura para capturar mais pixels à direita
                        vh * 3                            # Mantém a altura como está
                    )

                    # Gera o hash para o nome do arquivo
                    hash_name = hashlib.md5(str(time.time()).encode()).hexdigest()

                    # Caminho da pasta cache
                    cache_dir = "./cache"
                    os.makedirs(cache_dir, exist_ok=True)  # Cria a pasta se não existir

                    screenshot_top = pyautogui.screenshot(region=top_region)
                    screenshot_top_path = os.path.join(cache_dir, f"screenshot_{hash_name}.png")
                    screenshot_top.save(screenshot_top_path)

                    print(f"Captura da área acima do botão 'Vender' salva em: {screenshot_top_path}")

                    eficiencia = calcular_eficiencia_da_runa()
                    eficienciaPercent = eficiencia['eficiencia']
                    print(f"\nRetorno Calc:\n{eficiencia}")
                    if eficienciaPercent >= 50.0:
                        FoundClick("./img/button/MelhoriaBtn.png",threshold=0.8)
                        FoundClick("./img/button/MelhoriaUpBtn.png",threshold=0.8)
                    else:
                        VenderVerificada = FoundOneTime("./img/button/VenderPriceBtn.png", threshold=0.8)
                        if VenderVerificada:
                            FoundClickOneTime("./img/button/VenderPriceBtn.png", threshold=0.8)
                            RunaLegend = FoundOneTime("./img/button/SimBtn.png", threshold=0.8)
                            if RunaLegend:
                                FoundClick("./img/button/SimBtn.png", threshold=0.8)
                        else:
                            FoundClick("./img/button/OkBtn.png", threshold=0.8)
            else:
                FoundClick("./img/button/XBtn.png", threshold=0.8)

            star_count += 1
            input("Pressione Enter para continuar...")

    return star_count


def main():
    hist_image_path = "./img/runes/Hist.png"
    star_image_path = "./img/runes/Star.png"

    # Procura pela imagem Hist.png
    print("Procurando pela imagem Hist.png na tela...")
    hist_position = find_image_on_screen(hist_image_path, confidence=0.7)

    if hist_position is None:
        print("Não foi possível encontrar a imagem Hist.png.")
        sys.exit()

    print(f"Imagem Hist.png encontrada em: {hist_position}")

    # Define a região abaixo de Hist.png até o final da tela
    screen_width, screen_height = pyautogui.size()
    x, y = hist_position
    search_region = (0, int(y), int(screen_width), int(screen_height - y))

    # Conta e imprime as coordenadas das imagens Star.png encontradas
    print("Procurando pela imagem Star.png abaixo de Hist.png...")
    star_count = count_and_print_coordinates(star_image_path, search_region, confidence=0.7)

    print(f"Imagem Star.png foi encontrada {star_count} vezes na região abaixo de Hist.png.")

if __name__ == "__main__":
    main()
