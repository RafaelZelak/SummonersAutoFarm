import cv2
import numpy as np
import pyautogui
import time

def FoundClickOneTime(template_path, threshold=0.8):

    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"Erro: Não foi possível carregar a imagem '{template_path}'")
        return

    template_h, template_w = template.shape[:2] 

    print(f"Iniciando click em '{template_path}'")
    screenshot = pyautogui.screenshot()
    
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        center_x = max_loc[0] + template_w // 2
        center_y = max_loc[1] + template_h // 2
        print(f"Imagem '{template_path}' Clicada")
        pyautogui.click(center_x, center_y)
        time.sleep(0.5)
        found = True
    else:
        print("Imagem não Clicada")
    
    time.sleep(0.1)

