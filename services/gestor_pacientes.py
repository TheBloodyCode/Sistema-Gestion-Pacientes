from models.paciente import Paciente
from data_structures.lista_enlazada import ListaEnlazada
from data_structures.pila import Pila
from data_structures.cola import Cola
from utils.manejador_csv import ManejadorCSV
from utils.logger import logger
# Importamos las nuevas clases para emergencias y especialidades
from services.gestor_triaje import GestorTriaje
from services.gestor_especialidades import GestorEspecialidades
from models.especialidad import EspecialidadMedica, TipoCita

class GestorPacientes:

    def __init__(self, patients_filename="patients.csv", history_filename="history.csv"):
        
        try:
            # Inicializamos la lista enlazada para almacenar los pacientes activos
            self.patient_list = ListaEnlazada()
            # Inicializamos la cola para gestionar la sala de espera (consulta general)
            self.waiting_queue = Cola()
            # Inicializamos la pila (se podría usar para historial de consultas, en esta versión no se usa)
            self.medical_history_stack = Pila()
            # Inicializamos el manejador de CSV con el nombre de archivo proporcionado
            self.csv_handler = ManejadorCSV(patients_filename)
            
            # ======== NUEVAS INICIALIZACIONES PARA EMERGENCIAS Y ESPECIALIDADES ========
            
            # Inicializamos el Gestor de Triaje para manejar emergencias
            # Este gestor mantendrá una cola de prioridad de pacientes en emergencias
            self.gestor_triaje = GestorTriaje()
            
            # Inicializamos el Gestor de Especialidades para manejar citas programadas
            # Este gestor gestiona la programación de citas con diferentes especialidades
            self.gestor_especialidades = GestorEspecialidades()
            
            # Diccionario de salas de espera por especialidad
            # Cada especialidad tiene su propia cola de espera
            self.salas_espera = {
                'general': Cola(),                           # Sala de espera general
                'dermatologia': Cola(),                      # Sala de espera dermatología
                'urologia': Cola(),                          # Sala de espera urología
                'cardiologia': Cola(),                       # Sala de espera cardiología
                'pediatria': Cola(),                         # Sala de espera pediatría
                'ginecologia': Cola(),                       # Sala de espera ginecología
                'traumatologia': Cola(),                     # Sala de espera traumatología
                'oftalmologia': Cola(),                      # Sala de espera oftalmología
                'otorrinolaringologia': Cola(),              # Sala de espera otorrinolaringología
                'neurologia': Cola()                         # Sala de espera neurología
            }
            
            # ======== FIN DE NUEVAS INICIALIZACIONES ========
            
            # Cargamos los pacientes desde el archivo CSV
            self.load_patients()
            # Registramos en los logs que se ha inicializado correctamente el gestor
            logger.info("GestorPacientes inicializado correctamente con triaje y especialidades")
        except Exception as e:
            # Si ocurre un error durante la inicialización, lo registramos y relanzamos la excepción
            logger.error(f"Error al inicializar GestorPacientes: {e}")
            raise

    def load_patients(self):
        
        try:
            # Leemos los datos del CSV usando el manejador
            patients_data = self.csv_handler.read_data()
            # Recorremos cada paciente en los datos leídos
            for p_data in patients_data:
                try:
                    # Convertimos el diccionario a un objeto Paciente usando el método de clase
                    patient = Paciente.from_dict(p_data)
                    # Añadimos el paciente a la lista enlazada
                    self.patient_list.append(patient)
                    # Si el paciente tiene historial médico, aquí podríamos cargarlo en una pila
                    # (en esta versión, el historial está dentro del propio paciente)
                    if patient.medical_history:
                        for record in patient.medical_history:
                            # Por ahora, no hacemos nada extra con el historial
                            pass
                except Exception as e:
                    # Si ocurre un error al cargar un paciente en particular, lo registramos y continuamos
                    logger.warning(f"Error al cargar paciente desde datos {p_data}: {e}")
            # Registramos en los logs cuántos pacientes se cargaron
            logger.info(f"Cargados {len(self.patient_list.to_list())} pacientes")
        except Exception as e:
            # Si ocurre un error general durante la carga, lo registramos
            logger.error(f"Error al cargar pacientes: {e}")

    def save_patients(self):
        
        try:
            # Convertimos la lista enlazada a una lista de Python
            patients_list = self.patient_list.to_list()
            # Convertimos cada objeto Paciente a un diccionario usando to_dict()
            patients_to_save = [p.to_dict() for p in patients_list]
            # Escribimos los diccionarios en el archivo CSV
            self.csv_handler.write_data(patients_to_save)
        except Exception as e:
            # Si ocurre un error al guardar, lo registramos
            logger.error(f"Error al guardar pacientes: {e}")

    def add_patient(self, patient_id, name, age, gender):
        
        try:
            # Primero verificamos si ya existe un paciente con ese ID
            existing_patient = self.patient_list.search(patient_id)
            if existing_patient:
                logger.warning(f"Intento de añadir paciente con ID duplicado: {patient_id}")
                return None
            
            # Paso 1: Creamos un nuevo paciente con los datos proporcionados
            patient = Paciente(patient_id, name, age, gender)
            # Paso 2: Añadimos el paciente a la lista enlazada de pacientes activos
            self.patient_list.append(patient)
            # Paso 3: Añadimos el paciente a la cola de sala de espera
            self.waiting_queue.enqueue(patient)
            # Paso 4: Guardamos los cambios en el archivo CSV
            self.csv_handler.append_data(patient.to_dict())
            # Paso 5: Registramos la acción en los logs
            logger.info(f"Paciente añadido: {patient.name} (Cédula: {patient.id})")
            # Paso 6: Devolvemos el paciente creado
            return patient
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos None
            logger.error(f"Error al añadir paciente: {e}")
            return None

    def get_patient(self, patient_id_or_name):
        
        try:
            # Buscamos el paciente en la lista enlazada
            patient = self.patient_list.search(patient_id_or_name)
            # Registramos en los logs si lo encontramos o no (nivel DEBUG para no saturar)
            if patient:
                logger.debug(f"Paciente encontrado: {patient_id_or_name}")
            else:
                logger.debug(f"Paciente no encontrado: {patient_id_or_name}")
            # Devolvemos el paciente (o None)
            return patient
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos None
            logger.error(f"Error al buscar paciente {patient_id_or_name}: {e}")
            return None

    def remove_patient(self, patient_id):
        
        try:
            # Primero buscamos el paciente para ver si existe
            patient = self.patient_list.search(patient_id)
            if patient:
                # Si existe, lo eliminamos de la lista enlazada
                self.patient_list.delete_node(patient_id)
                # Guardamos los cambios en el archivo CSV
                self.save_patients()
                # Registramos la acción en los logs
                logger.info(f"Paciente eliminado: {patient_id}")
                # Devolvemos True para indicar éxito
                return True
            # Si el paciente no existe, registramos una advertencia y devolvemos False
            logger.warning(f"Intentó eliminar paciente no encontrado: {patient_id}")
            return False
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos False
            logger.error(f"Error al eliminar paciente {patient_id}: {e}")
            return False

    def get_next_patient_in_queue(self):
        
        try:
            # Sacamos al siguiente paciente de la cola
            patient = self.waiting_queue.dequeue()
            if patient:
                # Si hay un paciente, registramos la acción
                logger.info(f"Atendiendo paciente: {patient.name} (ID: {patient.id})")
            else:
                # Si la cola está vacía, registramos un mensaje de debug
                logger.debug("Sala de espera vacía")
            # Devolvemos el paciente (o None)
            return patient
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos None
            logger.error(f"Error al obtener siguiente paciente: {e}")
            return None

    def add_medical_record(self, patient_id, record):
        
        try:
            # Buscamos el paciente por su ID
            patient = self.patient_list.search(patient_id)
            if patient:
                # Si el paciente existe, añadimos el registro a su historial
                patient.medical_history.append(record)
                # Guardamos los cambios en el archivo CSV
                self.save_patients()
                # Registramos la acción en los logs
                logger.info(f"Registro médico añadido a paciente {patient_id}")
                # Devolvemos True para indicar éxito
                return True
            # Si el paciente no existe, registramos una advertencia y devolvemos False
            logger.warning(f"Intentó añadir registro a paciente no encontrado: {patient_id}")
            return False
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos False
            logger.error(f"Error al añadir registro médico: {e}")
            return False

    def get_medical_history(self, patient_id):
        
        try:
            # Buscamos el paciente por su ID
            patient = self.patient_list.search(patient_id)
            if patient:
                # Si el paciente existe, registramos la acción y devolvemos el historial
                logger.debug(f"Obteniendo historial médico de paciente {patient_id}")
                return patient.medical_history
            # Si el paciente no existe, registramos una advertencia y devolvemos None
            logger.warning(f"Paciente no encontrado para historial: {patient_id}")
            return None
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos None
            logger.error(f"Error al obtener historial médico: {e}")
            return None

    def list_all_patients(self):
        
        try:
            # Convertimos la lista enlazada a una lista de Python
            patients = self.patient_list.to_list()
            # Registramos la acción en los logs (nivel DEBUG)
            logger.debug(f"Listando {len(patients)} pacientes")
            # Devolvemos la lista de pacientes
            return patients
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos una lista vacía
            logger.error(f"Error al listar pacientes: {e}")
            return []

    def sort_patients_by_age(self):
        
        try:
            # Convertimos la lista enlazada a una lista de Python
            patients = self.patient_list.to_list()
            # Ordenamos la lista usando la edad como clave
            patients.sort(key=lambda p: p.age)
            # Registramos la acción en los logs
            logger.debug("Ordenando pacientes por edad")
            # Devolvemos la lista ordenada
            return patients
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos una lista vacía
            logger.error(f"Error al ordenar pacientes por edad: {e}")
            return []

    def sort_patients_by_name(self):
        
        try:
            # Convertimos la lista enlazada a una lista de Python
            patients = self.patient_list.to_list()
            # Ordenamos la lista usando el nombre como clave
            patients.sort(key=lambda p: p.name)
            # Registramos la acción en los logs
            logger.debug("Ordenando pacientes por nombre")
            # Devolvemos la lista ordenada
            return patients
        except Exception as e:
            # Si ocurre un error, lo registramos y devolvemos una lista vacía
            logger.error(f"Error al ordenar pacientes por nombre: {e}")
            return []
    
    # ==================== NUEVAS FUNCIONES PARA EMERGENCIAS Y ESPECIALIDADES ====================
    
    def registrar_paciente_con_emergencia(self, name, age, gender, sintomas, signos_vitales=None):
        
        try:
            # Paso 1: Generar un ID único para el nuevo paciente
            # Usamos un contador basado en el número de pacientes + 1
            patient_id = f"EMRG_{len(self.patient_list.to_list()) + 1:05d}"
            
            # Paso 2: Crear el paciente
            paciente = Paciente(patient_id, name, age, gender)
            
            # Paso 3: Añadirlo a la lista enlazada
            self.patient_list.append(paciente)
            
            # Paso 4: Evaluar el nivel de urgencia
            prioridad = self.gestor_triaje.evaluar_urgencia(paciente, sintomas, signos_vitales)
            
            # Paso 5: Si es urgente (prioridad >= 3), añadirlo a emergencias
            if prioridad >= 3:
                razon = f"Síntomas: {', '.join(sintomas)}"
                self.gestor_triaje.añadir_emergencia(paciente, prioridad, razon)
            else:
                # Si no es urgente, añadirlo a la cola de espera general
                self.waiting_queue.enqueue(paciente)
            
            # Paso 6: Guardar cambios
            self.csv_handler.append_data(paciente.to_dict())
            
            # Paso 7: Obtener descripción del triaje
            descripcion = self.gestor_triaje.obtener_descripcion_triaje(prioridad)
            
            # Paso 8: Registrar en logs
            logger.info(f"Paciente de emergencia registrado: {paciente.name} - Prioridad {prioridad}")
            
            # Paso 9: Retornar el paciente, prioridad y descripción
            return paciente, prioridad, descripcion
            
        except Exception as e:
            logger.error(f"Error al registrar paciente de emergencia: {e}")
            return None, 1, "Error en el registro"
    
    def registrar_paciente_especialidad(self, name, age, gender, especialidad, sintomas):
        
        try:
            # Paso 1: Generar ID único
            patient_id = f"ESP_{len(self.patient_list.to_list()) + 1:05d}"
            
            # Paso 2: Crear paciente
            paciente = Paciente(patient_id, name, age, gender)
            
            # Paso 3: Almacenar la especialidad en el paciente
            paciente.especialidad = especialidad
            paciente.sintomas = sintomas
            
            # Paso 4: Añadir a lista de pacientes
            self.patient_list.append(paciente)
            
            # Paso 5: Añadir a la cola de espera de la especialidad
            clave_especialidad = especialidad.value.lower().replace(" ", "")
            if clave_especialidad in self.salas_espera:
                self.salas_espera[clave_especialidad].enqueue(paciente)
            
            # Paso 6: Guardar cambios
            self.csv_handler.append_data(paciente.to_dict())
            
            # Paso 7: Registrar en logs
            logger.info(f"Paciente registrado para {especialidad.value}: {paciente.name}")
            
            return paciente
            
        except Exception as e:
            logger.error(f"Error al registrar paciente por especialidad: {e}")
            return None
    
    def atender_siguiente_paciente(self, especialidad=None):
        
        try:
            # Paso 1: Verificar si hay emergencias
            if self.gestor_triaje.contar_emergencias() > 0:
                paciente = self.gestor_triaje.obtener_siguiente_emergencia()
                if paciente:
                    logger.info(f"Atendiendo emergencia: {paciente.name}")
                    return paciente
            
            # Paso 2: Si se especifica especialidad, atender de esa especialidad
            if especialidad:
                clave = especialidad.value.lower().replace(" ", "")
                if clave in self.salas_espera:
                    paciente = self.salas_espera[clave].dequeue()
                    if paciente:
                        logger.info(f"Atendiendo {especialidad.value}: {paciente.name}")
                        return paciente
            
            # Paso 3: Atender de la sala general
            paciente = self.waiting_queue.dequeue()
            if paciente:
                logger.info(f"Atendiendo consulta general: {paciente.name}")
                return paciente
            
            return None
            
        except Exception as e:
            logger.error(f"Error al atender siguiente paciente: {e}")
            return None
    
    def obtener_estado_salas_espera(self):
        
        try:
            estado = {
                'emergencias': self.gestor_triaje.contar_emergencias(),
                'general': self.waiting_queue.size(),
            }
            
            # Añadir el estado de cada especialidad
            for nombre_sala, cola in self.salas_espera.items():
                estado[nombre_sala] = cola.size()
            
            return estado
            
        except Exception as e:
            logger.error(f"Error al obtener estado de salas: {e}")
            return {}
    
    def programar_cita_especialista(self, patient_id, especialidad, tipo_cita, 
                                   fecha, hora, notas="", prioridad=3):
        
        try:
            # Paso 1: Verificar que el paciente existe
            paciente = self.patient_list.search(patient_id)
            if not paciente:
                return None, f" Paciente {patient_id} no encontrado"
            
            # Paso 2: Programar la cita usando el gestor de especialidades
            cita, mensaje = self.gestor_especialidades.programar_cita(
                patient_id, especialidad, tipo_cita, fecha, hora, notas, prioridad
            )
            
            logger.info(f"Cita programada para {paciente.name}: {mensaje}")
            return cita, mensaje
            
        except Exception as e:
            logger.error(f"Error al programar cita: {e}")
            return None, " Error al programar cita"
    
    def obtener_horarios_disponibles(self, especialidad, fecha):
        
        try:
            return self.gestor_especialidades.obtener_horarios_disponibles(especialidad, fecha)
        except Exception as e:
            logger.error(f"Error al obtener horarios disponibles: {e}")
            return []
    
    def obtener_citas_paciente(self, patient_id):
        
        try:
            return self.gestor_especialidades.obtener_citas_paciente(patient_id)
        except Exception as e:
            logger.error(f"Error al obtener citas del paciente: {e}")
            return []
    
    def cancelar_cita(self, cita_id):
        
        try:
            return self.gestor_especialidades.cancelar_cita(cita_id)
        except Exception as e:
            logger.error(f"Error al cancelar cita: {e}")
            return False
    
    def obtener_lista_emergencias(self):
        
        try:
            return self.gestor_triaje.obtener_lista_emergencias()
        except Exception as e:
            logger.error(f"Error al obtener lista de emergencias: {e}")
            return []
