import numpy as np
import pandas as pd


class Node():
    def __init__(self,name, **kwargs):
        """
        name : ten cua node: unique voi cac nam khac:
        transform: callable để gọi node khác.
        previous_node: node_phía trước trong graph
        """
        self.name = name
        
        self.hashing = 14
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

    def excute(self, context):
        print(
            f'Node {self.name} is not define excute function'
        )        
        pass 
    
class PathGraph:
    def __init__(self, unique_id):
        self.paths =[]
        self.unique_id = unique_id
    def matched(self, another_path):
        if len(self.paths) != len(another_path.paths):return False
        match = [i.name == j.name for i,j in zip(self.paths, another_path.paths)]
        if sum(match) != len(match):return False
        return True


class Graph:
    def __init__(self):
        self.graphs = []
    
