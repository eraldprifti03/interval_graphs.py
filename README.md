# interval_graphs.py
 
This repository contains a Python script designed for graph analysis, implementing Lexicographic Breadth-First Search (LexBFS) to perform various graph-related computations.  

### **Table of Contents**  
- **Methods**  
  - LexBFS Ordering  
  - Chordality Check  
  - Interval Graph Verification  

### **Methods**  

#### **LexBFS Ordering**  
This function computes the LexBFS ordering of nodes within a graph. LexBFS is a traversal algorithm that generates a specific node order using a lexicographic breadth-first approach. The resulting order has important applications in graph theory and optimization.  

#### **Chordality Check**  
A chordal graph is one in which every cycle of four or more vertices includes a chord—an edge that connects two non-adjacent vertices in the cycle. This function determines whether a given graph is chordal.  

#### **Interval Graph Verification**  
An interval graph is a graph that can be represented by a set of intervals on a number line, where two intervals overlap if and only if their corresponding vertices share an edge. This function checks whether a given graph qualifies as an interval graph.
