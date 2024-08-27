import os
import django
import json
import logging
# Configurando o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')  
django.setup()

from patients.models import (Student, ClassGroup, StudentInfo, Employee, 
                             Department, EmployeeInfo, Visitor)
from patients.views import (create_students, create_student_info, create_class_group, 
                            create_employees, create_employee_info, create_department, 
                            create_visitor)
from appointments.views import create_infirmary, create_nurses
from controller.crud import create_objects, update_info

def create_student_info_direct(data):
    """
    Função auxiliar para criar ou atualizar StudentInfo diretamente usando um dicionário de dados.
    """
    try:
        logger.info("Creating or updating student info directly")
        logger.debug(f"Request data: {data}")

        if not isinstance(data, dict):
            logger.error("Invalid data format, expected a dictionary")
            return {'status': 'error', 'message': 'Invalid data format, expected a dictionary'}
        
        student_id = data.get('student_id')
        allergies = data.get('allergies')
        notes = data.get('notes')

        if not student_id:
            logger.error("Missing required field: student_id")
            return {'status': 'error', 'message': 'Missing required field: student_id'}

        logger.info(f"Calling update_info for student_id: {student_id}")
        updated_info = update_info(StudentInfo, student_id, 'student_id', allergies, notes)
        logger.info(f"Student info updated successfully for student_id: {student_id}")

        return {'status': 'success', 'message': 'Student info updated successfully', 'data': updated_info.id}

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {'status': 'error', 'message': str(e)}

# Função auxiliar de criação direta de Visitor
def create_visitors_direct(data_list):
    """
    Função auxiliar para criar visitantes diretamente usando uma lista de dicionários.
    """
    logger.info("Creating visitors directly")
    if isinstance(data_list, list):
        for data in data_list:
            if not isinstance(data, dict):
                logger.error("Invalid data format, expected a dictionary")
                return {'status': 'error', 'message': 'Invalid data format, expected a dictionary'}
            
            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')
            relationship = data.get('relationship')
            allergies = data.get('allergies', '')
            notes = data.get('notes', '')

            if not name or not age or not gender or not relationship:
                logger.error("Missing required fields in visitor data")
                return {'status': 'error', 'message': 'Missing required fields'}

            visitor = Visitor.objects.create(
                name=name,
                age=age,
                gender=gender,
                relationship=relationship,
                allergies=allergies,
                notes=notes
            )
            logger.info(f"Visitor {visitor.name} created successfully")
        return {'status': 'success', 'message': 'Visitors created successfully'}
    else:
        logger.error("Invalid data format, expected a list of dictionaries")
        return {'status': 'error', 'message': 'Invalid data format, expected a list of dictionaries'}

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_data_insertion():
    logger.info("Starting data insertion script")

    # Dados para inserir no banco
    class_groups_data = [
        {'name': 'Turma A', 'segment': 'Primário', 'director': 'Carlos Silva'},
        {'name': 'Turma B', 'segment': 'Secundário', 'director': 'Maria Oliveira'}
    ]

    students_data = [
        {'name': 'João da Silva', 'age': 12, 'gender': 'Masculino', 'registry': 'STU001', 'class_group_id': 1, 'birth_date': '2012-05-10'},
        {'name': 'Ana Maria', 'age': 14, 'gender': 'Feminino', 'registry': 'STU002', 'class_group_id': 2, 'birth_date': '2010-07-12'}
    ]

    student_info_data = [
        {'student_id': 1, 'allergies': 'Amendoim', 'notes': 'Alergia leve'},
        {'student_id': 2, 'allergies': 'Lactose', 'notes': 'Usar leite sem lactose'}
    ]

    departments_data = [
        {'name': 'Recursos Humanos', 'director': 'Joana Almeida'},
        {'name': 'TI', 'director': 'Roberto Costa'}
    ]

    employees_data = [
        {'name': 'Pedro Gomes', 'age': 30, 'gender': 'Masculino', 'registry': 'EMP001', 'department_id': 1, 'position': 'Gerente', 'birth_date': '1994-04-23'},
        {'name': 'Mariana Lima', 'age': 25, 'gender': 'Feminino', 'registry': 'EMP002', 'department_id': 2, 'position': 'Analista', 'birth_date': '1999-09-19'}
    ]

    employee_info_data = [
        {'employee_id': 1, 'allergies': 'Poeira', 'notes': 'Evitar locais empoeirados'},
        {'employee_id': 2, 'allergies': 'Nenhuma', 'notes': 'Nenhuma observação'}
    ]

    visitors_data = [
        {'name': 'Carlos Souza', 'age': 45, 'gender': 'Masculino', 'relationship': 'Pai', 'allergies': 'Nenhuma', 'notes': 'Visita mensal'},
        {'name': 'Maria Santos', 'age': 35, 'gender': 'Feminino', 'relationship': 'Mãe', 'allergies': 'Nenhuma', 'notes': 'Visita semanal'}
    ]

    infirmaries_data = [
        {'name': 'Enfermaria Central', 'location': 'Prédio Principal'},
        {'name': 'Enfermaria Secundária', 'location': 'Prédio B'}
    ]

    nurses_data = [
        {'name': 'Camila Ferreira', 'username': 'camila.ferreira', 'badge_number': 'NUR001'},
        {'name': 'Lucas Mendes', 'username': 'lucas.mendes', 'badge_number': 'NUR002'}
    ]

    # Inserir dados usando as funções de criação
    create_class_group(class_groups_data)
    create_students(students_data)

    # Criar informações adicionais para os estudantes usando a função auxiliar
    for info in student_info_data:
        create_student_info_direct(info)

    create_department(departments_data)
    create_employees(employees_data)

    # Criar informações adicionais para os funcionários usando a função auxiliar
    for info in employee_info_data:
        create_student_info_direct(info)

    # Usar a nova função para criar visitantes diretamente
    create_visitors_direct(visitors_data)

    create_infirmary(infirmaries_data)
    create_nurses(nurses_data)

    logger.info("Data insertion completed successfully")

# Executar o script
if __name__ == "__main__":
    run_data_insertion()