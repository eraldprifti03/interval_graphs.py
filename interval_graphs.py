import sys
from collections import deque
from typing import Hashable # for use with the type annotation below


def lexbfs(g: dict) -> list[int]: 
    
    S = [[]]
    for i in g.keys():
        S[0].append(i)

    lexbfs = []
    while len(S) > 0:
#'Οσο η λίστα Σ δεν είναι άδεια αφαιρούμε έναν κόμβο u από την πρώτη υπολίστα της και το προσθέτουμε στην lexbfs.
        lexbfs.append(S[0][0])
        S[0].remove(S[0][0])
        if len(S[0]) == 0:
            S.remove(S[0])
#Για κάθε υπολίστα της Σ αφαιρούμε από αυτήν τους γείτονες του κάθε φορά u μέχρι να αδειάσει και είσαγουμε σε  
#μία θέση πριν, μία άλλη λίστα στην οποία εισάγουμε τους γείτονες που αφαιρέσαμε. 
        i = 0
        while len(S) > i:    
            SN = []   
            for n in S[i].copy():
                if n in g[lexbfs[-1]]:
                    S[i].remove(n)
                    SN.append(n)  
            if len(SN) > 0 and not SN == S[i]:   
                S.insert(i,SN)
            if len(S[i]) == 0:
                S.remove(S[i])
            else:
                i += 1
        
    return lexbfs

 
def chordal(g: dict, lexbfs):
    
    lexbfs.reverse()

    for i in range(len(lexbfs)):
        if len(g[lexbfs[i]]) > 0:
            #Οι γείτονες του u που έπονται του u   
            RNu = { lexbfs[j] for j in range(len(lexbfs)) if j > i and lexbfs[j] in g[lexbfs[i]] }
            #ο πρωτος γείτονας του u
            v = g[lexbfs[i]][0]
            #Oi γείτονες του ν που έπονται του ν
            RNv = { lexbfs[j] for j in range(len(lexbfs)) if lexbfs[j] in g[v] and j > i }
            #RN(u) \ {v} ⊄ RNv
            result = (RNu - {v}) <= RNv
            if result == False:
                return False

    return True


def bfs_connected_components(g: dict) -> list[list[Hashable]]:

    q = deque()  

    if len(g) > 0:
        visited = [False] * (max(g.keys()) + 1)
    else:
        visited = []

    components = []

    for node in g.keys():
        if not visited[node]:
            q.appendleft(node)
            visited[node] = True
            component = []

            while len(q) > 0:
                c = q.pop()
                component.append(c)
                for v in g[c]:
                    if not visited[v]:
                        q.appendleft(v)
                        visited[v] = True
            components.append(component)

    return components


def interval(g: dict):

    L = [[]] * len(g)
#Για κάθε κόμβο u τον αφαιρούμε από τον γράφο μαζί με τους γείτονές του και επείτα βρίσκουμε τις συνιστώσες 
#που προκύπτουν από αυτόν τον γράφο,καλώντας την αντίστοιχη συνάρτηση,και το τοποθετούμε σε μία λίστα στην θέση u. 
    for u in g.keys():
        g1 = {k: list(v) for k, v in g.items()}
        g1.pop(u)
        for n in g[u]:
            g1.pop(n)
            for i in g1.keys():
                if u in g1[i]:       
                    g1[i].remove(u)
                if n in g1[i]:
                    g1[i].remove(n)

        L[u] = bfs_connected_components(g1)

#Δημιουρούμε τον πίνακα C διαστάσων |V|x|V|, όπου στα κελία u,v βάζουμε 0 αν οι κόμβοι αυτοί είναι γείτονες, 
#διαφορετικά βάζουμε την συνιστώσα του G \ N(u) στην οποία ανήκει ο κόμβος ν.      
    C = []
    for i in g.keys(): 
        row = [] 
        for j in g.keys():
            if  i == j:
                row.append(0)
            elif i in g[j] or j in g[i]:
                row.append(0)
            else:
                for s in L[i]:
                    if j in s:    
                        row.append(s)
        C.append(row)
#Βρίσκουμε τρεις κόμβους u,v,w που δεν είναι γείτονες μεταξύ τους και για κάθε μια τέτοια ανεξάρτητη τριάδα, 
#ελέγχουμε την συνθήκη για να αποφανθούμε αν ο γράφος είναι διαστημάτων ή όχι.    
    for u in range(len(C)):
        for v in range(len(C)):
            if C[u][v] != 0 and C[v][u] != 0:
                for w in range(len(C)):
                    if C[u][w] != 0 and C[v][w] != 0 and C[w][u] != 0 and C[w][v] != 0:                    
                        if C[u][v] == C[u][w] and C[v][u] == C[v][w] and C[w][u] == C[w][v]:
                            return False
                                            
    return True


input_filename = sys.argv[2]

g = {}

with open(input_filename) as graph_input:
    for line in graph_input:
        # Split line and convert line parts to integers.
        nodes = [int(x) for x in line.split()]
        if len(nodes) != 2:
            continue
        # If a node is not already in the graph
        # we must create a new empty list.
        if nodes[0] not in g:
            g[nodes[0]] = []
        if nodes[1] not in g:
            g[nodes[1]] = []
        # We need to append the "to" node
        # to the existing list for the "from" node.
        g[nodes[0]].append(nodes[1])
        # And also the other way round.
        g[nodes[1]].append(nodes[0])

        
if sys.argv[1] == "lexbfs":
    print(lexbfs(g))
elif sys.argv[1] == "chordal":
    lexbfs = lexbfs(g)
    print(chordal(g, lexbfs))
elif sys.argv[1] == "interval":
    print(interval(g))