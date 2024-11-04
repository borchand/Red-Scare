from Utils.GraphComponents import Node, Edge, Graph
class BaseRead:

    """
    Summary: 
        This is base class from reading in the files.
        This class contains utility methods
    
    Methods:
        <b>printNodes</b>: Print each node
        <b>printEdges</b>: Print each edge
        <b>getEdgeList</b>: returns the edgeTupleList


    Variables
        <b>nodes (list<Node>)</b>: List of nodes
        <b>edges (list<Edge>)</b>: List of edges
        <b>edgeTupleList (list<tuple(u, v)>)</b>: List of edges as tuple (used for networkx)
    """

    def __init__(self) -> None:
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.edgeTupleList = []
        self.is_directed = None

    def printNodes(self):
        """
        Prints each node
        """
        if self.nodes is []:
            raise Exception("No data: Base class can not be used on its own. Use ReadFile or ReadInput")
        
        for node in self.nodes:
            print(node)  
    
    def printEdges(self):
        """
        Prints each edge
        """
        if self.edges is []:
            raise Exception("No data: Base class can not be used on its own. Use ReadFile or ReadInput")
        for edge in self.edges:
            print(edge)
    
    def getEdgeList(self) -> list :
        if self.edgeTupleList is []:
            raise Exception("No data: Base class can not be used on its own. Use ReadFile or ReadInput")

        return self.edgeTupleList
    
    def toGraph(self) -> Graph:
        if self.is_directed is None:
            raise Exception("No data: Base class can not be used on its own. Use ReadFile or ReadInput")
        return Graph(self.nodes, self.edgeTupleList, self.is_directed)
    
    def getNodeFromName(self, name: str) -> Node:
        for node in self.nodes:
            if node.node == name:
                return node
        return None

    def __str__(self) -> str:
        self.printNodes()
        print()
        self.printEdges()
            
        return ""

class ReadFile(BaseRead):

    """
    Summary: 
    
    This class can be used to read in graph data from a file path

    Methods:
        <b>read_file</b>: Reads the input from a file path (read_file is called in contructor)
        <b>printNodes</b>: Print each node
        <b>printEdges</b>: Print each edge
        <b>getEdgeList</b>: returns the edgeTupleList

    Variables
        <b>nodes (list<Node>)</b>: List of nodes
        <b>edges (list<Edge>)</b>: List of edges
        <b>edgeTupleList (list<tuple(u, v)>)</b>: List of edges as tuple (used for networkx)
        <b>s</b>: Start node
        <b>t</b>: End node
        <b>r</b>: Cardinality of reds
    """

    def __init__(self, path: str) -> None:
        super().__init__()
        self.read_file(path)

    def read_file(self, path: str):

        with open(path) as file:
            n, m, self.r = map(int, file.readline().split())
            self.s, self.t = file.readline().split()
            for _ in range(n):
                node = Node(file.readline().strip())
                self.nodes.append(node)
            
            for _ in range(m):
                edge = Edge(file.readline().strip())
                self.edges.append(edge)
                self.edgeTupleList.append(edge.toTuple())
        
        self.is_directed = edge.is_directed
    
    def __str__(self) -> str:
        return super().__str__() 

class ReadInput(BaseRead): 
    
    """
    Methods:
        <b>read_input</b>: Reads the input file (is called in contructor)
        <b>printNodes</b>: Print each node
        <b>printEdges</b>: Print each edge
        <b>getEdgeList</b>: returns the edgeTupleList


    Variables
        <b>nodes (list<Node>)</b>: List of nodes
        <b>edges (list<Edge>)</b>: List of edges
        <b>edgeTupleList (list<tuple(u, v)>)</b>: List of edges as tuple (used for networkx)
        <b>s</b>: Start node
        <b>t</b>: End node
        <b>r</b>: Cardinality of reds
    """    
    def __init__(self) -> None:
        super().__init__()
        self.read_input()

    def read_input(self): 
        """
        Reads input data for a graph file.
        """

        n, m, self.r = map(int, input().split())
        self.s, self.t = input().split()

        # Read nodes
        for _ in range(n):
            node = Node(input().strip())
            self.nodes.append(node)
        
        # Read edges
        for _ in range(m):
            edge = Edge(input().strip())
            self.edges.append(edge)
            self.edgeTupleList.append(edge.toTuple())
        
        self.is_directed = edge.is_directed
        
    def __str__(self) -> str:
        return super().__str__()

    