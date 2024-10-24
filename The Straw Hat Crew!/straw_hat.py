from heap import Heap
from crewmate import CrewMate
from custom import Comparison
class StrawHatTreasury:
    def __init__(self, number_of_crew_mates):
        self.number_of_crew_mates = number_of_crew_mates
        self.crewmate_heap = Heap(Comparison.compCrewmate, [CrewMate() for _ in range(number_of_crew_mates)])
        self.treasures = [] 

    def add_treasure(self, treasure):
        self.treasures.append(treasure)
        current_crewmate = self.crewmate_heap.top() 
        current_crewmate.list.append(treasure) 
        current_crewmate.load = max(treasure.arrival_time + treasure.size, current_crewmate.load + treasure.size)
        self.crewmate_heap.down_heap(0) 

    def get_completion_time(self):
        completed_treasures = []
        original_treasure_sizes = [treasure_item.size for treasure_item in self.treasures]
        
        crew_mates_copy = self.crewmate_heap.heap[:]
        while not self.crewmate_heap.is_empty():
            current_crewmate = self.crewmate_heap.extract()
            if current_crewmate.load == 0:
                continue
            current_time = 0
            for treasure_item in current_crewmate.list:
                while not current_crewmate.treasures.is_empty():
                    top_treasure = current_crewmate.treasures.top()
                    if treasure_item.arrival_time - current_time >= top_treasure.size:
                        processed_treasure = current_crewmate.treasures.extract()
                        processed_treasure.completion_time = current_time + processed_treasure.size
                        completed_treasures.append(processed_treasure)
                        current_time += processed_treasure.size
                    else:
                        top_treasure.size -= (treasure_item.arrival_time - current_time)
                        current_crewmate.treasures.down_heap(0)
                        break
                current_crewmate.treasures.insert(treasure_item)
                current_time = treasure_item.arrival_time
                
            while not current_crewmate.treasures.is_empty():
                remaining_treasure = current_crewmate.treasures.extract()
                current_time += remaining_treasure.size
                remaining_treasure.completion_time = current_time
                completed_treasures.append(remaining_treasure)
        
        for i, treasure_item in enumerate(self.treasures):
            treasure_item.size = original_treasure_sizes[i]
        
        self.crewmate_heap = Heap(Comparison.compCrewmate, crew_mates_copy)
        
        return sorted(completed_treasures, key=lambda treasure_item: treasure_item.id)
