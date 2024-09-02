import pytesseract
from PIL import ImageGrab, ImageTk, Image
import tkinter as tk
import pyautogui

# Configuração do pytesseract para apontar para o executável do Tesseract (necessário no Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_screen():
    # Captura a tela inteira
    screen = ImageGrab.grab()
    return screen

def search_word_on_screen(phrase):
    # Captura a tela
    screen_image = capture_screen()
    screen_image = screen_image.convert('L')
    screen_image = screen_image.point(lambda p: p > 128 and 255)

    # Extrai o texto e as caixas de localização da imagem
    d = pytesseract.image_to_data(screen_image, output_type=pytesseract.Output.DICT, config='--psm 6')

    # Obtém o texto extraído e as caixas de localização
    words = d['text']
    left = d['left']
    top = d['top']
    width = d['width']
    height = d['height']

    # Reconstrói o texto completo, preservando a ordem das palavras
    reconstructed_text = " ".join(words).strip()

    # Verifica se a frase está no texto reconstruído
    if phrase.lower() in reconstructed_text.lower():
        # Encontra a localização da primeira palavra da frase
        phrase_words = phrase.split()
        for i, w in enumerate(words):
            # Verifica se a primeira palavra da frase foi encontrada
            if phrase_words[0].lower() in w.lower():
                # Verifica as próximas palavras para garantir que é a frase correta
                match = True
                for j in range(1, len(phrase_words)):
                    if i + j >= len(words) or phrase_words[j].lower() not in words[i + j].lower():
                        match = False
                        break

                # Se encontrou a frase completa, calcula as coordenadas que englobam todas as palavras da frase
                if match:
                    # Coordenadas da primeira palavra
                    x1, y1, w1, h1 = left[i], top[i], width[i], height[i]

                    # Coordenadas da última palavra
                    x2, y2, w2, h2 = left[i + len(phrase_words) - 1], top[i + len(phrase_words) - 1], width[i + len(phrase_words) - 1], height[i + len(phrase_words) - 1]

                    # Calcula as coordenadas do retângulo ao redor da frase
                    x_left = x1
                    y_top = min(y1, y2)
                    x_right = x2 + w2
                    y_bottom = max(y1 + h1, y2 + h2)

                    return (x_left, y_top, x_right, y_bottom)

    return None

def simulate_click(coords):
    # Simula o clique no centro das coordenadas encontradas
    x1, y1, x2, y2 = coords
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2

    # Simula o clique usando o pyautogui
    pyautogui.click(x_center, y_center)

def update_ui():
    global tk_image, searching_replay

    # Captura a tela
    screen_image = capture_screen()

    # Reduz a imagem para exibição no canvas
    display_image = screen_image.resize((screen_display_width, screen_display_height), Image.Resampling.LANCZOS)

    # Converte a imagem para o formato do Tkinter
    tk_image = ImageTk.PhotoImage(display_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Se a frase foi encontrada, começa a buscar a palavra "replay"
    if searching_replay:
        palavra_atual = "replay"
    else:
        palavra_atual = palavra

    # Encontrar e desenhar a palavra na tela
    coords = search_word_on_screen(palavra_atual)
    if coords:
        # Ajustar coordenadas de acordo com o redimensionamento da imagem
        x1, y1, x2, y2 = coords
        x1 = x1 * screen_display_width / screen_width
        y1 = y1 * screen_display_height / screen_height
        x2 = x2 * screen_display_width / screen_width
        y2 = y2 * screen_display_height / screen_height
        canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

        if searching_replay:
            # Simula o clique na palavra "replay"
            simulate_click(coords)
            status_label.config(text=f'Palavra "{palavra_atual}" encontrada e clicada!', fg="green")
        else:
            status_label.config(text=f'Frase "{palavra}" encontrada!', fg="green")
            searching_replay = True  # Habilita a busca pela palavra "replay"
    else:
        status_label.config(text=f'Procurando "{palavra_atual}"...', fg="red")

    # Atualiza a tela a cada 1000 ms (1 segundo)
    root.after(100, update_ui)

if __name__ == "__main__":
    palavra = "The Repeat Battle has ended."
    searching_replay = False  # Variável para controlar a busca pela palavra "replay"

    # Configuração da UI com Tkinter
    root = tk.Tk()
    root.title("Detecção de Palavra")

    # Configurações do tamanho da tela e do canvas
    screen_width = 1920  # Largura da tela capturada (ajuste conforme necessário)
    screen_height = 1080  # Altura da tela capturada (ajuste conforme necessário)
    screen_display_width = 800  # Largura do canvas para exibir a captura de tela
    screen_display_height = 600  # Altura do canvas para exibir a captura de tela

    # Frame principal para a captura de tela e o painel de informações
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Canvas para exibir a captura de tela
    canvas = tk.Canvas(main_frame, width=screen_display_width, height=screen_display_height, bg="black")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Frame para o status e outras informações
    info_frame = tk.Frame(root, bg="black")
    info_frame.pack(fill=tk.BOTH, expand=True)

    # Adiciona a label para mostrar o status
    status_label = tk.Label(info_frame, text=f'Procurando frase "{palavra}"...', font=("Arial", 16), bg="black", fg="white")
    status_label.pack(pady=10, padx=10, anchor=tk.W)

    # Inicializa a imagem Tkinter global
    tk_image = None

    # Inicia o loop de atualização da UI
    update_ui()
    root.mainloop()
