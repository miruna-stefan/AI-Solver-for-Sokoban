from sokoban.map import Map
from search_methods.heuristics import first_heuristic_manhattan_distance
from search_methods.heuristics import second_heuristic_hungarian_algo


import random

class lrta_star:
    def __init__(self, initial_map: Map):
        self.s_prev = None
        self.a_prev = None
        self.H = {} 

        self.initial_map = initial_map.copy()

    def cost(self, s_prev, s):
        pull_penalty = 0
        if s.undo_moves > s_prev.undo_moves:
            pull_penalty = 100

        moving_box_from_target_penalty = 0
        for target_pos in s_prev.targets:
            # Daca in s_prev exista o cutie pe un target si in s nu mai e acolo
            if target_pos in s_prev.positions_of_boxes and target_pos not in s.positions_of_boxes:
                moving_box_from_target_penalty += 200

        if str(s) not in self.H:
            return moving_box_from_target_penalty + pull_penalty + 1 + second_heuristic_hungarian_algo(s)
        return moving_box_from_target_penalty + pull_penalty + 60 + self.H[str(s)]
    
    # Aceasta functie de cost a fost folosita in testarea primei euristici
    # def cost(self, s_prev, s):
    #     if str(s) not in self.H:
    #         return 1 + first_heuristic_manhattan_distance(s)
    #     return 60 + self.H[str(s)]

    def solve(self):
        current_state = self.initial_map
        path = [current_state]

        while not current_state.is_solved():
            s = current_state
            if str(s) not in self.H:
                self.H[str(s)] = second_heuristic_hungarian_algo(s)

            if self.s_prev is not None:
                min_cost = float('inf')

                for neigh_state in self.s_prev.get_neighbours():
                    cost_est = self.cost(self.s_prev, neigh_state)
                    if cost_est < min_cost:
                        min_cost = cost_est

                self.H[str(self.s_prev)] = min_cost

            min_cost = float('inf')
            best_resulting_state = None

            #Alege starea care minimizeaza costul
            for next_state in s.get_neighbours():
                cost_est = self.cost(s, next_state)
                if cost_est < min_cost:
                    min_cost = cost_est
                    best_resulting_state = next_state

            self.s_prev = s

            current_state = best_resulting_state
            path.append(current_state)


        return path
