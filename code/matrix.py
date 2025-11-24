import tkinter as tk
from tkinter import ttk

MATRIX_WIDTH = 13
MATRIX_HEIGHT = 8
CELL_SIZE = 40  # taille des carres en pixels

class MatrixEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UNO Q Editeur de matrice de leds 13x8")

        # etat des LEDs : False = eteint, True = allume
        self.led_state = [
            [False for _ in range(MATRIX_WIDTH)]
            for _ in range(MATRIX_HEIGHT)
        ]

        # Frame principale
        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Canvas pour dessiner la matrice
        self.canvas = tk.Canvas(
            main_frame,
            width=MATRIX_WIDTH * CELL_SIZE,
            height=MATRIX_HEIGHT * CELL_SIZE,
            bg="gray20",
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # dessine la grille
        self.rects = [
            [None for _ in range(MATRIX_WIDTH)]
            for _ in range(MATRIX_HEIGHT)
        ]

        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):
                x0 = x * CELL_SIZE
                y0 = y * CELL_SIZE
                x1 = x0 + CELL_SIZE - 2
                y1 = y0 + CELL_SIZE - 2
                rect = self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill="black",
                    outline="dim gray"
                )
                self.rects[y][x] = rect

        # clic sur le canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Boutons d'action
        btn_generate = ttk.Button(main_frame, text="Generer les 4 mots", command=self.generer_mots)
        btn_generate.grid(row=1, column=0, sticky="w", pady=5)

        btn_clear = ttk.Button(main_frame, text="Effacer", command=self.clear_matrix)
        btn_clear.grid(row=1, column=1, sticky="w", pady=5, padx=(10, 0))

        btn_copy = ttk.Button(main_frame, text="Copier", command=self.copy_to_clipboard)
        btn_copy.grid(row=1, column=2, sticky="e", pady=5)

        # Zone de resultat : plus grande, police plus grande
        self.result_text = tk.Text(
            main_frame,
            width=75,
            height=12,
            font=("Courier", 18)   # police encore plus grande
        )
        self.result_text.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        self.result_text.insert("1.0", "Les mots generes apparaitront ici...\n")

        # redimensionnement
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def on_canvas_click(self, event):
        """Detecte sur quel carre on a clique et bascule son etat."""
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE

        if 0 <= x < MATRIX_WIDTH and 0 <= y < MATRIX_HEIGHT:
            self.led_state[y][x] = not self.led_state[y][x]
            rect = self.rects[y][x]
            if self.led_state[y][x]:
                self.canvas.itemconfig(rect, fill="deep sky blue")  # LED bleue
            else:
                self.canvas.itemconfig(rect, fill="black")

    def clear_matrix(self):
        """Eteint toutes les LEDs."""
        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):
                self.led_state[y][x] = False
                rect = self.rects[y][x]
                self.canvas.itemconfig(rect, fill="black")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Matrice effacee.\n")

    def generer_mots(self):
        """Calcule les 4 mots de 32 bits a partir de l'etat de la matrice."""
        out = [0, 0, 0, 0]

        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):
                if  self.led_state[y][x]:
                    

                    index = y * MATRIX_WIDTH + x   # 0..103
                    mot = index // 32             # 0..3
                    bit = index % 32              # 0..31

                    out[mot] |= (1 << bit)

        # Affichage du resultat directement sous forme de tableau C
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", "// Tableau a transmettre a matrixWrite()\n")
        self.result_text.insert("end", "const uint32_t frame[4] = {\n")
        for i, val in enumerate(out):
            comma = "," if i < 3 else ""
            self.result_text.insert("end", f"    0x{val:08X}{comma}\n")
        self.result_text.insert("end", "};\n")

    def copy_to_clipboard(self):
        """Copie le contenu de la zone de texte dans le presse-papiers."""
        content = self.result_text.get("1.0", "end").strip()
        if not content:
            return
        self.clipboard_clear()
        self.clipboard_append(content)

if __name__ == "__main__":
    app = MatrixEditor()
    app.mainloop()

