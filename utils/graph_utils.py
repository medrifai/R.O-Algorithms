import networkx as nx
import numpy as np
import tkinter as tk
from tkinter import messagebox 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config.settings import GRAPH_SETTINGS, ALGORITHM_COLORS

class GraphVisualizer:
    def __init__(self):
        self.window = None
        self.fig = None

    def _create_window(self, title):
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("800x800")
        
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        plt.clf()  # Nettoyer la figure précédente
        self.fig, self.ax = plt.subplots(figsize=GRAPH_SETTINGS['FIGURE_SIZE'])
        return main_frame, self.ax  # Retourner aussi l'axe

    def _add_info_and_close(self, main_frame, info_text):
        # Vérification si main_frame est un tuple
        if isinstance(main_frame, tuple):
            main_frame = main_frame[0]

        canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Ajouter les informations
        info_label = tk.Label(main_frame, text=info_text, 
                            font=("Arial", 12), wraplength=700)
        info_label.pack(pady=10)

        # Bouton de fermeture
        close_button = tk.Button(main_frame, text="Fermer",
                                command=self.window.destroy)
        close_button.pack(pady=10)


    def display_welsh_powell(self, G, colors, num_colors):
        main_frame = self._create_window("Coloration de graphe - Welsh Powell")
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_color=[colors[node] for node in G.nodes()],
               with_labels=True, node_size=GRAPH_SETTINGS['NODE_SIZE'],
               cmap=plt.cm.rainbow)
        self._add_info_and_close(main_frame, f"Nombre de couleurs utilisées: {num_colors}")

    def display_dijkstra(self, G, path, path_length):
        main_frame = self._create_window("Plus court chemin - Dijkstra")
        pos = nx.spring_layout(G)
        
        nx.draw_networkx_edges(G, pos, alpha=0.2)
        nx.draw_networkx_nodes(G, pos, node_size=GRAPH_SETTINGS['NODE_SIZE'],
                             node_color=ALGORITHM_COLORS['dijkstra']['node_default'])
        
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                             edge_color=ALGORITHM_COLORS['dijkstra']['path_highlight'],
                             width=GRAPH_SETTINGS['EDGE_WIDTH'])
        
        nx.draw_networkx_labels(G, pos)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        
        info_text = f"Plus court chemin: {' -> '.join(map(str, path))}\nDistance totale: {path_length}"
        self._add_info_and_close(main_frame, info_text)

    def display_kruskal(self, G, mst_edges, total_weight):
        main_frame = self._create_window("Arbre couvrant minimal - Kruskal")
        pos = nx.spring_layout(G)
        
        nx.draw_networkx_edges(G, pos, alpha=0.2)
        nx.draw_networkx_nodes(G, pos, node_size=GRAPH_SETTINGS['NODE_SIZE'])
        
        mst_edge_list = [(u, v) for u, v, _ in mst_edges]
        nx.draw_networkx_edges(G, pos, edgelist=mst_edge_list,
                             edge_color=ALGORITHM_COLORS['kruskal']['mst_highlight'],
                             width=GRAPH_SETTINGS['EDGE_WIDTH'])
        
        nx.draw_networkx_labels(G, pos)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        
        info_text = f"Coût total de l'arbre couvrant minimal: {total_weight}"
        self._add_info_and_close(main_frame, info_text)

    def display_bellman_ford(self, G, distances, predecessors):
        main_frame = self._create_window("Plus court chemin - Bellman-Ford")
        pos = nx.spring_layout(G)
        
        # Dessin des arêtes du graphe
        nx.draw_networkx_edges(G, pos, alpha=0.2)
        nx.draw_networkx_nodes(G, pos, node_size=GRAPH_SETTINGS['NODE_SIZE'],
                            node_color=ALGORITHM_COLORS['bellman_ford']['node_default'])
        
        # Vérification et conversion des données si nécessaire
        if isinstance(distances, list):
            distances_dict = {i: dist for i, dist in enumerate(distances)}
        else:
            distances_dict = distances
            
        if not isinstance(predecessors, dict):
            if isinstance(predecessors, list):
                predecessors_dict = {i: pred for i, pred in enumerate(predecessors) if pred is not None}
            else:
                predecessors_dict = {}
        else:
            predecessors_dict = predecessors
        
        # Affichage des chemins les plus courts
        for node in G.nodes:
            if node in predecessors_dict:
                path = []
                current_node = node
                
                # Remonter les prédécesseurs jusqu'à la source
                while current_node is not None and current_node in predecessors_dict:
                    path.append(current_node)
                    current_node = predecessors_dict.get(current_node)
                if current_node is not None:
                    path.append(current_node)
                path.reverse()
                
                # Affichage des arêtes du chemin le plus court
                if len(path) > 1:
                    path_edges = list(zip(path[:-1], path[1:]))
                    nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                                        edge_color=ALGORITHM_COLORS['bellman_ford']['path_highlight'],
                                        width=GRAPH_SETTINGS['EDGE_WIDTH'])
        
        # Dessiner les étiquettes des noeuds
        nx.draw_networkx_labels(G, pos)
        
        # Affichage des poids des arêtes
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        
        # Texte d'information sur les distances
        info_text = "Distances minimales depuis la source :\n"
        for node, dist in distances_dict.items():
            info_text += f"{node}: {dist}\n"
        
        self._add_info_and_close(main_frame, info_text)


    def display_ford_fulkerson(self, G, flow_dict, flow_value, partition):
        main_frame = self._create_window("Flot maximum - Ford-Fulkerson")
        pos = nx.spring_layout(G)
        reachable, non_reachable = partition
        
        nx.draw_networkx_nodes(G, pos, nodelist=reachable,
                             node_color=ALGORITHM_COLORS['ford_fulkerson']['source_node'],
                             node_size=GRAPH_SETTINGS['NODE_SIZE'])
        nx.draw_networkx_nodes(G, pos, nodelist=non_reachable,
                             node_color=ALGORITHM_COLORS['ford_fulkerson']['sink_node'],
                             node_size=GRAPH_SETTINGS['NODE_SIZE'])
        
        nx.draw_networkx_edges(G, pos,
                             edge_color=ALGORITHM_COLORS['ford_fulkerson']['edge_default'],
                             arrows=True, arrowsize=20)
        
        nx.draw_networkx_labels(G, pos)
        
        edge_labels = {}
        for u, v, data in G.edges(data=True):
            flow = flow_dict[u][v]
            capacity = data['capacity']
            edge_labels[(u, v)] = f'{flow}/{capacity}'
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        info_text = f"Flot maximum: {flow_value}"
        self._add_info_and_close(main_frame, info_text)
        
    def display_transport_solution(self, supply, demand, costs, solution, total_cost, method_name):
        """
        Affiche la solution du problème de transport avec le nom de la méthode utilisée.
        
        Args:
            method_name: str - 'nord_ouest', 'moindre_cout', ou 'stepping_stone'
        """
        method_titles = {
            'nord_ouest': 'Méthode du Nord-Ouest',
            'moindre_cout': 'Méthode du Moindre Coût',
            'stepping_stone': 'Méthode du Stepping Stone'
        }
        
        title = method_titles.get(method_name, 'Solution du problème de transport')
        main_frame, ax = self._create_window(title)
        
        # Préparer les données du tableau
        cell_text = []
        col_labels = ['Sources'] + [f'D{j+1}' for j in range(len(demand))] + ['Offre']
        
        # Données des cellules avec coûts et quantités
        total_allocated = 0
        for i in range(len(supply)):
            row = [f'S{i+1}']
            row_cost = 0
            row_quantity = 0
            for j in range(len(demand)):
                quantity = solution[i][j]
                cost = costs[i][j]
                cell_cost = quantity * cost
                row_cost += cell_cost
                row_quantity += quantity
                row.append(f'{quantity}\n({cost})\n={cell_cost}')
            row.append(f'{supply[i]}\n({row_cost})')
            total_allocated += row_quantity
            cell_text.append(row)
        
        # Ligne de demande avec totaux
        demand_row = ['Demande']
        for j in range(len(demand)):
            col_cost = sum(solution[i][j] * costs[i][j] for i in range(len(supply)))
            demand_row.append(f'{demand[j]}\n({col_cost})')
        demand_row.append(f'{sum(demand)}\n({total_cost})')
        cell_text.append(demand_row)
        
        # Créer et personnaliser le tableau
        table = ax.table(cellText=cell_text,
                        colLabels=col_labels,
                        loc='center',
                        cellLoc='center',
                        bbox=[0.1, 0.1, 0.8, 0.8])
        
        # Personnalisation
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)
        
        # Masquer les axes
        ax.axis('off')
        
        # Titre
        ax.set_title(f"Solution du problème de transport - {title}")
        
        # Information détaillée selon la méthode
        method_info = {
            'nord_ouest': "Allocation séquentielle depuis le coin nord-ouest",
            'moindre_cout': "Allocation prioritaire aux coûts minimaux",
            'stepping_stone': "Solution optimisée par la méthode du Stepping Stone"
        }
        
        info_text = (
            f"Méthode utilisée: {title}\n"
            f"{method_info.get(method_name, '')}\n"
            f"Coût total de transport: {total_cost}\n"
            f"Quantité totale transportée: {total_allocated}\n"
            f"Coût moyen par unité: {total_cost/total_allocated:.2f}\n"
            f"Offre totale: {sum(supply)}\n"
            f"Demande totale: {sum(demand)}"
        )
        
        self._add_info_and_close(main_frame, info_text)
        
    def display_potentiel_metra(self, tasks, early_dates, project_duration):
        main_frame, ax = self._create_window("Potentiel Metra - Diagramme PERT")
        
        # Créer un graphe dirigé
        G = nx.DiGraph()
        
        # Créer les nœuds pour chaque événement (il y a n+1 événements pour n tâches)
        num_events = len(tasks) + 1
        for i in range(num_events):
            G.add_node(i)
        
        # Ajouter les arcs (tâches)
        for i, task in enumerate(tasks):
            G.add_edge(i, i+1, 
                    task=task,
                    duration=early_dates[i])
        
        # Positionner les nœuds de gauche à droite
        pos = {}
        for i in range(num_events):
            pos[i] = (i * 2, 0)  # Espacement horizontal régulier
        
        # Dessiner les nœuds (événements)
        nx.draw_networkx_nodes(G, pos,
                            node_color='white',
                            node_size=1500,
                            edgecolors='black')
        
        # Dessiner les arcs (tâches)
        nx.draw_networkx_edges(G, pos,
                            edge_color='black',
                            arrows=True,
                            arrowsize=20)
        
        # Labels des nœuds
        node_labels = {i: f"E{i}" for i in range(num_events)}
        nx.draw_networkx_labels(G, pos, node_labels, font_size=10)
        
        # Labels des arcs (tâches et durées)
        edge_labels = {}
        for i, (task, duration) in enumerate(zip(tasks, early_dates)):
            edge_labels[(i, i+1)] = f"{task}\n{duration}j"
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
        
        plt.title("Diagramme PERT")
        
        info_text = (
            f"Nombre de tâches: {len(tasks)}\n"
            f"Durée totale du projet: {project_duration} jours\n"
            "Les nœuds représentent les événements\n"
            "Les arcs représentent les tâches avec leurs durées"
        )
        
        self._add_info_and_close(main_frame, info_text)


class GraphGenerator:
    @staticmethod
    def create_random_graph(num_nodes=8):
        """Crée un graphe aléatoire avec des poids et des capacités."""
        G = nx.gnm_random_graph(num_nodes, num_nodes * 2)
        
        for (u, v) in G.edges():
            G[u][v]['weight'] = np.random.randint(1, 10)
            G[u][v]['capacity'] = np.random.randint(1, 10)
        
        return G

    @staticmethod
    def load_graph_from_file(filename):
        """Charge un graphe depuis un fichier GraphML."""
        try:
            return nx.read_graphml(filename)
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement du graphe : {str(e)}")