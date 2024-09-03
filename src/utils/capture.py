from PIL import ImageGrab

def capture_screen():
    # Captura a tela inteira
    screen = ImageGrab.grab()
    return screen
