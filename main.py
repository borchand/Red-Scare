from Utils.ReadInput import ReadInput
from Utils.GraphComponents import Graph
import networkx as nx

def main()-> None:
    i = ReadInput()
    print(i)

    # edgeList = i.edgeTupleList
    # graph = Graph(i.nodes, edgeList, i.is_directed)
    
    # nx.draw(graph.nxGraph)

    # print(graph.nxGraph.edges)
if __name__ == "__main__":
    main()