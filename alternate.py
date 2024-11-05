from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph
import Utils.data_files as files
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

rom typing import Tuple, List  # Add this import at the top

def has_alternating_path(graph: nx.Graph, red_nodes: dict, s: str, t: str) -> Tuple[bool, List[str]]:
    queue = deque()
    # Store (node, prev_was_red, path) in queue
    queue.append((s, not red_nodes[s], [s]))
    
    visited = set()
    
    print("\n=== BFS Exploration ===")
    while queue:
        current, prev_was_red, path = queue.popleft()
        
        # Print current state
        print(f"\nAt node {current} (is_red={red_nodes[current]})")
        print(f"Came from {'red' if prev_was_red else 'non-red'} node")
        print(f"Current path: {' → '.join(path)}")
        
        if (current, prev_was_red) in visited:
            print("State already visited, skipping")
            continue
            
        visited.add((current, prev_was_red))

        if current == t:
            print("\nFound target!")
            print(f"Final path: {' → '.join(path)}")
            return True, path
            
        if red_nodes[current] == prev_was_red:
            print("Violates alternating rule, skipping")
            continue
            
        # Look at neighbors
        for neighbor in graph.neighbors(current):
            print(f"Considering neighbor {neighbor} (is_red={red_nodes[neighbor]})")
            if (neighbor, red_nodes[current]) not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, red_nodes[current], new_path))
                print(f"Added {neighbor} to queue")
    
    return False, []

def main()-> None:
    i = ReadInput()
    graph = i.toGraph().nxGraph
    red_nodes = {node.node: node.is_red for node in i.nodes}
    
    exists, path = has_alternating_path(graph, red_nodes, i.s, i.t)
    print(f"\nAlternating path exists: {exists}")
    if exists:
        print(f"Path found: {' → '.join(path)}")
        # Print the colors of nodes in the path
        colors = ['red' if red_nodes[node] else 'non-red' for node in path]
        print(f"Colors: {' → '.join(colors)}")
    
    # Visualize
    plt.figure(figsize=(10,10))
    pos = nx.spring_layout(graph)
    
    # Draw nodes
    color_map = ['red' if red_nodes[node] else 'lightblue' for node in graph.nodes()]
    nx.draw(graph, pos, node_color=color_map, with_labels=True, node_size=500)
    
    # If path exists, highlight it
    if exists and len(path) > 1:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='g', width=2)
    
    plt.title(f"Graph (Red nodes marked in red)\nAlternating path exists: {exists}")
    plt.show()

if __name__ == "__main__":
    main()