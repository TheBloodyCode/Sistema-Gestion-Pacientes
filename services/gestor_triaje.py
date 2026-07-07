from data_structures.cola_prioridad import ColaProioridad
from utils.logger import logger

class GestorTriaje:

    def __init__(self):
        
        try:
            # Inicializamos la cola de prioridad para pacientes en emergencias
            self.cola_emergencias = ColaProioridad()
            
            # Diccionario que describe cada nivel de triaje
            # Cada nivel tiene una descripción clara de qué significa y el tiempo máximo de espera
            self.criterios_triaje = {
                5: " Emergencia Vital - Atención Inmediata (Riesgo de muerte)",
                4: " Urgencia Mayor - Atención en 15 minutos",
                3: " Urgencia Menor - Atención en 30 minutos",
                2: " Consulta Prioritaria - Atención en 1 hora",
                1: " Consulta Normal - Atención según orden"
            }
            
            # Registramos en logs que el gestor se inicializó correctamente
            logger.info("GestorTriaje inicializado correctamente")
        except Exception as e:
            # Si ocurre un error, lo registramos
            logger.error(f"Error al inicializar GestorTriaje: {e}")
            raise
    
    def evaluar_urgencia(self, paciente, sintomas, signos_vitales=None):
        
        try:
            # Paso 1: Inicializar prioridad por defecto en el nivel más bajo
            prioridad = 1
            
            # Paso 2: Definir palabras clave que indican emergencias
            # Estas son palabras que si aparecen en los síntomas, indica un nivel alto de urgencia
            palabras_clave_emergencia = [
                'dolor torácico',      # Indicador de problemas cardíacos
                'hemorragia',          # Pérdida de sangre importante
                'dificultad respiratoria',  # No puede respirar adecuadamente
                'pérdida de conciencia',    # Desvanecimiento o desmayo
                'trauma',              # Accidente o lesión importante
                'quemadura',           # Lesión por fuego
                'convulsión',          # Crisis neurológica
                'ataque',              # Ataque cardíaco o similar
                'alergia severa',      # Reacción alérgica grave
                'intoxicación',        # Envenenamiento
                'ahogo',               # Asfixia
                'hemorragia interna',  # Sangrado interno
                'crisis diabética',    # Hipoglucemia o hiperglucemia grave
                'infarto',             # Infarto de miocardio
                'accidente cerebrovascular',  # Derrame cerebral
            ]
            
            # Paso 3: Recorrer cada síntoma proporcionado
            for sintoma in sintomas:
                # Para cada síntoma, verificar si contiene alguna palabra clave de emergencia
                # Convertir a minúsculas para hacer la búsqueda insensible a mayúsculas
                for palabra_clave in palabras_clave_emergencia:
                    if palabra_clave in sintoma.lower():
                        # Si encontramos una palabra clave, la prioridad es máxima (5)
                        prioridad = max(prioridad, 5)
                        break  # No necesitamos buscar más palabras clave en este síntoma
            
            # Paso 4: Analizar signos vitales si se proporcionan
            if signos_vitales:
                # Verificar presión arterial sistólica crítica (riesgo de accidente cerebrovascular)
                if signos_vitales.get('presion_sistolica', 0) > 180:
                    # Presión muy alta: prioridad 4
                    prioridad = max(prioridad, 4)
                
                # Verificar frecuencia cardíaca crítica (taquicardia peligrosa)
                if signos_vitales.get('frecuencia_cardiaca', 0) > 140:
                    # Frecuencia cardíaca muy alta: prioridad 4
                    prioridad = max(prioridad, 4)
                
                # Verificar fiebre muy alta (puede indicar infección grave)
                if signos_vitales.get('temperatura', 0) > 39.5:
                    # Fiebre muy alta: prioridad 3
                    prioridad = max(prioridad, 3)
                
                # Verificar presión arterial muy baja (shock)
                if signos_vitales.get('presion_sistolica', 0) < 90:
                    # Presión muy baja: prioridad 5 (riesgo de choque)
                    prioridad = max(prioridad, 5)
                
                # Verificar frecuencia cardíaca muy baja (bradicardia peligrosa)
                if signos_vitales.get('frecuencia_cardiaca', 0) < 40:
                    # Frecuencia muy baja: prioridad 4
                    prioridad = max(prioridad, 4)
            
            # Paso 5: Considerar factores de riesgo por edad
            if hasattr(paciente, 'age'):
                # Adultos mayores (>65 años) tienen mayor riesgo
                if paciente.age > 65:
                    prioridad = max(prioridad, 2)
                
                # Bebés (<2 años) son muy vulnerables
                if paciente.age < 2:
                    prioridad = max(prioridad, 3)
            
            # Paso 6: Asegurar que la prioridad no exceda el máximo
            prioridad = min(prioridad, 5)
            
            # Paso 7: Registrar la evaluación en logs
            logger.info(f"Triaje de {paciente.name} (ID: {paciente.id}) - Prioridad: {prioridad}")
            
            # Paso 8: Retornar la prioridad calculada
            return prioridad
            
        except Exception as e:
            # Si ocurre un error durante la evaluación, lo registramos
            logger.error(f"Error al evaluar urgencia de {paciente.name}: {e}")
            # Retornar prioridad por defecto en caso de error
            return 3
    
    def añadir_emergencia(self, paciente, prioridad, razon):
        
        try:
            # Paso 1: Añadir el paciente a la cola de emergencias
            self.cola_emergencias.encolar(paciente, prioridad)
            
            # Paso 2: Almacenar información adicional en el paciente
            # Esto permite saber después cuál fue la razón de la emergencia
            paciente.emergency_reason = razon
            paciente.emergency_priority = prioridad
            
            # Paso 3: Registrar en logs
            logger.warning(f"EMERGENCIA: {paciente.name} (ID: {paciente.id}) - Prioridad {prioridad}: {razon}")
            
            # Paso 4: Crear y retornar mensaje de confirmación
            mensaje = f" Paciente {paciente.name} añadido a emergencias con prioridad {prioridad}"
            return mensaje
            
        except Exception as e:
            # Si ocurre un error, lo registramos
            logger.error(f"Error al añadir emergencia para {paciente.name}: {e}")
            return f" Error al registrar emergencia"
    
    def obtener_siguiente_emergencia(self):
        
        try:
            # Paso 1: Desencolar el paciente con mayor prioridad
            paciente = self.cola_emergencias.desencolar()
            
            # Paso 2: Si hay paciente, registrar que se está atendiendo
            if paciente:
                logger.info(f"Atendiendo emergencia: {paciente.name}")
            
            # Paso 3: Retornar el paciente (puede ser None si cola está vacía)
            return paciente
            
        except Exception as e:
            # Si ocurre un error, lo registramos
            logger.error(f"Error al obtener siguiente emergencia: {e}")
            return None
    
    def obtener_lista_emergencias(self):
        
        try:
            # Paso 1: Obtener todos los pacientes de la cola
            return self.cola_emergencias.obtener_todos()
        except Exception as e:
            # Si ocurre un error, lo registramos
            logger.error(f"Error al obtener lista de emergencias: {e}")
            return []
    
    def obtener_descripcion_triaje(self, prioridad):
        
        # Paso 1: Buscar la prioridad en el diccionario de criterios
        # Si no existe, retornar "Prioridad no definida"
        return self.criterios_triaje.get(prioridad, " Prioridad no definida")
    
    def contar_emergencias(self):
        
        try:
            return self.cola_emergencias.tamaño()
        except Exception as e:
            logger.error(f"Error al contar emergencias: {e}")
            return 0
    
    def limpiar_cola_emergencias(self):
        
        try:
            self.cola_emergencias.limpiar()
            logger.info("Cola de emergencias limpiada")
        except Exception as e:
            logger.error(f"Error al limpiar cola de emergencias: {e}")
