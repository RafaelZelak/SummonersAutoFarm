import pyautogui

def simulate_click(coords):
    x1, y1, x2, y2 = coords
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2

    pyautogui.click(x_center, y_center)
