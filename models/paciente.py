import uuid

class Paciente:

    def __init__(self, patient_id, name, age, gender, medical_history=None):
        
        # El ID es el número de cédula del paciente
        self.id = patient_id
        # Almacenamos el nombre del paciente
        self.name = name
        # Almacenamos la edad del paciente
        self.age = age
        # Almacenamos el género del paciente
        self.gender = gender
        # Inicializamos el historial médico: si se proporciona, lo usamos; si no, lista vacía
        self.medical_history = medical_history if medical_history is not None else []

    def __str__(self):
        
        # Devolvemos una cadena con formato claro para el paciente
        return (
            f"╔════════════════════════════════════════╗\n"
            f"║ Cédula: {self.id:<32}║\n"
            f"╠════════════════════════════════════════╣\n"
            f"║ Nombre: {self.name:<32}║\n"
            f"║ Edad: {self.age:<35}║\n"
            f"║ Género: {self.gender:<32}║\n"
            f"╚════════════════════════════════════════╝"
        )

    def to_dict(self):
        
        # Creamos y devolvemos un diccionario con los datos del paciente
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "medical_history": self.medical_history
        }

    @classmethod
    def from_dict(cls, data):
        
        # Paso 1: Creamos un nuevo paciente con todos los datos (incluyendo el ID)
        patient = cls(
            data["id"],
            data["name"],
            data["age"],
            data["gender"],
            data.get("medical_history")  # Usamos get() para evitar errores si no existe la clave
        )
        # Paso 2: Devolvemos el paciente completo
        return patient
