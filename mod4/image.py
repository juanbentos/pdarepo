
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from utils import crearMatrix
import scipy as sp
from scipy import signal

#CLASES
class Image():
    """Documentación de Image"""

    def __init__(self, dimensiones:tuple = None, filename:str = ""):
        """Crea una imagen
        Paramas:
            - dimensiones: tupla con las dimensiones de la imágen a formar
            - filenme: nombre del archivo de imágen a cargar
        """
        if dimensiones:
            self.image = crearMatrix(dimensiones) #generamos una matriz de ceros
            self.filas = self.image.shape[0]
            self.columnas = self.image.shape[1]
            self.canales = self.image.shape[2]
        elif filename:
            self.image = self._loadImage(filename)
            self.filas = self.image.shape[0] #número de filas
            self.columnas = self.image.shape[1] #número de columnas
            self.canales = self.image.shape[2]
        else:
            raise ValueError("No se ha dado una dimensión ni un archivo")

    def _loadImage(self, filename:str):
        """Cargamos imágen"""
        return mpimg.imread(filename).astype(np.uint8)
        
    def show(self):
        """Mostramos imágen"""
        plt.imshow(self.image) #.astype(np.uint8)
        plt.show()

    def size(self):
        """Retorna una tupla de la forma (filas, columnas, canales)
        Si Image posee un solo canal, devuelve una tupla de la forma (filas, columnas)
        """
        return (self.filas,self.columnas,self.canales)

    def saveImage(self, filename:str):
        """Guarda la imágen en un archivo jpg"""
        
        return mpimg.imsave(filename,self.image)

#FUNCIONES
def ajustarContraste(image, alfa):
    """Ajusta el contraste de una imágen.
    
    Retorna una nueva imágen con las mismas dimensiones de la imágen original.
    """
    filas = image.image.shape[0] #cantidad de filas
    columnas = image.image.shape[1] #cantidad de columnas
    canales = image.image.shape[2]
    #Creo un nuevo objeto Image
    imagenProcesada = Image(dimensiones = (filas, columnas, canales))
    for canal in range(canales):
        for i in range(filas):
            for j in range(columnas):
                pixel = int(alfa*(image.image[i][j][canal]-128) + 128)
                if pixel < 0:
                    pixel = 0
                elif pixel > 255:
                    pixel = 255
                imagenProcesada.image[i][j][canal] = int(pixel)

    imagenProcesada.image = imagenProcesada.image.astype(np.uint8)
                
    return imagenProcesada
def ajustarBrillo(image, ajuste):
    """Doc..."""
    pass

def getHistograma(image):
    """Doc..."""
    plt.hist(image.ravel(), bins=256)
    plt.show()    

def getChannels(image, channel):
    """Doc..."""
    if channel == 0:
        return image.image[:,:,0]
    elif(channel == 1):
        return image.image[:,:,1]
    elif (channel == 2):
        return image.image[:,:,2]
        
def ajustarGamma(image, gamma):
    """Doc..."""
    maximo=np.amax(image.image)
    c=(255/maximo)
    filas = image.image.shape[0] #cantidad de filas
    columnas = image.image.shape[1] #cantidad de columnas
    canales = image.image.shape[2]
    #Creo un nuevo objeto Image
    imagenProcesada = Image(dimensiones = (filas, columnas, canales))
    
    for canal in range(canales):
        for i in range(filas):
            for j in range(columnas):
                pixel = int(c*(image.image[i][j][canal])**gamma)
                if pixel < 0:
                    pixel = 0
                elif pixel > 255:
                    pixel = 255
                imagenProcesada.image[i][j][canal] = int(pixel)

    imagenProcesada.image = imagenProcesada.image.astype(np.uint8)
                
    return imagenProcesada

def aplicarKernel(imagen, kernel):    
    
    KERNELS = {"topSobel": np.array([[-1,-1,-1],[-1, 8,-1],[-1,-1,-1]]),
                "blur": np.array([[0.0625, 0.125,0.0625],[0.125, 0.25, 0.125],[0.0625, 0.125,0.0625]]),
                "bottomSobel": np.array([[-1,-2,-1],[0,0,0],[1,2,1]]),
                "leftSobel": np.array([[1,0,-1],[2,0,-2],[1,0,-1]]),
                "rightSobel": np.array([[-1,0,1],[-2,0,2],[-1,0,1]]),
                "emboss": np.array([[-2,-1,0],[-1,1,1],[0,1,2]]),
                "ouutline": np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),
                "sharpen": np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])}
    
    imagen=imagen.image
    kernel= KERNELS[kernel]
    imagen_list = []
    for d in range(3):
        temp = signal.convolve2d(imagen[:,:,d] , kernel,  boundary='symm',mode='same')
        imagen_list.append(temp)

    imagen_filt = np.stack(imagen_list, axis=2)
    imagen_filt[imagen_filt > 255] = 255
    imagen_filt[imagen_filt < 0] = 0
    imagen_filt = imagen_filt.astype("uint8")

    return imagen_filt

def graficarShow(imagen):
    
    plt.rcParams["figure.figsize"]=(10,5)
    plt.plot
    plt.imshow(imagen)
    plt.show()   

def main():
    #Mostrar su implementación aquí
    imagen1=Image(filename="C:\pda\Modulo 4\Ejercitacion\coronary1.jpg")
    #np.amax(imagen1)   
    #getHistograma(procesada)
    # #imagen1.size()
    # #imagen1.saveImage("hola.jpg")     
    imagen1=ajustarContraste(imagen1,3)       
    #imagen1.saveImage("C:\pda\Modulo 4\Ejercitacion\hola.jpg")
    procesada = aplicarKernel(imagen1,"topSobel")
    graficarShow(procesada)

if __name__ == '__main__':
    main()