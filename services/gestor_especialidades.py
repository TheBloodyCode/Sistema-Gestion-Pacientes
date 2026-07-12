from models.especialidad import EspecialidadMedica, TipoCita
from models.cita_medica import CitaMedica
from datetime import datetime
import csv
import os
from utils.logger import logger

class GestorEspecialidades:

    def __init__(self, archivo_citas="citas.csv"):
        
        try:
            # Paso 1: Guardar el nombre del archivo de citas
            self.archivo_citas = archivo_citas
            
            # Paso 2: Construir la ruta completa del archivo (dentro de carpeta 'data')
            self.ruta_citas = os.path.join('data', archivo_citas)
            
            # Paso 3: Inicializar lista de citas programadas
            self.citas = []
            
            # Paso 4: Definir el horario de atención por especialidad
            # Cada especialidad tiene horarios específicos y duración de consulta
            self.horarios_especialidades = {
                EspecialidadMedica.MEDICINA_GENERAL: {
                    'horas': ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', 
                             '11:00', '11:30', '12:00', '14:00', '14:30', '15:00', 
                             '15:30', '16:00', '16:30', '17:00'],
                    'duracion_minutos': 30  # Cada consulta dura 30 minutos
                },
                EspecialidadMedica.DERMATOLOGIA: {
                    'horas': ['09:00', '09:45', '10:30', '11:15', '12:00', 
                             '14:00', '14:45', '15:30', '16:15', '17:00'],
                    'duracion_minutos': 45  # Dermatología requiere más tiempo
                },
                EspecialidadMedica.UROLOGIA: {
                    'horas': ['08:30', '09:10', '09:50', '10:30', '11:10', '11:50',
                             '14:30', '15:10', '15:50', '16:30', '17:10'],
                    'duracion_minutos': 40
                },
                EspecialidadMedica.CARDIOLOGIA: {
                    'horas': ['08:00', '09:00', '10:00', '11:00', '12:00',
                             '14:00', '15:00', '16:00', '17:00'],
                    'duracion_minutos': 50  # Cardiología requiere evaluación completa
                },
                EspecialidadMedica.PEDIATRIA: {
                    'horas': ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
                             '11:00', '11:30', '14:00', '14:30', '15:00', '15:30',
                             '16:00', '16:30', '17:00'],
                    'duracion_minutos': 35
                },
                EspecialidadMedica.GINECOLOGIA: {
                    'horas': ['09:00', '09:45', '10:30', '11:15', '12:00',
                             '14:00', '14:45', '15:30', '16:15'],
                    'duracion_minutos': 45
                },
                EspecialidadMedica.TRAUMATOLOGIA: {
                    'horas': ['08:00', '08:45', '09:30', '10:15', '11:00', '11:45',
                             '14:00', '14:45', '15:30', '16:15', '17:00'],
                    'duracion_minutos': 45
                },
                EspecialidadMedica.OFTALMOLOGIA: {
                    'horas': ['08:30', '09:10', '09:50', '10:30', '11:10', '11:50',
                             '14:30', '15:10', '15:50', '16:30'],
                    'duracion_minutos': 40
                },
                EspecialidadMedica.OTORRINOLARINGOLOGIA: {
                    'horas': ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
                             '11:00', '11:30', '14:00', '14:30', '15:00', '15:30',
                             '16:00', '16:30', '17:00'],
                    'duracion_minutos': 35
                },
                EspecialidadMedica.NEUROLOGIA: {
                    'horas': ['08:00', '09:00', '10:00', '11:00', '12:00',
                             '14:00', '15:00', '16:00', '17:00'],
                    'duracion_minutos': 50
                }
            }
            
            # Paso 5: Cargar las citas existentes desde el archivo CSV
            self.cargar_citas()
            
            # Paso 6: Registrar inicialización exitosa en logs
            logger.info("GestorEspecialidades inicializado correctamente")
            
        except Exception as e:
            # Si ocurre un error, lo registramos
            logger.error(f"Error al inicializar GestorEspecialidades: {e}")
            raise
    
    def cargar_citas(self):
        
        try:
            # Paso 1: Verificar si el archivo existe
            if os.path.exists(self.ruta_citas):
                # Paso 2: Abrir el archivo CSV para lectura
                with open(self.ruta_citas, 'r', encoding='utf-8') as archivo:
                    # Paso 3: Crear un lector de diccionarios
                    lector = csv.DictReader(archivo)
                    
                    # Paso 4: Recorrer cada fila del CSV
                    for fila in lector:
                        try:
                            # Paso 5: Convertir la fila a un objeto CitaMedica
                            cita = CitaMedica.from_dict(fila)
                            # Paso 6: Añadir la cita a la lista
                            self.citas.append(cita)
                        except Exception as e:
                            # Si hay error al cargar una cita, lo registramos y continuamos
                            logger.warning(f"Error al cargar cita: {e}")
                
                # Paso 7: Registrar cuántas citas se cargaron
                logger.info(f"Cargadas {len(self.citas)} citas del archivo CSV")
        except Exception as e:
            # Si ocurre error general, lo registramos
            logger.error(f"Error al cargar citas: {e}")
    
    def guardar_citas(self):
        
        try:
            # Paso 1: Crear el directorio 'data' si no existe
            os.makedirs(os.path.dirname(self.ruta_citas), exist_ok=True)
            
            # Paso 2: Abrir el archivo para escritura
            with open(self.ruta_citas, 'w', newline='', encoding='utf-8') as archivo:
                # Paso 3: Si hay citas, escribir el encabezado
                if self.citas:
                    # Paso 4: Obtener las claves del primer diccionario
                    campos = self.citas[0].to_dict().keys()
                    # Paso 5: Crear el escritor de CSV
                    escritor = csv.DictWriter(archivo, fieldnames=campos)
                    # Paso 6: Escribir el encabezado
                    escritor.writeheader()
                    # Paso 7: Escribir cada cita como una fila
                    for cita in self.citas:
                        escritor.writerow(cita.to_dict())
            
            # Paso 8: Registrar que se guardó exitosamente
            logger.info(f"Guardadas {len(self.citas)} citas en CSV")
            
        except Exception as e:
            # Si ocurre error, lo registramos
            logger.error(f"Error al guardar citas: {e}")
    
    def programar_cita(self, patient_id, especialidad, tipo_cita,
                       fecha, hora, notas="", prioridad=3):
        
        try:
            # Paso 1: Verificar que el horario esté disponible
            if not self.verificar_disponibilidad(especialidad, fecha, hora):
                return None, " Horario no disponible para esta especialidad"
            
            # Paso 2: Verificar citas anteriores para reprogramar
            # Si el paciente ya tiene una cita para esta MISMA especialidad que no esté cancelada,
            # la cancelamos automáticamente para que esta nueva cita cuente como una "reprogramación".
            citas_previas = self.obtener_citas_paciente(patient_id)
            reprogramada = False
            for cita_previa in citas_previas:
                if cita_previa.specialty == especialidad and cita_previa.status != "Cancelada":
                    cita_previa.status = "Cancelada"
                    reprogramada = True
                    logger.info(f"Cita anterior {cita_previa.id} cancelada automáticamente (Reprogramación)")
            
            # Paso 3: Crear el objeto CitaMedica
            cita = CitaMedica(
                patient_id=patient_id,
                specialty=especialidad,
                appointment_type=tipo_cita,
                date=fecha,
                time=hora,
                notes=notas,
                priority=prioridad
            )
            
            # Paso 4: Añadir la cita a la lista
            self.citas.append(cita)
            
            # Paso 5: Guardar las citas en el archivo CSV
            self.guardar_citas()
            
            # Paso 6: Registrar en logs
            logger.info(f"Cita programada: {cita.id} para paciente {patient_id}")
            
            # Paso 7: Retornar la cita y un mensaje de éxito
            mensaje = " Cita reprogramada exitosamente" if reprogramada else " Cita programada exitosamente"
            return cita, mensaje
            
        except Exception as e:
            # Si ocurre error, lo registramos
            logger.error(f"Error al programar cita: {e}")
            return None, f" Error al programar cita"
    
    def verificar_disponibilidad(self, especialidad, fecha, hora):
        
        try:
            # Paso 1: Obtener el horario de la especialidad
            horario = self.horarios_especialidades.get(especialidad)
            if not horario:
                # Si no hay horario definido, no está disponible
                return False
            
            # Paso 2: Verificar que la hora esté en el horario de la especialidad
            if hora not in horario['horas']:
                # La hora no está en el horario permitido
                return False
            
            # Paso 3: Verificar que no haya conflicto con otra cita
            for cita in self.citas:
                # Buscar citas de la misma especialidad, fecha y hora
                # Que NO estén canceladas
                if (cita.specialty == especialidad and
                    cita.date == fecha and
                    cita.time == hora and
                    cita.status != "Cancelada"):
                    # Ya existe una cita en este horario
                    return False
            
            # Paso 4: Si llegamos aquí, el horario está disponible
            return True
            
        except Exception as e:
            # Si ocurre error, lo registramos y retornamos False
            logger.error(f"Error al verificar disponibilidad: {e}")
            return False
    
    def obtener_horarios_disponibles(self, especialidad, fecha):
        
        try:
            # Paso 1: Obtener el horario de la especialidad
            horario = self.horarios_especialidades.get(especialidad, {})
            
            # Paso 2: Crear lista de horarios disponibles
            horarios_disponibles = []
            
            # Paso 3: Recorrer cada hora del horario de la especialidad
            for hora in horario.get('horas', []):
                # Paso 4: Verificar si la hora está disponible
                if self.verificar_disponibilidad(especialidad, fecha, hora):
                    # Si está disponible, añadirla a la lista
                    horarios_disponibles.append(hora)
            
            # Paso 5: Retornar lista de horarios disponibles
            return horarios_disponibles
            
        except Exception as e:
            # Si ocurre error, lo registramos
            logger.error(f"Error al obtener horarios disponibles: {e}")
            return []
    
    def obtener_citas_paciente(self, patient_id):
        
        try:
            # Paso 1: Filtrar citas que pertenezcan al paciente
            return [cita for cita in self.citas if cita.patient_id == patient_id]
        except Exception as e:
            # Si ocurre error, lo registramos
            logger.error(f"Error al obtener citas del paciente {patient_id}: {e}")
            return []
    
    def cancelar_cita(self, cita_id):
        
        try:
            # Paso 1: Buscar la cita con el ID proporcionado
            for cita in self.citas:
                if cita.id == cita_id:
                    # Paso 2: Cambiar el estado a "Cancelada"
                    cita.status = "Cancelada"
                    # Paso 3: Guardar los cambios
                    self.guardar_citas()
                    # Paso 4: Registrar en logs
                    logger.info(f"Cita {cita_id} cancelada")
                    # Paso 5: Retornar True indicando éxito
                    return True
            
            # Si no se encontró, retornar False
            return False
            
        except Exception as e:
            # Si ocurre error, lo registramos
            logger.error(f"Error al cancelar cita {cita_id}: {e}")
            return False
    
    def obtener_citas_especialidad(self, especialidad):
        
        try:
            # Paso 1: Filtrar citas que sean de la especialidad y NO estén canceladas
            return [cita for cita in self.citas 
                    if cita.specialty == especialidad and cita.status != "Cancelada"]
        except Exception as e:
            # Si ocurre error, lo registramos
            logger.error(f"Error al obtener citas de especialidad: {e}")
            return []
