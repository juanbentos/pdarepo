import math

class Punto():
    

    """Clase para crear y operar puntos en un plano 2D, con operaciones como :
    - Mover un punto a una nueva coordenada
    - Calcular la distancia euclidiana entre estos dos puntos
    - Calcular la pendiente entre estos dos puntos
    """
    
    def __init__(self, x:float = 0.0, y:float = 0.0) ->None:
        """Iniciamos coordenadas de los puntos.
        Si los puntos x e y no se dan, se los inicializa en el origen"""
        self.moveTo(x, y)  
    
        
    def moveTo(self, newx:float, newy:float) ->None:
        """Mueve un punto a una nueva coordenada"""
        self.x = newx
        self.y = newy
        
    def calcularDistancia(self, otroPunto: "Punto") ->float:
        """Calcula la distancia euclidiana entre dos puntos
        
        Parámetro:
            - otroPunto: Instancia de un Punto()
            
        Retorna:
            - La distancia entre puntos (float)
        """
        return math.hypot(self.x - otroPunto.x, self.y - otroPunto.y)
    
    def calcularPendiente(self, otroPunto: "Punto") ->float:
        """Calcula la pendiente entre dos puntos
        
        Parámetro:
            - otroPunto: Instancia de un Punto()
            
        Retorna:
            - La pendeinte entre puntos (float)
        """
        pendiente=(self.y-otroPunto.y)/(self.x-otroPunto.x)
        return pendiente

#Creamos la clase Triangle()
class Triangle():
    """Utilizando los puntos creados en la clase Punto() con cordenadas x e y, los utilizamos en la clase triangle
    """
    def __init__(self, punto1:"Punto", punto2:"Punto", punto3:"Punto") ->None:
        if punto1==punto2  or punto2==punto3 or punto1==punto3:
            raise ValueError('Los puntos no forman un triangulo, puntos iguales')
        elif (punto1.x == punto2.x and punto1.x == punto3.x) or (punto1.y == punto2.y and punto1.y == punto3.y):
            raise ValueError('Los puntos no forman un triangulo, coinciden cordenadas de x o y')
        elif punto1.calcularPendiente(punto2)==punto2.calcularPendiente(punto3):
            raise ValueError('Los puntos no forman un triangulo, pendientes iguales')        
        else:
            self.punto1=punto1
            self.punto2=punto2
            self.punto3=punto3
    
    def getLargoLados(self):
        """Calculamos el la distancia entre los puntos, obteniendo así el largo de los lados de el triangulo."""
        
        distanciaP1P2=round(self.punto1.calcularDistancia(self.punto2),2)
        distanciaP2P3=round(self.punto2.calcularDistancia(self.punto3),2)
        distanciaP3P1=round(self.punto3.calcularDistancia(self.punto1),2)
        
        return [distanciaP1P2,distanciaP2P3,distanciaP3P1]
    
    def getArea(self):
        """Calculamos el aréa del triangulo, con sus datos calculamos el perimetro y posteriormente se calcula el areá"""
        lados=self.getLargoLados()
        perimetro = (lados[0] + lados[1] + lados[2])/2 #Calculamos el perimetro con los datos obtenidos en la lista de getLargoLados
        area= math.sqrt(perimetro * (perimetro - lados[0]) * (perimetro - lados[1]) * (perimetro - lados[2]))
        return round(area,2)
    
    def getType(self):
        """Obtenemos el tipo de triangulo a partir de la comparación del largo de sus lados"""
        lados=self.getLargoLados() #Asignamos la lista de getLargoLados a lados
        typeTriangulo=""
        if lados[0]==lados[1] and lados[1]==lados[2]:
            typeTriangulo = "Equilatero"
        elif lados[0]==lados[1] or lados[1]==lados[2] or lados[0]==lados[2]:
            typeTriangulo = "Isósceles"
        elif (lados[0]*2)+(lados[1]*2) == (lados[2]*2):
            typeTriangulo = "Rectangulo"
        else:
            typeTriangulo = "Escaleno"
        
        return typeTriangulo

p1=Punto(-3,10)
p2=Punto(-105,-7)
p3=Punto(-98,2)
triangulo1=Triangle(p1,p2,p3)
print(triangulo1.getLargoLados())
print(triangulo1.getArea())
print(triangulo1.getType())