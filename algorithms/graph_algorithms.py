import networkx as nx
import random
from typing import Dict, List, Tuple, Set
from config.settings import GRAPH_SETTINGS

class GraphAlgorithms:
    @staticmethod
    def welsh_powell(G: nx.Graph) -> Dict[int, int]:
        """
        Implémentation corrigée de l'algorithme de Welsh-Powell pour la coloration de graphe.
        """
        # Trier les nœuds par degré décroissant
        nodes = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
        colors = {}
        max_color = 0

        for node in nodes:
            # Obtenir les couleurs utilisées par les voisins
            neighbor_colors = {colors.get(neighbor) for neighbor in G.neighbors(node) 
                             if neighbor in colors}
            
            # Trouver la première couleur disponible
            color = 0
            while color in neighbor_colors:
                color += 1
            
            colors[node] = color
            max_color = max(max_color, color)

        return colors, max_color + 1

    @staticmethod
    def dijkstra(G: nx.Graph, start: str, end: str) -> Tuple[List[str], float]:
        """
        Implémentation corrigée de l'algorithme de Dijkstra.
        """
        try:
            path = nx.dijkstra_path(G, start, end, weight='weight')
            path_length = nx.dijkstra_path_length(G, start, end, weight='weight')
            return path, path_length
        except nx.NetworkXNoPath:
            raise ValueError("Aucun chemin n'existe entre les sommets spécifiés")

    @staticmethod
    def kruskal(G: nx.Graph) -> Tuple[List[Tuple[int, int]], float]:
        """
        Implémentation corrigée de l'algorithme de Kruskal.
        """
        mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
        mst_edges = list(mst.edges(data=True))
        total_weight = sum(data['weight'] for _, _, data in mst_edges)
        return mst_edges, total_weight

    @staticmethod
    def ford_fulkerson(G: nx.DiGraph, source: int, sink: int) -> Tuple[float, Dict]:
        """
        Implémentation corrigée de l'algorithme de Ford-Fulkerson.
        """
        try:
            flow_value, flow_dict = nx.maximum_flow(G, source, sink)
            cut_value, partition = nx.minimum_cut(G, source, sink)
            return flow_value, flow_dict, cut_value, partition
        except nx.NetworkXError:
            raise ValueError("Le graphe doit être dirigé avec des capacités valides")
        
    @staticmethod
    def bellman_ford(G: nx.DiGraph, start: str, end: str) -> Tuple[list, float]:
        """
        Implémentation de l'algorithme de Bellman-Ford pour trouver le plus court chemin.
        """
        try:
            length, path = nx.single_source_bellman_ford(G, source=start, target=end)
            return path, length
        except nx.NetworkXUnbounded:
            raise ValueError("Le graphe contient un cycle de poids négatif.")
        except nx.NetworkXError:
            raise ValueError("Erreur dans les données du graphe. Vérifiez les sommets et les arêtes.")


    @staticmethod
    def potentiel_metra(tasks: Dict[int, Dict]) -> Tuple[Dict[int, int], int]:
        """
        Implémentation corrigée de la méthode METRA (calcul des dates au plus tôt).
        """
        G = nx.DiGraph()
        
        # Créer le graphe
        for task_id, task_info in tasks.items():
            G.add_node(task_id, duration=task_info['duration'])
            for pred in task_info['predecessors']:
                G.add_edge(pred, task_id)

        # Vérifier s'il y a des cycles
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("Le graphe des tâches contient des cycles")

        # Calculer les dates au plus tôt
        early_dates = {0: 0}
        for task in nx.topological_sort(G):
            if task not in early_dates:
                early_dates[task] = 0
            task_duration = tasks[task]['duration']
            for pred in tasks[task]['predecessors']:
                early_dates[task] = max(early_dates[task],
                                      early_dates[pred] + tasks[pred]['duration'])

        # Calculer la durée totale du projet
        project_duration = max(early_dates[task] + tasks[task]['duration'] 
                             for task in tasks)

        return early_dates, project_duration

    @staticmethod
    def generate_random_graph(num_vertices: int, algorithm_type: str) -> nx.Graph:
        """
        Génère un graphe aléatoire adapté à l'algorithme spécifié.
        """
        if algorithm_type == "welsh_powell":
            G = nx.Graph()
            # Assurer la connexité
            for i in range(num_vertices):
                G.add_node(i)
            for i in range(1, num_vertices):
                G.add_edge(i-1, i)
            
            # Ajouter des arêtes aléatoires
            for i in range(num_vertices):
                for j in range(i + 2, num_vertices):
                    if random.random() < GRAPH_SETTINGS['RANDOM_EDGE_PROBABILITY']:
                        G.add_edge(i, j)
            return G

        elif algorithm_type in ["dijkstra", "kruskal"]:
            G = nx.Graph()
            for i in range(num_vertices):
                G.add_node(f'X{i}')
            # Assurer la connexité avec des poids
            for i in range(num_vertices - 1):
                weight = random.randint(GRAPH_SETTINGS['MIN_WEIGHT'],
                                    GRAPH_SETTINGS['MAX_WEIGHT'])
                G.add_edge(f'X{i}', f'X{i+1}', weight=weight)
            # Ajouter des arêtes supplémentaires
            for i in range(num_vertices):
                for j in range(i + 2, num_vertices):
                    if random.random() < GRAPH_SETTINGS['RANDOM_EDGE_PROBABILITY']:
                        weight = random.randint(GRAPH_SETTINGS['MIN_WEIGHT'],
                                            GRAPH_SETTINGS['MAX_WEIGHT'])
                        G.add_edge(f'X{i}', f'X{j}', weight=weight)
            return G

        elif algorithm_type == "ford_fulkerson":
            G = nx.DiGraph()
            for i in range(num_vertices):
                G.add_node(i)
            # Assurer la connexité avec des capacités
            for i in range(num_vertices - 1):
                capacity = random.randint(1, 20)
                G.add_edge(i, i+1, capacity=capacity)
            # Ajouter des arcs supplémentaires
            for i in range(num_vertices):
                for j in range(i + 2, num_vertices):
                    if random.random() < GRAPH_SETTINGS['RANDOM_EDGE_PROBABILITY']:
                        capacity = random.randint(1, 20)
                        G.add_edge(i, j, capacity=capacity)
            return G

        elif algorithm_type == "bellman_ford":
            G = nx.Graph()
            for i in range(num_vertices):
                G.add_node(f'X{i}')
            # Assurer la connexité avec des poids
            for i in range(num_vertices - 1):
                weight = random.randint(GRAPH_SETTINGS['MIN_WEIGHT'],
                                    GRAPH_SETTINGS['MAX_WEIGHT'])
                G.add_edge(f'X{i}', f'X{i+1}', weight=weight)
            # Ajouter des arêtes supplémentaires
            for i in range(num_vertices):
                for j in range(i + 2, num_vertices):
                    if random.random() < GRAPH_SETTINGS['RANDOM_EDGE_PROBABILITY']:
                        weight = random.randint(GRAPH_SETTINGS['MIN_WEIGHT'],
                                            GRAPH_SETTINGS['MAX_WEIGHT'])
                        G.add_edge(f'X{i}', f'X{j}', weight=weight)
            return G

        raise ValueError(f"Type d'algorithme non supporté: {algorithm_type}")
