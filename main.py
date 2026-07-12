

from services.gestor_pacientes import GestorPacientes
from models.especialidad import EspecialidadMedica, TipoCita
from utils.logger import logger

def mostrar_menu_principal():
    
    print("\n" + "="*60)
    print(" SISTEMA DE GESTIÓN DE PACIENTES ".center(60))
    print("="*60)
    
    print("\n REGISTRO DE PACIENTES:")
    print("  1.  Registrar nuevo paciente (consulta general)")
    print("  2.  Registrar paciente por especialidad")
    print("  3.  REGISTRAR EMERGENCIA (triaje urgente)")
    
    print("\n ATENCIÓN DE PACIENTES:")
    print("  4.  Atender siguiente paciente")
    print("  5.  Ver estado de TODAS las salas de espera")
    
    print("\n CITAS CON ESPECIALISTAS:")
    print("  6.  Agendar cita con especialista")
    print("  7.  Ver horarios disponibles de especialidad")
    print("  8.  Ver citas programadas de un paciente")
    print("  9.  Cancelar una cita médica")
    
    print("\n CONSULTAS Y BÚSQUEDA:")
    print("  10.  Ver todos los pacientes")
    print("  11.  Buscar paciente por CI o nombre")
    print("  12.  Ver lista de pacientes en emergencias")
    
    print("\n HISTORIAL MÉDICO:")
    print("  13.  Añadir registro médico a paciente")
    print("  14.  Ver historial médico de un paciente")
    
    print("\n GESTIÓN DEL SISTEMA:")
    print("  15.  Ordenar pacientes por edad")
    print("  16.  Ordenar pacientes por nombre")
    print("  17.  Ordenar pacientes por género")
    print("  18.  Ordenar pacientes por fecha")
    print("  19.  Ordenar pacientes por día")
    print("  20.  Ordenar pacientes por tipo de enfermedad")
    print("  21.  Eliminar paciente del sistema")
    
    print("\n  0.  Salir del sistema")
    print("="*60)

def obtener_edad_valida():
    
    while True:
        try:
            # Paso 1: Pedir la edad como texto
            edad_str = input(" Ingrese la edad del paciente (0-150): ").strip()
            
            # Paso 2: Convertir a entero
            edad = int(edad_str)
            
            # Paso 3: Validar rango razonable
            if 0 <= edad <= 150:
                return edad
            else:
                print(" Por favor, ingrese una edad entre 0 y 150 años.")
        except ValueError:
            # Si no es un número válido
            print(" Por favor, ingrese un número válido.")

def main():
    
    logger.info("Iniciando SISTEMA DE GESTIÓN DE PACIENTES v2.0")
    
    try:
        # Inicializar el gestor de pacientes (con triaje y especialidades)
        gestor = GestorPacientes()
        logger.info("GestorPacientes inicializado correctamente")
    except Exception as e:
        logger.critical(f"Error crítico al inicializar: {e}")
        print(" Error grave al iniciar el sistema. Por favor, revise los logs.")
        return
    
    # Bucle principal de la aplicación
    while True:
        try:
            # Mostrar menú
            mostrar_menu_principal()
            
            # Recibir opción
            opcion = input("\n Seleccione una opción (0-21): ").strip()
            
            # Procesar opción elegida
            if opcion == '1':
                print("\n" + "="*60)
                print(" REGISTRAR NUEVO PACIENTE - CONSULTA GENERAL")
                print("="*60)
                try:
                    cedula = input(" Número de cédula del paciente: ").strip()
                    if not cedula:
                        print(" La cédula no puede estar vacía.")
                        continue
                    
                    nombre = input(" Nombre(s) del paciente: ").strip()
                    if not nombre:
                        print(" El nombre no puede estar vacío.")
                        continue
                        
                    apellido = input(" Apellido(s) del paciente: ").strip()
                    if not apellido:
                        print(" Los apellidos no pueden estar vacíos.")
                        continue
                    
                    edad = obtener_edad_valida()
                    genero = input(" Género (M/F): ").strip().upper()
                    
                    paciente = gestor.add_patient(cedula, nombre, apellido, edad, genero)
                    
                    if paciente:
                        print("\n PACIENTE REGISTRADO EXITOSAMENTE!")
                        print("="*60)
                        print(paciente)
                        print("="*60)
                    else:
                        print(" Error: No se pudo registrar el paciente (posiblemente CI duplicada)")
                        
                except Exception as e:
                    logger.error(f"Error al registrar paciente general: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '2':
                print("\n" + "="*60)
                print(" REGISTRAR PACIENTE POR ESPECIALIDAD")
                print("="*60)
                try:
                    print("\n Especialidades disponibles:")
                    especialidades = list(EspecialidadMedica)
                    for i, esp in enumerate(especialidades, 1):
                        print(f"  {i}. {esp.value}")
                    
                    try:
                        opcion = int(input("\n Seleccione especialidad (número): ").strip())
                        if 1 <= opcion <= len(especialidades):
                            especialidad = especialidades[opcion - 1]
                        else:
                            print(" Opción inválida")
                            continue
                    except ValueError:
                        print(" Por favor ingrese un número válido")
                        continue
                    
                    cedula = input("\n Número de cédula del paciente: ").strip()
                    if not cedula:
                        print(" La cédula no puede estar vacía")
                        continue
                    
                    nombre = input(" Nombre(s) del paciente: ").strip()
                    if not nombre:
                        print(" El nombre no puede estar vacío")
                        continue
                        
                    apellido = input(" Apellido(s) del paciente: ").strip()
                    if not apellido:
                        print(" Los apellidos no pueden estar vacíos")
                        continue
                    
                    edad = obtener_edad_valida()
                    genero = input(" Género (M/F): ").strip().upper()
                    
                    print("\n Síntomas (ingrese uno por línea, enter vacío para terminar):")
                    sintomas = []
                    while True:
                        sintoma = input("  > ").strip()
                        if not sintoma:
                            break
                        sintomas.append(sintoma)
                    
                    paciente = gestor.registrar_paciente_especialidad(
                        cedula, nombre, apellido, edad, genero, especialidad, sintomas
                    )
                    
                    if paciente:
                        print(f"\n PACIENTE REGISTRADO EN {especialidad.value}")
                        print("="*60)
                        print(f"  CI: {paciente.id}")
                        print(f"  Nombre: {paciente.name}")
                        print(f"  Edad: {paciente.age}")
                        print(f"  Especialidad: {especialidad.value}")
                        print(f"  Síntomas: {', '.join(sintomas) if sintomas else 'No especificado'}")
                        print("="*60)
                    else:
                        print(" Error al registrar paciente")
                        
                except Exception as e:
                    logger.error(f"Error al registrar paciente por especialidad: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '3':
                print("\n" + "="*60)
                print(" REGISTRO DE EMERGENCIA MÉDICA ")
                print("="*60)
                try:
                    print("\n INFORMACIÓN DEL PACIENTE:")
                    cedula = input(" Número de cédula: ").strip()
                    if not cedula:
                        print(" La cédula es requerida")
                        continue
                    
                    nombre = input(" Nombre(s) del paciente: ").strip()
                    if not nombre:
                        print(" El nombre es requerido")
                        continue
                        
                    apellido = input(" Apellido(s) del paciente: ").strip()
                    if not apellido:
                        print(" Los apellidos son requeridos")
                        continue
                    
                    edad = obtener_edad_valida()
                    genero = input(" Género (M/F): ").strip().upper()
                    
                    print("\n SÍNTOMAS ACTUALES:")
                    print("   (Ingrese uno por línea, enter vacío para terminar)")
                    sintomas = []
                    while True:
                        sintoma = input("  > ").strip()
                        if not sintoma:
                            break
                        sintomas.append(sintoma)
                    
                    if not sintomas:
                        print(" Debe ingresar al menos un síntoma")
                        continue
                    
                    print("\n SIGNOS VITALES (opcional - presione ENTER para omitir):")
                    signos_vitales = {}
                    
                    temp = input("  Temperatura (°C): ").strip()
                    if temp:
                        try:
                            signos_vitales['temperatura'] = float(temp)
                        except ValueError:
                            print(" Temperatura no válida, omitida")
                    
                    presion = input("  Presión arterial sistólica (mmHg): ").strip()
                    if presion:
                        try:
                            signos_vitales['presion_sistolica'] = int(presion)
                        except ValueError:
                            print(" Presión no válida, omitida")
                    
                    fc = input("  Frecuencia cardíaca (lpm): ").strip()
                    if fc:
                        try:
                            signos_vitales['frecuencia_cardiaca'] = int(fc)
                        except ValueError:
                            print(" FC no válida, omitida")
                    
                    paciente, prioridad, descripcion = gestor.registrar_paciente_con_emergencia(
                        cedula, nombre, apellido, edad, genero, sintomas,
                        signos_vitales if signos_vitales else None
                    )
                    
                    if paciente:
                        print("\n" + "="*60)
                        print(" PACIENTE REGISTRADO EN EMERGENCIAS")
                        print("="*60)
                        print(f"\n CI: {paciente.id}")
                        print(f" Nombre: {paciente.name}")
                        print(f" Edad: {paciente.age} años")
                        print(f" Género: {paciente.gender}")
                        print(f"\n PRIORIDAD DE ATENCIÓN: {prioridad} de 5")
                        print(f" {descripcion}")
                        print(f"\n Síntomas reportados:")
                        for i, sintoma in enumerate(sintomas, 1):
                            print(f"  {i}. {sintoma}")
                        
                        if signos_vitales:
                            print(f"\n Signos vitales:")
                            for clave, valor in signos_vitales.items():
                                print(f"  - {clave}: {valor}")
                        
                        print("\n" + "="*60)
                    else:
                        print(" Error al registrar la emergencia")
                        
                except Exception as e:
                    logger.error(f"Error al registrar emergencia: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '4':
                print("\n" + "="*60)
                print(" ATENDER SIGUIENTE PACIENTE")
                print("="*60)
                try:
                    print("\n ESTADO ACTUAL DE SALAS DE ESPERA:")
                    estado = gestor.obtener_estado_salas_espera()
                    emergencias_count = estado.get('emergencias', 0)
                    
                    print(f"   Emergencias: {emergencias_count}")
                    print(f"   General: {estado.get('general', 0)}")
                    print(f"   Dermatología: {estado.get('dermatologia', 0)}")
                    print(f"   Urología: {estado.get('urologia', 0)}")
                    
                    paciente = gestor.atender_siguiente_paciente()
                    
                    if paciente:
                        print("\n" + "="*60)
                        print(" PACIENTE SIENDO ATENDIDO")
                        print("="*60)
                        print(f"\n Nombre: {paciente.name}")
                        print(f" CI: {paciente.id}")
                        print(f" Edad: {paciente.age} años")
                        print(f" Género: {paciente.gender}")
                        
                        if hasattr(paciente, 'emergency_priority'):
                            print(f"\n EMERGENCIA - Prioridad: {paciente.emergency_priority}")
                            if hasattr(paciente, 'emergency_reason'):
                                print(f" Razón: {paciente.emergency_reason}")
                        
                        if hasattr(paciente, 'especialidad'):
                            print(f"\n Especialidad: {paciente.especialidad.value}")
                        
                        if paciente.medical_history:
                            print(f"\n HISTORIAL MÉDICO:")
                            for i, registro in enumerate(paciente.medical_history, 1):
                                print(f"  {i}. {registro}")
                        else:
                            print("\n Historial médico: Sin registros anteriores")
                        
                        print("\n" + "="*60)
                    else:
                        print("\n No hay pacientes en espera")
                        
                except Exception as e:
                    logger.error(f"Error al atender paciente: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '5':
                print("\n" + "="*60)
                print(" ESTADO COMPLETO DE SALAS DE ESPERA")
                print("="*60)
                try:
                    estado = gestor.obtener_estado_salas_espera()
                    
                    print("\n CANTIDAD DE PACIENTES:")
                    print(f"   Emergencias: {estado.get('emergencias', 0)}")
                    print(f"   Medicina General: {estado.get('general', 0)}")
                    print(f"   Dermatología: {estado.get('dermatologia', 0)}")
                    print(f"   Urología: {estado.get('urologia', 0)}")
                    print(f"   Cardiología: {estado.get('cardiologia', 0)}")
                    print(f"   Pediatría: {estado.get('pediatria', 0)}")
                    print(f"   Ginecología: {estado.get('ginecologia', 0)}")
                    print(f"   Traumatología: {estado.get('traumatologia', 0)}")
                    print(f"   Oftalmología: {estado.get('oftalmologia', 0)}")
                    print(f"   ORL: {estado.get('otorrinolaringologia', 0)}")
                    print(f"   Neurología: {estado.get('neurologia', 0)}")
                    
                    if estado.get('emergencias', 0) > 0:
                        print("\n" + "="*60)
                        print(" PACIENTES EN EMERGENCIAS (por prioridad):")
                        print("="*60)
                        lista_emergencias = gestor.obtener_lista_emergencias()
                        for i, paciente in enumerate(lista_emergencias, 1):
                            prioridad = getattr(paciente, 'emergency_priority', 'N/A')
                            razon = getattr(paciente, 'emergency_reason', 'No especificada')
                            print(f"  {i}. {paciente.name} | Prioridad: {prioridad} | {razon}")
                    
                    print("\n" + "="*60)
                    
                except Exception as e:
                    logger.error(f"Error al mostrar estado de salas: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '6':
                print("\n" + "="*60)
                print(" AGENDAR CITA CON ESPECIALISTA")
                print("="*60)
                try:
                    patient_id = input("\n ID del paciente: ").strip()
                    paciente = gestor.get_patient(patient_id)
                    
                    if not paciente:
                        print(f" Paciente {patient_id} no encontrado")
                        continue
                    
                    print(f"\n Paciente encontrado: {paciente.name}")
                    
                    print("\n Especialidades disponibles:")
                    especialidades = list(EspecialidadMedica)
                    for i, esp in enumerate(especialidades, 1):
                        print(f"  {i}. {esp.value}")
                    
                    try:
                        opcion = int(input("\n Seleccione especialidad (número): ").strip())
                        if 1 <= opcion <= len(especialidades):
                            especialidad = especialidades[opcion - 1]
                        else:
                            print(" Opción inválida")
                            continue
                    except ValueError:
                        print(" Ingrese un número válido")
                        continue
                    
                    print("\n Tipos de cita disponibles:")
                    tipos = list(TipoCita)
                    for i, tipo in enumerate(tipos, 1):
                        print(f"  {i}. {tipo.value}")
                    
                    try:
                        opcion = int(input("\n Seleccione tipo de cita (número): ").strip())
                        if 1 <= opcion <= len(tipos):
                            tipo_cita = tipos[opcion - 1]
                        else:
                            print(" Opción inválida")
                            continue
                    except ValueError:
                        print(" Ingrese un número válido")
                        continue
                    
                    from datetime import datetime
                    
                    fecha = input("\n Fecha de la cita (YYYY-MM-DD): ").strip()
                    try:
                        datetime.strptime(fecha, "%Y-%m-%d")
                    except ValueError:
                        print(" Formato de fecha inválido")
                        continue
                    
                    horarios = gestor.obtener_horarios_disponibles(especialidad, fecha)
                    
                    if horarios:
                        print(f"\n Horarios disponibles para {especialidad.value}:")
                        for i, hora in enumerate(horarios, 1):
                            print(f"  {i}. {hora}")
                        
                        try:
                            opcion_hora = int(input("\n Seleccione horario (número): ").strip())
                            if 1 <= opcion_hora <= len(horarios):
                                hora = horarios[opcion_hora - 1]
                            else:
                                print(" Opción inválida")
                                continue
                        except ValueError:
                            print(" Ingrese un número válido")
                            continue
                    else:
                        print(f"\n No hay horarios disponibles para {especialidad.value} en {fecha}")
                        continue
                    
                    notas = input("\n Notas adicionales (Enter para omitir): ").strip()
                    
                    cita, mensaje = gestor.programar_cita_especialista(
                        patient_id, especialidad, tipo_cita, fecha, hora, notas
                    )
                    
                    if cita:
                        print("\n" + "="*60)
                        print(" CITA PROGRAMADA EXITOSAMENTE")
                        print("="*60)
                        print(f"\n ID de cita: {cita.id}")
                        print(f" Paciente: {paciente.name}")
                        print(f" Especialidad: {especialidad.value}")
                        print(f" Tipo de cita: {tipo_cita.value}")
                        print(f" Fecha: {fecha}")
                        print(f" Hora: {hora}")
                        if notas:
                            print(f" Notas: {notas}")
                        print("\n" + "="*60)
                    else:
                        print(f"\n {mensaje}")
                        
                except Exception as e:
                    logger.error(f"Error al programar cita: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '7':
                print("\n" + "="*60)
                print(" CONSULTAR HORARIOS DISPONIBLES")
                print("="*60)
                try:
                    print("\n Especialidades disponibles:")
                    especialidades = list(EspecialidadMedica)
                    for i, esp in enumerate(especialidades, 1):
                        print(f"  {i}. {esp.value}")
                    
                    try:
                        opcion = int(input("\n Seleccione especialidad (número): ").strip())
                        if 1 <= opcion <= len(especialidades):
                            especialidad = especialidades[opcion - 1]
                        else:
                            print(" Opción inválida")
                            continue
                    except ValueError:
                        print(" Ingrese un número válido")
                        continue
                    
                    from datetime import datetime
                    fecha = input("\n Fecha (YYYY-MM-DD): ").strip()
                    try:
                        datetime.strptime(fecha, "%Y-%m-%d")
                    except ValueError:
                        print(" Formato de fecha inválido")
                        continue
                    
                    horarios = gestor.obtener_horarios_disponibles(especialidad, fecha)
                    
                    if horarios:
                        print(f"\n Horarios disponibles para {especialidad.value} el {fecha}:")
                        for hora in horarios:
                            print(f"  • {hora}")
                    else:
                        print(f"\n No hay horarios disponibles para {especialidad.value} en {fecha}")
                    
                except Exception as e:
                    logger.error(f"Error al ver horarios: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '8':
                print("\n" + "="*60)
                print(" CITAS DEL PACIENTE")
                print("="*60)
                try:
                    patient_id = input("\n CI del paciente: ").strip()
                    paciente = gestor.get_patient(patient_id)
                    
                    if not paciente:
                        print(f" Paciente {patient_id} no encontrado")
                        continue
                    
                    citas = gestor.obtener_citas_paciente(patient_id)
                    
                    if citas:
                        print(f"\n Citas de {paciente.name}:")
                        for i, cita in enumerate(citas, 1):
                            estado_emoji = {
                                "Programada": "",
                                "En Progreso": "",
                                "Completada": "",
                                "Cancelada": ""
                            }.get(cita.status, "")
                            
                            print(f"\n  {i}. {estado_emoji} {cita.status}")
                            print(f"     ID: {cita.id}")
                            print(f"     Especialidad: {cita.specialty.value}")
                            print(f"     Tipo: {cita.appointment_type.value}")
                            print(f"     Fecha: {cita.date} a las {cita.time}")
                            if cita.notes:
                                print(f"     Notas: {cita.notes}")
                    else:
                        print(f"\n {paciente.name} no tiene citas programadas")
                    
                except Exception as e:
                    logger.error(f"Error al ver citas del paciente: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '9':
                print("\n" + "="*60)
                print(" CANCELAR CITA MÉDICA")
                print("="*60)
                try:
                    cita_id = input("\n ID de la cita a cancelar: ").strip()
                    
                    if gestor.cancelar_cita(cita_id):
                        print(f"\n Cita {cita_id} cancelada exitosamente")
                    else:
                        print(f"\n No se pudo cancelar la cita (ID no encontrado)")
                    
                except Exception as e:
                    logger.error(f"Error al cancelar cita: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '10':
                print("\n" + "="*60)
                print(" LISTA DE TODOS LOS PACIENTES")
                print("="*60)
                try:
                    pacientes = gestor.list_all_patients()
                    
                    if pacientes:
                        print(f"\n Total de pacientes: {len(pacientes)}\n")
                        for i, paciente in enumerate(pacientes, 1):
                            print(f"  {i}. {paciente.name} {paciente.apellido}")
                            print(f"     Cédula: {paciente.id}")
                            print(f"     Edad: {paciente.age} años | Género: {paciente.gender}")
                            print(f"     Condición: {paciente.condicion_actual}")
                            if paciente.medical_history:
                                print(f"     Registros médicos: {len(paciente.medical_history)}")
                            print()
                    else:
                        print("\n No hay pacientes registrados")
                    
                except Exception as e:
                    logger.error(f"Error al listar pacientes: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '11':
                print("\n" + "="*60)
                print(" BUSCAR PACIENTE (AVANZADA)")
                print("="*60)
                try:
                    print(" Opciones de búsqueda:")
                    print("  1. Buscar por CI, Nombre o Apellido")
                    print("  2. Buscar por género (M/F)")
                    print("  3. Buscar por fecha de registro (YYYY-MM-DD)")
                    print("  4. Buscar por edad")
                    print("  5. Buscar por día de la semana (ej. Lunes)")
                    
                    sub_opcion = input("\n Seleccione una opción (1-5): ").strip()
                    pacientes_encontrados = []
                    
                    if sub_opcion == '1':
                        busqueda = input("\n Ingrese CI, Nombre o Apellido del paciente: ").strip()
                        paciente = gestor.get_patient(busqueda)
                        if paciente:
                            pacientes_encontrados.append(paciente)
                    elif sub_opcion == '2':
                        genero = input("\n Ingrese el género (M/F): ").strip()
                        pacientes_encontrados = gestor.buscar_por_genero(genero)
                    elif sub_opcion == '3':
                        fecha = input("\n Ingrese la fecha (YYYY-MM-DD): ").strip()
                        pacientes_encontrados = gestor.buscar_por_fecha(fecha)
                    elif sub_opcion == '4':
                        edad = obtener_edad_valida()
                        pacientes_encontrados = gestor.buscar_por_edad(edad)
                    elif sub_opcion == '5':
                        dia = input("\n Ingrese el día de la semana: ").strip()
                        pacientes_encontrados = gestor.buscar_por_dia(dia)
                    else:
                        print(" Opción no válida")
                        continue
                    
                    if pacientes_encontrados:
                        print(f"\n Se encontraron {len(pacientes_encontrados)} pacientes:")
                        for p in pacientes_encontrados:
                            print("\n" + "="*60)
                            print(p)
                            
                            # Mostrar citas agendadas
                            citas = gestor.obtener_citas_paciente(p.id)
                            if citas:
                                print(f"\n 📅 PRÓXIMAS CITAS ({len(citas)} programadas):")
                                for cita in citas:
                                    print(f"  - Fecha: {cita.date} | Hora: {cita.time} | Esp: {cita.specialty.value}")
                                    
                            if p.medical_history:
                                print(f"\n 📋 HISTORIAL MÉDICO ({len(p.medical_history)} registros):")
                                for i, registro in enumerate(p.medical_history, 1):
                                    print(f"  {i}. {registro}")
                        print("="*60)
                    else:
                        print("\n No se encontraron pacientes con esos criterios.")
                    
                except Exception as e:
                    logger.error(f"Error al buscar paciente: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '12':
                print("\n" + "="*60)
                print(" PACIENTES EN EMERGENCIAS")
                print("="*60)
                try:
                    emergencias = gestor.obtener_lista_emergencias()
                    
                    if emergencias:
                        print(f"\n Total en emergencias: {len(emergencias)}\n")
                        for i, paciente in enumerate(emergencias, 1):
                            prioridad = getattr(paciente, 'emergency_priority', 'N/A')
                            razon = getattr(paciente, 'emergency_reason', 'N/A')
                            desc = gestor.gestor_triaje.obtener_descripcion_triaje(prioridad)
                            
                            print(f"  {i}. {paciente.name} | CI: {paciente.id}")
                            print(f"     Prioridad: {prioridad} - {desc}")
                            print(f"     Razón: {razon}")
                            print()
                    else:
                        print("\n No hay pacientes en emergencias")
                    
                except Exception as e:
                    logger.error(f"Error al ver emergencias: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '13':
                print("\n" + "="*60)
                print(" AÑADIR REGISTRO MÉDICO")
                print("="*60)
                try:
                    patient_id = input("\n CI del paciente: ").strip()
                    
                    paciente = gestor.get_patient(patient_id)
                    if not paciente:
                        print(f" Paciente no encontrado")
                        continue
                    
                    print(f"\n Paciente: {paciente.name}")
                    
                    registro = input("\n Ingrese el registro médico: ").strip()
                    if not registro:
                        print(" El registro no puede estar vacío")
                        continue
                    
                    if gestor.add_medical_record(patient_id, registro):
                        print("\n Registro médico añadido exitosamente")
                    else:
                        print("\n Error al añadir registro")
                    
                except Exception as e:
                    logger.error(f"Error al añadir historial: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '14':
                print("\n" + "="*60)
                print(" HISTORIAL MÉDICO DEL PACIENTE")
                print("="*60)
                try:
                    patient_id = input("\n CI del paciente: ").strip()
                    
                    paciente = gestor.get_patient(patient_id)
                    if not paciente:
                        print(f" Paciente no encontrado")
                        continue
                    
                    print(f"\n Paciente: {paciente.name}")
                    
                    historial = gestor.get_medical_history(patient_id)
                    
                    if historial:
                        print(f"\n Historial médico ({len(historial)} registros):")
                        for i, registro in enumerate(historial, 1):
                            print(f"  {i}. {registro}")
                    else:
                        print("\n El paciente no tiene registros médicos")
                    
                except Exception as e:
                    logger.error(f"Error al ver historial: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '15':
                print("\n" + "="*60)
                print(" PACIENTES ORDENADOS POR EDAD")
                print("="*60)
                try:
                    pacientes = gestor.sort_patients_by_age()
                    
                    if pacientes:
                        print(f"\n Total: {len(pacientes)} pacientes\n")
                        for i, paciente in enumerate(pacientes, 1):
                            print(f"  {i}. {paciente.name} - {paciente.age} años (CI: {paciente.id})")
                    else:
                        print("\n No hay pacientes")
                    
                except Exception as e:
                    logger.error(f"Error al ordenar por edad: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '16':
                print("\n" + "="*60)
                print(" PACIENTES ORDENADOS POR NOMBRE")
                print("="*60)
                try:
                    pacientes = gestor.sort_patients_by_name()
                    
                    if pacientes:
                        print(f"\n Total: {len(pacientes)} pacientes\n")
                        for i, paciente in enumerate(pacientes, 1):
                            print(f"  {i}. {paciente.name} - {paciente.age} años (CI: {paciente.id})")
                    else:
                        print("\n No hay pacientes")
                    
                except Exception as e:
                    logger.error(f"Error al ordenar por nombre: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '17':
                print("\n" + "="*60)
                print(" PACIENTES ORDENADOS POR GÉNERO")
                print("="*60)
                try:
                    pacientes = gestor.sort_patients_by_gender()
                    if pacientes:
                        print(f"\n Total: {len(pacientes)} pacientes\n")
                        for i, p in enumerate(pacientes, 1):
                            print(f"  {i}. {p.name} - {getattr(p, 'gender', 'N/A')} (CI: {p.id})")
                    else:
                        print("\n No hay pacientes")
                except Exception as e:
                    logger.error(f"Error al ordenar por género: {e}")
                    print(f" Error inesperado: {e}")

            elif opcion == '18':
                print("\n" + "="*60)
                print(" PACIENTES ORDENADOS POR FECHA")
                print("="*60)
                try:
                    pacientes = gestor.sort_patients_by_date()
                    if pacientes:
                        print(f"\n Total: {len(pacientes)} pacientes\n")
                        for i, p in enumerate(pacientes, 1):
                            print(f"  {i}. {p.name} - {getattr(p, 'fecha_registro', 'N/A')} (CI: {p.id})")
                    else:
                        print("\n No hay pacientes")
                except Exception as e:
                    logger.error(f"Error al ordenar por fecha: {e}")
                    print(f" Error inesperado: {e}")

            elif opcion == '19':
                print("\n" + "="*60)
                print(" PACIENTES ORDENADOS POR DÍA")
                print("="*60)
                try:
                    pacientes = gestor.sort_patients_by_day()
                    if pacientes:
                        print(f"\n Total: {len(pacientes)} pacientes\n")
                        for i, p in enumerate(pacientes, 1):
                            print(f"  {i}. {p.name} - {getattr(p, 'dia_registro', 'N/A')} (CI: {p.id})")
                    else:
                        print("\n No hay pacientes")
                except Exception as e:
                    logger.error(f"Error al ordenar por día: {e}")
                    print(f" Error inesperado: {e}")

            elif opcion == '20':
                print("\n" + "="*60)
                print(" PACIENTES ORDENADOS POR ENFERMEDAD")
                print("="*60)
                try:
                    pacientes = gestor.sort_patients_by_disease()
                    if pacientes:
                        print(f"\n Total: {len(pacientes)} pacientes\n")
                        for i, p in enumerate(pacientes, 1):
                            print(f"  {i}. {p.name} - {getattr(p, 'enfermedad_principal', 'N/A')} (CI: {p.id})")
                    else:
                        print("\n No hay pacientes")
                except Exception as e:
                    logger.error(f"Error al ordenar por enfermedad: {e}")
                    print(f" Error inesperado: {e}")

            elif opcion == '21':
                print("\n" + "="*60)
                print(" ELIMINAR PACIENTE")
                print("="*60)
                try:
                    patient_id = input("\n CI del paciente a eliminar: ").strip()
                    
                    paciente = gestor.get_patient(patient_id)
                    if not paciente:
                        print(f" Paciente no encontrado")
                        continue
                    
                    print(f"\n Paciente: {paciente.name}")
                    confirmacion = input("¿Está seguro de que desea eliminar este paciente? (S/N): ").strip().upper()
                    
                    if confirmacion == 'S':
                        if gestor.remove_patient(patient_id):
                            print(f"\n Paciente {patient_id} eliminado exitosamente")
                        else:
                            print("\n Error al eliminar paciente")
                    else:
                        print("\n Operación cancelada")
                    
                except Exception as e:
                    logger.error(f"Error al eliminar paciente: {e}")
                    print(f" Error inesperado: {e}")
                    
            elif opcion == '0':
                print("\n" + "="*60)
                print(" GRACIAS POR USAR EL SISTEMA DE GESTIÓN DE PACIENTES")
                print("="*60)
                logger.info("Aplicación cerrada por el usuario")
                break
            else:
                print("\n Opción no válida. Por favor, intente de nuevo.")
            
            if opcion != '0':
                input("\n Presione ENTER para continuar...")
                import os
                os.system("cls" if os.name == "nt" else "clear")
        
        except KeyboardInterrupt:
            print("\n\n Aplicación interrumpida por el usuario")
            logger.info("Aplicación interrumpida (Ctrl+C)")
            break
        except Exception as e:
            logger.error(f"Error inesperado en el bucle principal: {e}")
            print(f"\n Error inesperado: {e}")
            print("   Por favor, intente de nuevo")

if __name__ == "__main__":
    main()
