import networkx as nx

class Graph:

    def __init__(self, nodes: list, edges: list, is_directed: bool) -> None:
        
        if (is_directed):
            self.nxGraph :nx.DiGraph = nx.from_edgelist(edges, create_using=nx.DiGraph)
        else:
            self.nxGraph :nx.Graph = nx.from_edgelist(edges)
        
        self.Nodes = nodes
        self.Edges = edges
        

    

class Node:
    """
    Reads in a node.

    Inputs
        <b>edge (str)</b>: A string with the node and "*" if it is red


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
    def __init__(self, edge: str) -> None:
        edge_splitted = edge.split("->") if ">" in edge else edge.split("--")
        self.u = edge_splitted[0].strip()
        self.v = edge_splitted[1].strip()
        self.is_directed = ">" in edge ## ->

    def toTuple(self) -> tuple:
        return (self.u, self.v)

    def __str__(self) -> str:
        s = "->" if self.is_directed else "--"
        return f"Edge: {self.u} {s} {self.v}"