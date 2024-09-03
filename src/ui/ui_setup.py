import tkinter as tk

def setup_ui(root, screen_display_width, screen_display_height, palavra, toggle_var, toggle_callback):
    root.configure(bg="#2e3b4e")

    # Frame principal
    main_frame = tk.Frame(root, bg="#2e3b4e")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Botão Toggle
    toggle_button = tk.Checkbutton(
        main_frame, text="Mostrar/Esconder Imagem", variable=toggle_var,
        command=toggle_callback, font=("Helvetica", 12, "bold"), fg="white", bg="#2e3b4e",
        selectcolor="#2e3b4e", activebackground="#2e3b4e", activeforeground="white"
    )
    toggle_button.pack(pady=10)

    # Frame do Canvas
    canvas_frame = tk.Frame(main_frame, bg="black", width=screen_display_width, height=screen_display_height)
    canvas_frame.pack(fill=tk.BOTH, expand=False)  # pack to control layout initially

    canvas = tk.Canvas(canvas_frame, width=screen_display_width, height=screen_display_height, bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Frame de Informações
    info_frame = tk.Frame(main_frame, bg="#2e3b4e")
    info_frame.pack(fill=tk.X, pady=10)

    status_label = tk.Label(info_frame, text=f'Procurando frase "{palavra}"...', font=("Helvetica", 14, "bold"), bg="#2e3b4e", fg="white")
    status_label.pack(pady=5, padx=10)

    return canvas_frame, canvas, status_label, toggle_button
