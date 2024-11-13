# from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph, Node, Edge
import Utils.data_files as files
import networkx as nx
from Utils.ReadInput import ReadInput

def none(graph, source, sink):

    """
    Find shortest path without any red nodes.

    Return the length of a shortest s-t path internally avoiding Red nodes.
    To be precise, let P be the set of s-t paths (v_1 ... v_l) such that v_i is not R if 1< i <l.
    Let l(p) denote the length of a path p.
    Return min(l(p), p in P).
    If no such path exists, return -1.
    Note that the edge st, if it exists, is an s-t path with l=2.
    Thus, if st in E(G) then the answer is 1, no matter the colour of s or t.
    In G_ex, the answer is 3 (because of the path 0, 1, 2, 3.)
    """

    # Remove all red nodes from the graph
    for node in graph.nodes:
        if node.is_red:
            graph.nxGraph.remove_node(node)

    # If exists, find the shortest path from s to t, return length, if no path -1
    try:
        return nx.shortest_path_length(graph.nxGraph, source, sink)
    
    except:
        return -1
    
if __name__ == "__main__":
    
    data = ReadInput()
    graph = data.toGraph()
    s_node = data.s
    t_node = data.t
    print(none(graph, s_node, t_node))
