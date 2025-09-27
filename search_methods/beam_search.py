from sokoban.map import Map
from search_methods.heuristics import first_heuristic_manhattan_distance
from search_methods.heuristics import second_heuristic_hungarian_algo

class beam_search:
    def __init__(self, initial_state, k=5):

        self.initial_state = initial_state
        self.k = k


    def solve(self):
        # lista in care tinem tupluri de forma (stare curenta, path pana la aceasta stare, valoarea euristicii)
        LIST = [(self.initial_state.copy(), [], second_heuristic_hungarian_algo(self.initial_state.copy()))]

        # map in care tinem starile deja vizitate si numarul de vizite pentru fiecare stare
        visited_states = {}
        visited_states[str(self.initial_state)] = 1

        # In cazul in care algoritmul nu gaseste o solutie, vom returna cea mai
        # buna cale gasita (va fi de ajutor la debug sa urmarim gif-ul)
        best_path = []
        best_score = float('inf')

        # wrapper peste functia euristica menit sa penalizeze miscarile de pull si starile deja vizitate
        def pull_and_already_explored_penalizing_heuristic(state, prev_state):
            base_score = second_heuristic_hungarian_algo(state)

            pull_penalty = 0
            if state.undo_moves > prev_state.undo_moves:
                pull_penalty = 100

            visit_count = visited_states.get(str(state), 0)
            visit_penalty = visit_count * 300

            return base_score + pull_penalty + visit_penalty
        

        while LIST:
            cand_LIST = []

            for state, path, heuristic in LIST:

                if state.is_solved():
                    new_path = path + [state]
                    return new_path
                
                neighbours = state.get_neighbours()

                for neigh in neighbours:
                    key = str(neigh)
                    if key in visited_states:
                        visited_states[key] += 1
                    else:
                        visited_states[key] = 1

                    new_path = path + [state]
                    score = pull_and_already_explored_penalizing_heuristic(neigh, state)
                    if score < best_score:
                        best_score = score
                        best_path = new_path

                    cand_LIST.append((neigh, new_path, score))

            if not cand_LIST:
                break

            # Pastram doar cele mai bune k stari
            cand_LIST.sort(key=lambda x: x[2])
            best_candidates = cand_LIST[:self.k]
            LIST = best_candidates

        print("No solution found. Returning best path so far.")
        return best_path