import random
import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import GUI_SETTINGS, ERROR_MESSAGES
from utils.graph_utils import GraphVisualizer
from algorithms.graph_algorithms import GraphAlgorithms
from algorithms.transport import TransportAlgorithms

class BaseDialog:
    def __init__(self, parent, title):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x200")
        self.dialog.config(bg=GUI_SETTINGS['BACKGROUND_COLOR'])
        self.setup_ui()

    def setup_ui(self):
        pass

    def validate_input(self):
        pass

class WelshPowellDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Welsh Powell - Paramètres")

    def setup_ui(self):
        tk.Label(
            self.dialog,
            text="Nombre de sommets:",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        
        self.vertices_entry = tk.Entry(self.dialog)
        self.vertices_entry.pack(pady=5)

        tk.Button(
            self.dialog,
            text="Générer",
            command=self.generate_graph
        ).pack(pady=20)

    def generate_graph(self):
        try:
            num_vertices = int(self.vertices_entry.get())
            if num_vertices <= 0:
                raise ValueError(ERROR_MESSAGES['invalid_vertices'])

            G = GraphAlgorithms.generate_random_graph(num_vertices, "welsh_powell")
            colors, num_colors = GraphAlgorithms.welsh_powell(G)
            
            visualizer = GraphVisualizer()
            visualizer.display_welsh_powell(G, colors, num_colors)
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

class DijkstraDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Dijkstra - Paramètres")

    def setup_ui(self):
        # Nombre de sommets
        tk.Label(
            self.dialog,
            text="Nombre de sommets:",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        self.vertices_entry = tk.Entry(self.dialog)
        self.vertices_entry.pack(pady=5)

        # Sommet de départ
        tk.Label(
            self.dialog,
            text="Sommet de départ (X0, X1, ...):",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        self.start_entry = tk.Entry(self.dialog)
        self.start_entry.pack(pady=5)

        # Sommet d'arrivée
        tk.Label(
            self.dialog,
            text="Sommet d'arrivée (X0, X1, ...):",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        self.end_entry = tk.Entry(self.dialog)
        self.end_entry.pack(pady=5)

        tk.Button(
            self.dialog,
            text="Générer",
            command=self.generate_graph
        ).pack(pady=20)

    def generate_graph(self):
        try:
            num_vertices = int(self.vertices_entry.get())
            if num_vertices <= 0:
                raise ValueError(ERROR_MESSAGES['invalid_vertices'])

            start_node = self.start_entry.get()
            end_node = self.end_entry.get()

            if not start_node.startswith('X') or not end_node.startswith('X'):
                raise ValueError(ERROR_MESSAGES['invalid_node_format'])

            start_index = int(start_node[1:])
            end_index = int(end_node[1:])

            if start_index >= num_vertices or end_index >= num_vertices:
                raise ValueError(ERROR_MESSAGES['invalid_node_index'])

            G = GraphAlgorithms.generate_random_graph(num_vertices, "dijkstra")
            path, path_length = GraphAlgorithms.dijkstra(G, start_node, end_node)

            visualizer = GraphVisualizer()
            visualizer.display_dijkstra(G, path, path_length)
            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            
class BellmanFordDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Bellman-Ford - Paramètres")

    def setup_ui(self):
        # Nombre de sommets
        tk.Label(
            self.dialog,
            text="Nombre de sommets:",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        self.vertices_entry = tk.Entry(self.dialog)
        self.vertices_entry.pack(pady=5)

        # Sommet de départ
        tk.Label(
            self.dialog,
            text="Sommet de départ (X0, X1, ...):",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        self.start_entry = tk.Entry(self.dialog)
        self.start_entry.pack(pady=5)

        # Sommet d'arrivée
        tk.Label(
            self.dialog,
            text="Sommet d'arrivée (X0, X1, ...):",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        self.end_entry = tk.Entry(self.dialog)
        self.end_entry.pack(pady=5)

        # Bouton de génération
        tk.Button(
            self.dialog,
            text="Générer",
            command=self.generate_graph
        ).pack(pady=20)

    def generate_graph(self):
        try:
            num_vertices = int(self.vertices_entry.get())
            if num_vertices <= 0:
                raise ValueError(ERROR_MESSAGES['invalid_vertices'])

            start_node = self.start_entry.get()
            end_node = self.end_entry.get()

            if not start_node.startswith('X') or not end_node.startswith('X'):
                raise ValueError(ERROR_MESSAGES['invalid_node_format'])

            start_index = int(start_node[1:])
            end_index = int(end_node[1:])

            if start_index >= num_vertices or end_index >= num_vertices:
                raise ValueError(ERROR_MESSAGES['invalid_node_index'])

            G = GraphAlgorithms.generate_random_graph(num_vertices, "bellman_ford")
            path, path_length = GraphAlgorithms.bellman_ford(G, start_node, end_node)

            visualizer = GraphVisualizer()
            visualizer.display_bellman_ford(G, path, path_length)
            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

class KruskalDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Kruskal - Paramètres")

    def setup_ui(self):
        tk.Label(
            self.dialog,
            text="Nombre de sommets:",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        
        self.vertices_entry = tk.Entry(self.dialog)
        self.vertices_entry.pack(pady=5)

        tk.Button(
            self.dialog,
            text="Générer",
            command=self.generate_graph
        ).pack(pady=20)

    def generate_graph(self):
        try:
            num_vertices = int(self.vertices_entry.get())
            if num_vertices <= 0:
                raise ValueError(ERROR_MESSAGES['invalid_vertices'])

            G = GraphAlgorithms.generate_random_graph(num_vertices, "kruskal")
            mst_edges, total_weight = GraphAlgorithms.kruskal(G)

            visualizer = GraphVisualizer()
            visualizer.display_kruskal(G, mst_edges, total_weight)
            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

class FordFulkersonDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Ford Fulkerson - Paramètres")

    def setup_ui(self):
        tk.Label(
            self.dialog,
            text="Nombre de sommets:",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        
        self.vertices_entry = tk.Entry(self.dialog)
        self.vertices_entry.pack(pady=5)

        tk.Button(
            self.dialog,
            text="Générer",
            command=self.generate_graph
        ).pack(pady=20)

    def generate_graph(self):
        try:
            num_vertices = int(self.vertices_entry.get())
            if num_vertices <= 0:
                raise ValueError(ERROR_MESSAGES['invalid_vertices'])

            G = GraphAlgorithms.generate_random_graph(num_vertices, "ford_fulkerson")
            flow_value, flow_dict, cut_value, partition = GraphAlgorithms.ford_fulkerson(
                G, 0, num_vertices-1)

            visualizer = GraphVisualizer()
            visualizer.display_ford_fulkerson(G, flow_dict, flow_value, partition)
            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

class PotentielMetraDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Potentiel METRA - Paramètres")

    def setup_ui(self):
        tk.Label(
            self.dialog,
            text="Nombre de tâches:",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        
        self.tasks_entry = tk.Entry(self.dialog)
        self.tasks_entry.pack(pady=5)

        tk.Button(
            self.dialog,
            text="Générer",
            command=self.generate_graph
        ).pack(pady=20)

    def generate_graph(self):
        try:
            num_tasks = int(self.tasks_entry.get())
            if num_tasks <= 0:
                raise ValueError(ERROR_MESSAGES['invalid_vertices'])

            tasks = {}
            for i in range(num_tasks):
                duration = random.randint(1, 10)
                predecessors = [j for j in range(i) if random.random() < 0.3]
                tasks[i] = {'duration': duration, 'predecessors': predecessors}

            early_dates, project_duration = GraphAlgorithms.potentiel_metra(tasks)

            visualizer = GraphVisualizer()
            visualizer.display_potentiel_metra(tasks, early_dates, project_duration)
            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

class TransportDialog(BaseDialog):
    def __init__(self, parent, method):
        self.method = method
        super().__init__(parent, f"{method.replace('_', ' ').title()} - Paramètres")

    def setup_ui(self):
        tk.Label(
            self.dialog,
            text="Nombre de sources:",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        self.sources_entry = tk.Entry(self.dialog)
        self.sources_entry.pack(pady=5)

        tk.Label(
            self.dialog,
            text="Nombre de destinations:",
            bg=GUI_SETTINGS['BACKGROUND_COLOR']
        ).pack(pady=10)
        self.destinations_entry = tk.Entry(self.dialog)
        self.destinations_entry.pack(pady=5)

        tk.Button(
            self.dialog,
            text="Générer",
            command=self.solve_transport
        ).pack(pady=20)

    def solve_transport(self):
        try:
            num_sources = int(self.sources_entry.get())
            num_destinations = int(self.destinations_entry.get())

            if num_sources <= 0 or num_destinations <= 0:
                raise ValueError("Le nombre de sources et de destinations doit être positif")

            # Générer des données aléatoires
            supply = [random.randint(50, 100) for _ in range(num_sources)]
            demand = [random.randint(50, 100) for _ in range(num_destinations)]
            
            # Équilibrer l'offre et la demande
            total_supply = sum(supply)
            total_demand = sum(demand)
            if total_supply > total_demand:
                demand[-1] += total_supply - total_demand
            elif total_demand > total_supply:
                supply[-1] += total_demand - total_supply

            costs = [[random.randint(10, 100) for _ in range(num_destinations)] 
                    for _ in range(num_sources)]

            # Résoudre selon la méthode choisie
            if self.method == "nord_ouest":
                solution, total_cost = TransportAlgorithms.nord_ouest(supply, demand, costs)
            elif self.method == "moindre_cout":
                solution, total_cost = TransportAlgorithms.moindre_cout(supply, demand, costs)
            else:  # stepping_stone
                initial_solution, _ = TransportAlgorithms.nord_ouest(supply, demand, costs)
                solution, total_cost = TransportAlgorithms.stepping_stone(initial_solution, costs)

            # ✅ Définir la méthode utilisée
            method_name = self.method

            # ✅ Appel de la visualisation avec method_name
            visualizer = GraphVisualizer()
            visualizer.display_transport_solution(supply, demand, costs, solution, total_cost, method_name)
            self.dialog.destroy()
        #hhhh
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))