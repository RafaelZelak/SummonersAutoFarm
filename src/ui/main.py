import tkinter as tk
from src.ui.ui_setup import setup_ui
from src.ui.update_ui import update_ui

def run_app():
    palavra = "True"
    searching_replay = False
    stop_searching = True  # A leitura da tela começa parada

    root = tk.Tk()
    root.title("Detecção de Palavra")

    screen_display_width = 800
    screen_display_height = 600

    toggle_var = tk.IntVar(value=1)  # Estado inicial do toggle (1 = imagem visível)

    # Função de callback para o botão toggle
    def toggle_canvas():
        if toggle_var.get() == 1:
            canvas_frame.pack(fill=tk.BOTH, expand=True)
        else:
            canvas_frame.pack_forget()

    # Configura a interface inicial
    canvas_frame, canvas, status_label, toggle_button = setup_ui(
        root, screen_display_width, screen_display_height, palavra, toggle_var, toggle_canvas
    )

    # Função para alternar entre iniciar e parar a leitura da tela
    def toggle_searching():
        nonlocal stop_searching

        if stop_searching:  # Se a leitura está parada, queremos começar
            stop_searching = False
            start_button.config(text="Parar Leitura da Tela", bg="red", fg="white")  # Muda o texto e cor do botão

            # Inicia a leitura da tela
            update_ui(
                root, canvas, status_label, screen_display_width, screen_display_height,
                root.winfo_screenwidth(), root.winfo_screenheight(), palavra, searching_replay, lambda: stop_searching
            )
        else:  # Se a leitura está ativa, queremos parar
            stop_searching = True
            canvas.delete("all")  # Limpa o canvas
            canvas.create_rectangle(0, 0, screen_display_width, screen_display_height, fill="black")  # Preenche o canvas com preto
            start_button.config(text="Iniciar Leitura da Tela", bg="green", fg="white")  # Muda o texto e cor do botão

    # Botão de iniciar/parar leitura
    start_button = tk.Button(root, text="Iniciar Leitura da Tela", command=toggle_searching, font=("Helvetica", 12, "bold"), fg="white", bg="green")
    start_button.pack(pady=10)

    # Inicializa o canvas com preto
    canvas.create_rectangle(0, 0, screen_display_width, screen_display_height, fill="black")

    root.mainloop()

if __name__ == "__main__":
    run_app()
