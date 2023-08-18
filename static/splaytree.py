class Node:
    def __init__(self,data=None,parent=None,left=None,right=None):
        self.data=data
        self.parent=parent
        self.left=left
        self.right=right
class SplayTree:
    def __init__(self) -> None:
        self.root=None

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y

        elif x == x.parent.left:
            x.parent.left = y

        else:                       
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x
  
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def splay(self, n):
        while n.parent != None:
            if n.parent == self.root:
                if n == n.parent.left:
                    self.right_rotate(n.parent)
                else:
                    self.left_rotate(n.parent)

            else:
                p = n.parent
                g = p.parent
                if n.parent.left == n and p.parent.left == p:
                    self.right_rotate(g)
                    self.right_rotate(p)

                elif n.parent.right == n and p.parent.right == p:
                    self.left_rotate(g)
                    self.left_rotate(p)

                elif n.parent.right == n and p.parent.left == p:
                    self.left_rotate(p)
                    self.right_rotate(g)

                elif n.parent.left == n and p.parent.right == p:
                    self.right_rotate(p)
                    self.left_rotate(g)
    def maxelt(self, x):
        while x.right != None:
            x = x.right
        return x
    def insert(self, n):
        y = None
        temp = self.root
        while temp != None:
            y = temp
            if n.data < temp.data:
                temp = temp.left
            else:
                temp = temp.right

        n.parent = y

        if y == None:
            self.root = n
        elif n.data < y.data:
            y.left = n
        else:
            y.right = n

        self.splay(n)

    def search(self, n, x):
        if x == n.data:
            self.splay(n)
            return n

        elif x < n.data:
            return self.search(n.left, x)
        elif x > n.data:
            return self.search(n.right, x)
        else:
            return None

    def delete(self, n):
        self.splay(n)

        left_subtree = SplayTree()
        left_subtree.root = self.root.left
        if left_subtree.root != None:
            left_subtree.root.parent = None

        right_subtree = SplayTree()
        right_subtree.root = self.root.right
        if right_subtree.root != None:
            right_subtree.root.parent = None

        if left_subtree.root != None:
            m = left_subtree.maxelt(left_subtree.root)
            left_subtree.splay(m)
            left_subtree.root.right = right_subtree.root
            self.root = left_subtree.root

        else:
            self.root = right_subtree.root

    def inorder(self, n=1):
        if n==1:
            n=self.root
        if n != None:
            self.inorder(n.left)
            print(n.data)
            self.inorder(n.right)
    def preorder(self, n=1):
        if n==1:
            n=self.root
        if n != None:
            print(n.data)
            self.preorder(n.left)
            self.preorder(n.right)

st= SplayTree()
e1 = Node(11)
e2= Node(22)
e3= Node(33)
e4= Node(110)
e5= Node(99)
e6= Node(44)
e7= Node(55)
e8= Node(66)
st.insert(e1)
st.insert(e2)
st.insert(e3)
st.insert(e4)
st.insert(e5)
st.insert(e6)
st.insert(e7)
st.insert(e8)
st.search(st.root,33)
print("Inorder:")
st.inorder()
print("Preorder:\nThe recently accessed node became the root now!")
st.preorder()