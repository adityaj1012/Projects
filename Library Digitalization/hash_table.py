from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        self.collision_type=collision_type
        self.params=params
        self.item_count=0
        if collision_type=="Chain" or collision_type=="Linear":
            self.table_size=params[1]
            self.z=params[0]
            self.hash_table=[None for i in range(params[1])]
        else:
            self.z1=params[0]
            self.z2=params[1]
            self.c2=params[2]
            self.table_size=params[3]
            self.hash_table=[None for i in range(params[3])]
            
    def char_to_index(self,char):
        if char.islower():
            return ord(char)-ord('a')
        else:
            return (ord(char.lower()) - ord('a')) + 26 
        
    def polynomial(self, s, multiplier, start, end):
        hash_value = 0
        current_multiplier = 1
        
        for i in range(len(s)):
            term = self.char_to_index(s[i]) * current_multiplier
            hash_value += term
            current_multiplier *= multiplier
            
        return hash_value

    def insert(self, item):
        key = item[0] if isinstance(item, tuple) else item 
        z = self.z1 if self.collision_type == "Double" else self.z
        hash_key = self.polynomial(key, z, 0, len(key) - 1)
        index = hash_key % self.table_size
        if self.collision_type == "Chain":
            if self.hash_table[index] is None:
                self.hash_table[index] = [item]
                self.item_count += 1
            elif item not in self.hash_table[index]:
                self.hash_table[index].append(item)
                self.item_count += 1
            return
        if self.collision_type in ["Linear", "Double"]:
            step = 1
            if self.collision_type == "Double":
                secondary_hash = self.polynomial(key, self.z2, 0, len(key) - 1)
                step = self.c2 - (secondary_hash % self.c2)
            for _ in range(self.table_size):
                if self.hash_table[index] is None:
                    self.hash_table[index] = item
                    self.item_count += 1
                    return
                elif self.hash_table[index] == item:
                    return  # Avoid duplicates
                index = (index + step) % self.table_size
            raise Exception("Table is full")

    def find(self, key):  
        primary_hash = self.polynomial(key, self.z1 if self.collision_type == "Double" else self.z, 0, len(key) - 1) % self.table_size
        if self.collision_type == "Chain":
            return self.hash_table[primary_hash] is not None and key in self.hash_table[primary_hash]
        elif self.collision_type == "Linear":
            for _ in range(self.table_size):
                if self.hash_table[primary_hash] is None:
                    return False
                if self.hash_table[primary_hash] == key:
                    return True
                primary_hash = (primary_hash + 1) % self.table_size
            return False
        elif self.collision_type == "Double":
            secondary_hash = self.c2 - (self.polynomial(key, self.z2, 0, len(key) - 1) % self.c2)
            for j in range(self.table_size):
                current_position = (primary_hash + j * secondary_hash) % self.table_size
                if self.hash_table[current_position] is None:
                    return False
                if self.hash_table[current_position] == key:
                    return True
            return False
        
    def get_slot(self, key):
        z_value = self.z if self.collision_type in ["Chain", "Linear"] else self.z1
        hash_key = self.polynomial(key, z_value, 0, len(key) - 1)
        return hash_key % self.table_size

    def get_load(self):
        return self.item_count/self.table_size
    
    def __str__(self):
        pass
    
    def rehash(self):
        pass
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)
    
    def insert(self, key):
        super().insert(key)
    
    def find(self, key):
        return super().find(key)
    
    def get_slot(self, key):
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        parts = []
        for i in range(self.table_size):
            if self.collision_type == "Chain":
                if self.hash_table[i] is None:
                    parts.append("<EMPTY>")
                else:
                    chain = " ; ".join(str(item) for item in self.hash_table[i])
                    parts.append(chain)
            else:
                parts.append(str(self.hash_table[i]) if self.hash_table[i] is not None else "<EMPTY>")
        
        return " | ".join(parts)

class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)
    
    def insert(self, x):
        super().insert(x)
    
    def find(self, key):
        k = self.polynomial(key, self.z1 if self.collision_type == "Double" else self.z, 0, len(key) - 1)
        cell = k % self.table_size
        if self.collision_type == "Chain":
            if self.hash_table[cell] is None:
                return None
            for item in self.hash_table[cell]:
                if item[0] == key:
                    return item[1]
        elif self.collision_type in ["Linear", "Double"]:
            for _ in range(self.table_size):
                if self.hash_table[cell] is None:
                    return None
                if self.hash_table[cell][0] == key:
                    return self.hash_table[cell][1]
                if self.collision_type == "Linear":
                    cell = (cell + 1) % self.table_size
                else:  # Double hashing
                    j = (self.c2 - (self.polynomial(key, self.z2, 0, len(key) - 1) % self.c2)) % self.c2
                    cell = (cell + j) % self.table_size
        return None

    def get_slot(self, key):
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        result = []
        for i in range(self.table_size):
            if self.hash_table[i] is None:
                result.append("<EMPTY>")
            else:
                if self.collision_type == "Chain":
                    items = "; ".join(f"({item[0]}, {item[1]})" for item in self.hash_table[i])
                    result.append(items)
                else:  # For Linear and Double hashing
                    result.append(f"({self.hash_table[i][0]}, {self.hash_table[i][1]})")
        return " | ".join(result)