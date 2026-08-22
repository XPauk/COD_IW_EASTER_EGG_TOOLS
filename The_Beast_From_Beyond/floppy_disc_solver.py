import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path

# ------------------------------------------------------------
# Beast From Beyond - Floppy Disk Icon Solver
#
# ICON INDEXING:
# 0  = original picture_1  (symbol "1" on the cheat sheet)
# 1  = original picture_2  (symbol "2")
# 2  = original picture_3  (symbol "3")
# 3  = original picture_4  (symbol "4")
# 4  = original picture_5  (symbol "6")
# 5  = original picture_6  (symbol "7")
# 6  = original picture_7  (symbol "A")
# 7  = original picture_8  (symbol "8")
# 8  = original picture_9  (symbol "9")
# 9  = original picture_10 (symbol "B")
# 10 = original picture_11 (symbol "C")
# 11 = original picture_0  (symbol "5")
#
# Put the PNGs into a folder and name them:
# icon_0.png ... icon_11.png
# ------------------------------------------------------------

ICON_FILES = [f"Floppy_Icon_{i}.png" for i in range(12)]

# Six rows from the known Floppy Disk cheat sheet.
# Each row defines the LEFT -> RIGHT order of its six symbols.
SEQUENCES = [
    [1, 2, 3, 4, 0, 5],
    [6, 5, 8, 9, 7, 1],
    [9, 10, 7, 8, 6, 1],
    [9, 4, 3, 0, 5, 2],
    [1, 11, 3, 2, 0, 5],
    [4, 11, 0, 2, 5, 8],
]

MAX_SELECTION = 4
ICON_SIZE = 88
RESULT_ICON_SIZE = 135


class FloppySolverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Beast From Beyond - Floppy Disk Solver")
        self.geometry("1050x760")
        self.minsize(900, 680)

        self.icon_dir = Path(__file__).resolve().parent / "icons"
        self.selected = []
        self.images = {}
        self.result_images = {}
        self.buttons = {}

        self._build_ui()
        self.load_icons()

    def _build_ui(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        top = ttk.Frame(self, padding=14)
        top.pack(fill="x")

        title = ttk.Label(
            top,
            text="Floppy Disk Solver",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(side="left")

        ttk.Button(
            top,
            text="Icon-Ordner auswählen",
            command=self.choose_icon_folder
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            top,
            text="6 Lösungen anzeigen",
            command=self.show_solutions
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            top,
            text="Reset",
            command=self.reset
        ).pack(side="right")

        explanation = ttk.Label(
            self,
            text=(
                "Wähle die 4 Symbole aus, die du im Spiel hast. "
                "Die Reihenfolge deiner Klicks ist egal. "
                "Das Tool ordnet sie anhand der sechs bekannten Reihen."
            ),
            font=("Segoe UI", 11),
            wraplength=900,
            justify="center",
        )
        explanation.pack(pady=(0, 12))

        self.status = ttk.Label(
            self,
            text="Wähle 4 Symbole.",
            font=("Segoe UI", 12, "bold")
        )
        self.status.pack(pady=(0, 8))

        self.icon_frame = ttk.Frame(self, padding=10)
        self.icon_frame.pack()

        for i in range(12):
            btn = tk.Button(
                self.icon_frame,
                text=str(i),
                relief="raised",
                bd=3,
                padx=4,
                pady=4,
                command=lambda idx=i: self.toggle_icon(idx)
            )
            btn.grid(row=i // 6, column=i % 6, padx=8, pady=8)
            self.buttons[i] = btn

        sep = ttk.Separator(self, orient="horizontal")
        sep.pack(fill="x", padx=28, pady=18)

        self.result_title = ttk.Label(
            self,
            text="Ergebnis",
            font=("Segoe UI", 18, "bold")
        )
        self.result_title.pack()

        self.result_text = ttk.Label(
            self,
            text="Noch keine vier Symbole ausgewählt.",
            font=("Segoe UI", 11),
            justify="center",
            wraplength=900,
        )
        self.result_text.pack(pady=(4, 10))

        self.result_frame = ttk.Frame(self, padding=6)
        self.result_frame.pack()

    def choose_icon_folder(self):
        folder = filedialog.askdirectory(
            title="Ordner mit icon_0.png bis icon_11.png auswählen"
        )
        if folder:
            self.icon_dir = Path(folder)
            self.load_icons()

    def load_icons(self):
        self.images.clear()
        missing = []

        for idx, filename in enumerate(ICON_FILES):
            path = self.icon_dir / filename
            if not path.exists():
                missing.append(filename)
                self.buttons[idx].configure(
                    image="",
                    text=f"Icon {idx}\n({filename})"
                )
                continue

            try:
                img = Image.open(path).convert("RGBA")
                img.thumbnail((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)

                # Put the icon onto a consistent transparent/white canvas.
                canvas = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (255, 255, 255, 0))
                x = (ICON_SIZE - img.width) // 2
                y = (ICON_SIZE - img.height) // 2
                canvas.alpha_composite(img, (x, y))

                photo = ImageTk.PhotoImage(canvas)
                self.images[idx] = photo
                self.buttons[idx].configure(image=photo, text="", compound="center")
            except Exception as exc:
                missing.append(filename)
                self.buttons[idx].configure(
                    image="",
                    text=f"Fehler\nIcon {idx}"
                )
                print(f"Could not load {path}: {exc}")

        if missing:
            self.status.configure(
                text=(
                    f"Icon-Ordner: {self.icon_dir} — "
                    f"{12 - len(missing)}/12 PNGs geladen."
                )
            )
        else:
            self.status.configure(
                text=f"Alle 12 PNGs geladen. Wähle 4 Symbole."
            )

        self.update_button_states()

    def toggle_icon(self, idx):
        if idx in self.selected:
            self.selected.remove(idx)
        else:
            if len(self.selected) >= MAX_SELECTION:
                return
            self.selected.append(idx)

        self.update_button_states()

        if len(self.selected) == MAX_SELECTION:
            self.solve()
        else:
            self.clear_result()
            remaining = MAX_SELECTION - len(self.selected)
            self.status.configure(
                text=f"Noch {remaining} Symbol{'e' if remaining != 1 else ''} auswählen."
            )

    def update_button_states(self):
        for idx, btn in self.buttons.items():
            if idx in self.selected:
                btn.configure(
                    relief="sunken",
                    bd=6,
                    bg="#7fb3ff",
                    activebackground="#7fb3ff",
                    highlightthickness=5,
                    highlightbackground="#005eff",
                    highlightcolor="#005eff"
                )
            else:
                btn.configure(
                    relief="raised",
                    bd=2,
                    bg="#f0f0f0",
                    activebackground="#e6e6e6",
                    highlightthickness=2,
                    highlightbackground="#b8b8b8",
                    highlightcolor="#b8b8b8"
                )

    def solve(self):
        selected_set = set(self.selected)

        matches = []
        for row_index, sequence in enumerate(SEQUENCES, start=1):
            if selected_set.issubset(sequence):
                ordered = [icon for icon in sequence if icon in selected_set]
                matches.append((row_index, ordered))

        if not matches:
            self.status.configure(text="Keine passende Reihe gefunden.")
            self.result_text.configure(
                text=(
                    "Diese Kombination aus vier Symbolen kommt in keiner "
                    "der hinterlegten sechs Reihen vor."
                )
            )
            self.clear_result_icons()
            return

        # Remove duplicate result orders. Different six-symbol rows can
        # theoretically contain the same four symbols in the same order.
        unique = []
        seen_orders = set()
        for row_index, ordered in matches:
            key = tuple(ordered)
            if key not in seen_orders:
                seen_orders.add(key)
                unique.append((row_index, ordered))

        if len(unique) == 1:
            row_index, ordered = unique[0]
            self.status.configure(text=f"Passende Reihe: {row_index}")
            self.result_text.configure(
                text="Korrekte Reihenfolge: " + " → ".join(map(str, ordered))
            )
            self.draw_result(ordered)
        else:
            # Rare ambiguity: show all possible orderings rather than silently
            # choosing the wrong row.
            self.status.configure(
                text=f"{len(unique)} mögliche Reihen gefunden."
            )
            descriptions = [
                f"Reihe {row}: " + " → ".join(map(str, order))
                for row, order in unique
            ]
            self.result_text.configure(
                text=(
                    "Diese vier Symbole passen zu mehreren Reihen:\n"
                    + "\n".join(descriptions)
                )
            )
            # Display the first possibility visually.
            self.draw_result(unique[0][1])

    def draw_result(self, ordered):
        self.clear_result_icons()
        self.result_images.clear()

        for col, idx in enumerate(ordered):
            path = self.icon_dir / ICON_FILES[idx]

            if path.exists():
                try:
                    img = Image.open(path).convert("RGBA")
                    img.thumbnail(
                        (RESULT_ICON_SIZE, RESULT_ICON_SIZE),
                        Image.Resampling.LANCZOS
                    )
                    photo = ImageTk.PhotoImage(img)
                    self.result_images[idx, col] = photo

                    label = ttk.Label(
                        self.result_frame,
                        image=photo,
                        text=f"\nIcon {idx}",
                        compound="top",
                        font=("Segoe UI", 10, "bold")
                    )
                except Exception:
                    label = ttk.Label(
                        self.result_frame,
                        text=f"Icon {idx}",
                        font=("Segoe UI", 14, "bold")
                    )
            else:
                label = ttk.Label(
                    self.result_frame,
                    text=f"Icon {idx}",
                    font=("Segoe UI", 14, "bold")
                )

            label.grid(row=0, column=col * 2, padx=8, pady=4)

            if col < len(ordered) - 1:
                arrow = ttk.Label(
                    self.result_frame,
                    text="→",
                    font=("Segoe UI", 24, "bold")
                )
                arrow.grid(row=0, column=col * 2 + 1, padx=2)

    def clear_result_icons(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

    def clear_result(self):
        self.result_text.configure(text="Noch keine vier Symbole ausgewählt.")
        self.clear_result_icons()

    def show_solutions(self):
        win = tk.Toplevel(self)
        win.title("Die 6 möglichen Reihenfolgen")
        win.resizable(False, False)
        win.transient(self)

        outer = ttk.Frame(win, padding=16)
        outer.pack(fill="both", expand=True)

        title = ttk.Label(
            outer,
            text="Die 6 vollständigen Lösungen",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=(0, 12))

        info = ttk.Label(
            outer,
            text=(
                "Jede Zeile zeigt die komplette Reihenfolge der 6 Symbole "
                "von links nach rechts."
            ),
            font=("Segoe UI", 10),
            justify="center"
        )
        info.pack(pady=(0, 14))

        grid = ttk.Frame(outer)
        grid.pack()

        # Keep PhotoImage references alive for the lifetime of the window.
        win.solution_images = []

        for row_idx, sequence in enumerate(SEQUENCES):
            row_label = ttk.Label(
                grid,
                text=f"Reihe {row_idx + 1}:",
                font=("Segoe UI", 11, "bold")
            )
            row_label.grid(row=row_idx, column=0, padx=(0, 12), pady=8, sticky="e")

            for col, icon_idx in enumerate(sequence, start=1):
                path = self.icon_dir / ICON_FILES[icon_idx]

                if path.exists():
                    try:
                        img = Image.open(path).convert("RGBA")
                        img.thumbnail((58, 58), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        win.solution_images.append(photo)

                        label = ttk.Label(grid, image=photo)
                        label.grid(row=row_idx, column=col, padx=4, pady=4)
                    except Exception:
                        ttk.Label(
                            grid,
                            text=str(icon_idx),
                            font=("Segoe UI", 11, "bold")
                        ).grid(row=row_idx, column=col, padx=8, pady=4)
                else:
                    ttk.Label(
                        grid,
                        text=str(icon_idx),
                        font=("Segoe UI", 11, "bold")
                    ).grid(row=row_idx, column=col, padx=8, pady=4)

        ttk.Button(
            outer,
            text="Schließen",
            command=win.destroy
        ).pack(pady=(16, 0))

    def reset(self):
        self.selected.clear()
        self.update_button_states()
        self.clear_result()
        self.status.configure(text="Wähle 4 Symbole.")

if __name__ == "__main__":
    app = FloppySolverApp()
    app.mainloop()
