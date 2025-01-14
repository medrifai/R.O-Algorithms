import numpy as np
from typing import List, Set, Tuple, Dict

class TransportAlgorithms:
    @staticmethod
    def nord_ouest(supply: List[int], demand: List[int], costs: List[List[int]]) -> Tuple[List[List[int]], int]:
        """
        Implémentation corrigée de la méthode du coin Nord-Ouest.
        """
        if sum(supply) != sum(demand):
            raise ValueError("L'offre totale doit être égale à la demande totale")

        m, n = len(supply), len(demand)
        allocation = [[0 for _ in range(n)] for _ in range(m)]
        total_cost = 0
        
        i, j = 0, 0
        supply_temp = supply.copy()
        demand_temp = demand.copy()
        
        while i < m and j < n:
            quantity = min(supply_temp[i], demand_temp[j])
            allocation[i][j] = quantity
            total_cost += quantity * costs[i][j]
            
            supply_temp[i] -= quantity
            demand_temp[j] -= quantity
            
            if supply_temp[i] == 0:
                i += 1
            if demand_temp[j] == 0:
                j += 1
                
        return allocation, total_cost

    @staticmethod
    def moindre_cout(supply: List[int], demand: List[int], costs: List[List[int]]) -> Tuple[List[List[int]], int]:
        """
        Implémentation corrigée de la méthode du coût minimum.
        """
        if sum(supply) != sum(demand):
            raise ValueError("L'offre totale doit être égale à la demande totale")

        m, n = len(supply), len(demand)
        allocation = [[0 for _ in range(n)] for _ in range(m)]
        total_cost = 0
        
        supply_temp = supply.copy()
        demand_temp = demand.copy()
        
        while True:
            # Trouver la cellule avec le coût minimum parmi les cellules disponibles
            min_cost = float('inf')
            min_i, min_j = -1, -1
            
            for i in range(m):
                if supply_temp[i] == 0:
                    continue
                for j in range(n):
                    if demand_temp[j] == 0:
                        continue
                    if costs[i][j] < min_cost:
                        min_cost = costs[i][j]
                        min_i, min_j = i, j
            
            if min_i == -1:  # Toutes les allocations sont faites
                break
                
            quantity = min(supply_temp[min_i], demand_temp[min_j])
            allocation[min_i][min_j] = quantity
            total_cost += quantity * costs[min_i][min_j]
            
            supply_temp[min_i] -= quantity
            demand_temp[min_j] -= quantity
            
        return allocation, total_cost

    @staticmethod
    def stepping_stone(initial_solution: List[List[int]], 
                      costs: List[List[int]]) -> Tuple[List[List[int]], int]:
        """
        Implémentation corrigée de la méthode du Stepping Stone.
        """
        m, n = len(initial_solution), len(initial_solution[0])
        current_solution = [row[:] for row in initial_solution]
        
        while True:
            # Calculer les coûts réduits pour les cellules non utilisées
            best_improvement = 0
            best_path = None
            
            for i in range(m):
                for j in range(n):
                    if current_solution[i][j] == 0:
                        # Trouver un cycle pour cette cellule
                        path = TransportAlgorithms._find_cycle(current_solution, i, j)
                        if path is None:
                            continue
                            
                        # Calculer l'amélioration potentielle
                        improvement = 0
                        sign = 1
                        for pi, pj in path:
                            improvement += sign * costs[pi][pj]
                            sign *= -1
                            
                        if improvement < best_improvement:
                            best_improvement = improvement
                            best_path = path
            
            if best_improvement >= 0:  # Pas d'amélioration possible
                break
                
            # Appliquer l'amélioration
            min_quantity = float('inf')
            for idx, (i, j) in enumerate(best_path):
                if idx % 2 == 1:  # Cellules négatives dans le cycle
                    min_quantity = min(min_quantity, current_solution[i][j])
                    
            sign = 1
            for i, j in best_path:
                current_solution[i][j] += sign * min_quantity
                sign *= -1
        
        # Calculer le coût total
        total_cost = sum(current_solution[i][j] * costs[i][j]
                        for i in range(m)
                        for j in range(n))
                        
        return current_solution, total_cost

    @staticmethod
    def _find_cycle(solution: List[List[int]], start_i: int, start_j: int) -> List[Tuple[int, int]]:
        """
        Trouve un cycle pour la méthode du Stepping Stone.
        """
        m, n = len(solution), len(solution[0])
        used_cells = [(i, j) for i in range(m) for j in range(n)
                     if solution[i][j] > 0]
        used_cells.append((start_i, start_j))
        
        def find_path(current: Tuple[int, int], 
                     target: Tuple[int, int], 
                     path: List[Tuple[int, int]], 
                     visited: Set[Tuple[int, int]]) -> bool:
            if current == target and len(path) > 3:
                return True
                
            i, j = current
            # Essayer horizontalement
            for next_j in range(n):
                if next_j != j:
                    next_cell = (i, next_j)
                    if next_cell in used_cells and next_cell not in visited:
                        path.append(next_cell)
                        visited.add(next_cell)
                        if find_path(next_cell, target, path, visited):
                            return True
                        path.pop()
                        visited.remove(next_cell)
                        
            # Essayer verticalement
            for next_i in range(m):
                if next_i != i:
                    next_cell = (next_i, j)
                    if next_cell in used_cells and next_cell not in visited:
                        path.append(next_cell)
                        visited.add(next_cell)
                        if find_path(next_cell, target, path, visited):
                            return True
                        path.pop()
                        visited.remove(next_cell)
                        
            return False
        
        path = [(start_i, start_j)]
        visited = {(start_i, start_j)}
        if find_path((start_i, start_j), (start_i, start_j), path, visited):
            return path
        return None