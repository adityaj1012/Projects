from heap import Heap
from custom import Comparison
class CrewMate:
    def __init__(self):
        self.list = []
        self.load = 0
        self.treasures = Heap(Comparison.compTreasure, [])