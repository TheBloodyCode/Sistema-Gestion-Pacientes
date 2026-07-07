class Cola:

    def __init__(self):
        
        # Inicializamos una lista vacía para almacenar los elementos de la cola
        self.items = []

    def enqueue(self, item):
        
        # Insertamos el nuevo elemento al principio de la lista
        self.items.insert(0, item)

    def dequeue(self):
        
        # Verificamos si la cola no está vacía
        if not self.is_empty():
            # Si hay elementos, sacamos y devolvemos el último elemento de la lista
            # (que es el primero que entró)
            return self.items.pop()
        # Si la cola está vacía, devolvemos None
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
