from bin import Bin
from avl import AVLTree
from avl import nested_Tree
from object import Object, Color
from exceptions import NoBinFoundException
class GCMS:
    def __init__(self):
        self.object_address=nested_Tree()
        self.helper=nested_Tree()
        self.arrangement=nested_Tree()
    def add_bin(self, bin_id, capacity):
        ST = AVLTree()
        self.arrangement.root = self.arrangement.insert(self.arrangement.root, bin_id, capacity, ST)
        def insert_into_helper(temp, capacity, bin_id):
            while temp is not None:
                if temp.x == capacity:
                    temp.ST.root = temp.ST.insert(temp.ST.root, bin_id)
                    return True
                temp = temp.right if temp.x < capacity else temp.left
            return False
        if not insert_into_helper(self.helper.root, capacity, bin_id):
            ct = AVLTree()
            ct.root = ct.insert(ct.root, bin_id)
            self.helper.root = self.helper.insert(self.helper.root, capacity, 0, ct)
    def add_object(self, object_id, size, color):
        def find_bin_and_update(possible_capacity, direction, object_id, size, color):
            temp = self.helper.root
            while temp is not None:
                if temp.x < possible_capacity:
                    temp = temp.right
                elif temp.x > possible_capacity:
                    temp = temp.left
                else:
                    temp2 = temp.ST.root
                    while getattr(temp2, direction) is not None:
                        temp2 = getattr(temp2, direction)
                    req_bin = temp2.data
                    self.object_address.root = self.object_address.insert(self.object_address.root, object_id, (size, color), req_bin)
                    z = self.arrangement.root
                    while z is not None:
                        if z.x == req_bin:
                            initial = z.y
                            z.y -= size
                            final = z.y
                            z.ST.root = z.ST.insert(z.ST.root, object_id)
                            break
                        z = z.left if z.x > req_bin else z.right
                    temp.ST.root = temp.ST.delete(temp.ST.root, req_bin)
                    if temp.ST.root is None:
                        self.helper.root = self.helper.delete(self.helper.root, temp.x)
                    update_bin(final, req_bin)
                    break
        def update_bin(final, req_bin):
            temp = self.helper.root
            seen_capacity = False
            while temp is not None:
                if temp.x == final:
                    temp.ST.root = temp.ST.insert(temp.ST.root, req_bin)
                    seen_capacity = True
                    break
                temp = temp.right if temp.x < final else temp.left
            if not seen_capacity:
                ct = AVLTree()
                ct.root = ct.insert(ct.root, req_bin)
                self.helper.root = self.helper.insert(self.helper.root, final, 0, ct)
        found = 0
        temp = self.helper.root
        possible_capacity = None
        while temp is not None:
            if temp.x < size:
                temp = temp.right
            elif temp.x >= size:
                possible_capacity = temp.x
                temp = temp.left if color in {Color.BLUE, Color.YELLOW} else temp.right
                found = 1
        if found == 0:
            raise NoBinFoundException
        direction = 'left' if color in {Color.BLUE, Color.RED} else 'right'
        find_bin_and_update(possible_capacity, direction, object_id, size, color)
    def delete_object(self, object_id):
        temp = self.object_address.root
        while temp:
            if temp.x == object_id:
                bin_address, hidden_size = temp.ST, temp.y[0]
                z = self.arrangement.root
                while z:
                    if z.x == bin_address:
                        z.ST.root = z.ST.delete(z.ST.root, object_id)
                        z.y += hidden_size
                        break
                    z = z.right if z.x < bin_address else z.left
                break
            temp = temp.left if temp.x > object_id else temp.right
        self.object_address.root = self.object_address.delete(self.object_address.root, object_id)
    def bin_info(self, bin_id):
        temp = self.arrangement.root
        while temp:
            if temp.x == bin_id:
                return temp.y, temp.ST.inorder(temp.ST.root)
            temp = temp.right if temp.x < bin_id else temp.left
    def object_info(self, object_id):
        temp = self.object_address.root
        while temp:
            if temp.x == object_id:
                return temp.ST
            temp = temp.right if temp.x < object_id else temp.left
        raise ValueError