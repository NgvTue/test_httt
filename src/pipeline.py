import pickle
class PipeLine():
    def __init__(self):
        self.pipe = []
        self.hashing=44
    def add_pipe(self, pipeline):
        self.pipe.append(pipeline)
    def save(self,fpath):
        with open(fpath, 'wb') as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)
    @staticmethod
    def load(fpath):
        with open(fpath, 'rb') as inp:
            object_variable = pickle.load(inp)
        assert object_variable.hashing == 44, 'Invalid hashing code'
        assert isinstance(object_variable, PipeLine), f'Invalid tupe of object {type(object_variable)}'
        assert isinstance(object_variable.pipe, list), f'Invalid pipeline {type(object_variable.pipe)}'
        return object_variable 