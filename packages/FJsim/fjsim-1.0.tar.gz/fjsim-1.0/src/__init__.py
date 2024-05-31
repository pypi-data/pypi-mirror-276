import numpy as np

class Friedkin_Johnsen:
    
    
    """
    This class simulates how opinions spread using the Friedkin-Johnsen model:
    weight is the weight matrix of the network chosen, it's a row-stochastis matrix where the diagonal ha the self influences of each node of the network;
    influence is the matrix of how much each person is influenced by its initial opinions, by default it's set to 0 for all nodes(De Groot model);
    initial is the nx1 matrix of the initial opinon of the initial opinion of each node.
    """
    
    
    def __init__(self, weight : np.array, influence: np.array) -> None:
        self.weight = weight
        self.influence = influence
        
    
    def simulate(self, initial: np.array) -> np.array:
        self.initial = initial
        C = (np.identity(self.weight.shape[0]) - (self.influence @ self.weight))
        #check i    f matrix C is nonsingular
        if np.linalg.det(C) == 0:
            return -1
        else:
            pass
        self.V = (np.linalg.inv(C)) @ ((np.identity(self.weight.shape[0]) - self.influence))
        return np.matmul(self.V, self.initial)
    
    
    def __str__(self) -> str:
        return 'Calculate the opinion of each person in a network'





if __name__ == '__main__':
    print('Calculate the opinion of each person in a network')
else:
    pass