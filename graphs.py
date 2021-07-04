import math

class Graphs(object):
       
        def __init__(self, number_of_vertices):
            self.matrix = [[0] * number_of_vertices for _ in range(number_of_vertices)]
            
        def __repr__(self):
            #print('\n'.join([list(map(str, sub)) for sub in self.matrix]))
            return ('['+'\n'.join([str(e) for e in self.matrix])+']')

            #return str([list(map(str, sub)) for sub in self.matrix])

        def add_edge(self, v1, v2):
            self.matrix[v1][v2] = self.matrix[v2][v1] = 1
                
        def add_vertex(self):
            self.number_of_vertices += 1
            for vertices in self.matrix:
                vertices.append(0)
            self.matrix.append([0] * self.number_of_vertices)
            
        def remove_edge(self, v1, v2):
            self.matrix[v1][v2] = 0
            self.matrix[v2][v1] = 0
            
        def remove_vertex(self, v):
            for vertices in self.matrix:
                vertices.remove(vertices[v])
            self.matrix.remove(self.matrix[v])
            self.number_of_vertices -= 1    
 
            