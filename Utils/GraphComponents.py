import networkx as nx

class Graph:

    def __init__(self, nodes: list, edges: list, is_directed: bool) -> None:
        
        if (is_directed):
            self.nxGraph = nx.from_edgelist(edges, create_using=nx.DiGraph)
        else:
            self.nxGraph = nx.from_edgelist(edges)
        

    

class Node:
    def __init__(self, node: str) -> None:
        self.is_red = "*" in node
        self.node = node.replace("*", "").strip()
    
    def __str__(self) -> str:
        s = "red" if self.is_red else "black"
        return f"Node: {self.node} is {s}"

class Edge:
    def __init__(self, edge: str) -> None:
        edge_splitted = edge.split("->") if ">" in edge else edge.split("--")
        self.u = edge_splitted[0]
        self.v = edge_splitted[1]
        self.is_directed = ">" in edge ## ->

    def toTuple(self) -> tuple:
        return (self.u, self.v)

    def __str__(self) -> str:
        s = "->" if self.is_directed else "--"
        return f"Edge: {self.u} {s} {self.v}"