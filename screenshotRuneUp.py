import cv2
import numpy as np
import pyautogui
import hashlib
import time
import os

def screenshotRuneUp(template_path, threshold=0.8):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        raise FileNotFoundError(f"Erro: Imagem '{template_path}' não encontrada.")

    template_h, template_w = template.shape[:2]
    screenshot = np.array(pyautogui.screenshot())
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        vx, vy = max_loc
        vw, vh = template_w, template_h

        # Configurações para ajuste de região
        width_left = 1.6  # Ajuste para a largura à esquerda (multiplicador do template_w)
        width_right = 7.5  # Ajuste para a largura à direita (multiplicador do template_w)
        height_down = 8  # Ajuste para a altura abaixo (multiplicador do template_h)
        height_up = 0  # Ajuste para a altura acima (multiplicador do template_h)

        # Offset para onde a captura começa
        offset_x = 0  # Deslocamento horizontal (negativo para esquerda, positivo para direita)
        offset_y = vh+1  # Deslocamento vertical (negativo para cima, positivo para baixo)

        # Definir a região baseada nos ajustes
        region = (
            max(0, vx - int(vw * width_left) + offset_x),
            max(0, vy - int(vh * height_up) + offset_y),
            int(vw * (width_left + width_right)),
            int(vh * (height_up + height_down))
        )

        # Capturar a região e salvar com hash
        screenshot_region = pyautogui.screenshot(region=region)
        hash_name = hashlib.md5(str(time.time()).encode()).hexdigest()
        cache_dir = "./cache"
        os.makedirs(cache_dir, exist_ok=True)
        file_path = os.path.join(cache_dir, f"screenshot_up_{hash_name}.png")
        screenshot_region.save(file_path)

        print(f"Imagem encontrada e captura salva em: {file_path}")
        return file_path
    else:
        print("Imagem não encontrada.")
        return None

screenshotRuneUp("./img/runes/Rune12.png", threshold=.8)