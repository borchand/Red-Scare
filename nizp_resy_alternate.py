from Utils.ReadInput import ReadInput
from collections import deque

def get_path(parent_dict, s, t, final_was_red):
    """
    Function where we can get the path.
    """

    # we initialise an empty list that consists of the path, and we do it from the sink and then reverse at the end
    path = []
    current = t
    was_red = final_was_red
    
    # we make a condition to check whether there are more nodes
    while current is not None:
        # we append the current node to the path
        path.append(current)
        # this will update the current and was_red from the parent dictionary 
        current, was_red = parent_dict.get((current, was_red), (None, None))
    
    return list(reversed(path))


def has_alternating_path(graph, colour_of_nodes, s, t):
    # we check if s and t are even in the graph 
    if s not in graph.nodes() or t not in graph.nodes():
        return False
        
    # check if s and end t nodes exist in colour_of_nodes dictionary
    if s not in colour_of_nodes or t not in colour_of_nodes:
        return False

    queue = deque()

    # we add the s node and the colour of the previous node, which would be the opposite of the s node's colour
    queue.append((s, not colour_of_nodes[s]))
    visited = set()

    # dictionary to store parent nodes and their red/non-red state
    parent = {}
    
    # we start the bfs exploration
    print("\n === BFS Exploration ===")
    while queue:
        print(f"\n This is the {queue}")

        # now we look at the current and the previous_was_red node and pop it from the queue to be processed
        current, prev_was_red = queue.popleft()
        print(f"This is the {queue} now after popleft(), and we will look at node {current}")
        
        # print current state
        print(f"Node {current} is_red={colour_of_nodes[current]}")
        print(f"We came from a is_red={prev_was_red} node")
        
        # if the current and prev_was_red is in the visited set, we skip it, as it's supposed to be a simple path
        if (current, prev_was_red) in visited:
            print("State already visited, skipping")
            continue
        
        # here we add the pair of current and prev_was_red (if not already in visited) to the visited set
        print(f"We add {current, prev_was_red} to the visited set") 
        visited.add((current, prev_was_red))
        print(f"Visited state is now: {visited}")

        # if the current is the same as the sink, we have found the target, and print out some summary things
        if current == t:
            print("Found target!")
            # Reconstruct and print the path
            path = get_path(parent, s, t, prev_was_red)
            print("\nFound alternating path:")
            print(" -> ".join(str(node) for node in path))
            print("\nNode colours along path:")
            print(" -> ".join(['red' if colour_of_nodes[node] else 'non-red' for node in path]))
            return True
            
        # if the colour of the current node is the same as the colour of the previous node, we skip it
        if colour_of_nodes[current] == prev_was_red:
            print(f"Unlucky, the node {current}'s colour is_red={colour_of_nodes[current]} is the same as the previous nodes that was visited (is_red={prev_was_red}), we skip")
            continue

        # and if not, we we use it
        print(f"Lucky, the node {current}'s colour is_red={colour_of_nodes[current]} is not the same as the previous nodes that was visited (is_red={prev_was_red}), we will look at the next neighbours")
            
        # we look at the neighbours of the current in the graph
        for neighbor in graph.neighbors(current):
            # we check if the neighbour exists in colour_of_nodes dictionary
            if neighbor not in colour_of_nodes:
                print(f"Warning: Neighbour {neighbor} not in colour_of_nodes dictionary, skipping")
                continue
            # we're considering the colour of the neighbours
            print(f"Considering neighbor {neighbor} (is_red={colour_of_nodes[neighbor]})")
            
            # if the neighbour, the colour of the current nodes are not in visited
            if (neighbor, colour_of_nodes[current]) not in visited:
                # we append it to the queue
                queue.append((neighbor, colour_of_nodes[current]))
                # we store the parent information
                parent[(neighbor, colour_of_nodes[current])] = (current, prev_was_red)
                print(f"Added {neighbor} to queue")
    
    # we did not find a path that is alternating
    print("\n No alternating path found!")
    return False

def main():
    try:
        i = ReadInput()
        graph = i.toGraph().nxGraph
        
        # create dictionary of red nodes, ensuring node names match graph nodes
        colour_of_nodes = {}
        for node in i.nodes:
            # clean up node name to match graph representation
            clean_node = node
            colour_of_nodes[clean_node] = node.is_red
        
        # we call the has_alternating_path function to get the result
        result = has_alternating_path(graph, colour_of_nodes, i.s, i.t)
        print(f"\nAlternating path exists: {result}")
        
    except Exception as e:
        raise

if __name__ == "__main__":
    main()