import numpy as np

def nord_ouest(supply, demand):
    """
    Méthode du coin Nord-Ouest pour résoudre le problème de transport initial.
    
    Args:
        supply: Liste des capacités des sources
        demand: Liste des demandes des destinations
    
    Returns:
        np.array: Matrice de la solution initiale
    """
    supply = np.array(supply, dtype=float)
    demand = np.array(demand, dtype=float)
    m, n = len(supply), len(demand)
    solution = np.zeros((m, n))
    
    i, j = 0, 0
    while i < m and j < n:
        # Prendre le minimum entre l'offre disponible et la demande restante
        quantity = min(supply[i], demand[j])
        solution[i, j] = quantity
        
        # Mettre à jour l'offre et la demande
        supply[i] -= quantity
        demand[j] -= quantity
        
        # Passer à la ligne suivante si l'offre est épuisée
        if supply[i] <= 0:
            i += 1
        # Passer à la colonne suivante si la demande est satisfaite
        if demand[j] <= 0:
            j += 1
    
    return solution

def moindre_cout(supply, demand, costs):
    """
    Méthode du coût minimum pour résoudre le problème de transport.
    
    Args:
        supply: Liste des capacités des sources
        demand: Liste des demandes des destinations
        costs: Matrice des coûts de transport
    
    Returns:
        np.array: Matrice de la solution
    """
    supply = np.array(supply, dtype=float)
    demand = np.array(demand, dtype=float)
    costs = np.array(costs, dtype=float)
    m, n = len(supply), len(demand)
    solution = np.zeros((m, n))
    
    while True:
        # Vérifier s'il reste de l'offre et de la demande
        if np.all(supply <= 0) or np.all(demand <= 0):
            break
        
        # Trouver la cellule avec le coût minimum parmi les cellules valides
        valid_mask = (supply.reshape(-1, 1) > 0) & (demand.reshape(1, -1) > 0)
        if not np.any(valid_mask):
            break
            
        costs_masked = np.where(valid_mask, costs, np.inf)
        i, j = np.unravel_index(np.argmin(costs_masked), costs_masked.shape)
        
        # Affecter la quantité maximum possible
        quantity = min(supply[i], demand[j])
        solution[i, j] = quantity
        
        # Mettre à jour l'offre et la demande
        supply[i] -= quantity
        demand[j] -= quantity
    
    return solution

def stepping_stone(initial_solution, costs):
    """
    Méthode du Stepping Stone pour optimiser une solution de transport.
    
    Args:
        initial_solution: Solution initiale
        costs: Matrice des coûts de transport
    
    Returns:
        np.array: Solution optimisée
        float: Coût total de la solution
    """
    solution = initial_solution.copy()
    m, n = solution.shape
    
    def find_cycle(start_i, start_j):
        """Trouve un cycle pour une cellule vide"""
        def find_path(current_i, current_j, used_rows, used_cols, path):
            # Si on revient au point de départ avec un cycle valide
            if len(path) > 3 and current_i == start_i and current_j == start_j:
                return path
            
            # Explorer les possibilités horizontalement
            for j in range(n):
                if j != current_j and (solution[current_i, j] > 0 or (current_i == start_i and j == start_j)):
                    if j not in used_cols:
                        # Explorer verticalement depuis ce nouveau point
                        for i in range(m):
                            if i != current_i and (solution[i, j] > 0 or (i == start_i and j == start_j)):
                                if i not in used_rows:
                                    new_path = find_path(i, j, 
                                                       used_rows | {current_i}, 
                                                       used_cols | {current_j}, 
                                                       path + [(current_i, j), (i, j)])
                                    if new_path:
                                        return new_path
            return None
        
        # Commencer la recherche
        for j in range(n):
            if j != start_j and solution[start_i, j] > 0:
                path = find_path(start_i, j, {start_i}, {start_j}, [(start_i, start_j), (start_i, j)])
                if path:
                    return path
        return None
    
    while True:
        improvement_found = False
        best_improvement = 0
        best_cycle = None
        
        # Chercher la meilleure amélioration possible
        for i in range(m):
            for j in range(n):
                if solution[i, j] == 0:
                    cycle = find_cycle(i, j)
                    if cycle:
                        # Calculer l'amélioration potentielle
                        cycle_cost = 0
                        for idx, (ci, cj) in enumerate(cycle):
                            cycle_cost += costs[ci, cj] * (-1 if idx % 2 else 1)
                            
                        if cycle_cost < best_improvement:
                            best_improvement = cycle_cost
                            best_cycle = cycle
                            improvement_found = True
        
        # Si aucune amélioration n'est trouvée, on arrête
        if not improvement_found:
            break
            
        # Appliquer la meilleure amélioration trouvée
        # Trouver la quantité maximum qu'on peut déplacer
        max_quantity = float('inf')
        for idx, (i, j) in enumerate(best_cycle):
            if idx % 2:  # Pour les cellules négatives du cycle
                max_quantity = min(max_quantity, solution[i, j])
                
        # Appliquer le changement
        for idx, (i, j) in enumerate(best_cycle):
            solution[i, j] += max_quantity * (-1 if idx % 2 else 1)
    
    # Calculer le coût total de la solution
    total_cost = np.sum(solution * costs)
    
    return solution, total_cost

def vogel(supply, demand, costs):
    """
    Méthode d'approximation de Vogel pour le problème de transport.
    
    Args:
        supply: Liste des capacités des sources
        demand: Liste des demandes des destinations
        costs: Matrice des coûts de transport
    
    Returns:
        np.array: Matrice de la solution
    """
    supply = np.array(supply, dtype=float)
    demand = np.array(demand, dtype=float)
    costs = np.array(costs, dtype=float)
    m, n = len(supply), len(demand)
    solution = np.zeros((m, n))
    
    while np.any(supply > 0) and np.any(demand > 0):
        # Calculer les pénalités pour chaque ligne et colonne
        penalties = np.zeros(m + n)
        
        # Pénalités des lignes
        for i in range(m):
            if supply[i] > 0:
                valid_costs = costs[i, demand > 0]
                if len(valid_costs) >= 2:
                    penalties[i] = np.diff(np.partition(valid_costs, 1)[:2])[0]
                
        # Pénalités des colonnes
        for j in range(n):
            if demand[j] > 0:
                valid_costs = costs[supply > 0, j]
                if len(valid_costs) >= 2:
                    penalties[m + j] = np.diff(np.partition(valid_costs, 1)[:2])[0]
        
        # Trouver la plus grande pénalité
        max_penalty_idx = np.argmax(penalties)
        
        if max_penalty_idx < m:  # Ligne
            i = max_penalty_idx
            valid_costs = np.where(demand > 0, costs[i], np.inf)
            j = np.argmin(valid_costs)
        else:  # Colonne
            j = max_penalty_idx - m
            valid_costs = np.where(supply > 0, costs[:, j], np.inf)
            i = np.argmin(valid_costs)
        
        # Affecter la quantité maximum possible
        quantity = min(supply[i], demand[j])
        solution[i, j] = quantity
        
        # Mettre à jour l'offre et la demande
        supply[i] -= quantity
        demand[j] -= quantity
    
    return solution