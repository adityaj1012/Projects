from avl import AVLTree
from object import Object
class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.list_object = AVLTree()
    def add_object(self, object):
        self.capacity -= object.size
        self.list_ob.root=self.list_ob.insert(self.list_ob.root,object.object_id)
