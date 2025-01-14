from tkinter import ttk, messagebox
import tkinter as tk
from algorithms.graph_algorithms import *
from algorithms.transport import *
from utils.graph_utils import create_and_display_graph

class BaseDialog:
    def __init__(self, root):
        self.dialog = tk.Toplevel(root)
        self.dialog.geometry("300x200")
        self.dialog.config(bg="#FFE4F2")
        self.setup_dialog()

    def setup_dialog(self):
        raise NotImplementedError("Subclasses must implement setup_dialog")

class WelshPowellDialog(BaseDialog):
    def setup_dialog(self):
        self.dialog.title("Welsh Powell - Paramètres")
        tk.Label(self.dialog, text="Nombre de sommets:", bg="#FFE4F2").pack(pady=10)
        self.vertices_entry = tk.Entry(self.dialog)
        self.vertices_entry.pack(pady=5)

        tk.Button(self.dialog, text="Générer", command=self.generate_graph).pack(pady=20)

    def generate_graph(self):
        try:
            num_vertices = int(self.vertices_entry.get())
            if num_vertices <= 0:
                raise ValueError("Le nombre de sommets doit être positif")
            create_and_display_graph(num_vertices, "welsh_powell")
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

class DijkstraDialog(BaseDialog):
    def setup_dialog(self):
        self.dialog.title("Dijkstra - Paramètres")
        tk.Label(self.dialog, text="Sommet de départ:", bg="#FFE4F2").pack(pady=5)
        self.start_entry = tk.Entry(self.dialog)
        self.start_entry.pack(pady=5)

        tk.Label(self.dialog, text="Sommet d'arrivée:", bg="#FFE4F2").pack(pady=5)
        self.end_entry = tk.Entry(self.dialog)
        self.end_entry.pack(pady=5)

        tk.Button(self.dialog, text="Calculer", command=self.calculate_path).pack(pady=10)

    def calculate_path(self):
        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
            create_and_display_graph(max(start, end) + 1, "dijkstra", start_node=start, end_node=end)
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides")

class FordFulkersonDialog(BaseDialog):
    def setup_dialog(self):
        self.dialog.title("Ford-Fulkerson - Paramètres")
        tk.Label(self.dialog, text="Source:", bg="#FFE4F2").pack(pady=5)
        self.source_entry = tk.Entry(self.dialog)
        self.source_entry.pack(pady=5)

        tk.Label(self.dialog, text="Puits:", bg="#FFE4F2").pack(pady=5)
        self.sink_entry = tk.Entry(self.dialog)
        self.sink_entry.pack(pady=5)

        tk.Button(self.dialog, text="Calculer", command=self.calculate_flow).pack(pady=10)

    def calculate_flow(self):
        try:
            source = int(self.source_entry.get())
            sink = int(self.sink_entry.get())
            create_and_display_graph(max(source, sink) + 1, "ford_fulkerson", source=source, sink=sink)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides")

class TransportDialog(BaseDialog):
    def setup_dialog(self):
        self.dialog.title("Problème de Transport - Paramètres")
        tk.Label(self.dialog, text="Nombre de sources:", bg="#FFE4F2").pack(pady=5)
        self.sources_entry = tk.Entry(self.dialog)
        self.sources_entry.pack(pady=5)

        tk.Label(self.dialog, text="Nombre de destinations:", bg="#FFE4F2").pack(pady=5)
        self.destinations_entry = tk.Entry(self.dialog)
        self.destinations_entry.pack(pady=5)

        algorithms = ["Nord Ouest", "Moindre Coût", "Stepping Stone"]
        self.selected_algo = tk.StringVar(value=algorithms[0])
        tk.OptionMenu(self.dialog, self.selected_algo, *algorithms).pack(pady=5)

        tk.Button(self.dialog, text="Générer", command=self.generate_problem).pack(pady=10)

    def generate_problem(self):
        try:
            sources = int(self.sources_entry.get())
            destinations = int(self.destinations_entry.get())
            if sources <= 0 or destinations <= 0:
                raise ValueError("Les nombres doivent être positifs")
            
            algorithm = self.selected_algo.get().lower().replace(" ", "_")
            create_and_display_graph(0, algorithm, sources=sources, destinations=destinations)
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

class BellmanFordDialog(BaseDialog):
    def setup_dialog(self):
        self.dialog.title("Bellman-Ford - Paramètres")
        tk.Label(self.dialog, text="Sommet de départ:", bg="#FFE4F2").pack(pady=5)
        self.start_entry = tk.Entry(self.dialog)
        self.start_entry.pack(pady=5)

        tk.Button(self.dialog, text="Calculer", command=self.calculate_distances).pack(pady=10)

    def calculate_distances(self):
        try:
            start = int(self.start_entry.get())
            create_and_display_graph(start + 5, "bellman_ford", start_node=start)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide")

class PotentielMetraDialog(BaseDialog):
    def setup_dialog(self):
        self.dialog.title("Potentiel METRA - Paramètres")
        tk.Label(self.dialog, text="Nombre d'activités:", bg="#FFE4F2").pack(pady=5)
        self.activities_entry = tk.Entry(self.dialog)
        self.activities_entry.pack(pady=5)

        tk.Button(self.dialog, text="Générer", command=self.generate_network).pack(pady=10)

    def generate_network(self):
        try:
            activities = int(self.activities_entry.get())
            if activities <= 0:
                raise ValueError("Le nombre d'activités doit être positif")
            create_and_display_graph(activities, "potentiel_metra")
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))