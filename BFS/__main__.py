from Graph import Graph
from Node import Node
from bfs import BFS

graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : [],
  '4' : ['8'],
  '8' : []
}

graph = Graph(name="Graph1",
              nodes=[
                  Node(5, [3, 7]),
                  Node(3, [2, 4]),
                  Node(7, [8]),
                  Node(2, []),
                  Node(4 ,[8]),
                  Node(8,[])
              ],
              nodes_cnt=6)

bfs = BFS(graph)

bfs.run()