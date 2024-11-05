from Utils.ReadInput import ReadFile
import Utils.data_files as files
import time
import os
from nizp_resy_alternate import has_alternating_path
import networkx as nx

def run_test_case(file_path: str) -> tuple:
    """
    Run a single test case and return the results
    Returns: (filename, num_nodes, result_A, result_F, result_M, result_N, result_S, execution_time)
    """
    try:
        start_time = time.time()
        
        # Read the input file
        i = ReadFile(file_path)
        graph = i.toGraph().nxGraph
        num_nodes = i.num_nodes
        
        # Create dictionary of red nodes
        red_nodes = {}
        for node in i.nodes:
            clean_node = node.node.strip()
            red_nodes[clean_node] = node.is_red
        
        # Run the algorithm with print statements disabled
        result_A = has_alternating_path(graph, red_nodes, i.s, i.t)
        # result_F = func(graph, red_nodes, i.s, i.t)
        # result_M = func(graph, red_nodes, i.s, i.t)
        # result_N = func(graph, red_nodes, i.s, i.t)
        # result_S = func(graph, red_nodes, i.s, i.t)
        
        execution_time = time.time() - start_time
        return (os.path.basename(file_path), num_nodes, result_A, execution_time)
        
    except Exception as e:
        return (os.path.basename(file_path), 0, f"Error: {str(e)}", -1)#, -1)

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
        filename, num_nodes, result_A, execution_time = run_test_case(file_path)
        results.append((filename, num_nodes, result_A, execution_time))
        
        # Update statistics
        if execution_time >= 0:  # Test ran without errors
            total_time += execution_time
            if isinstance(result_A, bool):
                if result_A:
                    successful_tests += 1
                else:
                    failed_tests += 1
        else:  # Test encountered an error
            error_tests += 1
    
    
    output_lines = []



    # Print results
    output_lines.append("\nTest results:")
    output_lines.append("-" * 80)
    output_lines.append(f"{'Instance name':<40} {'# nodes'}         {'Result_A':<10}") #{'Result_F':<10} {'Result_M':<10} {'Result_N':<10} {'Result_S':<10}") {'Time (s)':<10}")
    output_lines.append("-" * 80)
    
    for filename, num_nodes, result_A, execution_time in results:
        #time_str = f"{execution_time:.4f}" if execution_time >= 0 else "ERROR"
        result_str = str(result_A) if isinstance(result_A, bool) else "ERROR"
        output_lines.append(f"{filename:<40}    {num_nodes:<10}     {result_str:<10}") #{time_str:<10}")
    
    # hope this works for your problems also
    output_lines.append("-" * 80)
    output_lines.append(f"\nSummary:")
    output_lines.append(f"Total tests: {len(test_files)}")
    output_lines.append(f"Paths found: {successful_tests}")
    output_lines.append(f"No paths found: {failed_tests}")
    output_lines.append(f"Errors: {error_tests}")
    output_lines.append(f"Total execution time: {total_time:.2f} seconds")
    output_lines.append(f"Average execution time: {total_time/len(test_files):.4f} seconds")



    with open("results_output.txt", "w") as file:
        for line in output_lines:
            file.write(line + "\n")
    
    # Optionally, print to console
    for line in output_lines:
        print(line)


if __name__ == "__main__":
    main()