import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from utils import crearMatrix
import scipy as sp
from scipy import signal
from PIL import Image,ImageEnhance

#CLASES
class Image():
    """Documentación de Image
    Clase denominada Image() que recibe parametros como dimensiones de la imagen a formar y/o su nombre.
    Con los parametros recibidos se pueden realizar acciones como:
     - Cargar la imagen
     - Mostrar la imagen
     - Mostrar el tamaño de la imagen
     - Guardar la imagen en un archivo jpg
     """
    def __init__(self, dimensiones:tuple = None, filename:str = ""):
        """Crea una imagen
        Parametros:
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
        imgplot = plt.imshow(self.image) #.astype(np.uint8)

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
    """Ajuste del brillo recibiendo parametros como la imagen y el valor de ajuste """
    img = ImageEnhance.Brightness(image)
    return img.enhance(ajuste).show()

def getHistograma(image):
    """Se grafica el histograma de la imagen por medio del conteo de la frecuencía de los bins, los cuales se almacenan en una matriz para posteriormente poder graficar el histograma"""
    plt.hist(image.image.ravel(),bins=256)   
    plt.show() 

def getChannels(image, channel):
    """Se muestra una matriz de datos para el canal especificado"""
    if channel == 0:
        return image.image[:,:,0] #Si el canal es 0 "R", retorno la matris de datos para dicho canal
    elif(channel == 1):
        return image.image[:,:,1] #Si el canal es 1 "G", retorno la matris de datos para dicho canal
    elif (channel == 2):
        return image.image[:,:,2] #Si el canal es 2 "B" , retorno la matris de datos para dicho canal

def ajustarGamma(image, gamma):
    """Función utilizada para modificar el rango dinamico de una imagen, recibiendo como parametros la imagen y factor gama.
    Por medio de calculos matematicos se genera una nueva imagen con las modificaciones"""
    maximo=np.amax(image.image)
    c=(255/maximo)
    filas = image.image.shape[0] #cantidad de filas
    columnas = image.image.shape[1] #cantidad de columnas
    canales = image.image.shape[2]
    #Creo un nuevo objeto Image
    imagenProcesada = Image(dimensiones = (filas, columnas, canales))
    
    for canal in range(canales): #En los for a continuación se recorren todos los pixels de cada columna y fila en cada canal y se realiza el calculo denominado "Pixel" , para la modificación de estos
        for i in range(filas):
            for j in range(columnas):
                pixel = int(c*(image.image[i][j][canal])**gamma)
                if pixel < 0: #Se pone la condición para delimitar los limites entre 0 y 255
                    pixel = 0
                elif pixel > 255:
                    pixel = 255
                imagenProcesada.image[i][j][canal] = int(pixel) #Almaceno los pixel modificados en el obteto imagen procesada creado anteriormente

    imagenProcesada.image = imagenProcesada.image.astype(np.uint8) #El objeto imagen procesada se especifica de tipo uint8, para que la imagen tenga un rango de valores de 0 a 255
                
    return imagenProcesada

def aplicarKernel(imagen, kernel):  
    """Se realiza la convolución de una imagen, por medio de recibir parametros como la imagen y el nombre de un kernel para realizar dicha convolución"""
    #Almaceno los diferentes kernels por medio de arrays
    KERNELS = {"topSobel": np.array([[-1,-1,-1],[-1, 8,-1],[-1,-1,-1]]),
                "blur": np.array([[0.0625, 0.125,0.0625],[0.125, 0.25, 0.125],[0.0625, 0.125,0.0625]]),
                "bottomSobel": np.array([[-1,-2,-1],[0,0,0],[1,2,1]]),
                "leftSobel": np.array([[1,0,-1],[2,0,-2],[1,0,-1]]),
                "rightSobel": np.array([[-1,0,1],[-2,0,2],[-1,0,1]]),
                "emboss": np.array([[-2,-1,0],[-1,1,1],[0,1,2]]),
                "ouutline": np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),
                "sharpen": np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])}
    
    imagen=imagen.image #Almaceno la matriz de la imagen en la variable imagen
    kernel= KERNELS[kernel] #Almaceno los kernes en una variable denominada kernel, y podre acceder a estos por su nombre
    imagen_list = [] #Creo una lista denominada imagen_list 
    for d in range(3): #Se recorren los tres canales de la imagen
        temp = signal.convolve2d(imagen[:,:,d] , kernel,  boundary='symm',mode='same') #se genera una variable temporal, donde se reraliza la convolución de la imagen en sus tres canales por  medio del uso de la libreria signal
        imagen_list.append(temp)   #Agregamos la variable temporal a la lista imagen_list
 
    imagen_filt = np.stack(imagen_list, axis=2) #
    imagen_filt[imagen_filt > 255] = 255
    imagen_filt[imagen_filt < 0] = 0
    imagen_filt = imagen_filt.astype("uint8")

    return imagen_filt

def graficarShow(imagen):
    """Función utilizada para graficar la imagen modificada luego de aplicar el kernell"""
    
    plt.rcParams["figure.figsize"]=(10,5)
    plt.plot
    plt.imshow(imagen)
    plt.show()

def main():
    #Mostrar su implementación aquí
    imagen1=Image(filename="C:\pdagit\pdarepo\mod4\EJERCITACIÓN\coronary1.jpg")  
    #img=ajustarContraste(imagen1,3)   
    #img = getHistograma(imagen1)
    #img = getChannels(imagen1,2)
    #img = ajustarGamma(imagen1,2)       
    #img = aplicarKernel(imagen1,"topSobel")
    #graficarShow(img)
    
if __name__ == '__main__':
    main()