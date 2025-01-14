import tkinter as tk
from tkinter import ttk
from config.settings import GUI_SETTINGS
from gui.dialogs import (WelshPowellDialog, DijkstraDialog, KruskalDialog,
                        FordFulkersonDialog, PotentielMetraDialog,
                        TransportDialog)

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title(GUI_SETTINGS['WINDOW_TITLE'])
        self.root.geometry(GUI_SETTINGS['WINDOW_SIZE'])
        self.root.config(bg=GUI_SETTINGS['BACKGROUND_COLOR'])
        self.create_main_frame()

    def create_main_frame(self):
        """Crée la fenêtre principale de l'application"""
        # Titre principal
        title = tk.Label(
            self.root,
            text="Interface Graphique Tkinter GUI",
            font=GUI_SETTINGS['TITLE_FONT'],
            fg="#8B0000",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        )
        title.pack(pady=20)

        # Cadre pour le menu d'entrée
        frame = tk.Frame(
            self.root,
            bg=GUI_SETTINGS['FRAME_COLOR'],
            bd=3,
            relief="solid"
        )
        frame.pack(pady=20, padx=50)

        # Sous-titre dans le cadre
        subtitle = tk.Label(
            frame,
            text="Algorithmes de Recherche Opérationnelle",
            font=GUI_SETTINGS['SUBTITLE_FONT'],
            fg="black",
            bg="#FFC0CB"
        )
        subtitle.pack(pady=10, padx=20)

        # Boutons Entrée et Sortie
        button_frame = tk.Frame(frame, bg="#FFC0CB")
        button_frame.pack(pady=20)

        btn_entree = tk.Button(
            button_frame,
            text="Entrée",
            font=GUI_SETTINGS['BUTTON_FONT'],
            bg=GUI_SETTINGS['BUTTON_COLOR'],
            fg="black",
            width=15,
            height=2,
            relief="groove",
            command=self.afficher_algorithmes
        )
        btn_entree.grid(row=0, column=0, padx=10)

        btn_sortie = tk.Button(
            button_frame,
            text="Sortie",
            font=GUI_SETTINGS['BUTTON_FONT'],
            bg=GUI_SETTINGS['BUTTON_COLOR'],
            fg="black",
            width=15,
            height=2,
            relief="groove",
            command=self.root.quit
        )
        btn_sortie.grid(row=0, column=1, padx=10)

    def afficher_algorithmes(self):
        """Affiche la liste des algorithmes disponibles"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Titre principal
        title = tk.Label(
            self.root,
            text="Liste des Algorithmes",
            font=GUI_SETTINGS['TITLE_FONT'],
            fg="#8B0000",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        )
        title.pack(pady=20)

        # Cadre pour les boutons des algorithmes
        frame_algos = tk.Frame(
            self.root,
            bg=GUI_SETTINGS['FRAME_COLOR'],
            bd=3,
            relief="solid"
        )
        frame_algos.pack(pady=20, padx=50)

        algorithmes = {
            "Welsh Powell": lambda: WelshPowellDialog(self.root),
            "Dijkstra": lambda: DijkstraDialog(self.root),
            "Kruskal": lambda: KruskalDialog(self.root),
            "Ford Fulkerson": lambda: FordFulkersonDialog(self.root),
            "Potentiel METRA": lambda: PotentielMetraDialog(self.root),
            "Nord-Ouest": lambda: TransportDialog(self.root, "nord_ouest"),
            "Moindre Coût": lambda: TransportDialog(self.root, "moindre_cout"),
            "Stepping-Stone": lambda: TransportDialog(self.root, "stepping_stone")
        }

        # Ajouter les boutons dans une grille
        for i, (algo, command) in enumerate(algorithmes.items()):
            btn_algo = tk.Button(
                frame_algos,
                text=algo,
                font=GUI_SETTINGS['BUTTON_FONT'],
                bg=GUI_SETTINGS['BUTTON_COLOR'],
                fg="teal",
                width=20,
                height=2,
                relief="groove",
                command=command
            )
            btn_algo.grid(row=i//3, column=i%3, padx=10, pady=10)