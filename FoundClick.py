import cv2
import numpy as np
import pyautogui
import time
import random
from scipy.interpolate import splprep, splev

def bezier_curve(points, num_points=10):
    """Gera pontos ao longo de uma curva de Bézier com suavidade"""
    points = np.array(points)
    tck, u = splprep(points.T, s=0)
    u_new = np.linspace(0, 1, num_points)
    x_new, y_new = splev(u_new, tck, der=0)
    return np.stack((x_new, y_new), axis=-1)

def human_like_mouse_move(start_x, start_y, end_x, end_y, duration=.01):
    """Move o mouse de forma orgânica, simulando um arrasto humano"""
    # Define pontos intermediários com alguma aleatoriedade
    control_points = [
        (start_x, start_y),
        (start_x + random.uniform(-20, 20), start_y + random.uniform(-20, 20)),
        (end_x + random.uniform(-20, 20), end_y + random.uniform(-20, 20)),
        (end_x, end_y)
    ]

    # Gera a curva de Bézier
    path = bezier_curve(control_points, num_points=int(duration * 120))

    # Move o mouse ao longo do caminho gerado
    for x, y in path:
        pyautogui.moveTo(x, y, duration=0.1)

def FoundClick(template_path, threshold=0.8):
    found = False

    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"Erro: Não foi possível carregar a imagem '{template_path}'")
        return

    template_h, template_w = template.shape[:2]

    print(f"Iniciando click em '{template_path}'")
    while not found:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            center_x = max_loc[0] + template_w // 2
            center_y = max_loc[1] + template_h // 2

            # Pega a posição atual do mouse
            current_x, current_y = pyautogui.position()

            # Move suavemente até o ponto
            human_like_mouse_move(current_x, current_y, center_x, center_y, duration=0.3)

            print(f"Imagem '{template_path}' Clicada")
            pyautogui.click(center_x, center_y)

            time.sleep(0.2)
            found = True
        else:
            print("Imagem não Clicada")

        time.sleep(0.05)

FoundClick("./img/button/a.png", threshold=.8)