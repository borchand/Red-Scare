from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph
import Utils.data_files as files
import networkx as nx
from collections import deque
import time
import os

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
    # Check if start and end nodes exist
    if s not in graph.nodes() or t not in graph.nodes() or s not in red_nodes or t not in red_nodes:
        return False

    queue = deque()
    queue.append((s, True))
    queue.append((s, False))
    
    visited = set()
    parent = {}
    
    while queue:
        current, prev_was_red = queue.popleft()
        
        if (current, prev_was_red) in visited:
            continue
            
        visited.add((current, prev_was_red))

        if current == t:
            return True
            
        if red_nodes[current] == prev_was_red:
            continue
            
        for neighbor in graph.neighbors(current):
            if neighbor not in red_nodes:
                continue
                
            if (neighbor, red_nodes[current]) not in visited:
                queue.append((neighbor, red_nodes[current]))
                parent[(neighbor, red_nodes[current])] = (current, prev_was_red)
    
    return False

def run_test_case(file_path: str) -> tuple:
    """
    Run a single test case and return the results
    Returns: (filename, result, execution_time)
    """
    try:
        start_time = time.time()
        
        # Read the input file
        i = ReadFile(file_path)
        graph = i.toGraph().nxGraph
        
        # Create dictionary of red nodes
        red_nodes = {node.node.strip(): node.is_red for node in i.nodes}
        
        # Run the algorithm
        result = has_alternating_path(graph, red_nodes, i.s, i.t)
        
        execution_time = time.time() - start_time
        return (os.path.basename(file_path), result, execution_time)
        
    except Exception as e:
        return (os.path.basename(file_path), f"Error: {str(e)}", -1)

def main():
    # Get all test files from data_files.py
    test_files = [getattr(files, attr) for attr in dir(files) if not attr.startswith('__')]
    
    # Sort test files by name for better organization
    test_files.sort()
    
    # Results storage
    results = []
    total_time = 0
    successful_tests = 0
    failed_tests = 0
    error_tests = 0
    
    print(f"\nRunning {len(test_files)} test cases...")
    print("-" * 80)
    
    # Run all test cases
    for file_path in test_files:
        filename, result, execution_time = run_test_case(file_path)
        results.append((filename, result, execution_time))
        
        # Update statistics
        if execution_time >= 0:  # Test ran without errors
            total_time += execution_time
            if isinstance(result, bool):
                if result:
                    successful_tests += 1
                else:
                    failed_tests += 1
        else:  # Test encountered an error
            error_tests += 1
    
    # Print results
    print("\nTest Results:")
    print("-" * 80)
    print(f"{'File Name':<40} {'Result':<10} {'Time (s)':<10}")
    print("-" * 80)
    
    for filename, result, execution_time in results:
        time_str = f"{execution_time:.4f}" if execution_time >= 0 else "ERROR"
        result_str = str(result) if isinstance(result, bool) else "ERROR"
        print(f"{filename:<40} {result_str:<10} {time_str:<10}")
    
    print("-" * 80)
    print(f"\nSummary:")
    print(f"Total tests: {len(test_files)}")
    print(f"Paths found: {successful_tests}")
    print(f"No paths found: {failed_tests}")
    print(f"Errors: {error_tests}")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Average execution time: {total_time/len(test_files):.4f} seconds")

if __name__ == "__main__":
    main()