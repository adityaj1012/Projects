class Heap:
    def __init__(self, comparison_function, init_array):
        self.heap = []
        self.compare = comparison_function
        for value in init_array:
            self.insert(value)
    def is_empty(self):
        return len(self.heap) == 0

    def left(self, index):
        return 2 * index + 1
    def right(self, index):
        return 2 * index + 2
    
    def has_left(self, index):
        return self.left(index) < len(self.heap)
    def has_right(self, index):
        return self.right(index) < len(self.heap)

    def down_heap(self, index):
        if (2 * index + 1) < len(self.heap):
            left = 2 * index + 1
            small_child = left
            if (2 * index + 2) < len(self.heap):
                right = 2 * index + 2
                if self.compare(self.heap[right], self.heap[left]):
                    small_child = right
            if self.compare(self.heap[small_child], self.heap[index]):
                self.heap[index], self.heap[small_child] = self.heap[small_child], self.heap[index]
                self.down_heap(small_child)

    def up_heap(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.compare(self.heap[index], self.heap[parent]):
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.up_heap(parent)
            
    def insert(self, value):
        self.heap.append(value)
        self.up_heap(len(self.heap) - 1)

    def extract(self):
        if len(self.heap) == 0:
            return None
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        item = self.heap.pop()
        self.down_heap(0)
        return item

    def top(self):
        return self.heap[0] if not self.is_empty() else None
