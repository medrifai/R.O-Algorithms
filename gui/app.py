import tkinter as tk
from tkinter import ttk
from config.settings import *
from gui.dialogs import (WelshPowellDialog, DijkstraDialog, KruskalDialog,
                        FordFulkersonDialog, PotentielMetraDialog, 
                        NordOuestDialog, MoindreCoutDialog, SteppingStoneDialog)

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Graphique Tkinter")
        self.root.geometry(WINDOW_SIZE)
        self.root.config(bg=BACKGROUND_COLOR)
        self.create_main_frame()

    def create_main_frame(self):
        title = tk.Label(
            self.root,
            text="Interface Graphique Tkinter GUI",
            font=("Arial", 20, "bold"),
            fg=TITLE_COLOR,
            bg=BACKGROUND_COLOR
        )
        title.pack(pady=20)

        frame = tk.Frame(self.root, bg=FRAME_COLOR, bd=3, relief="solid")
        frame.pack(pady=20, padx=50)

        subtitle = tk.Label(
            frame,
            text="Algorithme de Recherche Opérationnelle",
            font=("Arial", 14, "bold"),
            fg="black",
            bg="#FFC0CB"
        )
        subtitle.pack(pady=10, padx=20)

        self.create_buttons(frame)

    def create_buttons(self, frame):
        button_frame = tk.Frame(frame, bg="#FFC0CB")
        button_frame.pack(pady=20)

        buttons = [
            ("Entrée", self.afficher_algorithmes),
            ("Sortie", self.root.quit)
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg=BUTTON_COLOR,
                fg=BUTTON_TEXT_COLOR,
                width=15,
                height=2,
                relief="groove",
                command=command
            )
            btn.pack(side=tk.LEFT, padx=10)

    def afficher_algorithmes(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.root,
            text="Liste des Algorithmes",
            font=("Arial", 20, "bold"),
            fg=TITLE_COLOR,
            bg=BACKGROUND_COLOR
        )
        title.pack(pady=20)

        frame_algos = tk.Frame(self.root, bg=FRAME_COLOR, bd=3, relief="solid")
        frame_algos.pack(pady=20, padx=50)

        algorithms = {
            "Welsh Powell": WelshPowellDialog,
            "Dijkstra": DijkstraDialog,
            "Kruskal": KruskalDialog,
            "Ford Fulkerson": FordFulkersonDialog,
            "Potentiel Metra": PotentielMetraDialog,
            "Nord-Ouest": NordOuestDialog,
            "Moindre Coût": MoindreCoutDialog,
            "Stepping-Stone": SteppingStoneDialog
        }

        for i, (algo_name, dialog_class) in enumerate(algorithms.items()):
            btn = tk.Button(
                frame_algos,
                text=algo_name,
                font=("Arial", 12, "bold"),
                bg=BUTTON_COLOR,
                fg="teal",
                width=20,
                height=2,
                relief="groove",
                command=lambda d=dialog_class: d(self.root)
            )
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)