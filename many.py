from Utils.ReadInput import ReadInput
from Utils.GraphComponents import Graph
import networkx as nx
from collections import defaultdict


def has_red_cycle(G, red_nodes, s):
    visited = []
    stack = [(s, -1)]
    cycle_nodes = set()

    while stack:
        curr, parent = stack.pop()

        if curr in visited: 
            # cycle detected, let's look at the nodes collected in the cycle
            cycle_nodes.add(curr)
            if any(n in red_nodes for n in cycle_nodes):
                return True
            continue    

        # if node was not visited add
        visited.append(curr)
        cycle_nodes.add(curr)

        for node in G.nxGraph.neighbors(curr):
            if node not in visited: 
                stack.append((node, curr))  
            elif node != parent:
                # cycle detected: back edge to a visited node that isn't the parent
                cycle_nodes.add(node)
                if any(n in red_nodes for n in cycle_nodes):
                    return True 
    return False


def get_weight(v, red_nodes):
    if v in red_nodes:
        return -1 
    else:
        return 0 
    


def bellman(G, start, target, red_nodes):
    # https://www.geeksforgeeks.org/bellman-ford-algorithm-in-python/
    num_vertices = len(G.nxGraph.nodes)

    distance = defaultdict(lambda: float('inf')) # initialise dict with inf values, unless added 
    distance[start] = 0

    predecessor = defaultdict(lambda: None) # initialise dict of predecessors with None, unless added 

    for i in range(num_vertices - 1):
        for u in G.nxGraph.nodes:            
            for v in G.nxGraph.neighbors(u):
                weight = get_weight(v, red_nodes= red_nodes)
                if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    predecessor[v] = u

    for u in G.nxGraph.nodes:
        for v in G.nxGraph.neighbors(u):
            weight = get_weight(v, red_nodes=red_nodes)
            if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                raise ValueError

    # Check if target is reachable
    if distance[target] == float('inf'):
        return -1
    

    return abs(distance[target])


def solve(i: ReadInput):
    G = i.toGraph()
    source, sink = i.s, i.t 

    # get the list of red nodes 
    red_nodes = set()
    for node in i.nodes:
        if node.is_red:
            red_nodes.add(node.node)


    # Case 1: Directed Acyclic Graph (DAG) -> Topological Sort
    if nx.is_directed_acyclic_graph(G.nxGraph):
        print("Case 1: Directed Acyclic Graph (DAG). Using topological sort to solve")
        print("---------------------------------------------------------------------")

        # Topological sort and track red nodes on paths
        top_order = list(nx.topological_sort(G.nxGraph))
        max_red_count = {node: 0 for node in G.nxGraph.nodes} # returns nodes as string, let's stick at that. 
        max_red_count[source] = 1 if source in red_nodes else 0
    
        # loop after
        for node in top_order:
            for neighbor in G.nxGraph.successors(node):
                if max_red_count[neighbor] < max_red_count[node] + (1 if neighbor in red_nodes else 0):
                    max_red_count[neighbor] = max_red_count[node] + (1 if neighbor in red_nodes else 0)
        
        return max_red_count[sink] if max_red_count[sink] > 0 else -1

    elif nx.is_tree(G.nxGraph):
        print("Case 2, Undirected graph and no cycles.")
        print("--------------------------------------------------------------")

        path = nx.shortest_path(G.nxGraph, source=source, target=sink)
        counter = 0 
        for node in path:
            if node in red_nodes:
                counter += 1
        return counter


    # Case 2: Undirected graph with no red cycles -> Bellman-Ford
    elif G.nxGraph.is_directed():
        try:
            print("Case 3, directed graph and no red cycles. Using Bellman Ford")
            print("--------------------------------------------------------------")
            return bellman(G, source, sink, red_nodes=red_nodes) 
        
        except ValueError:
            print('Negative cycle detected cannot perform Bellman-Ford')
            pass 

    
    # Case 3: NP-hard, complete search
    else:
        print("Case 3: NP-hard case, have to do complete search")
        print("------------------------------------------------")
        print("\n")
        print("This may take some time")
        # nx DFS 
        max_red_count = -1

        # Use dfs_edges to get paths from s, traverse each to count red nodes until t
        for path in nx.all_simple_paths(G.nxGraph, source=i.s, target=i.t):
            # Count red nodes in the current path
            red_count = sum(1 for node in path if node in red_nodes)
            #print(red_count)
            max_red_count = max(max_red_count, red_count)

        return max_red_count if max_red_count != -1 else -1


def main()-> None:
    i = ReadInput()
    print(solve(i))

if __name__ == "__main__":
    main()