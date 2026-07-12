import unittest
import os
import shutil
from models.paciente import Paciente
from data_structures.lista_enlazada import ListaEnlazada
from data_structures.cola import Cola
from data_structures.pila import Pila
from services.gestor_pacientes import GestorPacientes

class TestPaciente(unittest.TestCase):
    def test_patient_creation(self):
        paciente = Paciente("123456789", "Juan", "Perez", 30, "Masculino")
        self.assertEqual(paciente.id, "123456789")
        self.assertEqual(paciente.name, "Juan")
        self.assertEqual(paciente.apellido, "Perez")
        self.assertEqual(paciente.age, 30)
        self.assertEqual(paciente.gender, "Masculino")
        self.assertEqual(paciente.medical_history, [])

    def test_patient_to_dict_and_from_dict(self):
        paciente = Paciente("987654321", "Maria", "Lopez", 25, "Femenino")
        paciente.medical_history = ["Consulta general 2023-01-01"]
        paciente_dict = paciente.to_dict()
        self.assertEqual(paciente_dict["id"], "987654321")
        self.assertEqual(paciente_dict["name"], "Maria")
        self.assertEqual(paciente_dict["apellido"], "Lopez")
        self.assertEqual(paciente_dict["age"], 25)
        
        nuevo_paciente = Paciente.from_dict(paciente_dict)
        self.assertEqual(nuevo_paciente.id, paciente.id)
        self.assertEqual(nuevo_paciente.name, paciente.name)
        self.assertEqual(nuevo_paciente.medical_history, ["Consulta general 2023-01-01"])

class TestListaEnlazada(unittest.TestCase):
    def test_append_and_to_list(self):
        lista = ListaEnlazada()
        p1 = Paciente("111111111", "A", "A", 20, "M")
        p2 = Paciente("222222222", "B", "B", 30, "F")
        lista.append(p1)
        lista.append(p2)
        self.assertEqual(lista.to_list(), [p1, p2])

    def test_search(self):
        lista = ListaEnlazada()
        p = Paciente("333333333", "Carlos", "Sainz", 40, "M")
        lista.append(p)
        self.assertEqual(lista.search("333333333"), p)
        self.assertEqual(lista.search("Carlos"), p)
        self.assertEqual(lista.search("Sainz"), p)
        self.assertEqual(lista.search("Carlos Sainz"), p)
        self.assertIsNone(lista.search("No Existe"))

class TestCola(unittest.TestCase):
    def test_queue_operations(self):
        cola = Cola()
        p1 = Paciente("444444444", "A", "A", 10, "M")
        p2 = Paciente("555555555", "B", "B", 20, "F")
        cola.enqueue(p1)
        cola.enqueue(p2)
        self.assertEqual(cola.dequeue(), p1)
        self.assertEqual(cola.dequeue(), p2)
        self.assertIsNone(cola.dequeue())

class TestPila(unittest.TestCase):
    def test_stack_operations(self):
        pila = Pila()
        pila.push("Registro 1")
        pila.push("Registro 2")
        self.assertEqual(pila.pop(), "Registro 2")
        self.assertEqual(pila.peek(), "Registro 1")
        self.assertEqual(pila.pop(), "Registro 1")
        self.assertIsNone(pila.pop())

class TestGestorPacientes(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = "test_data"
        if not os.path.exists(self.test_data_dir):
            os.makedirs(self.test_data_dir)

    def tearDown(self):
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        if os.path.exists("data"):
            shutil.rmtree("data")

    def test_add_and_get_patient(self):
        # Usamos un nombre de archivo temporal para pruebas
        gestor = GestorPacientes(patients_filename="test_pacientes_temp.csv")
        # Limpiamos la lista antes de la prueba
        gestor.patient_list = ListaEnlazada()
        # Añadimos un paciente
        paciente = gestor.add_patient("1122334455", "Test", "User", 50, "Otro")
        self.assertIsNotNone(paciente)
        # Buscamos el paciente
        recuperado = gestor.get_patient(paciente.id)
        self.assertEqual(recuperado.name, "Test")

    def test_add_and_remove_patient(self):
        gestor = GestorPacientes(patients_filename="test_pacientes_temp.csv")
        gestor.patient_list = ListaEnlazada()
        # Añadimos un paciente
        paciente = gestor.add_patient("5544332211", "To", "Remove", 60, "Masculino")
        self.assertTrue(gestor.remove_patient(paciente.id))
        # Verificamos que ya no exista
        self.assertIsNone(gestor.get_patient(paciente.id))

    def test_add_medical_history(self):
        gestor = GestorPacientes(patients_filename="test_pacientes_temp.csv")
        gestor.patient_list = ListaEnlazada()
        # Añadimos un paciente
        paciente = gestor.add_patient("9988776655", "History", "Test", 35, "Femenino")
        # Añadimos un registro médico
        self.assertTrue(gestor.add_medical_record(paciente.id, "Primera consulta"))
        # Verificamos que el registro exista
        historial = gestor.get_medical_history(paciente.id)
        self.assertEqual(historial, ["Primera consulta"])
    
    def test_duplicate_patient_id(self):
        gestor = GestorPacientes(patients_filename="test_pacientes_temp.csv")
        gestor.patient_list = ListaEnlazada()
        # Añadimos un paciente inicial
        gestor.add_patient("1234567890", "Paciente", "Uno", 30, "Masculino")
        # Intentamos añadir otro paciente con el mismo ID
        paciente2 = gestor.add_patient("1234567890", "Paciente", "Duplicado", 35, "Masculino")
        
        # Debe retornar el paciente actualizado, no un error ni None
        self.assertIsNotNone(paciente2)
        # Verificamos que sus datos se hayan actualizado
        self.assertEqual(paciente2.apellido, "Duplicado")
        self.assertEqual(paciente2.age, 35)
        # La lista no debe haber crecido
        self.assertEqual(len(gestor.list_all_patients()), 1)

if __name__ == "__main__":
    unittest.main()
