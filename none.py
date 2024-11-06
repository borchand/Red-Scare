# from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph, Node, Edge
import Utils.data_files as files
import networkx as nx

def none(graph, source, sink):

    for node in graph.Nodes:
        if node.is_red:
            # print("red node: ", node)
            graph.nxGraph.remove_node(node.node)

    try:
        # print(f'source: {source}')
        # print(f'sink: {sink}')

        # print(nx.draw_networkx(graph.nxGraph))
        # s_path = nx.shortest_path_length(graph.nxGraph, source, sink)
        # return s_path
        return nx.shortest_path_length(graph.nxGraph, source, sink)
    
    except:
        return -1
