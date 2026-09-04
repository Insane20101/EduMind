# BCS-202 - Principles of Data Structures
## Detailed Step-Wise Solutions — Units I–IV (Combined)

## Detailed Step-Wise Solutions — UNIT I: Introduction to Data Structures
### Section A: Definitions & Concept Questions

**Q1. [Unit I | Topic: Basic Terminology | Type: Theory | Difficulty: Basic]**  
**Question:** Define the term "data structure" and explain its importance in computer science.  

*Concept from scratch:* A data structure is a specialized format for organizing, processing, and storing data in a computer. It allows for efficient access and modification of data, which is crucial for various algorithms and applications. Data structures can be used to manage large amounts of data efficiently and are fundamental in developing software applications.  

*Result:* Data structures are essential as they enable efficient data manipulation and storage, impacting performance and scalability in software development.

**Q2. [Unit I | Topic: Complexity | Type: Theory | Difficulty: Basic]**  
**Question:** What is time-space trade-off? Provide an example to illustrate your explanation.  

*Concept from scratch:* The time-space trade-off refers to the concept in computer science where the amount of memory usage can be reduced at the cost of increased processing time, or vice versa. This trade-off helps optimize algorithms based on the constraints of either memory or speed.  

*Example:* For example, using a hash table for searching can significantly reduce the search time to O(1) compared to O(n) for a list, but it requires additional space for storing the hash table.  

*Result:* The time-space trade-off is pivotal in algorithm design, balancing between memory usage and execution speed.

**Q3. [Unit I | Topic: Arrays | Type: Theory | Difficulty: Basic]**  
**Question:** Describe the representation of arrays in memory.  

*Concept from scratch:* An array is a collection of elements stored in contiguous memory locations. The elements are accessed using an index, starting from zero in most programming languages. The size of the array is fixed upon creation, and all elements are of the same data type.  

*Step 1 — Memory allocation:* When an array is declared, a block of memory is allocated based on the size of the array and the size of each element.  

*Step 2 — Address calculation:* The address of an element can be calculated using the formula:  
  `Address of A[i] = Base address + (i * size of element)`.  

*Result:* Arrays are represented in contiguous memory, facilitating efficient access through index-based addressing.

**Q4. [Unit I | Topic: Stacks | Type: Theory | Difficulty: Basic]**  
**Question:** What is a stack? List its main operations.  

*Concept from scratch:* A stack is a linear data structure that follows the Last In First Out (LIFO) principle, meaning the last element added is the first to be removed. It is akin to a stack of plates where you can only add or remove the top plate.  
*Main operations:*  

1. **Push:** Add an element to the top of the stack.  

2. **Pop:** Remove the element from the top of the stack.  

3. **Peek (or Top):** View the element at the top without removing it.  

4. **IsEmpty:** Check if the stack is empty.  

*Result:* Stacks are crucial for managing function calls, expression evaluations, and backtracking algorithms.

### Section B: Computational & Applied Problems

**Q1. [Unit I | Topic: Address Calculation | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Given an array of integers stored at the base address 1000 and each integer occupies 4 bytes, find the address of the element at index 5.  

*Concept from scratch:* To find the address of an array element, we use the address calculation formula described earlier.  

*Step 1 — Base address:* The base address of the array is 1000.  

*Step 2 — Size of each element:* Each integer occupies 4 bytes.  

*Step 3 — Index:* We need to find the address for index 5.  

*Step 4 — Calculation:*  
`Address of A[5] = Base address + (5 * size of element)`  
`Address of A[5] = 1000 + (5 * 4)`  
`Address of A[5] = 1000 + 20 = 1020`.  

*Result:* The address of the element at index 5 is 1020.

**Q2. [Unit I | Topic: Stack Operations | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Implement the infix to postfix conversion for the expression `(A + B) * C`.  

*Concept from scratch:* Infix notation is the conventional notation where operators are placed between operands. Postfix notation (Reverse Polish Notation) places operators after their operands.  

*Step 1 — Use a stack for operators and output for postfix.*  

*Step 2 — Process each symbol:*  
- Encounter `(`: Push onto stack.  
- Encounter `A`: Add to output.  
- Encounter `+`: Push onto stack.  
- Encounter `B`: Add to output.  
- Encounter `)`: Pop from stack to output until `(` is encountered.  
- Encounter `*`: Push onto stack.  
- Encounter `C`: Add to output.  

*Step 3 — Pop all operators from the stack to output.*  

*Result:* The postfix expression is `AB+C*`.

**Q3. [Unit I | Topic: Tower of Hanoi | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Solve the Tower of Hanoi problem for 3 disks and show the sequence of moves.  

*Concept from scratch:* The Tower of Hanoi is a classic problem involving three pegs and a number of disks of different sizes that can slide onto any peg. The objective is to move the entire stack to another peg, following specific rules.  

*Step 1 — Rules:*  

1. Only one disk can be moved at a time.  

2. Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack or an empty peg.  

3. No larger disk may be placed on top of a smaller disk.  

*Step 2 — Moves for 3 disks (A, B, C):*  

1. Move disk A to peg 3  

2. Move disk B to peg 2  

3. Move disk A to peg 2  

4. Move disk C to peg 3  

5. Move disk A to peg 1  

6. Move disk B to peg 3  

7. Move disk A to peg 3  

*Result:* The sequence of moves for 3 disks is: 1→3, 1→2, 3→2, 1→3, 2→1, 2→3, 1→3.

### Section C: Advanced Theory & Numericals

**Q1. [Unit I | Topic: Stack Applications | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss the applications of stacks in depth, providing examples in various algorithmic scenarios.  

*Concept from scratch:* Stacks are versatile data structures used in various applications in computing, which include:  

1. **Function Calls:** Stacks are used to keep track of function calls (call stack) and local variables.  

2. **Expression Evaluation:** Evaluating expressions (infix, postfix) and converting between notations.  

3. **Backtracking Algorithms:** Used in algorithms like Depth First Search (DFS) where the previous state needs to be preserved.  

4. **Undo Mechanisms:** In applications like text editors, stacks are used to implement undo features.  

*Example:* In expression evaluation, using a stack allows for efficient calculation of postfix expressions.  

*Result:* Stacks play a fundamental role in many algorithms and application designs, enabling efficient data management.

**Q2. [Unit I | Topic: Complexity Analysis | Type: Numerical | Difficulty: Advanced]**  
**Question:** Analyze the time and space complexity of stack operations and justify your answers with examples.  

*Concept from scratch:* The main operations of a stack include push, pop, and peek.  

*Step 1 — Time Complexity:*  
- **Push:** O(1) - Adding an element to the top is a constant-time operation.  
- **Pop:** O(1) - Removing the top element is also a constant-time operation.  
- **Peek:** O(1) - Viewing the top element without removal is constant time.  

*Step 2 — Space Complexity:* The space complexity is O(n), where n is the number of elements in the stack since it stores all elements.  

*Example:* In recursive function calls, the stack grows with each call, demonstrating O(n) space complexity.  

*Result:* Stack operations exhibit O(1) time complexity for primary operations and O(n) space complexity, highlighting their efficiency.

---

## Detailed Step-Wise Solutions — UNIT II: Queues and Linked Lists
### Section A: Definitions & Concept Questions

**Q1. [Unit II | Topic: Queues | Type: Theory | Difficulty: Basic]**  
**Question:** Define a queue and explain its characteristics.  

*Concept from scratch:* A queue is a linear data structure that follows the First In First Out (FIFO) principle, where the first element added is the first to be removed. It is used when the order of processing is important.  
*Characteristics:*  

1. **FIFO Order:** Elements are processed in the order they were added.  

2. **Operations:** Main operations include enqueue (adding) and dequeue (removing).  

3. **Dynamic Size:** Can grow or shrink in size based on the number of elements.  

*Result:* Queues are essential in scenarios where order of processing matters, such as scheduling and buffering.

**Q2. [Unit II | Topic: Linked Lists | Type: Theory | Difficulty: Basic]**  
**Question:** What is a singly linked list? How does it differ from an array?  

*Concept from scratch:* A singly linked list is a linear data structure where elements (nodes) are connected through pointers. Each node contains data and a pointer to the next node.  

*Differences from an array:*  

1. **Dynamic Size:** Linked lists can grow and shrink in size dynamically, while arrays have a fixed size.  

2. **Memory Allocation:** Arrays require contiguous memory allocation, whereas linked lists do not.  

3. **Access Time:** Accessing elements in an array is O(1), while in a linked list, it is O(n) due to traversal.  

*Result:* Singly linked lists provide flexibility in managing data, contrasting with the fixed nature of arrays.

### Section B: Computational & Applied Problems

**Q1. [Unit II | Topic: Circular Queues | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Implement the operations of a circular queue, including enqueue and dequeue operations.  

*Concept from scratch:* A circular queue allows efficient use of space by connecting the end of the queue back to the front.  

*Step 1 — Structure:* Define an array and two pointers (front and rear).  

*Step 2 — Enqueue operation:*  
- Check if the queue is full (when `(rear + 1) % size == front`).  
- Add the element at `rear`, then update `rear` using `(rear + 1) % size`.  

*Step 3 — Dequeue operation:*  
- Check if the queue is empty (when `front == rear`).  
- Remove the element from `front`, then update `front` using `(front + 1) % size`.  

*Result:* Circular queues optimize space and maintain efficient operations for enqueue and dequeue.

**Q2. [Unit II | Topic: Insertion/Deletion in Linked Lists | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Write a function to delete a node from a doubly linked list given a specific value.  

*Concept from scratch:* A doubly linked list allows traversal in both directions and contains pointers to both the next and previous nodes.  

*Step 1 — Function Definition:* Define a function that takes the head of the list and the value to be deleted.  

*Step 2 — Traversal:* Iterate through the list to find the node with the specified value.  
- If found, adjust the pointers of the adjacent nodes to bypass the node to be deleted.  

*Step 3 — Edge Cases:* Handle cases where the node to delete is the head or tail.  

*Result:* The function effectively removes the specified node from the doubly linked list.

### Section C: Advanced Theory & Numericals

**Q1. [Unit II | Topic: Garbage Collection | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the concept of garbage collection in linked lists and its significance in memory management.  

*Concept from scratch:* Garbage collection is an automatic memory management process that reclaims memory occupied by objects that are no longer in use.  

*Significance:*  

1. **Memory Efficiency:** It helps prevent memory leaks by ensuring that unused memory is released back to the system.  

2. **Performance Improvement:** Reduces the risk of fragmentation and optimizes memory usage for applications.  

3. **Safety:** Automates the deallocation process, preventing errors related to manual memory management.  

*Result:* Garbage collection is crucial for maintaining efficient memory management in linked lists and other dynamic data structures.

**Q2. [Unit II | Topic: D-queues | Type: Numerical | Difficulty: Advanced]**  
**Question:** Design a deque (double-ended queue) and implement its basic operations, emphasizing its applications.  

*Concept from scratch:* A deque is a linear data structure that allows insertion and deletion at both ends.  

*Step 1 — Structure:* Define an array or linked list with pointers for both ends (front and rear).  

*Step 2 — Operations:*  

1. **Insert Front:** Add an element to the front, adjusting the front pointer.  

2. **Insert Rear:** Add an element to the rear, adjusting the rear pointer.  

3. **Delete Front:** Remove an element from the front, adjusting the front pointer.  

4. **Delete Rear:** Remove an element from the rear, adjusting the rear pointer.  
*Applications:* Deques are used in scheduling algorithms and managing buffers.  

*Result:* A deque provides flexible data management allowing operations at both ends, enhancing performance in specific applications.

---

## Detailed Step-Wise Solutions — UNIT III: Trees and Binary Search Trees
### Section A: Definitions & Concept Questions

**Q1. [Unit III | Topic: Binary Trees | Type: Theory | Difficulty: Basic]**  
**Question:** Define a binary tree and state its properties.  

*Concept from scratch:* A binary tree is a hierarchical data structure in which each node has at most two children referred to as the left child and the right child.  
*Properties:*  

1. **Node Count:** A binary tree with n nodes has a maximum of n – 1 edges.  

2. **Height:** The height of a tree is the longest path from the root to a leaf.  

3. **Full & Complete Trees:** A full binary tree has all nodes with 0 or 2 children, while a complete binary tree is filled at all levels except possibly the last, which is filled from left to right.  

*Result:* Binary trees are fundamental in representing hierarchical relationships in data.

**Q2. [Unit III | Topic: Traversal Techniques | Type: Theory | Difficulty: Basic]**  
**Question:** What are the different types of tree traversal methods? Explain each briefly.  

*Concept from scratch:* Tree traversal refers to the process of visiting all the nodes in a tree structure.  
*Types of Traversal:*  

1. **In-order:** Left subtree, root, right subtree. Used for binary search trees to retrieve sorted data.  

2. **Pre-order:** Root, left subtree, right subtree. Used to create a copy of the tree or to get prefix expression.  

3. **Post-order:** Left subtree, right subtree, root. Used for deleting the tree or getting postfix expression.  

4. **Level-order:** Visits nodes level by level from top to bottom and left to right.  

*Result:* Different traversal methods serve various purposes in tree operations and applications.

### Section B: Computational & Applied Problems

**Q1. [Unit III | Topic: Insertion in BST | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Insert the following values into a Binary Search Tree: 30, 20, 40, 10, 25, 35, 50.  

*Concept from scratch:* A Binary Search Tree (BST) is a binary tree where for each node, the left subtree contains only nodes with values less than the node’s value and the right subtree only nodes with values greater.  

*Step 1 — Insert 30:* It becomes the root.  

*Step 2 — Insert 20:* It goes to the left of 30.  

*Step 3 — Insert 40:* It goes to the right of 30.  

*Step 4 — Insert 10:* It goes to the left of 20.  

*Step 5 — Insert 25:* It goes to the right of 20.  

*Step 6 — Insert 35:* It goes to the left of 40.  

*Step 7 — Insert 50:* It goes to the right of 40.  

*Result:* The BST structure is as follows:

```
       30
      /  \
    20    40
   / \    / \
  10  25 35  50
```

**Q2. [Unit III | Topic: Huffman Algorithm | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Construct a Huffman tree for the following frequencies: A(5), B(9), C(12), D(13), E(16), F(45).  

*Concept from scratch:* Huffman coding is a compression technique that uses variable-length codes based on the frequency of occurrence of the characters.  

*Step 1 — Create leaf nodes for each character and build a priority queue.*  

*Step 2 — While more than one node remains in the queue:*  
- Remove the two nodes with the smallest frequency.  
- Create a new internal node with these two nodes as children and with a frequency equal to the sum of their frequencies.  
- Insert the new node back into the queue.  

*Step 3 — Repeat until only one node remains.*  

*Result:* The Huffman tree will have the structure based on the frequencies, leading to optimal prefix codes for each character.

### Section C: Advanced Theory & Numericals

**Q1. [Unit III | Topic: AVL Trees | Type: Theory | Difficulty: Advanced]**  
**Question:** Discuss AVL trees and explain how balancing is achieved during insertion and deletion.  

*Concept from scratch:* An AVL tree is a self-balancing binary search tree where the difference between heights of left and right subtrees cannot be more than one for all nodes.  
*Balancing Technique:*  

1. **Rotations:** When the tree becomes unbalanced after an insertion or deletion, rotations are performed to restore balance.  
   - **Left Rotation:** Used when a right-heavy tree is encountered.
   - **Right Rotation:** Used when a left-heavy tree is encountered.
   - **Double Rotations:** Used in cases of left-right or right-left imbalances.  

*Result:* AVL trees maintain balance through these rotations, ensuring O(log n) time complexity for insertions and deletions.

**Q2. [Unit III | Topic: B-trees | Type: Numerical | Difficulty: Advanced]**  
**Question:** Create a B-tree of order 3 and insert the following keys: 10, 20, 5, 6, 12, 30, 7.  

*Concept from scratch:* A B-tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time. Each node can have multiple children.  

*Step 1 — Insert 10:* Root becomes 10.  

*Step 2 — Insert 20:* Node becomes [10, 20].  

*Step 3 — Insert 5:* Node becomes [5, 10, 20].  

*Step 4 — Insert 6:* Node becomes [5, 6, 10, 20]. (Split occurs, 10 becomes new root)  

*Step 5 — Insert 12:* Node becomes [10, 12, 20].  

*Step 6 — Insert 30:* Node becomes [10, 12, 20, 30].  

*Step 7 — Insert 7:* Node becomes [7, 10, 12, 20, 30]. (Split occurs, 12 becomes new root)  

*Result:* The final B-tree structure accommodates all keys and maintains order.

---

## Detailed Step-Wise Solutions — UNIT IV: Searching, Hashing, and Sorting
### Section A: Definitions & Concept Questions

**Q1. [Unit IV | Topic: Searching Algorithms | Type: Theory | Difficulty: Basic]**  
**Question:** Differentiate between sequential search and binary search.  

*Concept from scratch:* Searching algorithms are used to find an element in a data structure.  
*Sequential Search:*  
- **Method:** Checks each element sequentially until the desired element is found.  
- **Complexity:** O(n).  
*Binary Search:*  
- **Method:** Requires sorted data and divides the search interval in half repeatedly.  
- **Complexity:** O(log n).  

*Result:* Sequential search is simpler but less efficient than binary search, which is efficient for sorted arrays.

**Q2. [Unit IV | Topic: Hashing | Type: Theory | Difficulty: Basic]**  
**Question:** What is hashing and what are its applications?  

*Concept from scratch:* Hashing is a process of converting input data (keys) into a fixed-size string of bytes, typically using a hash function that generates a hash code.  
*Applications:*  

1. **Data Retrieval:** Hash tables use hashing for efficient data retrieval.  

2. **Cryptography:** Hashing is used in secure data storage and transmission.  

3. **Data Integrity:** Verifying data integrity through checksums and hashes.  

*Result:* Hashing enables efficient data management and security across various applications.

### Section B: Computational & Applied Problems

**Q1. [Unit IV | Topic: Collision Resolution | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Given a hash table of size 10 and the following keys: 15, 25, 35, 45, apply linear probing for collision resolution.  

*Concept from scratch:* Linear probing is a collision resolution method in hash tables where the next available slot is found by checking subsequent slots.  

*Step 1 — Hash Function:* Use a simple modulo function: `hash(key) = key % size`.  

*Step 2 — Insert keys:*  
- Insert 15: `15 % 10 = 5`.  
- Insert 25: `25 % 10 = 5`, collision occurs (move to next slot, 6).  
- Insert 35: `35 % 10 = 5`, collision (move to next, now 7).  
- Insert 45: `45 % 10 = 5`, collision (move to next, now 8).  

*Result:* The hash table will have the keys at positions:  

```
Index:    0  1  2  3  4  5  6  7  8  9
Value:    -  -  -  -  -  15 25 35 45  -
```

**Q2. [Unit IV | Topic: Sorting Algorithms | Type: Numerical | Difficulty: Intermediate]**  
**Question:** Sort the following array using quicksort: [34, 7, 23, 32, 5, 62].  

*Concept from scratch:* Quicksort is a divide-and-conquer algorithm that sorts an array by selecting a 'pivot' element and partitioning the other elements into two sub-arrays.  

*Step 1 — Choose Pivot:* Select the last element as pivot (62).  

*Step 2 — Partitioning:* Rearrange the array so that elements less than the pivot are on the left and those greater are on the right.  

*Step 3 — Recursive Sort:* Recursively apply this to the left and right sub-arrays until the base case is reached.  

*Result:* The sorted array is [5, 7, 23, 32, 34, 62].

### Section C: Advanced Theory & Numericals

**Q1. [Unit IV | Topic: Graph Representations | Type: Theory | Difficulty: Advanced]**  
**Question:** Explain the various ways to represent graphs and their advantages and disadvantages.  

*Concept from scratch:* Graphs can be represented in several ways:  

1. **Adjacency Matrix:** A 2D array where `matrix[i][j]` indicates if there is an edge between vertex i and j.  
   - **Advantages:** Simple and easy to implement, efficient for dense graphs.  
   - **Disadvantages:** Inefficient for sparse graphs due to high space usage.  

2. **Adjacency List:** An array of lists where each list corresponds to a vertex and contains its adjacent vertices.  
   - **Advantages:** More space-efficient for sparse graphs.  
   - **Disadvantages:** More complex to implement than an adjacency matrix.  

*Result:* The choice of representation affects the performance and efficiency of graph algorithms.

**Q2. [Unit IV | Topic: Minimum Cost Spanning Trees | Type: Numerical | Difficulty: Advanced]**  
**Question:** Using Prim's or Kruskal's algorithm, find the minimum spanning tree for the given weighted graph.  

*Concept from scratch:* Minimum spanning trees connect all vertices in a graph using the least total edge weight. Prim's algorithm builds the MST by starting from a vertex and growing the tree by adding the lowest weight edge.  

*Step 1 — Initialize:* Start with a vertex, and mark it as included in the MST.  

*Step 2 — Select Edge:* Choose the least weight edge connecting the MST to an excluded vertex.  

*Step 3 — Repeat:* Continue until all vertices are included.  

*Result:* The minimum spanning tree connects all vertices with the minimum total edge weight. 

---

This completes the detailed step-wise solutions for the full question bank for BCS-202 - Principles of Data Structures. Each question has been addressed thoroughly to provide a comprehensive understanding of the concepts and their applications.