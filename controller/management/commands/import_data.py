# controller/management/commands/import_data.py

from django.core.management.base import BaseCommand
from patients.models import *
from controller.import_script.api_totvs import (
    get_data,
    endpoint_departments,
    endpoint_employees,
    endpoint_students,
    endpoint_class
)
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa dados da API externa e atualiza o banco de dados.'

    def handle(self, *args, **options):
        # Obter dados de departamentos
        dados_departamentos = get_data(endpoint_departments)
        if dados_departamentos:
            
            self.import_departments(dados_departamentos)

        # Obter dados de turmas
        dados_turmas = get_data(endpoint_class)
        if dados_turmas:
            
            self.import_class_groups(dados_turmas)

        # Obter dados de alunos
        dados_alunos = get_data(endpoint_students)
        if dados_alunos:
            
            self.import_students(dados_alunos)

        # Obter dados de colaboradores
        dados_colaboradores = get_data(endpoint_employees)
        if dados_colaboradores:
            
            self.import_employees(dados_colaboradores)

    def import_departments(self, data):
        
        for item in data:
            dept_id = item.get('ID')
            name = item.get('NAME')
            director = item.get('DIRECTOR')

            # Verifica se o nome do departamento está presente
            if not name:
                self.stderr.write(f"Departamento com id {dept_id} sem nome. Registro ignorado.")
                continue

            # Atribui um valor padrão para o diretor se não estiver presente
            if not director:
                director = 'Diretor Desconhecido'

            try:
                department, created = Department.objects.update_or_create(
                    id=dept_id,
                    defaults={
                        'name': name,
                        'director': director,
                    }
                )
                if created:
                    self.stdout.write(f"Departamento criado: {department.name}")
                else:
                    self.stdout.write(f"Departamento atualizado: {department.name}")

                
            except Exception as e:
                self.stderr.write(f"Erro ao atualizar/criar Departamento com id {dept_id}: {e}")


    def import_class_groups(self, data):
      
        for item in data:
            group_id = item.get('ID')
            name = item.get('NAME')
            segment = item.get('SEGMENT')
            director = item.get('DIRECTOR')

            # Verificação do campo 'name'
            if not name:
                self.stderr.write(f"Turma com id {group_id} sem nome. Registro ignorado.")
                continue

            # Atribuição de valores padrão se necessário
            if not segment:
                segment = 'Segmento Desconhecido'
            if not director:
                director = 'Diretor Desconhecido'

            try:
                class_group, created = ClassGroup.objects.update_or_create(
                    id=group_id,
                    defaults={
                        'name': name,
                        'segment': segment,
                        'director': director,
                    }
                )
                if created:
                    self.stdout.write(f"Turma criada: {class_group.name}")
                else:
                    self.stdout.write(f"Turma atualizada: {class_group.name}")
            except Exception as e:
                self.stderr.write(f"Erro ao atualizar/criar Turma com id {group_id}: {e}")




    def import_students(self, data):
        for item in data:
            student_id = item.get('ID')
            name = item.get('NAME')
            age = item.get('AGE')
            gender = item.get('GENDER')
            email = item.get('EMAIL')
            registry = item.get('REGISTRY')
            class_group_id = item.get('CLASS_GROUP')
            birth_date = item.get('BIRTH_DATE')
            father_name = item.get('FATHER_NAME')
            father_phone = item.get('FATHER_PHONE')
            mother_name = item.get('MOTHER_NAME')
            mother_phone = item.get('MOTHER_PHONE')

            # Verificação dos campos obrigatórios
            if not name:
                self.stderr.write(f"Aluno com id {student_id} sem nome. Registro ignorado.")
                continue
            if not registry:
                self.stderr.write(f"Aluno {name} sem registro. Registro ignorado.")
                continue
            if not gender:
                gender = 'Não Informado'

           
            # Obter o objeto ClassGroup
            class_group = None
            if class_group_id:
                try:
                    class_group = ClassGroup.objects.get(id=class_group_id)
                except ClassGroup.DoesNotExist:
                    self.stderr.write(f"Turma não encontrada para o aluno {name} (ID: {class_group_id})")

            try:
                student, created = Student.objects.update_or_create(
                    id=student_id,
                    defaults={
                        'name': name,
                        'age': age if age is not None else 0,
                        'gender': gender,
                        'email': email,
                        'registry': registry,
                        'class_group': class_group,
                        'birth_date': birth_date,
                        'father_name': father_name,
                        'father_phone': father_phone,
                        'mother_name': mother_name,
                        'mother_phone': mother_phone,
                        'updated_at': timezone.now(),
                    }
                )
                if created:
                    self.stdout.write(f"Aluno criado: {student.name}")
                else:
                    self.stdout.write(f"Aluno atualizado: {student.name}")

                # Criar ou obter o StudentInfo associado
                student_info, info_created = StudentInfo.objects.get_or_create(
                    student=student,
                    defaults={
                        'allergies': '',
                        'patient_notes': '',
                    }
                )
                if info_created:
                    self.stdout.write(f"StudentInfo criado para: {student.name}")
                else:
                    self.stdout.write(f"StudentInfo já existia para: {student.name}")
            except Exception as e:
                self.stderr.write(f"Erro ao atualizar/criar Aluno com id {student_id}: {e}")



    def import_employees(self, data):
        
        for item in data:
            employee_id = item.get('ID')
            name = item.get('NAME')
            age = item.get('AGE')
            gender = item.get('GENDER')
            email = item.get('EMAIL')
            birth_date = item.get('BIRTH_DATE')
            department_id = item.get('DEPARTMENT')
            position = item.get('POSITION')
            registry = item.get('REGISTRY')

            # Verificação dos campos obrigatórios
            if not name:
                self.stderr.write(f"Colaborador com id {employee_id} sem nome. Registro ignorado.")
                continue
            if not registry:
                self.stderr.write(f"Colaborador {name} sem registro. Registro ignorado.")
                continue
            if not gender:
                gender = 'Não Informado'

        

            # Obter o objeto Department
            department = None
            if department_id:
                try:
                    department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    self.stderr.write(f"Departamento não encontrado para o colaborador {name} (ID: {department_id})")

            try:
                employee, created = Employee.objects.update_or_create(
                    id=employee_id,
                    defaults={
                        'name': name,
                        'age': age if age is not None else 0,
                        'gender': gender,
                        'email': email,
                        'birth_date': birth_date,
                        'department': department,
                        'position': position if position else 'Posição Desconhecida',
                        'registry': registry,
                        'updated_at': timezone.now(),
                    }
                )
                if created:
                    self.stdout.write(f"Colaborador criado: {employee.name}")
                else:
                    self.stdout.write(f"Colaborador atualizado: {employee.name}")


                    # Criar ou obter o EmployeeInfo associado
                employee_info, info_created = EmployeeInfo.objects.get_or_create(
                    employee=employee,
                    defaults={
                        'allergies': '',
                        'patient_notes': '',
                    }
                )
                if info_created:
                    self.stdout.write(f"EmployeeInfo criado para: {employee.name}")
                else:
                    self.stdout.write(f"EmployeeInfo já existia para: {employee.name}")

            except Exception as e:
                self.stderr.write(f"Erro ao atualizar/criar Colaborador com id {employee_id}: {e}")
