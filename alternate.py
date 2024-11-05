from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph
import Utils.data_files as files
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def get_path(parent_dict, s, t, final_was_red):
    """Helper function to reconstruct path from parent dictionary"""
    path = []
    current = t
    was_red = final_was_red
    
    while current is not None:
        path.append(current)
        current, was_red = parent_dict.get((current, was_red), (None, None))
    
    return list(reversed(path))

def has_alternating_path(graph: nx.Graph, red_nodes: dict, s: str, t: str) -> bool:
    # Check if start and end nodes exist in the graph
    if s not in graph.nodes() or t not in graph.nodes():
        print(f"\nError: Start node '{s}' or end node '{t}' not in graph!")
        return False
        
    # Check if start and end nodes exist in red_nodes dictionary
    if s not in red_nodes or t not in red_nodes:
        print(f"\nError: Start node '{s}' or end node '{t}' not in red_nodes dictionary!")
        return False

    queue = deque()
    queue.append((s, True))
    queue.append((s, False))
    
    visited = set()
    # Dictionary to store parent nodes and their red/non-red state
    parent = {}
    
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

        if current == t:
            print("Found target!")
            # Reconstruct and print the path
            path = get_path(parent, s, t, prev_was_red)
            print("\nFound alternating path:")
            print(" -> ".join(path))
            print("\nNode colors along path:")
            print(" -> ".join(['red' if red_nodes[node] else 'non-red' for node in path]))
            return True
            
        if red_nodes[current] == prev_was_red:
            print("Violates alternating rule, skipping")
            continue
            
        # Look at neighbors
        for neighbor in graph.neighbors(current):
            # Check if neighbor exists in red_nodes dictionary
            if neighbor not in red_nodes:
                print(f"Warning: Neighbor {neighbor} not in red_nodes dictionary, skipping")
                continue
                
            print(f"Considering neighbor {neighbor} (is_red={red_nodes[neighbor]})")
            if (neighbor, red_nodes[current]) not in visited:
                queue.append((neighbor, red_nodes[current]))
                # Store the parent information
                parent[(neighbor, red_nodes[current])] = (current, prev_was_red)
                print(f"Added {neighbor} to queue")
    
    print("\nNo alternating path found!")
    return False

def main() -> None:
    try:
        i = ReadInput()
        graph = i.toGraph().nxGraph
        
        # Create dictionary of red nodes, ensuring node names match graph nodes
        red_nodes = {}
        for node in i.nodes:
            # Clean up node name to match graph representation
            clean_node = node.node.strip()
            red_nodes[clean_node] = node.is_red
        
        print("\nNodes in graph:", list(graph.nodes()))
        print("Start node:", i.s)
        print("End node:", i.t)
        print("Red nodes:", {k: v for k, v in red_nodes.items() if v})
        
        result = has_alternating_path(graph, red_nodes, i.s, i.t)
        print(f"\nAlternating path exists: {result}")
        
        # Visualize
        plt.figure(figsize=(10,10))
        pos = nx.spring_layout(graph)
        color_map = ['red' if red_nodes.get(node, False) else 'lightblue' for node in graph.nodes()]
        nx.draw(graph, pos, node_color=color_map, with_labels=True, node_size=500)
        plt.title(f"Graph (Red nodes marked in red)\nAlternating path exists: {result}")
        plt.show()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()