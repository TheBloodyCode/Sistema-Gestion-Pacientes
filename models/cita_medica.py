from datetime import datetime
import uuid
from models.especialidad import EspecialidadMedica, TipoCita

class CitaMedica:

    def __init__(self, patient_id, specialty, appointment_type, 
                 date, time, notes="", priority=3):
        
        # Paso 1: Generar un ID único para la cita
        # uuid.uuid4() genera un identificador universal único
        # [:8] toma solo los primeros 8 caracteres para que sea más legible
        self.id = str(uuid.uuid4())[:8]
        
        # Paso 2: Almacenar el ID del paciente
        # Este ID debe coincidir con uno de los pacientes en el sistema
        self.patient_id = patient_id
        
        # Paso 3: Almacenar la especialidad médica
        self.specialty = specialty
        
        # Paso 4: Almacenar el tipo de cita
        self.appointment_type = appointment_type
        
        # Paso 5: Almacenar la fecha de la cita
        self.date = date
        
        # Paso 6: Almacenar la hora de la cita
        self.time = time
        
        # Paso 7: Almacenar notas adicionales si las hay
        self.notes = notes
        
        # Paso 8: Almacenar el nivel de prioridad de la cita
        # Esto es importante para emergencias o casos urgentes
        self.priority = priority
        
        # Paso 9: Establecer el estado inicial de la cita como "Programada"
        # Los estados posibles son:
        # - "Programada": Cita futura aún no atendida
        # - "En Progreso": Paciente actualmente siendo atendido
        # - "Completada": Cita ya realizada
        # - "Cancelada": Cita cancelada por el paciente o clínica
        self.status = "Programada"
        
        # Paso 10: Registrar la fecha y hora exacta de creación de la cita
        # isoformat() devuelve formato: 2024-12-25T10:30:45.123456
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        
        # Paso 1: Crear un diccionario con todos los atributos
        # Paso 2: Para los Enums (specialty, appointment_type), usar .value
        #         para obtener el texto en lugar del nombre del enum
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            # Verificar si specialty es un Enum y extraer su valor
            'specialty': self.specialty.value if isinstance(self.specialty, EspecialidadMedica) else self.specialty,
            # Verificar si appointment_type es un Enum y extraer su valor
            'appointment_type': self.appointment_type.value if isinstance(self.appointment_type, TipoCita) else self.appointment_type,
            'date': self.date,
            'time': self.time,
            'notes': self.notes,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        
        # Paso 1: Crear una nueva cita con los datos básicos
        # Nota: Necesitamos convertir los strings de specialty y appointment_type
        #       de vuelta a sus correspondientes Enums
        cita = cls(
            patient_id=data['patient_id'],
            # Convertir el string al Enum de EspecialidadMedica
            specialty=EspecialidadMedica(data['specialty']),
            # Convertir el string al Enum de TipoCita
            appointment_type=TipoCita(data['appointment_type']),
            date=data['date'],
            time=data['time'],
            notes=data.get('notes', ''),  # get() para evitar error si no existe
            priority=data.get('priority', 3)  # get() con valor por defecto
        )
        
        # Paso 2: Restaurar atributos adicionales si existen
        # Estos atributos no se pasan al constructor, pero los necesitamos
        cita.id = data.get('id', cita.id)  # Mantener el ID original si existe
        cita.status = data.get('status', 'Programada')  # Restaurar el estado
        cita.created_at = data.get('created_at', cita.created_at)  # Fecha de creación
        
        # Paso 3: Retornar la cita completamente reconstruida
        return cita
    
    def cambiar_estado(self, nuevo_estado):
        
        # Paso 1: Definir los estados válidos
        estados_validos = ["Programada", "En Progreso", "Completada", "Cancelada"]
        
        # Paso 2: Verificar si el nuevo estado es válido
        if nuevo_estado in estados_validos:
            # Si es válido, actualizar el estado
            self.status = nuevo_estado
            return True
        else:
            # Si no es válido, no cambiar nada y retornar False
            return False
    
    def __str__(self):
        
        # Construir una cadena de texto legible con los detalles principales
        return f"Cita {self.id} - {self.specialty.value} - {self.date} {self.time}"
    
    def obtener_duracion_estimada(self):
        
        # Diccionario con duraciones estimadas por especialidad
        duraciones = {
            EspecialidadMedica.MEDICINA_GENERAL: 30,
            EspecialidadMedica.DERMATOLOGIA: 45,
            EspecialidadMedica.UROLOGIA: 40,
            EspecialidadMedica.CARDIOLOGIA: 50,
            EspecialidadMedica.PEDIATRIA: 35,
            EspecialidadMedica.GINECOLOGIA: 45,
            EspecialidadMedica.TRAUMATOLOGIA: 45,
            EspecialidadMedica.OFTALMOLOGIA: 40,
            EspecialidadMedica.OTORRINOLARINGOLOGIA: 35,
            EspecialidadMedica.NEUROLOGIA: 50
        }
        
        # Retornar la duración estimada, o 30 minutos por defecto
        return duraciones.get(self.specialty, 30)
