from sokoban.map import Map
from search_methods.lrta_star import lrta_star
from search_methods.beam_search import beam_search

class Solver:

    def __init__(self, map: Map, algorithm: str = "lrta*") -> None:
        self.map = map
        self.algorithm = algorithm

    def solve(self):
        if self.algorithm == "lrta*":
            algo = lrta_star(self.map)
            return algo.solve()
        elif self.algorithm == "beam-search":
            algo = beam_search(self.map)
            return algo.solve()
        else:
            raise NotImplementedError
