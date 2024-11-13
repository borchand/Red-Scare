from Utils.GraphComponents import Graph, Node
from Utils.ReadInput import ReadInput, ReadFile, BaseRead
import networkx as nx
import interruptingcow
from collections import defaultdict

def get_weight(v: Node, red_nodes: list[Node]) -> int:
    if v in red_nodes:
        return -1 
    else:
        return 0 


def bellman(G: Graph, start: Node, target: Node, red_nodes: list[Node])-> int:
    '''
    Components of this implementation is taken from https://www.geeksforgeeks.org/bellman-ford-algorithm-in-python/. 
    '''
    num_vertices = len(G.nxGraph.nodes)

    distance = defaultdict(lambda: float('inf')) # initialise dict with inf values, unless added 
    distance[start] = 0

    for i in range(num_vertices - 1):
        for u in G.nxGraph.nodes:            
            for v in G.nxGraph.neighbors(u):
                weight = get_weight(v, red_nodes= red_nodes)
                if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight

    for u in G.nxGraph.nodes:
        for v in G.nxGraph.neighbors(u):
            weight = get_weight(v, red_nodes=red_nodes)
            if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                raise ValueError

    # Check if target is reachable
    if distance[target] == float('inf'):
        return -1
    
    return abs(distance[target])


def solve_many(i: BaseRead, verbose: bool = False) -> tuple[int, bool]:
    G = i.toGraph()
    source, sink = i.s, i.t 

    # get the list of red nodes 
    red_nodes = set()
    for node in i.nodes:
        if node.is_red:
            red_nodes.add(node)

    np_hard = False
    try:
        # Case 1: Directed Acyclic Graph (DAG) -> Topological Sort
        if nx.is_directed_acyclic_graph(G.nxGraph):
            if verbose:
                print("Case 1: Directed Acyclic Graph (DAG). Using topological sort to solve")
                print("--------------------------------------------------------------")
            # Topological sort and track red nodes on paths
            top_order = list(nx.topological_sort(G.nxGraph))
            max_red_count = {node: 0 for node in G.nxGraph.nodes} # returns nodes as string, let's stick at that. 
            max_red_count[source] = 1 if source in red_nodes else 0
        
            # loop after
            for node in top_order:
                for neighbor in G.nxGraph.successors(node):
                    if max_red_count[neighbor] < max_red_count[node] + (1 if neighbor in red_nodes else 0):
                        max_red_count[neighbor] = max_red_count[node] + (1 if neighbor in red_nodes else 0)
            
            return max_red_count[sink] if max_red_count[sink] > 0 else -1, np_hard

        elif nx.is_tree(G.nxGraph):
            if verbose:
                print("Case 2: Undirected graph and no cycles.")
                print("--------------------------------------------------------------")

            path = nx.shortest_path(G.nxGraph, source=source, target=sink)
            return sum(1 for node in path if node in red_nodes), np_hard
            

        # Case 2: Undirected graph with no red cycles -> Bellman-Ford
        elif G.nxGraph.is_directed():
            try:
                if verbose:
                    print("Case 3: Directed graph and no red cycles. Using Bellman Ford")
                    print("--------------------------------------------------------------")
                return bellman(G, source, sink, red_nodes=red_nodes), np_hard
            
            except ValueError:
                if verbose:
                    print('Negative cycle detected cannot perform Bellman-Ford')
                pass 

        # Case 3: NP-hard, complete search
        if verbose:
            print("Case 4: NP-hard case, have to do complete search")
            print("--------------------------------------------------------------")
        min_before_interrupt = 1
        np_hard = True
        try:
            # This will interrupt the task if it takes more than self.min_before_interrupt minutes
            with interruptingcow.timeout(60 * min_before_interrupt, exception=RuntimeError):
                # nx DFS 
                max_red_count = -1
                # Use dfs_edges to get paths from s, traverse each to count red nodes until t
                for path in nx.all_simple_paths(G.nxGraph, source=i.s, target=i.t):            
                    # Count red nodes in the current path
                    red_count = sum(1 for node in path if node in red_nodes)
                    max_red_count = max(max_red_count, red_count)

                return max_red_count if max_red_count != -1 else -1, np_hard
        except RuntimeError:
            return "Timeout", np_hard

    except (nx.NodeNotFound,  nx.NetworkXNoPath, nx.exception.NetworkXPointlessConcept):
        return -1, np_hard

def main()-> None:
    i = ReadInput()
    print(solve_many(i))

if __name__ == "__main__":
    main()