import pytesseract
from PIL import ImageGrab, ImageTk, Image
import tkinter as tk

# Configuração do pytesseract para apontar para o executável do Tesseract (necessário no Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_screen():
    # Captura a tela inteira
    screen = ImageGrab.grab()
    return screen

def search_word_on_screen(word):
    # Captura a tela
    screen_image = capture_screen()

    # Extrai o texto e as caixas de localização da imagem
    d = pytesseract.image_to_data(screen_image, output_type=pytesseract.Output.DICT)

    # Obtém o texto extraído e as caixas de localização
    words = d['text']
    left = d['left']
    top = d['top']
    width = d['width']
    height = d['height']

    # Verifica se a palavra está no texto extraído e retorna a localização
    for i, w in enumerate(words):
        if word.lower() in w.lower():
            (x, y, w, h) = (left[i], top[i], width[i], height[i])
            return (x, y, x + w, y + h)

    return None

def update_ui():
    global tk_image

    # Captura a tela
    screen_image = capture_screen()

    # Reduz a imagem para exibição no canvas
    display_image = screen_image.resize((screen_display_width, screen_display_height), Image.Resampling.LANCZOS)

    # Converte a imagem para o formato do Tkinter
    tk_image = ImageTk.PhotoImage(display_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

    # Encontrar e desenhar a palavra na tela
    coords = search_word_on_screen(palavra)
    if coords:
        # Ajustar coordenadas de acordo com o redimensionamento da imagem
        x1, y1, x2, y2 = coords
        x1 = x1 * screen_display_width / screen_width
        y1 = y1 * screen_display_height / screen_height
        x2 = x2 * screen_display_width / screen_width
        y2 = y2 * screen_display_height / screen_height
        canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
        status_label.config(text=f'Palavra "{palavra}" encontrada!', fg="green")
    else:
        status_label.config(text=f'Palavra "{palavra}" não encontrada.', fg="red")

    # Atualiza a tela a cada 1000 ms (1 segundo)
    root.after(1000, update_ui)

if __name__ == "__main__":
    palavra = "Lose"

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
    status_label = tk.Label(info_frame, text=f'Procurando palavra "{palavra}":', font=("Arial", 16), bg="black", fg="white")
    status_label.pack(pady=10, padx=10, anchor=tk.W)

    # Inicializa a imagem Tkinter global
    tk_image = None

    # Inicia o loop de atualização da UI
    update_ui()
    root.mainloop()
