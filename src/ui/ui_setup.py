import tkinter as tk

def create_toggle_button(root, toggle_var, toggle_callback):
    toggle_frame = tk.Frame(root, width=60, height=30, bg="black", relief="raised", bd=2)
    toggle_frame.pack_propagate(False)

    # Toggle slider
    slider = tk.Canvas(toggle_frame, width=28, height=28, bg="white", bd=0, highlightthickness=0)
    slider.place(x=2, y=2)

    def on_toggle_click(event=None):
        # Alterna o valor do toggle_var entre 1 (ativado) e 0 (desativado)
        if toggle_var.get() == 0:
            toggle_var.set(1)
            slider.place(x=30, y=2)
        else:
            toggle_var.set(0)
            slider.place(x=2, y=2)
        toggle_callback()  # Chama a função de callback para mostrar/ocultar o conteúdo do canvas

    # Bind the click event
    toggle_frame.bind("<Button-1>", on_toggle_click)
    slider.bind("<Button-1>", on_toggle_click)

    return toggle_frame

def setup_ui(root, screen_display_width, screen_display_height, palavra, toggle_var, toggle_callback):
    root.title("Detecção de Palavra")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Cria o toggle button deslizante
    toggle_button = create_toggle_button(main_frame, toggle_var, toggle_callback)
    toggle_button.pack(pady=10)

    # Frame do canvas
    canvas_frame = tk.Frame(main_frame, width=screen_display_width, bg="black")
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(canvas_frame, width=screen_display_width, height=screen_display_height, bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Frame de informações
    info_frame = tk.Frame(main_frame, bg="black", width=300)
    info_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

    status_label = tk.Label(info_frame, text=f'Procurando frase "{palavra}"...', font=("Arial", 16), bg="black", fg="white")
    status_label.pack(pady=10, padx=10, anchor=tk.W)

    return canvas_frame, canvas, status_label
