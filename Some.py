from Utils.ReadInput import ReadInput, ReadFile, BaseRead
from Utils.GraphComponents import Graph, Node
import Utils.data_files as files
import networkx as nx
from many import solve_many
from pathlib import Path
from interruptingcow import timeout

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

def someFlowPathRed(readFile: BaseRead, ogGraph: nx.Graph, source:Node, sink: Node, reds:list[Node]):
  np_hard = False
  try: nx.has_path(ogGraph, source, sink)
  except nx.NodeNotFound:
    return False, np_hard

  # If the graph is directed acyclic, use many
  if nx.is_directed_acyclic_graph(ogGraph):
    result, np_hard = solve_many(readFile)
    # if result is str
    if type(result) == str:
      return result, np_hard
    
    if result > 0:
      return True, np_hard
    else:
      return False, np_hard

  # If the graph is directed cyclic, it's NP-hard
  elif nx.is_directed(ogGraph):
    print("NP-hard")
    np_hard = True
    return "!?", np_hard
  
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
            return True, np_hard
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

  return False, np_hard

'''
Run the flow function on every file in the data folder
'''

def main():

  data = ReadInput()
  graph = data.toGraph()
  reds = [node for node in graph.nodes if node.is_red]

  print(someFlowPathRed(input, graph.nxGraph, data.s, data.t, reds))

if __name__ == "__main__":
  main()
