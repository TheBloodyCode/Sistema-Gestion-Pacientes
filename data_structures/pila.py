class Pila:

    def __init__(self):
        
        # Inicializamos una lista vacía para almacenar los elementos de la pila
        self.items = []

    def push(self, item):
        
        # Añadimos el nuevo elemento al final de la lista (cima de la pila)
        self.items.append(item)

    def pop(self):
        
        # Verificamos si la pila no está vacía
        if not self.is_empty():
            # Si hay elementos, sacamos y devolvemos el último elemento de la lista
            # (que es la cima de la pila)
            return self.items.pop()
        # Si la pila está vacía, devolvemos None
        return None

    def peek(self):
        
        # Verificamos si la pila no está vacía
        if not self.is_empty():
            # Si hay elementos, devolvemos el último elemento de la lista sin eliminarlo
            return self.items[-1]
        # Si la pila está vacía, devolvemos None
        return None

    def is_empty(self):
        
        # Comparamos la longitud de la lista con 0 para ver si está vacía
        return len(self.items) == 0

    def size(self):
        
        # Devolvemos la longitud de la lista
        return len(self.items)

    def to_list(self):
        
        # Devolvemos una copia de la lista de items
        return list(self.items)
