class BNODE:
    def __init__(self, L=None, R=None, par=None, val=None):
        self.L = L
        self.R = R
        self.par = par
        self.V = val
        self.subTH = 1 #single node
        self.subTcnt =1
class BST:
    def __init__(self):#assume all nodes are given their values beforehand
        self.root = None
    def update_height(self, node):
        node.subTcnt = (0 if node.L == None else node.L.subTcnt)\
                      +(0 if node.R == None else node.R.subTcnt) + 1
        node.subTH = max(0 if node.L == None else node.L.subTH,
                         0 if node.R == None else node.R.subTH) + 1
    def rotateL(self, node, OGparent): #rotate right node leftward, right node is right-heavy
        lchild = node.L #might be NULL
        grandpa = OGparent.par #might be NULL
        #make node the new root of parent's tree
        node.par = grandpa
        if grandpa != None:
            if OGparent == grandpa.L: grandpa.L = node
            else: grandpa.R = node
        #make original parent under node
        node.L = OGparent #assigning node.L to someone else doesn't change the pointer to the original object
        OGparent.par = node
        #restructure subtree
        OGparent.R = lchild
        if lchild != None: lchild.par = OGparent
        #maintain height info
        self.update_height(OGparent)#now below, so update first
        self.update_height(node)
        if self.root == OGparent: self.root = node
    def rotateR(self, node, OGparent): #rotate left node rightward, left node is left-heavy
        rchild = node.R #might be NULL
        grandpa = OGparent.par #might be NULL
        #make node the new root of parent's tree
        node.par = grandpa
        if grandpa != None:
            if OGparent == grandpa.L: grandpa.L = node
            else: grandpa.R = node
        #make original parent under node
        node.R = OGparent #assigning node.R to someone else doesn't change the pointer to the original object
        OGparent.par = node
        #restructure subtree
        OGparent.L = rchild
        if rchild != None: rchild.par = OGparent
        #maintain height info
        self.update_height(OGparent)#now below, so update first
        self.update_height(node)
        if self.root == OGparent: self.root = node
    def rotateRL(self, node, OGparent): #rotate right node leftward, right node is left-heavy
        lchild = node.L #node.L gets changed in the process, so point to the object directly
        self.rotateR(lchild, node)
        self.rotateL(lchild, OGparent)
    def rotateLR(self, node, OGparent): #rotate left node rightward, left node is right-heavy
        rchild = node.R #node.R gets changed in the process, so point to the object directly
        self.rotateL(rchild, node)
        self.rotateR(rchild, OGparent)
    def rebalance(self, node):
        #rebalancing (assume subtrees are all balanced when we reach this step for proof by induction)
        LRdiff = (0 if node.L == None else node.L.subTH) - (0 if node.R == None else node.R.subTH)
        if LRdiff > 1:#left is heavier and unbalanced (as a consequence it is not NULL)
            #left of left is heavier
            if (0 if node.L.L == None else node.L.L.subTH) > (0 if node.L.R == None else node.L.R.subTH):
                self.rotateR(node.L, node)
            #right of left is heavier (equality is trivial cause rotation change difference by at most 1)
            else: self.rotateLR(node.L, node)
        elif LRdiff < -1:#right is heavier and unbalanced (as a consequence it is not NULL)
            #right of right is heavier
            if (0 if node.R.R == None else node.R.R.subTH) > (0 if node.R.L == None else node.R.L.subTH):
                self.rotateL(node.R, node)
            #left of right is heavier (equality is trivial cause rotation change difference by at most 1)
            else: self.rotateRL(node.R, node)
    def insert(self, node, new):
        #when the tree is empty
        if self.root == None:#which also means node == None
            self.root = new
            self.root.par = None
            #self.root.subTH = 1
            #self.root.subTcnt = 1
            return
        #when at leaf node
        if node.L == None and node.R == None:
            if new.V > node.V: node.R = new
            else: node.L = new
            new.par = node
            #new.subTH = 1
            #new.subTcnt = 1
        #for internal nodes
        else:
            #divide and conquer (subtree of BST is also BST)
            if new.V > node.V:#insert to right (>)
                if node.R == None: #reached end of recursion
                    node.R = new
                    new.par = node
                    #new.subTH = 1
                    #new.subTcnt = 1
                else: self.insert(node.R, new)
            else:#insert to left (<=)
                if node.L == None: #reached end of recursion
                    node.L = new
                    new.par = node
                    #new.subTH = 1
                    #new.subTcnt = 1
                else: self.insert(node.L, new)
        self.update_height(node)
        self.rebalance(node)
    def search(self, node, value):
        if node == None: return None #not found in BST
        if value == node.V: return node #found value
        if value > node.V: return self.search(node.R, value) #query right
        return self.search(node.L, value) #query left
    def replace(self, par, node, rep_node):#replace by a new individual node
        lchild = node.L
        rchild = node.R
        #remove node from tree
        node.par = None
        node.L = None
        node.R = None
        node.subTH = 1
        node.subTcnt = 1
        #in case the root of BST is changed
        if self.root == node: self.root = rep_node
        #link replacement node to original node's parent
        if rep_node != None: rep_node.par = par
        #link original node's parent to replacement node
        if par != None:
            if par.L == node: par.L = rep_node
            else: par.R = rep_node
        #take over original node's children
        if rep_node != None:
            rep_node.L = lchild
            if lchild != None: lchild.par = rep_node
            rep_node.R = rchild
            if rchild != None: rchild.par = rep_node
            self.update_height(rep_node)
            #parent's subtree size remains unchanged
    def delete(self, node):
        vtx = node.par #assume leaf or at turn
        #no child exists (delete leaf)
        if node.L == None and node.R == None:
            if self.root == node: self.root = None
            self.replace(node.par, node, None)
        #only left child exists
        elif node.L != None and node.R == None:
            lchild = node.L
            self.replace(node, node.L, None)
            self.replace(node.par, node, lchild)
            if self.root == node: self.root = lchild
        #only right child exists
        elif node.R != None and node.L == None:
            rchild = node.R
            self.replace(node, node.R, None)
            self.replace(node.par, node, rchild)
            if self.root == node: self.root = rchild
        #when both child exist
        else:
            #extract max from left subtree (subproblem, falls into previous O(1) cases)
            #X >= L subtree members, X < R subtree members, so the left <= node < right property is maintained
            spot = self.find_max(node.L)
            vtx = spot if spot.par == node else spot.par
            #remove substitute node from tree directly (no rebalancing for now)
            self.replace(spot.par, spot, None) #because it is a leaf node
            #replace the targetted node with substitute
            if self.root == node: self.root = spot
            self.replace(node.par, node, spot)
        #rebalancing bottom to up through ancestors (subtrees are not)
        while vtx != None:
            self.update_height(vtx)
            self.rebalance(vtx)
            vtx = vtx.par
    def find_max(self, node):#keep going right to reach max
        if self.root == None: return None
        while node.R != None: node = node.R
        return node
    def find_min(self, node):#keep going left to reach min
        if self.root == None: return None
        while node.L != None: node = node.L
        return node
    def inorder(self, node):
        arr = []
        def traversal(node):
            if node == None: return
            print(node.V, end=' ')
            lchild = node.L
            rchild = node.R
            traversal(lchild)
            arr.append(node.V)
            traversal(rchild)
        traversal(node)
        print()
        return arr
    def display(self, node):
        if node == None: return True
        print(f"vertex value = {node.V}: ",end='')
        print(f"Lchild value = {node.L.V if node.L != None else 'None'}, Rchild value = {node.R.V if node.R != None else 'None'}, par value = {node.par.V if node.par != None else 'None'}, subtree height = {node.subTH}, subtree size = {node.subTcnt}")
        isAVL_L = self.display(node.L)
        isAVL_R = self.display(node.R)
        return abs((0 if node.L == None else node.L.subTH) - (0 if node.R == None else node.R.subTH)) < 2 and isAVL_L and isAVL_R
'''
vertexvalues = [8,3,10,1,6,14,4,7,13]
node_lookup = [BNODE() for i in range(len(vertexvalues))]
#construct BST testing
print("INSERTIONS")
bst = BST()
for i in range(len(vertexvalues)):
    print(f"insert {vertexvalues[i]}")
    node_lookup[i] = BNODE(val=vertexvalues[i])
    bst.insert(bst.root, node_lookup[i])
    print(f"root: {'None' if bst.root == None else bst.root.V}")
    print(bst.display(bst.root))
    print(bst.inorder(bst.root))
    mx = bst.find_max(bst.root)
    mn = bst.find_min(bst.root)
    print(f"MIN: {None if mn == None else mn.V}")
    print(f"MAX: {None if mx == None else mx.V}")
    print()
#test binary search on BST
print("SEARCHES")
queries = [4, 14, 8, 15]
for q in queries:
    node = bst.search(bst.root, q)
    print(None if node == None else node.V)
print()
#delete bst testing
print("DELETIONS")
for i in range(len(vertexvalues)):
    print(f"delete {vertexvalues[i]}")
    bst.delete(node_lookup[i])
    print(f"root: {'None' if bst.root == None else bst.root.V}")
    print(bst.display(bst.root))
    print(bst.inorder(bst.root))
    mx = bst.find_max(bst.root)
    mn = bst.find_min(bst.root)
    print(f"MIN: {None if mn == None else mn.V}")
    print(f"MAX: {None if mx == None else mx.V}")
    print()
'''