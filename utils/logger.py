import logging
import os
from datetime import datetime

def setup_logger(name='patient_management_system', log_dir='logs'):
    
    # Paso 1: Creamos el directorio de logs si no existe
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Crea la carpeta y cualquier carpeta padre necesaria
    
    # Paso 2: Obtenemos el logger con el nombre proporcionado
    logger = logging.getLogger(name)
    
    # Paso 3: Establecemos el nivel de logging (DEBUG = capturamos todos los mensajes)
    logger.setLevel(logging.DEBUG)
    
    # Paso 4: Evitamos duplicar handlers si el logger ya está configurado
    if logger.handlers:
        return logger  # Si ya hay handlers, devolvemos el logger sin modificar
    
    # Paso 5: Definimos el formato para los mensajes de log
    # Incluye: fecha y hora, nombre del logger, nivel de gravedad, mensaje
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Paso 6: Configuramos el handler para escribir en un archivo
    # El nombre del archivo incluye la fecha actual para organizar los logs
    log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')  # Usamos UTF-8 para tildes
    file_handler.setLevel(logging.DEBUG)  # Guardamos todos los mensajes en el archivo
    file_handler.setFormatter(formatter)  # Aplicamos el formato definido
    
    # Paso 7: Configuramos el handler para mostrar mensajes en la consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Mostramos solo mensajes importantes en consola
    console_handler.setFormatter(formatter)  # Aplicamos el mismo formato
    
    # Paso 8: Añadimos ambos handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Paso 9: Devolvemos el logger configurado
    return logger

# Logger global preconfigurado para usar en toda la aplicación
# Basta con importar 'logger' desde utils.logger para empezar a usarlo
logger = setup_logger()
