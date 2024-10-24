class Stack:
    def __init__(self):
        self.elements = []
    
    def push(self, element):
        self.elements.append(element)
    
    def pop(self):
        if self.isempty():
            raise IndexError("No element to pop")
        else:
            return self.elements.pop()
    
    def isempty(self):
        return len(self.elements) == 0

        
    