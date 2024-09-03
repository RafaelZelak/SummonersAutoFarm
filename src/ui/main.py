import tkinter as tk
from src.ui.ui_setup import setup_ui
from src.ui.update_ui import update_ui

def run_app():
    palavra = "True"
    searching_replay = False

    root = tk.Tk()

    screen_width = 1920
    screen_height = 1080
    screen_display_width = 800
    screen_display_height = 600
    min_height_with_canvas = 700
    min_height_without_canvas = 200

    toggle_var = tk.IntVar(value=1)  # Estado inicial do toggle (1 = tela visível)

    def toggle_callback():
        # Alterna entre mostrar e esconder o conteúdo do canvas e ajusta a altura da janela
        if toggle_var.get() == 1:
            # Mostrar o canvas e ajustar a altura
            canvas.config(height=screen_display_height)
            canvas_frame.pack(fill=tk.BOTH, expand=True)  # Mostra o canvas frame
            root.minsize(screen_display_width, min_height_with_canvas)
        else:
            # Esconder o conteúdo do canvas e ajustar a altura
            canvas_frame.pack_forget()  # Esconde o canvas frame
            root.minsize(screen_display_width, min_height_without_canvas)

    # Configura a interface inicial
    canvas_frame, canvas, status_label = setup_ui(
        root, screen_display_width, screen_display_height, palavra, toggle_var, toggle_callback
    )

    # Inicia o loop de atualização da UI
    update_ui(
        root, canvas, status_label, screen_display_width, screen_display_height,
        screen_width, screen_height, palavra, searching_replay
    )

    root.mainloop()

# Executa a aplicação
if __name__ == "__main__":
    run_app()
