class ColaProioridad:

    def __init__(self):
        
        # Inicializamos la lista que almacenará los elementos de la cola
        # Cada elemento será una tupla: (prioridad, contador, paciente)
        self.items = []
        
        # Contador para desempatar: cuando dos pacientes tienen la misma prioridad,
        # el que entró primero (número menor) se atiende primero
        self.counter = 0
    
    def encolar(self, paciente, prioridad):
        
        # Paso 1: Creamos una tupla (prioridad, contador, paciente)
        # La tupla facilita el ordenamiento automático
        tupla_paciente = (prioridad, self.counter, paciente)
        
        # Paso 2: Añadimos la tupla a la lista
        self.items.append(tupla_paciente)
        
        # Paso 3: Incrementamos el contador para el próximo paciente
        # Esto asegura que cada paciente tenga un número único secuencial
        self.counter += 1
        
        # Paso 4: Ordenamos la lista de pacientes
        # Usamos sort con una función lambda que ordena:
        # - Primero por prioridad descendente (-x[0], el negativo invierte el orden)
        # - Luego por contador ascendente (x[1], para FIFO en misma prioridad)
        self.items.sort(key=lambda x: (-x[0], x[1]))
    
    def desencolar(self):
        
        # Paso 1: Verificamos si la cola no está vacía
        if not self.esta_vacia():
            # Paso 2: Sacamos y retornamos el primer elemento (posición 0)
            # El element[2] es el paciente (el tercero de la tupla)
            return self.items.pop(0)[2]
        
        # Si la cola está vacía, retornamos None
        return None
    
    def esta_vacia(self):
        
        # Comparamos la longitud de la lista con 0
        return len(self.items) == 0
    
    def ver_primero(self):
        
        # Paso 1: Verificamos si la cola no está vacía
        if not self.esta_vacia():
            # Paso 2: Retornamos el paciente del primer elemento sin eliminarlo
            # self.items[0] accede al primer elemento
            # [2] accede al paciente dentro de la tupla
            return self.items[0][2]
        
        # Si la cola está vacía, retornamos None
        return None
    
    def tamaño(self):
        
        # Devolvemos la longitud de la lista
        return len(self.items)
    
    def obtener_todos(self):
        
        # Paso 1: Creamos una lista nueva
        # Paso 2: Recorremos cada elemento de self.items
        # Paso 3: Para cada tupla (prioridad, contador, paciente), extraemos el paciente [2]
        # Esto crea una lista solo con los objetos Paciente, sin las tuplas
        return [item[2] for item in self.items]
    
    def limpiar(self):
        
        # Vaciamos la lista de items
        self.items = []
        # Reiniciamos el contador
        self.counter = 0
