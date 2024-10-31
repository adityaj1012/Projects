from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        new_table_size = get_next_size()
        old_elements = []
        self.item_count = 0 
        for entry in self.hash_table:
            if self.collision_type == "Chain" and entry is not None:
                old_elements.extend(entry)
            elif entry is not None:
                old_elements.append(entry)
        self.hash_table = [None] * new_table_size
        self.table_size = new_table_size
        for element in old_elements:
            self.insert(element)

    def insert(self, x):
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        new_table_size = get_next_size()
        old_elements = []
        self.item_count = 0 
        for bucket in self.hash_table:
            if self.collision_type == "Chain" and bucket is not None:
                old_elements.extend(bucket)
            elif bucket is not None:
                old_elements.append(bucket)        
        self.hash_table = [None] * new_table_size
        self.table_size = new_table_size
        for element in old_elements:
            self.insert(element)

    def insert(self, x):
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()