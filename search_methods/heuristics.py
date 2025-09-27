import numpy as np
from scipy.optimize import linear_sum_assignment

def first_heuristic_manhattan_distance(state):
    # total_cost era initial format din suma distantelor Manhattan
    # minime de la fiecare cutie la targetul ei cel mai apropiat
    # ulterior, am mai adaugat la acest cost si alte componente pentru a imbunatati euristica
    total_cost = 0

    box_positions = [(box.x, box.y) for box in state.boxes.values()]
    target_positions = state.targets.copy()
    player_pos = (state.player.x, state.player.y)

    # pentru a nu asigna acelasi target mai multor cutii, mentinem un set cu target-urile deja asignate
    used_targets = set()

    # Calculeaza distanta Manhattan minima de la fiecare cutie la cel mai apropiat target
    for box_x, box_y in box_positions:

        # Daca cutia e deja pe un target, nu mai trebuie sa o mutam
        if (box_x, box_y) in target_positions:
            continue

        # Verifica daca box-ul curent ar fi intr-o pozitie din care nu ar mai
        # putea fi mutat fara a executa o actiune de pull
        if would_be_dead_pos(box_x, box_y, state):
            return float('inf')
    
        min_dist_to_target = float('inf')
        closest_target = None

        for target_x, target_y in target_positions:
            if (target_x, target_y) in used_targets:
                continue

            dist = abs(box_x - target_x) + abs(box_y - target_y)

            if dist < min_dist_to_target:
                min_dist_to_target = dist
                closest_target = (target_x, target_y)

        if closest_target:
            used_targets.add(closest_target)
            total_cost += min_dist_to_target

            # Adauga si distanta de la player la cutie
            dist = abs(player_pos[0] - box_x) + abs(player_pos[1] - box_y)
            total_cost += 0.9 * dist

            # Verifica daca asezarea curenta de pe tabla de joc ar necesita o actiune de pull
            if is_pull_position(player_pos, (box_x, box_y), closest_target):
                total_cost += 30

    return total_cost

def second_heuristic_hungarian_algo(state):
    box_positions = [(box.x, box.y) for box in state.boxes.values()]
    target_positions = state.targets.copy()
    player_pos = (state.player.x, state.player.y)

    num_boxes = len(box_positions)
    num_targets = len(target_positions)

    cost_matrix = np.zeros((num_boxes, num_targets))

    for i, (bx, by) in enumerate(box_positions):
        if would_be_dead_pos(bx, by, state):
            return float('inf')
        for j, (tx, ty) in enumerate(target_positions):
            cost_matrix[i][j] = abs(bx - tx) + abs(by - ty)

    box_indices, target_indices = linear_sum_assignment(cost_matrix)
    total_distance = cost_matrix[box_indices, target_indices].sum()

    min_player_to_box = min(abs(player_pos[0] - bx) + abs(player_pos[1] - by) for bx, by in box_positions)
    total_distance += 0.9 * min_player_to_box

    return total_distance

# Verifica daca o cutie aflata la (x, y) ar fi blocata definitiv
def would_be_dead_pos(x, y, map_obj):
    
    # Dacă e deja pe un target, clar nu e dead
    if (x, y) in map_obj.targets:
        return False

    # E blocat in stanga si in jos si nu e target acolo
    if ((x - 1, y) in map_obj.obstacles or x - 1 < 0) and ((x, y - 1) in map_obj.obstacles or y - 1 < 0) and ((x, y) not in map_obj.targets):
        return True
    # E blocat in stanga si in sus si nu e target acolo
    if ((x - 1, y) in map_obj.obstacles or x - 1 < 0) and ((x, y + 1) in map_obj.obstacles or y + 1 >= map_obj.width) and ((x, y) not in map_obj.targets):
        return True
    # E blocat in dreapta si in jos si nu e target acolo
    if ((x + 1, y) in map_obj.obstacles or x + 1 >= map_obj.length) and ((x, y - 1) in map_obj.obstacles or y - 1 < 0) and ((x, y) not in map_obj.targets):
        return True
    # E blocat in dreapta si in sus si nu e target acolo
    if ((x + 1, y) in map_obj.obstacles or x + 1 >= map_obj.length) and ((x, y + 1) in map_obj.obstacles or y + 1 >= map_obj.width) and ((x, y) not in map_obj.targets):
        return True

    return False


def is_pull_position(player_pos, box_pos, target_pos):
    dx = target_pos[0] - box_pos[0]
    dy = target_pos[1] - box_pos[1]

    # Verifica daca jucatorul este in pozitia corecta pentru a impinge cutia catre target
    if dx > 0: # cutia trebuie sa se miste la dreapta
        if player_pos[0] == box_pos[0] + 1 and player_pos[1] == box_pos[1]:
            return True
    elif dx < 0: # cutia trebuie sa se miste la stanga
        if player_pos[0] == box_pos[0] - 1 and player_pos[1] == box_pos[1]:
            return True
    elif dy > 0: # cutia trebuie sa se miste in sus
        if player_pos[0] == box_pos[0] and player_pos[1] == box_pos[1] + 1:
            return True
    elif dy < 0: # cutia trebuie sa se miste in jos
        if player_pos[0] == box_pos[0] and player_pos[1] == box_pos[1] - 1:
            return True
    return False


