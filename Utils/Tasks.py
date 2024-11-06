from Utils.ReadInput import ReadFile
import networkx as nx

class Tasks:
    """
    Summary:
        This class contains the tasks for the Red Scare assignment.
        The tasks are:
            - few : Return the minimum number of red vertices on any path from s 
    """
    def __init__(self, path: str) -> None:
        self.path = path
        self.data = ReadFile(path)

    def few(self, draw : bool = False) -> int:
        """
        Return the minimum number of red vertices on any path from s
        to t. To be precise, let P be the set of s, t-paths and let r(p) denote
        the number of red vertices on a path p. Return min{r(p): p ∈ P }.
        If no path from s to t exists, return ‘-1’. In Gex, the answer is 0
        (because of the path 0, 1, 2, 3.)

        Inputs
            <b>draw (bool)</b>: If True, draw the graph
        """
        weightedGraph = self.data.toWeightedGraph(1, 0)

        G = weightedGraph.nxGraph

        if draw:
            weightedGraph.draw()

        try:
            return nx.dijkstra_path_length(G, self.data.s, self.data.t, weight='weight')
        except (nx.NodeNotFound,  nx.NetworkXNoPath):
            return -1