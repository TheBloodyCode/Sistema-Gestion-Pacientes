import csv
import os
import ast
from .logger import logger

class ManejadorCSV:

    def __init__(self, filename):
        
        # Guardamos el nombre del archivo
        self.filename = filename
        # Construimos la ruta completa del archivo (dentro de la carpeta 'data')
        self.filepath = os.path.join('data', filename)
        # Aseguramos que exista la carpeta 'data'
        self.ensure_data_directory_exists()
        # Registramos en los logs que se ha inicializado el manejador
        logger.info(f"ManejadorCSV inicializado para archivo: {self.filepath}")

    def ensure_data_directory_exists(self):
        
        try:
            # Definimos el nombre de la carpeta
            data_dir = 'data'
            # Verificamos si la carpeta NO existe
            if not os.path.exists(data_dir):
                # Si no existe, la creamos (y todas las carpetas padre necesarias)
                os.makedirs(data_dir)
                logger.info(f"Directorio 'data' creado exitosamente")
        except Exception as e:
            # Si ocurre un error al crear la carpeta, lo registramos y relanzamos la excepción
            logger.error(f"Error al crear directorio 'data': {e}")
            raise

    def read_data(self):
        
        # Inicializamos una lista vacía para guardar los datos
        data = []
        
        # Verificamos si el archivo NO existe
        if not os.path.exists(self.filepath):
            logger.warning(f"Archivo {self.filepath} no encontrado, retornando lista vacía")
            return data  # Devolvemos lista vacía si no hay archivo
        
        try:
            # Abrimos el archivo en modo lectura
            with open(self.filepath, mode='r', newline='', encoding='utf-8') as file:
                # Creamos un lector de CSV que convierte cada fila a un diccionario
                reader = csv.DictReader(file)
                # Recorremos todas las filas del archivo
                for row in reader:
                    # Convertimos el historial médico de cadena a lista (si existe y no está vacío)
                    if 'medical_history' in row and row['medical_history']:
                        try:
                            # Usamos ast.literal_eval() en lugar de eval() por seguridad
                            row['medical_history'] = ast.literal_eval(row['medical_history'])
                        except (ValueError, SyntaxError):
                            # Si hay un error al convertir, inicializamos el historial como vacío
                            row['medical_history'] = []
                            logger.warning(f"Historial médico inválido en fila, estableciendo como lista vacía: {row}")
                    else:
                        # Si no hay historial o está vacío, inicializamos como lista vacía
                        row['medical_history'] = []
                    
                    if 'sintomas_actuales' in row and row['sintomas_actuales']:
                        try:
                            row['sintomas_actuales'] = ast.literal_eval(row['sintomas_actuales'])
                        except (ValueError, SyntaxError):
                            row['sintomas_actuales'] = []
                    elif 'sintomas_actuales' not in row:
                        row['sintomas_actuales'] = []

                    # Añadimos la fila (paciente) a la lista de datos
                    data.append(row)
            # Registramos en los logs cuántos registros leímos
            logger.info(f"Leídos {len(data)} registros desde {self.filepath}")
            return data
        except Exception as e:
            # Si ocurre un error durante la lectura, lo registramos y devolvemos lista vacía
            logger.error(f"Error al leer datos desde {self.filepath}: {e}")
            return []

    def write_data(self, data):
        
        try:
            # Verificamos si la lista de datos está vacía
            if not data:
                # Si no hay datos, creamos un archivo con solo los encabezados
                headers = ["id", "name", "age", "gender", "medical_history"]
                with open(self.filepath, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=headers)
                    writer.writeheader()
                logger.info(f"Archivo {self.filepath} creado con encabezados (sin datos)")
                return
            
            # Si hay datos:
            # Paso 1: Obtenemos los encabezados del primer diccionario de la lista
            headers = list(data[0].keys())
            # Paso 2: Abrimos el archivo en modo escritura
            with open(self.filepath, mode='w', newline='', encoding='utf-8') as file:
                # Creamos un escritor de CSV
                writer = csv.DictWriter(file, fieldnames=headers)
                # Escribimos la fila de encabezados
                writer.writeheader()
                # Recorremos cada paciente en la lista de datos
                for row in data:
                    # Hacemos una copia del diccionario para no modificar el original
                    row_copy = row.copy()
                    # Convertimos el historial médico de lista a cadena (si existe)
                    if 'medical_history' in row_copy:
                        row_copy['medical_history'] = str(row_copy['medical_history'])
                    if 'sintomas_actuales' in row_copy:
                        row_copy['sintomas_actuales'] = str(row_copy['sintomas_actuales'])
                    # Escribimos la fila en el archivo
                    writer.writerow(row_copy)
            # Registramos en los logs cuántos registros guardamos
            logger.info(f"Escritos {len(data)} registros en {self.filepath}")
        except Exception as e:
            # Si ocurre un error durante la escritura, lo registramos y relanzamos la excepción
            logger.error(f"Error al escribir datos en {self.filepath}: {e}")
            raise

    def append_data(self, row):
        
        try:
            file_exists = os.path.exists(self.filepath)
            # Aseguramos el orden exacto de las columnas usando las claves del dict
            headers = list(row.keys())
            
            with open(self.filepath, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
                
                if not file_exists or os.path.getsize(self.filepath) == 0:
                    writer.writeheader()
                
                row_copy = row.copy()
                if 'medical_history' in row_copy:
                    row_copy['medical_history'] = str(row_copy['medical_history'])
                if 'sintomas_actuales' in row_copy:
                    row_copy['sintomas_actuales'] = str(row_copy['sintomas_actuales'])
                
                writer.writerow(row_copy)
            logger.info(f"Registro añadido a {self.filepath}")
        except Exception as e:
            logger.error(f"Error al añadir registro a {self.filepath}: {e}")
            raise
