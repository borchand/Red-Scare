from Utils.GraphComponents import Node, Edge

class ReadInput: 
    """
    Methods:
        <b>read_input<b>: Reads the input file (is called in contructor)
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
        self.nodes = []
        self.edges = []
        self.edgeTupleList = []
        self.read_input()

    def read_input(self): 
        """
        Reads input data for a graph file.
        """

        n, m, self.r = map(int, input().split())
        self.s, self.t = input().split()

        # Read nodes
        for _ in range(n):
            node = Node(input())
            self.nodes.append(node)
        
        # Read edges
        for _ in range(m):
            edge = Edge(input())
            self.edges.append(edge)
            self.edgeTupleList.append(edge.toTuple())

    def printNodes(self):
        """
        Prints each node
        """
        for node in self.nodes:
            print(node)  
    
    def printEdges(self):
        """
        Prints each edge
        """
        for edge in self.edges:
            print(edge)
    
    def getEdgeList(self) -> list :
        return self.edgeTupleList
    
    def __str__(self) -> str:
        self.printNodes()
        print()
        self.printEdges()
            
        return ""