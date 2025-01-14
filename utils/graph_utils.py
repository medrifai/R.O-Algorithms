import networkx as nx
import matplotlib.pyplot as plt
import random

def create_and_display_graph(num_vertices, algorithm, **kwargs):
    """
    Create and display a graph based on the algorithm type and parameters.
    
    Parameters:
    -----------
    num_vertices : int
        Number of vertices in the graph
    algorithm : str
        Type of algorithm ('dijkstra', 'ford_fulkerson', etc.)
    **kwargs : dict
        Additional algorithm-specific parameters
    """
    G = nx.DiGraph() if algorithm in ['dijkstra', 'ford_fulkerson', 'bellman_ford'] else nx.Graph()
    
    # Add nodes
    G.add_nodes_from(range(num_vertices))
    
    if algorithm == 'dijkstra':
        # Generate random edges for Dijkstra
        edges = [(i, j, {'weight': random.randint(1, 10)}) 
                for i in range(num_vertices) 
                for j in range(i+1, num_vertices) 
                if random.random() < 0.3]
        G.add_edges_from(edges)
        # Highlight path if start and end nodes are provided
        if 'start_node' in kwargs and 'end_node' in kwargs:
            try:
                path = nx.shortest_path(G, kwargs['start_node'], kwargs['end_node'], weight='weight')
                for i in range(len(path)-1):
                    G[path[i]][path[i+1]]['color'] = 'red'
            except nx.NetworkXNoPath:
                print("No path exists between the specified nodes.")
    
    elif algorithm == 'ford_fulkerson':
        # Generate random edges for Ford-Fulkerson
        source = kwargs.get('source', 0)
        sink = kwargs.get('sink', num_vertices-1)
        for i in range(num_vertices):
            for j in range(i+1, num_vertices):
                if random.random() < 0.3:
                    G.add_edge(i, j, weight=random.randint(1, 10))
    
    elif algorithm in ['nord_ouest', 'moindre_cout', 'stepping_stone']:
        # Create bipartite graph for transport problems
        sources = kwargs.get('sources', 3)
        destinations = kwargs.get('destinations', 3)
        G = nx.complete_bipartite_graph(sources, destinations)
        pos = {}
        # Position sources on left
        for i in range(sources):
            pos[i] = (0, i)
        # Position destinations on right
        for i in range(sources, sources + destinations):
            pos[i] = (1, i - sources)
        
        # Add random weights
        for (u, v) in G.edges():
            G[u][v]['weight'] = random.randint(1, 10)
            
        nx.draw(G, pos=pos, with_labels=True, 
                node_color='lightblue', node_size=500, 
                font_size=10, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()
        return G
    
    # Default graph visualization for other algorithms
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, 
            node_color='lightblue', node_size=500, 
            font_size=10, font_weight='bold', 
            arrows=isinstance(G, nx.DiGraph))
    
    # Draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Draw edge colors if specified
    edge_colors = nx.get_edge_attributes(G, 'color').values()
    if edge_colors:
        nx.draw_networkx_edges(G, pos, 
                             edge_color=list(edge_colors), 
                             width=2)
    
    plt.show()
    return G

def display_graph(G, with_weights=True):
    """
    Display an existing networkx graph.
    
    Parameters:
    -----------
    G : networkx.Graph or networkx.DiGraph
        The graph to display
    with_weights : bool, optional
        Whether to display edge weights (default: True)
    """
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=500,
            font_size=10,
            font_weight='bold',
            arrows=isinstance(G, nx.DiGraph))
    
    if with_weights:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        if edge_labels:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.show()