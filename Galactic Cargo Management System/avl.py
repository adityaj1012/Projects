from node import Node
class AVLTree:
    def __init__(self):
        self.root=None
    def inorder(self,root):
        if root==None:
            return []
        else:
            return self.inorder(root.left)+[root.data]+self.inorder(root.right)
    def height(self,root):
        if root==None:
            return 0
        return root.height
    def balance(self,root):
        if root==None:
            return 0
        else:
            return self.height(root.left)-self.height(root.right)
    def left_rotate(self,a):
        T0=a.left
        b=a.right
        T1=b.left
        a.right=T1
        b.left=a
        a.height=1+max(self.height(a.left),self.height(a.right))
        b.height=1+max(self.height(b.left),self.height(b.right))
        return b
    def right_rotate(self,a):
        b=a.left
        T0=a.right
        T1=b.right
        a.left=T1
        b.right=a
        a.height=1+max(self.height(a.left),self.height(a.right))
        b.height=1+max(self.height(b.left),self.height(b.right))
        return b
    def insert(self,root,key):
        if root==None:
            a=Node(key)
            return a
        else:
            if root.data<key:
                root.right=self.insert(root.right,key)
            elif root.data>key:
                root.left=self.insert(root.left,key)
        root.height=1+max(self.height(root.left),self.height(root.right))
        bal = self.balance(root)
        if bal>1 and key<root.left.data:
            return self.right_rotate(root)
        elif bal>1 and key>root.left.data:
            root.left=self.left_rotate(root.left)
            return self.right_rotate(root)
        elif bal<-1 and key>root.right.data:
            return self.left_rotate(root)
        elif bal<-1 and key<root.right.data:
            root.right=self.right_rotate(root.right)
            return self.left_rotate(root)
        return root
    def delete(self,root,key):
        if root==None:
            return None
        else:
            if key<root.data:
                root.left=self.delete(root.left,key)
            elif key>root.data:
                root.right=self.delete(root.right,key)
            elif key==root.data:
                if root.left==root.right==None:
                    return None
                elif root.left==None:
                    root=root.right
                elif root.right==None:
                    root=root.left
                else:
                    temp=root.left
                    while temp.right!=None:
                        temp=temp.right
                    root.data=temp.data
                    root.left=self.delete(root.left,root.data)
        root.height=1+max(self.height(root.left),self.height(root.right))
        bal=self.balance(root)
        if bal>1 and self.balance(root.left)>=0:
            return self.right_rotate(root)
        elif bal>1 and self.balance(root.left)<0:
            root.left=self.left_rotate(root.left)
            return self.right_rotate(root)
        elif bal<-1 and self.balance(root.right)<=0:
            return self.left_rotate(root)
        elif bal<-1 and self.balance(root.right)>0:
            root.right=self.right_rotate(root.right)
            return self.left_rotate(root)
        return root
class nest_node:
    def __init__(self,x,y,ST):
        self.x=x
        self.y=y
        self.ST=ST
        self.left=None
        self.right=None
        self.height=1
class nested_Tree:
    def __init__(self):
        self.root=None
    def height(self,root):
        if root==None:
            return 0
        else:
            return root.height
    def balance(self,root):
        if root==None:
            return 0
        else:
            return self.height(root.left)-self.height(root.right)
    def left_rotate(self,a):
        T0=a.left
        b=a.right
        T1=b.left
        a.right=T1
        b.left=a
        a.height=1+max(self.height(a.left),self.height(a.right))
        b.height=1+max(self.height(b.left),self.height(b.right))
        return b
    def right_rotate(self,a):
        b=a.left
        T0=a.right
        T1=b.right
        a.left=T1
        b.right=a
        a.height=1+max(self.height(a.left),self.height(a.right))
        b.height=1+max(self.height(b.left),self.height(b.right))
        return b
    def insert(self, root, x, y, ST):
        if root is None:
            return nest_node(x, y, ST)
        if x < root.x:
            root.left = self.insert(root.left, x, y, ST)
        else:
            root.right = self.insert(root.right, x, y, ST)
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        bal = self.balance(root)
        if bal > 1 and x < root.left.x:
            return self.right_rotate(root)
        if bal < -1 and x > root.right.x:
            return self.left_rotate(root)
        if bal > 1 and x > root.left.x:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if bal < -1 and x < root.right.x:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root
    def delete(self, root, x):
        if not root:
            return None
        if x < root.x:
            root.left = self.delete(root.left, x)
        elif x > root.x:
            root.right = self.delete(root.right, x)
        else:
            if not (root.left or root.right):
                return None
            root = root.right if not root.left else root.left if not root.right else root
            if root.left and root.right:
                temp = root.left
                while temp.right:
                    temp = temp.right
                root.x, root.y, root.ST = temp.x, temp.y, temp.ST
                root.left = self.delete(root.left, temp.x)
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)
        if balance > 1:
            return self.right_rotate(root) if self.balance(root.left) >= 0 else self.left_right_rotate(root)
        elif balance < -1:
            return self.left_rotate(root) if self.balance(root.right) <= 0 else self.right_left_rotate(root)
        return root
    def left_right_rotate(self, root):
        root.left = self.left_rotate(root.left)
        return self.right_rotate(root)
    def right_left_rotate(self, root):
        root.right = self.right_rotate(root.right)
        return self.left_rotate(root)