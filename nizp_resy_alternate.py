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

def has_alternating_path(graph: nx.Graph, color_of_nodes: dict, s: str, t: str) -> bool:
    # We check if s and t is even in the graph 
    if s not in graph.nodes() or t not in graph.nodes():
        #print(f"\nError: Start node '{s}' or end node '{t}' not in graph!")
        return False
        
    # Check if start and end nodes exist in color_of_nodes dictionary
    if s not in color_of_nodes or t not in color_of_nodes:
        #print(f"\nError: Start node '{s}' or end node '{t}' not in color_of_nodes dictionary!")
        return False

    queue = deque()

    #we add the start node and the color of the previous node, which would be the opposite of the start nodes color
    queue.append((s, not color_of_nodes[s]))
    visited = set()

    # Dictionary to store parent nodes and their red/non-red state
    parent = {}
    
    #print("\n=== BFS Exploration ===")
    while queue:
        #print(f"\nThis is the {queue}")

        current, prev_was_red = queue.popleft()

        #print(f"This is the {queue} now after popleft(), and we will look at node {current}")

        
        #Print current state
        #print(f"Node {current} is_red={color_of_nodes[current]}")
        #print(f"We came from a is_red={prev_was_red} node")
        
        if (current, prev_was_red) in visited:
            #print("State already visited, skipping")
            continue
            
        #print(f"We add {current, prev_was_red} to the visited set") 
        visited.add((current, prev_was_red))
        #print(f"Visited state is now: {visited}")

        if current == t:
            #print("Found target!")
            # Reconstruct and print the path
            path = get_path(parent, s, t, prev_was_red)
            #print("\nFound alternating path:")
            #print(" -> ".join(path))
            #print("\nNode colors along path:")
            #print(" -> ".join(['red' if color_of_nodes[node] else 'non-red' for node in path]))
            return True
            
        if color_of_nodes[current] == prev_was_red:
            #print(f"Unlucky, the node {current}'s color is_red={color_of_nodes[current]} is the same as the previous nodes that was visited (is_red={prev_was_red}), we skip")
            continue

        #print(f"Lucky, the node {current}'s color is_red={color_of_nodes[current]} is not the same as the previous nodes that was visited (is_red={prev_was_red}), we will look at the next neighbours")
            
        # Look at neighbors
        for neighbor in graph.neighbors(current):
            # Check if neighbor exists in color_of_nodes dictionary
            if neighbor not in color_of_nodes:
                #print(f"Warning: Neighbor {neighbor} not in color_of_nodes dictionary, skipping")
                continue
                
            #print(f"Considering neighbor {neighbor} (is_red={color_of_nodes[neighbor]})")
            if (neighbor, color_of_nodes[current]) not in visited:
                queue.append((neighbor, color_of_nodes[current]))
                # Store the parent information
                parent[(neighbor, color_of_nodes[current])] = (current, prev_was_red)
                #print(f"Added {neighbor} to queue")
    
    #print("\nNo alternating path found!")
    return False

def main() -> None:
    try:
        i = ReadInput()
        graph = i.toGraph().nxGraph
        
        # Create dictionary of red nodes, ensuring node names match graph nodes
        color_of_nodes = {}
        for node in i.nodes:
            # Clean up node name to match graph representation
            clean_node = node.node.strip()
            color_of_nodes[clean_node] = node.is_red
        
        result = has_alternating_path(graph, color_of_nodes, i.s, i.t)
        #print(f"\nAlternating path exists: {result}")
        
        # Visualize
        #plt.figure(figsize=(10,10))
        #pos = nx.spring_layout(graph)
        #color_map = ['red' if color_of_nodes.get(node, False) else 'lightblue' for node in graph.nodes()]
        #nx.draw(graph, pos, node_color=color_map, with_labels=True, node_size=500)
        #plt.title(f"Graph (Red nodes marked in red)\nAlternating path exists: {result}")
        #plt.show()
        
    except Exception as e:
        #print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()