from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph
import Utils.data_files as files
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def main()-> None:
    i = ReadInput()
    
    # Let's first visualize and understand our graph
    graph = i.toGraph().nxGraph
    
    # Create mapping of which nodes are red (for easy lookup)
    red_nodes = {node.node: node.is_red for node in i.nodes}
    
    print("\n=== Graph Information ===")
    print(f"Start node: {i.s}, Is red? {red_nodes[i.s]}")
    print(f"Target node: {i.t}, Is red? {red_nodes[i.t]}")
    print("\nRed nodes:", [node.node for node in i.nodes if node.is_red])
    
    # Let's try some basic BFS exploration to understand the graph structure
    print("\n=== BFS Exploration ===")
    queue = deque([(i.s, None)])  # (node, previous_node)
    visited = set()
    
    while queue:
        current, prev = queue.popleft()
        if current in visited:
            continue
            
        visited.add(current)
        
        # Print info about current node
        print(f"\nAt node {current} ({'red' if red_nodes[current] else 'non-red'})")
        print(f"Came from: {prev}")
        
        # Look at neighbors
        neighbors = list(graph.neighbors(current))
        print(f"Neighbors: {neighbors}")
        print("Neighbor colors:", [(n, 'red' if red_nodes[n] else 'non-red') for n in neighbors])
        
        # Add neighbors to queue
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, current))
    
    # Visualize the graph
    plt.figure(figsize=(10,10))
    pos = nx.spring_layout(graph)
    
    # Draw with colors
    color_map = ['red' if red_nodes[node] else 'lightblue' for node in graph.nodes()]
    nx.draw(graph, pos, node_color=color_map, with_labels=True, node_size=500)
    
    plt.title("Graph (Red nodes marked in red)")
    plt.show()

if __name__ == "__main__":
    main()