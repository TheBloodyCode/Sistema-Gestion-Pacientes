class Nodo:

    def __init__(self, data):
        
        # Almacenamos los datos en el atributo 'data'
        self.data = data
        # Inicializamos el puntero al siguiente nodo como None (no hay siguiente nodo todavía)
        self.next = None
