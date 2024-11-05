from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph
import Utils.data_files as files
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def has_alternating_path(graph: nx.Graph, red_nodes: dict, s: str, t: str) -> bool:
    queue = deque()
    queue.append((s, True))
    queue.append((s, False))
    
    visited = set()

    
    print("\n=== BFS Exploration ===")
    while queue:
        current, prev_was_red = queue.popleft()
        
        # Print current state
        print(f"\nAt node {current} (is_red={red_nodes[current]})")
        print(f"Came from {'red' if prev_was_red else 'non-red'} node")
        
        if (current, prev_was_red) in visited:
            print("State already visited, skipping")
            continue
            
        visited.add((current, prev_was_red))
        print(f"Visited states: {visited}")
        print(current)
        print(prev_was_red)
        print(visited)

        if current == t:
            print("Found target!")
            return True
            
        if red_nodes[current] == prev_was_red:
            print("Violates alternating rule, skipping")
            continue
            
        # Look at neighbors
        for neighbor in graph.neighbors(current):
            print(f"Considering neighbor {neighbor} (is_red={red_nodes[neighbor]})")
            if (neighbor, red_nodes[current]) not in visited:
                queue.append((neighbor, red_nodes[current]))
                print(f"Added {neighbor} to queue")
    
    return False

def main()-> None:
    i = ReadInput()
    graph = i.toGraph().nxGraph
    red_nodes = {node.node: node.is_red for node in i.nodes}
    
    result = has_alternating_path(graph, red_nodes, i.s, i.t)
    print(f"\nAlternating path exists: {result}")
    
    # Visualize
    plt.figure(figsize=(10,10))
    pos = nx.spring_layout(graph)
    color_map = ['red' if red_nodes[node] else 'lightblue' for node in graph.nodes()]
    nx.draw(graph, pos, node_color=color_map, with_labels=True, node_size=500)
    plt.title(f"Graph (Red nodes marked in red)\nAlternating path exists: {result}")
    plt.show()

if __name__ == "__main__":
    main()