# AVL_Trees
Class project
- First, we implemented the AVL tree which achieves logarithmic time for insertions and deletions in the worst-case scenario.

- Then, we created the autocomplete system that stores a word bank within the AVL tree, and offers a UI to insert words, query words, find word suggestions based on a given prefix keyword, and allows the user to quit the program

  - Insertions and queries are default functionalities of the original AVL tree

  - The word suggestion functionality is achieved using an optimized inorder traversal technique using Divide and Conquer strategies
  
      - calculates the inorder index from parent node's inorder index
      
      - avoids unnecessary traversals with the monotonicity of inorder indices
      
          - left subtree's indices are all smaller
          
          - right subtree's indices are all greater
