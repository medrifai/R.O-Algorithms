# Configuration globale de l'application

# Paramètres de l'interface graphique
GUI_SETTINGS = {
    'WINDOW_TITLE': "Interface Graphique Tkinter",
    'WINDOW_SIZE': "800x600",
    'BACKGROUND_COLOR': "#FFE4F2",
    'FRAME_COLOR': "#FF69B4",
    'BUTTON_COLOR': "white",
    'TITLE_FONT': ("Arial", 20, "bold"),
    'SUBTITLE_FONT': ("Arial", 14, "bold"),
    'BUTTON_FONT': ("Arial", 12, "bold")
}

# Paramètres des graphes
GRAPH_SETTINGS = {
    'FIGURE_SIZE': (10, 8),
    'NODE_SIZE': 500,
    'EDGE_WIDTH': 2,
    'RANDOM_EDGE_PROBABILITY': 0.3,
    'MIN_WEIGHT': 1,
    'MAX_WEIGHT': 100
}

# Couleurs pour les algorithmes
ALGORITHM_COLORS = {
    'welsh_powell': {
        'node_default': 'lightblue',
        'edge_default': 'gray',
    },
    'dijkstra': {
        'node_default': 'lightblue',
        'edge_default': 'gray',
        'path_highlight': 'red',
    },
    'kruskal': {
        'node_default': 'lightblue',
        'edge_default': 'gray',
        'mst_highlight': 'red',
    },
    'ford_fulkerson': {
        'source_node': 'lightgreen',
        'sink_node': 'lightblue',
        'edge_default': 'gray',
    },
    'potentiel_metra': {
        'node_default': 'lightblue',
        'edge_default': 'gray',
        'critical_path': 'red',
        'task_bar': 'lightblue'
    },
    'bellman_ford': {
        'node_default': 'lightblue',
        'edge_default': 'gray',
        'mst_highlight': 'red'
    }
}

# Messages d'erreur
ERROR_MESSAGES = {
    'invalid_vertices': "Le nombre de sommets doit être positif",
    'invalid_node_format': "Les sommets doivent être au format X0, X1, etc.",
    'invalid_node_index': "Les indices des sommets doivent être inférieurs au nombre de sommets",
    'disconnected_graph': "Le graphe doit être connexe"
}