from enum import Enum

class EspecialidadMedica(Enum):

    # MEDICINA GENERAL: Para consultas generales y chequeos de rutina
    MEDICINA_GENERAL = "Medicina General"
    
    # DERMATOLOGÍA: Especialidad en piel, uñas y cabello
    DERMATOLOGIA = "Dermatología"
    
    # UROLOGÍA: Especialidad en sistema urinario y reproductivo masculino
    UROLOGIA = "Urología"
    
    # CARDIOLOGÍA: Especialidad en enfermedades del corazón y sistema circulatorio
    CARDIOLOGIA = "Cardiología"
    
    # PEDIATRÍA: Especialidad en medicina infantil (0-18 años)
    PEDIATRIA = "Pediatría"
    
    # GINECOLOGÍA: Especialidad en salud de la mujer y sistemas reproductivos
    GINECOLOGIA = "Ginecología"
    
    # TRAUMATOLOGÍA: Especialidad en huesos, articulaciones y lesiones traumáticas
    TRAUMATOLOGIA = "Traumatología"
    
    # OFTALMOLOGÍA: Especialidad en enfermedades de los ojos
    OFTALMOLOGIA = "Oftalmología"
    
    # OTORRINOLARINGOLOGÍA: Especialidad en oído, nariz y garganta
    OTORRINOLARINGOLOGIA = "Otorrinolaringología"
    
    # NEUROLOGÍA: Especialidad en sistema nervioso
    NEUROLOGIA = "Neurología"

class TipoCita(Enum):

    # EMERGENCIA: Atención inmediata, sin cita previa (vida en riesgo)
    EMERGENCIA = "Emergencia"
    
    # CONSULTA_GENERAL: Cita programada para consulta médica general
    CONSULTA_GENERAL = "Consulta General"
    
    # SEGUIMIENTO: Cita de seguimiento después de tratamiento o cirugía
    SEGUIMIENTO = "Seguimiento"
    
    # CIRUGIA_PROGRAMADA: Cita para cirugía planificada previamente
    CIRUGIA_PROGRAMADA = "Cirugía Programada"
    
    # CHEQUEO_PREVENTIVO: Cita de revisión preventiva (chequeo anual)
    CHEQUEO_PREVENTIVO = "Chequeo Preventivo"
    
    # CONSULTA_ESPECIALIZADA: Cita con especialista en algún área específica
    CONSULTA_ESPECIALIZADA = "Consulta Especializada"
    
    # DIAGNOSTICO: Cita para realizar diagnóstico de una enfermedad
    DIAGNOSTICO = "Diagnóstico"
    
    # LABORATORIO: Cita para toma de muestras o exámenes de laboratorio
    LABORATORIO = "Laboratorio"
