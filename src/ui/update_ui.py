import tkinter as tk
from PIL import ImageTk, Image
import threading
from src.utils.capture import capture_screen
from src.utils.search import search_word_on_screen
from src.actions.click import simulate_click

# Armazenar a referência à imagem globalmente
tk_image = None

def update_canvas_image(canvas, screen_display_width, screen_display_height):
    global tk_image  # Usar a variável global para armazenar a imagem

    # Captura e redimensiona a imagem da tela
    screen_image = capture_screen()
    display_image = screen_image.resize((screen_display_width, screen_display_height), Image.Resampling.LANCZOS)
    tk_image = ImageTk.PhotoImage(display_image)

    # Atualiza o canvas com a nova imagem
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

def search_and_update_ui(root, canvas, status_label, screen_display_width, screen_display_height, screen_width, screen_height, palavra, searching_replay, stop_searching_callback):
    while True:
        # Verifica se a leitura deve continuar
        if stop_searching_callback():  # Se a função callback retornar True, paramos o loop
            return  # Para o loop completamente, sem resetar

        # Atualiza a imagem no canvas
        update_canvas_image(canvas, screen_display_width, screen_display_height)

        # Procura a palavra na tela
        palavra_atual = "replay" if searching_replay else palavra
        coords = search_word_on_screen(palavra_atual)
        if coords:
            x1, y1, x2, y2 = coords
            x1 = x1 * screen_display_width / screen_width
            y1 = y1 * screen_display_height / screen_height
            x2 = x2 * screen_display_width / screen_width
            y2 = y2 * screen_display_height / screen_height
            canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

            if searching_replay:
                simulate_click(coords)
                status_label.config(text=f'Palavra "{palavra_atual}" encontrada e clicada!', fg="green")
            else:
                status_label.config(text=f'Frase "{palavra}" encontrada!', fg="green")
                searching_replay = True
        else:
            status_label.config(text=f'Procurando "{palavra_atual}"...', fg="red")

        # Aguarda 100 ms antes de atualizar novamente
        root.after(100)

def update_ui(root, canvas, status_label, screen_display_width, screen_display_height, screen_width, screen_height, palavra, searching_replay, stop_searching_callback):
    # Inicia um thread separado para atualizar a UI, apenas se a leitura estiver ativa
    if not stop_searching_callback():
        update_thread = threading.Thread(target=search_and_update_ui, args=(root, canvas, status_label, screen_display_width, screen_display_height, screen_width, screen_height, palavra, searching_replay, stop_searching_callback))
        update_thread.daemon = True
        update_thread.start()
