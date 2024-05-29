class mathrix:
    def __init__(self,datos:list)-> object:   #Incializa la clase
        
        '''
        Convierte una lista de lista a matriz
        '''
        
        self.datos=datos #Se ingresa una lista de listas
        self.filas=len(datos) #El número de elementos de las lista de datos es igual a el numero de filas
        self.columnas=len(datos[0]) #El número de elementos de cada fila es igual al número de columnas
    
        if not self.verificar_matriz(): 
            raise ValueError("Todas las filas deben tener la misma longitud")
        
    def verificar_matriz(self) -> bool:
        '''
        Comprueba que la longitud de todas las filas sea la misma
        '''
        return all(len(fila)==self.columnas for fila in self.datos)
        
    def dimension_igual(self,other) -> bool:
        '''
        Verifica si dos matrices tienen la misma dimensión
        '''
        
        return self.filas==other.filas and self.columnas==other.columnas
    
    def __add__(self,other) -> object:
        '''
        Suma dos matrices (Tienen que tener las mismas dimensiones)
        '''
        
        if not self.dimension_igual(other):
            raise ValueError('Las matrices tienen que tener las mismas dimensiones')
        
        matrix=[[0]*self.columnas for _ in range(self.filas)]
        
        for i in range((self.filas)):
            for j in range((self.columnas)):  
                matrix[i][j]=self.datos[i][j]+other.datos[i][j]
            
        return mathrix(matrix)
    
    def __sub__(self,other) -> object:
        '''
        Resta de dos matrices (Tienen que tener las mismas dimensiones)
        '''

        if not self.dimension_igual(other):
            raise ValueError('Las matrices tienen que tener las mismas dimensiones')
        
        matrix=[[0]*self.columnas for _ in range(self.filas)]
        
        for i in range((self.filas)):
            for j in range((self.columnas)):  
                matrix[i][j]=self.datos[i][j]-other.datos[i][j]
            
        return mathrix(matrix)
     
    def prod(self,*args) -> object:
        '''
        Multiplica una matriz por otra u otras matrices
        '''
        original=self
        
        
        for matriz in args:
            if original.columnas!=matriz.filas:
                raise ValueError('El número de columnas de la matriz de la izquierda debe coincidir con el número de filas de la columna de la derecha')
            
            resultado=[[0]*matriz.columnas for _ in range(original.filas)]
            
            for i in range(original.filas):
                for j in range(matriz.columnas):
                    suma=0
                    for k in range(original.columnas):
                        suma+=original.datos[i][k] * matriz.datos[k][j]
                    resultado[i][j]=suma
            original=mathrix(resultado)
        return mathrix(resultado)
    
    def scalar_mul(self,scalar:float) -> object:
        '''
        Multiplica una matriz por un escalar
        '''
        
        matrix=[[0]*self.columnas for _ in range(self.filas)]
        
        for i in range(self.filas):
            for j in range(self.columnas):
                matrix[i][j]=self.datos[i][j]*scalar
        
        return mathrix(matrix)

    def tr(self) -> float:
        '''
        Devulve la suma de los elementos diagonales de una matriz cuadrada
        '''
        
        if not self.filas==self.columnas:
            raise ValueError('La matriz tiene que ser cuadrada')
        
        traza=0
        
        for i in range(self.filas):
                traza+=self.datos[i][i]
                
        return traza
        
    def transpuesta(self) -> object:
        '''
        Devuelve una matriz con los indices alrrevez
        '''
        matrix=[[0]*self.filas for _ in range(self.columnas)]
        
        
        for i in range(self.filas):
            for j in range(self.columnas):
                matrix[j][i]=self.datos[i][j]

        return mathrix(matrix)
    
    def mIdentidad(numFila:int) -> object:
        '''
        Crea una matriz diagonal con solo numeros 1 de dimensiones numFila x numFila
        '''
        M=[[0]*numFila for _ in range(numFila)]
        
        for i in range(numFila):
            M[i][i]=1
            
        return mathrix(M)
    
    def potencia(self,potencia:int) ->object:
        '''
        Eleva una matriz cuadrada a una potencia
        '''
        
        if potencia <1:
            raise ValueError('La potencia tiene que ser mayor o igual que 1')
        original=self
        
        for _ in range(1,potencia):
            original=original.prod(self)
        return(original)

    def determinante(self:object) -> float:
        '''
        Calcula la determinante de una matriz - Tiene que ser cuadrada
        '''
        
        if self.filas!=self.columnas:
            raise ValueError('La matriz tiene que ser cuadrada')
        
        if self.filas==1:
            return self.datos[0][0]
        
        if self.filas==2:
            return self.datos[0][0]*self.datos[1][1]-self.datos[0][1]*self.datos[1][0]
        
        det=0 
        
        for columna in range(self.columnas):
            menor = [fila[:columna] + fila[columna+1:] for fila in self.datos[1:]]
            
            cofactor=(-1)**columna * self.datos[0][columna]*(mathrix(menor).determinante())
            
            det+=cofactor
            
        return det
          
    def __str__(self) -> str:
        '''
        Regresa una representación en cadena de la matriz
        '''
        mathrixSTR= '\n'.join ( '\t'.join ( map(str,fila) ) for fila in self.datos )
        
        return f'Matriz {self.filas}x{self.columnas}:\n{mathrixSTR}'            


def listaToMatriz(datos:list,numFilas:int,numColumnas:int)-> object:
    '''
    Genera una matriz de dimensiones deseadas a partir de una lista de números
    '''
    
    if numFilas*numColumnas!=len(datos):
        raise ValueError('Verificar dimensiones')
    
    
    M=[[0]*numColumnas for _ in range(numFilas)]

    for i in range(numFilas):
        for j in range(numColumnas):
            
            M[i][j]=datos[(numColumnas*i) + j]
    
    return mathrix(M)

matriz = mathrix([
    [2, -3, 7,3],
    [2, 0, -1,4],
    [1, 4, 5,6],
    [1, 6, 0,6]])

print(matriz.determinante())