from AVL_tree import BNODE, BST as AVL
class WordTree(AVL):
    def __init__(self):
        super(WordTree, self).__init__()
    def search(self, node, value):#override, we want to know inorder index (0-indexed)
        #Divide and Conquer:
        #   find inorder index under the scope of current subtree from that of children subtrees
        if node == None: return None, -1
        if value == node.V:
            #left subtree appends to the left
            return node, (0 if node.L == None else node.L.subTcnt)
        if value < node.V:
            vtx, count = self.search(node.L, value)
            #smaller than current node, so current node and right subtree appends to the right
            #if node == None: return None, -1
            return vtx, count
        vtx, count = self.search(node.R, value)
        if vtx == None: return None, -1
        #larger than current node, so current node and left subtree appends to the left
        return vtx, count + 1 + (0 if node.L == None else node.L.subTcnt)
    def get_smallest_larger(self, node, value):#inclusive
        if node == None: return None
        if value <= node.V:
            vtx = self.get_smallest_larger(node.L, value)
            return node if vtx == None else vtx
        #node.V < value
        return self.get_smallest_larger(node.R, value)
    def get_largest_smaller(self, node, value):#exclusive
        if node == None: return None
        if node.V < value:
            vtx = self.get_largest_smaller(node.R, value)
            return node if vtx == None else vtx
        #value <= node.V
        return self.get_largest_smaller(node.L, value)
    def traverse(self, node, start, end, index, arr):
        if node == None: return
        Lindex = index - (0 if node.L == None else (0 if node.L.R == None else node.L.R.subTcnt)) - 1
        Rindex = index + (0 if node.R == None else (0 if node.R.L == None else node.R.L.subTcnt)) + 1
        #left subtree have even smaller inorder indices so we don't need to traverse there
        if index < start: self.traverse(node.R, start, end, Rindex, arr)
        #right subtree have even larger inorder indices so we don't need to traverse there
        elif index > end: self.traverse(node.L, start, end, Lindex, arr)
        #I am now within range, expand left and right to get the consecutive segment that we are looking for
        else:
            self.traverse(node.L, start, end, Lindex, arr)
            arr.append(node.V)
            self.traverse(node.R, start, end, Rindex, arr)
    def find_matches(self, prefix):
        '''
        lexicographic order:
        1. Compare left-to-right by character, e.g. 'a'<'b' so "bcabc" < "bcbzz"
        2. If all comparable characters are equal, the shorter word is smaller, e.g. "abc" < "abcd"
        Consider a sorted array of all words:
        -> notice that words with the same prefix will be grouped in a consecutive subsequence of the array
            e.g. {"abc", "abcd", "abce", "abcgfdgdfg", "abe"}
        -> also notice that all words with the shared prefix have their index less than the incremented prefix
            e.g. "abc", "abcd", "abce", "abcgfdgdfg" are all smaller than "abd"
        -> S := index of the smallest word that is >= incremented prefix (done via binary search)
        -> E := find index of the largest word that is < incremented prefix (done via binary search)
        -> perform inorder traversal for [S, E]
        '''
        if prefix == "": return []
        #incremented prefix string
        incre_string = prefix[:len(prefix)-1]+(chr(ord(prefix[-1])+1))
        #get start and end indices' nodes
        start_node = self.get_smallest_larger(self.root, prefix)
        end_node = self.get_largest_smaller(self.root, incre_string)
        #catch the condition of no prefix match
        if start_node == None or end_node == None: return []
        start_index = self.search(self.root, start_node.V)[1]
        end_index = self.search(self.root, end_node.V)[1]
        print(start_node.V, start_index)
        print(end_node.V, end_index)
        print()
        arr = []
        self.display(self.root)
        self.traverse(self.root, start_index, end_index, 0 if self.root.L == None else self.root.L.subTcnt, arr)
        return arr
print("Welcome to the Autocomplete system!")
tree = WordTree()
while True:
    print("Choose an option:\n1. Insert a word\n2. Search for a word\n3. Autocomplete a word\n4. Exit\n")
    option = input("> ")
    while option not in ["1","2","3","4"]:
        print("invalid option")
        option = input("> ")
    if option == "1":
        word = input("Enter a word to insert: ")
        if tree.search(tree.root, word)[0] == None:
            tree.insert(tree.root, BNODE(val=word))
            print(f'Word "{word}" has been inserted')
        else: print(f'Word "{word}"" already exists in word bank')
    elif option == "2":
        word = input("Enter search keyword: ")
        print("keyword found" if tree.search(tree.root, word)[0] != None else "keyword not found")
    elif option == "3":
        word = input("Enter a prefix: ")
        print(tree.find_matches(word))
    else:
        print("APPLICATION CLOSED")
        break
    print()
