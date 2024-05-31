Documentación de la Biblioteca `mathrixpy`

Descripción

    `mathrixpy` es una biblioteca de Python para realizar operaciones matriciales. Permite la creación, manipulación y operaciones aritméticas con matrices. Esta biblioteca es útil para aplicaciones matemáticas y científicas que requieren cálculos matriciales.

Clase `mathrix`

    Constructor

        `__init__(self, datos: list) -> object`
            Inicializa una instancia de la clase `mathrix`.

            Parámetros:
                - `datos` (list): Lista de listas que representa la matriz.

            Excepciones:
                - `ValueError`: Si las filas no tienen la misma longitud.

    Métodos Privados

        `__verificar_matriz(self: object) -> bool`
            Comprueba que la longitud de todas las filas sea la misma.

        `__dimension_igual(self, other) -> bool`
            Verifica si dos matrices tienen la misma dimensión.

        `__matriz_cuadrada_error(self: object) -> bool`
            Verifica si la matriz es cuadrada. Lanza una excepción si no lo es.

    Métodos de Operación

        `__add__(self: object, other: object) -> object`
            Suma dos matrices de las mismas dimensiones.

            Parámetros:
                - `other` (object): Otra instancia de `mathrix`.

            Excepciones:
                - `ValueError`: Si las matrices no tienen las mismas dimensiones.

        `__sub__(self: object, other: object) -> object`
            Resta dos matrices de las mismas dimensiones.

            Parámetros:
                - `other` (object): Otra instancia de `mathrix`.

            Excepciones:
                - `ValueError`: Si las matrices no tienen las mismas dimensiones.


        `get_Datos(self:object) -> list`
            Regresa una lista de listas  perteneciente al atriputo datos


        `prod(self: object, *args: object) -> object`
            Multiplica una matriz por otra u otras matrices.

            Parámetros:
                - `*args` (object): Una o más instancias de `mathrix`.

            Excepciones:
                - `ValueError`: Si el número de columnas de la matriz izquierda no coincide con el número de filas de la matriz derecha.

        `scalar_mul(self: object, scalar: float) -> object`
            Multiplica una matriz por un escalar.

            Parámetros:
                - `scalar` (float): El escalar por el cual se multiplicará la matriz.

        `tr(self: object) -> float`
            Devuelve la suma de los elementos diagonales de una matriz cuadrada.

            Excepciones:
                - `ValueError`: Si la matriz no es cuadrada.

        `transpuesta(self: object) -> object`
            Devuelve la transpuesta de la matriz.

        `potencia(self: object, potencia: int) -> object`
            Eleva una matriz cuadrada a una potencia dada.

            Parámetros:
                - `potencia` (int): La potencia a la cual se elevará la matriz.

            Excepciones:
                - `ValueError`: Si la potencia es menor que 1.

        `determinante(self: object) -> float`
            Calcula el determinante de una matriz cuadrada.

            Excepciones:
                - `ValueError`: Si la matriz no es cuadrada.

        `submatriz(self: object, fila: int, columna: int) -> object`
            Devuelve una submatriz excluyendo la fila y columna especificada.

            Parámetros:
                - `fila` (int): La fila a excluir.
                - `columna` (int): La columna a excluir.

        `cofactor(self: object, fila: int, columna: int) -> float`
            Calcula el cofactor de un elemento en la fila y columna especificada.

            Parámetros:
                - `fila` (int): La fila del elemento.
                - `columna` (int): La columna del elemento.

        `adjunta(self: object) -> object`
            Devuelve la matriz adjunta de una matriz cuadrada.

        `inversa(self: object) -> object`
            Calcula la matriz inversa de una matriz cuadrada.

            Excepciones:
                - `ValueError`: Si la matriz no es cuadrada.

    Métodos Especiales

        `__str__(self: object) -> str`
            Regresa una representación en cadena de la matriz.

Funciones Auxiliares

    `listaToMatriz(datos: list, numFilas: int, numColumnas: int) -> object`
        Genera una matriz de dimensiones deseadas a partir de una lista de números.

        Parámetros:
            - `datos` (list): Lista de números para llenar la matriz.
            - `numFilas` (int): Número de filas de la matriz.
            - `numColumnas` (int): Número de columnas de la matriz.

        Excepciones:
            - `ValueError`: Si el número de elementos en `datos` no coincide con `numFilas * numColumnas`.

    `mIdentidad(numFila: int) -> object`
        Crea una matriz identidad de dimensiones `numFila x numFila`.

        Parámetros:
            - `numFila` (int): Dimensión de la matriz identidad.
