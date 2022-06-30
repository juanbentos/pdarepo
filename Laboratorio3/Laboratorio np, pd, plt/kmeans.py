class Kmeans():
    
    def __init__(self, nClusters:int = 2, maxIter:int = 300):
        """
        Constructor de clase.
        Args:
            - nClusters (int): Cantidad de clusters/grupos a encontrar
            - maxIter (int): número máximo de iteraciones a realizar para encontrar los cluster.
        """
        self.nClusters = nClusters
        self.maxIter = maxIter

    def fit(self, datos):
        """
        El método fit toma datos e para intentar encontrar nClusters.
        Argumentos:
            - datos (numpy.array): Patrones/Datos/Puntos con los cuales se buscarán clusters.
        """
        self.centroides = None
        self.etiquetas = None
        
        ## Implementar algoritmo de clustering