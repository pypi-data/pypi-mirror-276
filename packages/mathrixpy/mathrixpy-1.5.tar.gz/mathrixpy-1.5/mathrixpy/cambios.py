class matrizop:
    def __init__(self,datos:list)-> object:   #Incializa la clase    
        '''
        Convierte una lista de lista a matriz
        '''
        
        self.datos=datos #Se ingresa una lista de listas
        self.filas=len(datos) #El número de elementos de las lista de datos es igual a el numero de filas
        self.columnas=len(datos[0]) #El número de elementos de cada fila es igual al número de columnas

#Cambios  
    def extractColumna(self,numColumna)->list:
        resultado=[]
        
        for i in self.datos:
            resultado.append(i[numColumna-1])
        return resultado
    
    def apply_function(self, func) -> object:
        '''
        Aplica una función a cada elemento de la matriz
        '''
        matrix = [[func(self.datos[i][j]) for j in range(self.columnas)] for i in range(self.filas)]
        return matrizop(matrix)

    
if __name__=="__main__":
    
    v=matrizop([[1,2], 
                [4,5]])
    
    z=matrizop( [[1], 
                 [2],
                 [3]])
    
    m=matrizop.listaToMatriz([1,2,3,5,4,5],2,3)
    