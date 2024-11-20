from Utils.GraphComponents import Graph, Node
from Utils.ReadInput import ReadInput, ReadFile, BaseRead
import networkx as nx
from collections import defaultdict


def solve_many(i: BaseRead, verbose: bool = False) -> int:
    G = i.toGraph()
    source, sink = i.s, i.t 

    # get the list of red nodes 
    red_nodes = set()
    for node in i.nodes:
        if node.is_red:
            red_nodes.add(node)
    try:
        # Case 1: Directed Acyclic Graph (DAG) -> Topological Sort
        if nx.is_directed_acyclic_graph(G.nxGraph):
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
            
            return max_red_count[sink] if max_red_count[sink] > 0 else -1

        elif nx.is_tree(G.nxGraph):
            print("Case 2: Undirected graph and no cycles.")
            print("--------------------------------------------------------------")

            path = nx.shortest_path(G.nxGraph, source=source, target=sink)
            return sum(1 for node in path if node in red_nodes)
            

<<<<<<< Updated upstream
        # Case 2: Undirected graph with no red cycles -> Bellman-Ford
        elif G.nxGraph.is_directed():
            try:
                print("Case 3: Directed graph and no red cycles. Using Bellman Ford")
                print("--------------------------------------------------------------")
                return bellman(G, source, sink, red_nodes=red_nodes) 
            
            except ValueError:
                print('Negative cycle detected cannot perform Bellman-Ford')
                pass 

=======
>>>>>>> Stashed changes
        # Case 3: NP-hard, complete search
        else:
            print("Case 3: NP-hard case, have to do complete search")
            print("--------------------------------------------------------------")

            # nx DFS 
            max_red_count = -1
            # Use dfs_edges to get paths from s, traverse each to count red nodes until t
            for path in nx.all_simple_paths(G.nxGraph, source=i.s, target=i.t):            
                # Count red nodes in the current path
                red_count = sum(1 for node in path if node in red_nodes)
                max_red_count = max(max_red_count, red_count)

            return max_red_count if max_red_count != -1 else -1

    except (nx.NodeNotFound,  nx.NetworkXNoPath, nx.exception.NetworkXPointlessConcept):
        return -1

def main()-> None:
    i = ReadInput()
    print(solve_many(i))

if __name__ == "__main__":
    main()