from matplotlib import pyplot as plt
import networkx as nx

class Node:
    """
    Reads in a node.

    Inputs
        <b>node (str)</b>: A string with the node and "*" if it is red


    Variables
        <b>is_red (bool)</b>: If the node contains "*" then `is_red` is true
        <b>node (str)</b>: Name of the node without "*"
    """
    def __init__(self, node: str) -> None:
        self.is_red = "*" in node
        self.node = node.replace("*", "").strip()
    
    def __str__(self) -> str:
        s = "red" if self.is_red else "black"
        return f"Node: {self.node} is {s}"
    
    def __repr__(self) -> str:
        return self.__str__()

class Edge:
    """
        Reads in a edge.

        Inputs
            <b>edge (str)</b>: A string with edge u and v

        Variables
            <b>u (str)</b> from node
            <b>v (str)</b> to node
            <b>is_directed (bool)</b> If `edge` contains ">" it is directed
    """
    def __init__(self, u:  Node, v: Node, is_directed : bool) -> None:
        self.u = u
        self.v = v
        self.is_directed = is_directed

    def toTuple(self) -> tuple[Node, Node]:
        return (self.u, self.v)

    def __str__(self) -> str:
        s = "->" if self.is_directed else "--"
        return f"Edge: {self.u} {s} {self.v}"
    
    def __repr__(self) -> str:
        return self.__str__()

class Graph:

    def __init__(self, nodes: list[Node], edges: list[tuple[Node, Node]], is_directed: bool) -> None:
        self.nodes = nodes
        self.edges = edges
        self.is_directed = is_directed
        if (self.is_directed):
            self.nxGraph :nx.DiGraph = nx.from_edgelist(self.edges, create_using=nx.DiGraph)
        else:
            self.nxGraph :nx.Graph = nx.from_edgelist(self.edges)
        
    def __str__(self) -> str:
        return f"Nodes: {self.nodes}\nEdges: {self.edges}"

class WeightedGraph():
    def __init__(self, nodes: list[Node], edges: list[tuple[Node, Node]], is_directed: bool, red_weight: int, black_weight: int) -> None:

        self.nodes = nodes
        self.edges = edges
        self.is_directed = is_directed
        self.red_weight = red_weight
        self.black_weight = black_weight

        if self.is_directed:
            # directed graph - we add weight to the edges
            self.nxGraph = nx.DiGraph()

            for edge in self.edges:
                u, v = edge
                self.nxGraph.add_edge(u, v, weight = self.red_weight if v.is_red else self.black_weight)
        else:
            # undirected graph - we add weights in both directions for each edge
            self.nxGraph = nx.DiGraph()

            for edge in self.edges:
                u, v = edge                

                self.nxGraph.add_edge(u, v, weight = self.red_weight if v.is_red else self.black_weight)
                self.nxGraph.add_edge(v, u, weight = self.red_weight if u.is_red else self.black_weight)
    
    def draw(self):
        colors = ["red" if n.is_red else "black" for n in self.nxGraph.nodes]
        
        layout = nx.spring_layout(self.nxGraph)
        
        if(len(self.nodes)< 20):
            layout = nx.circular_layout(self.nxGraph)
        
        nx.draw(self.nxGraph, with_labels=False, node_color=colors, pos=layout)
        
        plt.show()