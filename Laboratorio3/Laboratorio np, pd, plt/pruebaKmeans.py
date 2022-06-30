#LABORATORIO NUMPY, PANDAS, MATPLOTLIB
#UNIDAD CURRICULAR: PROGRAMACIÓN DIGITAL AVANZADA
#ESTUDIANTES: MARTIN MARCHADO; JUAN BENTOS; MAXIMILIANO VESPA

from turtle import color
import numpy as np
import matplotlib.pyplot as plt

'' 'El marcador cuenta el número de ejecuciones recursivas' ''
flag = 0

'' 'Distancia ' ''
def ecludDist(x, y):
    "Función para calcular la distancia Euclideana entre los puntos x e y "
    return np.sqrt(sum(np.square(np.array(x) - np.array(y))))

'' 'Calcular el punto medio del clúster' ''
def clusterMean(dataset):
    """Función para calcular la suma de los valores medios de un dataset de datos agrupados
    Parametros: Dataset"""
    return sum(np.array(dataset)) / len(dataset)

'' 'Generar puntos medios aleatorios' ''
def CentroRandom(dataset, k):
    """Función para puntos medios aleatorios en nuestro sets de datos, la cantidad de esos puntos estara determinada por un valor k, el cual especificara la cantidad de puntos a generar
    Parametrós: - Dataset
                - k """
    temp = []
    while len(temp) < k:
        index = np.random.randint(0, len(dataset)-1)
        if  index not in temp:
            temp.append(index)
    return np.array([dataset[i] for i in temp])

'' 'Tome los primeros k puntos del conjunto de datos como puntos medios' ''
def orderCenter(dataset, k):
    """ Función que permite seleccionar los primeros valores de nuestro datasets a partir del valor de k, los cuales seran considerados como los valores medios
    Parametros: 
        - dataset
        - k"""
    return np.array([dataset[i] for i in range(k)])

'' 'Cluster' ''
def kMeans(dataset, dist, center, k):
    """Función para agrupar datos a traves de generar puntos medios considerando un valor K. A partir de generar K puntos medios los cuales se 
    nombraran como centroides, se calculara la distancia de cada punto en la agrupación con respecto a cada punto, luego de calculada dicha distancia
    se realizara la agrupación de cada punto con el centroide que le corresponda. Gráficandose dichas agrupaciones las cuales seran diferenciadas con un color
    Parametros:
    - dataset
    - dist
    - center
    - k"""
    global flag
    
    #almacenar resultados de cálculo intermedios
    resulIntermedios = []
    for i in range(k):
        temp = []
        resulIntermedios.append(temp)
    #Calcule la distancia desde cada punto a cada punto medio  
    for i in dataset:
        temp = []
        for j in center:
            temp.append(dist(i, j))
        resulIntermedios[temp.index(min(temp))].append(i)    
    flag += 1
    
    # Actualizar punto medio
    centroides = np.array([clusterMean(i) for i in resulIntermedios])
    print(centroides)
    if (centroides == center).all():
        print('Final')
        for i in range(k):            
            plt.scatter([j[0] for j in resulIntermedios[i]], [j[1] for j in resulIntermedios[i]])
        indice=0
        for i in centroides:
            plt.scatter(centroides[indice][0],centroides[indice][1],marker='*', color="black")
            indice+=1        
        plt.grid()
        plt.show()
        print(flag)
    else:
        #Recursivamente llamar a la función kMeans
        center = centroides
        kMeans(dataset, dist, center, k)

def main():
    import pandas as pd
    import numpy as np
    data = pd.read_csv("C:\pdagit\pdarepo\Laboratorio3\Laboratorio3\datos\dataClusters\data_anisotropica.csv") #cargo datos
    x = data.iloc[:,0].values
    y = data.iloc[:,1].values
    k= 3
    #points = [[i,j] for i, j in zip(x, y)]
    points = np.array([x,y]).T    
    centroInicial = CentroRandom(dataset=points, k=k)
    kMeans(dataset=points, dist=ecludDist, center=centroInicial, k=k)
if __name__ == '__main__':
    main() 
