from data_structures.nodo import Nodo

class ListaEnlazada:

    def __init__(self):
        
        # Inicializamos la cabeza de la lista como None (lista vacía)
        self.head = None

    def append(self, data):
        
        # Paso 1: Creamos un nuevo nodo con los datos recibidos
        new_node = Nodo(data)
        
        # Paso 2: Verificamos si la lista está vacía (la cabeza es None)
        if not self.head:
            # Si la lista está vacía, el nuevo nodo se convierte en la cabeza
            self.head = new_node
            return  # Terminamos la ejecución aquí
        
        # Paso 3: Si la lista no está vacía, buscamos el último nodo
        # Comenzamos desde la cabeza y avanzamos hasta que no haya un siguiente nodo
        last_node = self.head
        while last_node.next:  # Mientras el nodo actual tenga un siguiente...
            last_node = last_node.next  # Avanzamos al siguiente nodo
        
        # Paso 4: Añadimos el nuevo nodo como el 'siguiente' del último nodo
        last_node.next = new_node

    def prepend(self, data):
        
        # Paso 1: Creamos un nuevo nodo con los datos
        new_node = Nodo(data)
        
        # Paso 2: Hacemos que el nuevo nodo apunte a la cabeza actual
        new_node.next = self.head
        
        # Paso 3: Actualizamos la cabeza para que sea el nuevo nodo
        self.head = new_node

    def delete_node(self, key):
        
        # Paso 1: Empezamos desde la cabeza
        current_node = self.head
        
        # Caso especial: si el nodo a eliminar es la cabeza
        if current_node and current_node.data.id == key:
            # Hacemos que la nueva cabeza sea el siguiente nodo
            self.head = current_node.next
            # Eliminamos la referencia del nodo eliminado
            current_node = None
            return  # Terminamos
        
        # Paso 2: Buscamos el nodo a eliminar, manteniendo referencia al nodo anterior
        prev = None  # Variable para guardar el nodo anterior
        while current_node and current_node.data.id != key:
            prev = current_node  # Guardamos el nodo actual como anterior
            current_node = current_node.next  # Avanzamos al siguiente nodo
        
        # Paso 3: Si no encontramos el nodo (current_node es None), salimos
        if current_node is None:
            return  # Nodo no encontrado, no hacemos nada
        
        # Paso 4: Si encontramos el nodo, ajustamos las referencias
        # El nodo anterior ahora apunta al siguiente del nodo a eliminar
        prev.next = current_node.next
        # Eliminamos la referencia del nodo eliminado
        current_node = None

    def search(self, key):
        
        # Paso 1: Comenzamos desde la cabeza
        current = self.head
        
        # Paso 2: Recorremos toda la lista
        while current:
            # Verificamos si la clave coincide con el ID o el nombre del paciente
            if current.data.id == key or current.data.name == key:
                # Si encontramos una coincidencia, devolvemos los datos del paciente
                return current.data
            # Si no, avanzamos al siguiente nodo
            current = current.next
        
        # Paso 3: Si llegamos al final sin encontrar nada, devolvemos None
        return None

    def display(self):
        
        # Inicializamos una lista para guardar las representaciones de los elementos
        elements = []
        # Comenzamos desde la cabeza
        current = self.head
        
        # Recorremos toda la lista
        while current:
            # Convertimos los datos del nodo a cadena y los guardamos
            elements.append(str(current.data))
            # Avanzamos al siguiente nodo
            current = current.next
        
        # Unimos todos los elementos con ' -> ' y devolvemos la cadena
        return " -> ".join(elements)

    def to_list(self):
        
        # Inicializamos la lista vacía
        elements = []
        # Comenzamos desde la cabeza
        current = self.head
        
        # Recorremos toda la lista
        while current:
            # Añadimos los datos del nodo a la lista
            elements.append(current.data)
            # Avanzamos al siguiente nodo
            current = current.next
        
        # Devolvemos la lista completa
        return elements
