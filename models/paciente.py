import uuid
from datetime import datetime

class Paciente:

    def __init__(self, patient_id, name, apellido, age, gender, medical_history=None, 
                 fecha_registro=None, dia_registro=None, enfermedad_principal="Ninguna",
                 condicion_actual="Estable/General", sintomas_actuales=None):
        
        # El ID es el número de cédula del paciente
        self.id = patient_id
        # Almacenamos los nombres del paciente
        self.name = name
        # Almacenamos los apellidos del paciente
        self.apellido = apellido
        # Almacenamos la edad del paciente
        self.age = age
        # Almacenamos el género del paciente
        self.gender = gender
        # Historial médico (lista de strings). Si no se proporciona, iniciamos lista vacía
        self.medical_history = medical_history if medical_history is not None else []
        
        # Fecha de registro (si no se da, tomamos la de hoy)
        if fecha_registro:
            self.fecha_registro = fecha_registro
        else:
            self.fecha_registro = datetime.now().strftime("%Y-%m-%d")
            
        # Día de la semana (Lunes, Martes, etc.)
        self.dia_registro = dia_registro or self._calcular_dia(self.fecha_registro)
        
        # Enfermedad principal registrada (útil para ordenamiento)
        self.enfermedad_principal = enfermedad_principal
        
        # Condición actual del paciente (Emergencia, Sala de espera, etc.)
        self.condicion_actual = condicion_actual
        
        # Síntomas actuales del paciente
        self.sintomas_actuales = sintomas_actuales if sintomas_actuales is not None else []

    def _calcular_dia(self, fecha_str):
        # Método auxiliar para calcular el día de la semana en español
        try:
            dt = datetime.strptime(fecha_str, "%Y-%m-%d")
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            return dias[dt.weekday()]
        except:
            return "Desconocido"

    def __str__(self):
        
        # Devolvemos una cadena con formato claro para el paciente
        sintomas_str = ", ".join(self.sintomas_actuales) if self.sintomas_actuales else "Ninguno reportado"
        return (
            f"╔════════════════════════════════════════╗\n"
            f"║ Cédula: {self.id:<32}║\n"
            f"╠════════════════════════════════════════╣\n"
            f"║ Nombre: {self.name:<32}║\n"
            f"║ Apellidos: {self.apellido:<29}║\n"
            f"║ Edad: {self.age:<35}║\n"
            f"║ Género: {self.gender:<32}║\n"
            f"║ Ingreso: {self.fecha_registro} ({self.dia_registro}){'':<10}║\n"
            f"╠════════════════════════════════════════╣\n"
            f"║ ESTADO Y CONDICIÓN MÉDICA              ║\n"
            f"║ Condición: {self.condicion_actual:<29}║\n"
            f"║ Enfermedad: {self.enfermedad_principal:<28}║\n"
            f"║ Síntomas: {sintomas_str:<30}║\n"
            f"╚════════════════════════════════════════╝"
        )

    def to_dict(self):
        
        # Creamos y devolvemos un diccionario con los datos del paciente
        return {
            "id": self.id,
            "name": self.name,
            "apellido": self.apellido,
            "age": self.age,
            "gender": self.gender,
            "medical_history": self.medical_history,
            "fecha_registro": self.fecha_registro,
            "dia_registro": self.dia_registro,
            "enfermedad_principal": self.enfermedad_principal,
            "condicion_actual": self.condicion_actual,
            "sintomas_actuales": self.sintomas_actuales
        }

    @classmethod
    def from_dict(cls, data):
        
        # Creamos un nuevo paciente con todos los datos. 
        # Usamos get() para los nuevos campos así no rompemos compatibilidad con CSV viejos.
        patient = cls(
            data["id"],
            data["name"],
            data.get("apellido", ""),
            data["age"],
            data["gender"],
            data.get("medical_history"),
            data.get("fecha_registro"),
            data.get("dia_registro"),
            data.get("enfermedad_principal", "Ninguna"),
            data.get("condicion_actual", "Estable/General"),
            data.get("sintomas_actuales", [])
        )
        return patient
