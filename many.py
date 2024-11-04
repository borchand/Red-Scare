from Utils.GraphComponents import Node, Edge
from Utils.ReadInput import ReadInput
import networkx as nx



def has_red_cycle(G, red_nodes, s):
    visited = []
    stack = []

    stack.append(s)

    while len(stack):
        curr = stack[-1]
        stack.pop()

        if curr not in visited:
            visited.append(curr)
        
        for node in G.nxGraph.neighbors(curr):
            if node in visited:
                # cycle detected, let's check for red 
                idx = visited.index(node)
                for possible_red in visited[idx:]:
                    if possible_red in red_nodes:
                        return True
            if node not in visited:
                stack.append(node)
    return False



def get_weight(v, red_nodes):
    if v in red_nodes:
        return -1 
    else:
        return 0 






def bellman(G, start, target):
    # https://www.geeksforgeeks.org/bellman-ford-algorithm-in-python/
    num_vertices = len(G.nodes)
    distance = [float('inf')] * num_vertices
    distance[start] = 0

    predecessor = [None] * num_vertices  # To track paths

    for _ in range(num_vertices - 1):
        for u in G.nxGraph.nodes:
            for v in u.neighbors:
                weight = get_weight(u, v)
                if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    predecessor[v] = u

    # def get_path(target):
    #     path = []
    #     current = target
    #     while current is not None:
    #         path.append(current)
    #         current = predecessor[current]
    #     path.reverse()
    #     return path if path[0] == start else []


    # Check if target is reachable
    if distance[target] == float('inf'):
        return -1
    
    return abs(distance[target])



def dijkstra_(G, s):
   
    distances[s] = 0
    visited = [False] * N

    for _ in range(N):
        min_distance = float('inf')
        u = None
        for i in range(N):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                u = i

        if u is None:
            break

        visited[u] = True

        for v in range(self.size):
            if self.adj_matrix[u][v] != 0 and not visited[v]:
                alt = distances[u] + self.adj_matrix[u][v]
                if alt < distances[v]:
                    distances[v] = alt

    return distances



def max_red_vertices(i: ReadInput) -> int:
    G = i.toGraph()
    source = i.s
    sink = i.t
    red_nodes = set()
    for node in i.nodes:
        if node.is_red:
            red_nodes.add(node.node)
      # tjek om der er en cycle med red nodes
    # def has_red_cycle(G): # G_directed
    #     # Checks for red cycles -- needs a directed graph. 
    #     # hvis graf er undirected, lav den directed
    #     if not G.is_directed():
    #         G = G.to_directed()
    #         nx.set_edge_attributes(G, values = 1, name = 'weight')
    #         for rn in red_nodes:
    #             neigh = G.in_edges(rn)
    #             print(neigh)
    #     try:
    #         # Find any cycle in the entire graph
    #         cycle = nx.find_cycle(G, orientation="ignore")
    #         # Check if any node in the cycle is a red node
    #         return any(node in red_nodes for node, _, _ in cycle)
    #     except nx.NetworkXNoCycle:
    #         return False  # No cycle found

    # Case 1: Directed Acyclic Graph (DAG) -> Topological Sort
    if G.nxGraph.is_directed() and nx.is_directed_acyclic_graph(G.nxGraph):
        print("Case 1: Directed Acyclic Graph (DAG). Using topological sort to solve")
        print("---------------------------------------------------------------------")
        # Topological sort and track red nodes on paths
        top_order = list(nx.topological_sort(G.nxGraph))
        max_red_count = {node: 0 for node in G.nodes}
        max_red_count[source] = 1 if source in red_nodes else 0
        # loop after
        for node in top_order:
            for neighbor in G.nxGraph.successors(node):
                if max_red_count[neighbor] < max_red_count[node] + (1 if neighbor in red_nodes else 0):
                    max_red_count[neighbor] = max_red_count[node] + (1 if neighbor in red_nodes else 0)
        return max_red_count[sink] if max_red_count[sink] > 0 else -1
    


    ############# TJEK ##################
    # Case 2: Undirected graph with no red cycles -> Bellman-Ford
    elif not G.nxGraph.is_directed() and not has_red_cycle(G, red_nodes=red_nodes, s = source):
        print("Case 2, undirected graph and no red cycles. Using Bellman Ford")
        print("--------------------------------------------------------------")
        # weights: -1 for red nodes, 0 for others
        #weight_map = {node: -1 if node in red_nodes else 0 for node in G.nodes}
        #nx.set_node_attributes(G.nxGraph, weight_map, 'weight1')

        return bellman(G, source, sink)
        # try:
        #     # Bellman-Ford path to ensure we maximize red node count
        #     shortest_path = nx.bellman_ford_path(G, source=i.s, target=i.t, weight='weight1')
        #     # Count red nodes on path
        #     red_count = sum(1 for node in shortest_path if node in red_nodes)
        #     print(nx.get_node_attributes(G, 'weight1'))
        #     return red_count

        # except nx.NetworkXNoPath:
        #     return print("No path exists from s to t")



    ############# TJEK ##################
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

def main() -> None:
    i = ReadInput()
    G = i.toGraph()
    #print(nx.is_directed(G.nxGraph))
    for node in i.nodes:
        print(node.is_red)



    
    result = max_red_vertices(i)
    print(result)

if __name__ == "__main__":
    main()
