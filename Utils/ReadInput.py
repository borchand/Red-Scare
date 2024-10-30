from Utils.GraphComponents import Node, Edge
class ReadInput: 
    
    def __init__(self) -> None:
        self.nodes = []
        self.edges = []
        self.read_input()

    def read_input(self): 
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

    def printNodes(self):
        for node in self.nodes:
            print(node)  
    
    def printEdges(self):
        for edge in self.edges:
            print(edge)
    
    def __str__(self) -> str:
        self.printNodes()
        print()
        self.printEdges()
            
        return ""