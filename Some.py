from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph
import Utils.data_files as files
import networkx as nx
from many import solve_many, bellman
from pathlib import Path
from interruptingcow import timeout

'''
Get input
'''
def readInputSome(path):
  # Read input
  readFile = ReadFile(path)
  source = readFile.s
  sink = readFile.t

  # Nx graph
  graph = readFile.toGraph()
  gnx = graph.nxGraph

  # List of red nodes
  reds = [node.node for node in graph.nodes if node.is_red]

  return readFile, gnx, source, sink, reds

'''
For each of the red vertices, find the shortest path
from the start to the vertice, and from the vertice
to the end
'''
def someShortestPathRed(graph, source, sink, reds):
  for redNode in reds:
    try:
      # try a path from source to a red node

      nx.shortest_path(graph, source, redNode)
      # try a path from red node to sink
      nx.shortest_path(graph, redNode, sink)
      return True

    except nx.NetworkXNoPath:
      continue
  # If no path, return false
  return False

'''
Iterate through the red nodes.

In each iteration do the following:
1. Add a superSource connected to the red node with capacity 2
2. Add a superSink connected to the start and finish with capacities 1
3. Find if maximum flow between superSource and superSink is equal to 2
4. If yes, return True, if no, remove the edges of superSource and superSink

This becomes NP-hard for directed graphs, unless the first vertice is a red one,
and there exists a path between it and the sink.
'''

def someFlowPathRed(readFile, ogGraph, source, sink, reds) -> tuple[bool, bool]:
  try: nx.has_path(ogGraph, source, sink)
  except nx.NodeNotFound:
    return False

  # If the graph is directed acyclic, use many
  if nx.is_directed_acyclic_graph(ogGraph):
    if solve_many(readFile) > 0:
      return True, False
    else:
      return False, False

  # If the graph is directed cyclic, it's NP-hard
  elif nx.is_directed(ogGraph):
    print("NP-hard")
    return False, True
  
  # Otherwise, undirected
  else:

    thisGraph = nx.Graph()
    # Add flow capacity 1 to all edges
    for u, v in ogGraph.edges():
      thisGraph.add_edge(u, v, capacity=1)

    # Add a superSource and a superSink
    thisGraph.add_node('superSource')
    thisGraph.add_node('superSink')

    for redNode in reds:
      # Check if the rednode is in the graph
      if redNode in thisGraph.nodes:
      # Add new superSource with flow capacity edge val=2 connected to red node
        thisGraph.add_edge('superSource', redNode, capacity=2)

        # Add new superSink with flow capacity edges val=1 connected to the original
        thisGraph.add_edge(source, 'superSink', capacity=1)
        thisGraph.add_edge(sink, 'superSink', capacity=1)

        # Check if flow from superSource to superSink is equal to 2
        try:
          #print(redNode + ': ' + str(nx.maximum_flow(thisGraph, 'superSource', 'superSink', capacity='capacity')))
          if nx.maximum_flow(thisGraph, 'superSource', 'superSink')[0] == 2:
            return True, False
          else:
            thisGraph.remove_edge('superSource', redNode)
            thisGraph.remove_edge(source, 'superSink')
            thisGraph.remove_edge(sink, 'superSink')

        except nx.NetworkXUnfeasible:
          # If the path wasn't there, remove the unneeded edges
          thisGraph.remove_edge('superSource', redNode)
          thisGraph.remove_edge(source, 'superSink')
          thisGraph.remove_edge(sink, 'superSink')
          continue
        # If a red node is not connected to anything, do nothing

  return False, False

'''
Run the flow function on every file in the data folder
'''

def main():
  folder_path = Path('/content/data')

  for file in folder_path.iterdir():
    if file.is_file():
      try:
        with timeout(10, exception=RuntimeError):
          input, gnx, source, sink, reds = readInputSome(file)
          print(someFlowPathRed(input, gnx, source, sink, reds))
          continue
      except RuntimeError: 
        print("didn't finish within 10 seconds")
      print(False)

if __name__ == "__main__":
  main()
