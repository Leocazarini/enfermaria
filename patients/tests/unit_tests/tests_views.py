from django.test import TestCase, Client
from django.http import JsonResponse
from django.urls import reverse
from patients.models import Student, StudentInfo, ClassGroup
from ...views import *
import json




class TestCreateStudents(TestCase):

    def setUp(self):
        self.valid_data = [
            {
                'name': 'John Doe',
                'age': 15,
                'gender': 'Male',
                'registry': 'S123456',
                'current_class': '9th Grade'
            },
            {
                'name': 'Jane Doe',
                'age': 14,
                'gender': 'Female',
                'registry': 'S654321',
                'current_class': '8th Grade'
            }
        ]
        self.invalid_data_format = {
            'name': 'John Doe',
            'age': 15,
            'gender': 'Male',
            'registry': 'S123456',
            'current_class': '9th Grade'
        }
        self.no_data = None

    def test_create_students_success(self):
        response = create_students(self.valid_data)
        self.assertEqual(response['status'], 'success')
        self.assertEqual(Student.objects.count(), 2)

    def test_create_students_invalid_data_format(self):
        response = create_students(self.invalid_data_format)
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['message'], 'Invalid data format, expected a list of objects')

    def test_create_students_no_data_provided(self):
        response = create_students(self.no_data)
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['message'], 'No data provided')

class TestCreateStudentInfo(TestCase):

    def setUp(self):
        self.client = Client()
        self.class_group = ClassGroup.objects.create(
            name='Class 1',
            segment='Primary',
            director='Director 1'
        )
        self.student = Student.objects.create(
            name='John Doe',
            age=15,
            gender='Male',
            registry='S123456',
            current_class='9th Grade',
            class_group=self.class_group
        )
        self.valid_data_new = json.dumps({
            'student_id': self.student.id,  # Mudança para 'student_id'
            'allergies': 'Peanuts',
            'notes': 'Carries EpiPen'
        })
        self.valid_data_update = json.dumps({
            'student_id': self.student.id,  # Mudança para 'student_id'
            'allergies': 'Peanuts and Shellfish',
            'notes': 'Carries EpiPen and requires regular check-ups'
        })
        self.invalid_data_format = json.dumps([{
            'student_id': self.student.id,
            'allergies': 'Peanuts',
            'notes': 'Carries EpiPen'
        }])
        self.invalid_json = "{'student_id': " + str(self.student.id) + ", 'allergies': 'Peanuts', 'notes': 'Carries EpiPen'"  # JSON malformado

    def test_create_student_info_success(self):
        url = reverse('create_student_info')
        response = self.client.post(url, data=self.valid_data_new, content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Mudança de 201 para 200
        self.assertEqual(StudentInfo.objects.count(), 1)
        self.assertEqual(StudentInfo.objects.first().allergies, 'Peanuts')

    def test_update_student_info_success(self):
        # Primeiro, crie o registro inicial
        self.client.post(reverse('create_student_info'), data=self.valid_data_new, content_type='application/json')
        
        # Em seguida, faça uma atualização
        url = reverse('create_student_info')
        response = self.client.post(url, data=self.valid_data_update, content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Mudança de 201 para 200
        self.assertEqual(StudentInfo.objects.count(), 1)
        self.assertEqual(StudentInfo.objects.first().allergies, 'Peanuts and Shellfish')
        self.assertEqual(StudentInfo.objects.first().notes, 'Carries EpiPen and requires regular check-ups')

    def test_create_student_info_invalid_data_format(self):
        url = reverse('create_student_info')
        response = self.client.post(url, data=self.invalid_data_format, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Invalid data format, expected a dictionary')

    def test_create_student_info_invalid_json(self):
        url = reverse('create_student_info')
        response = self.client.post(url, data=self.invalid_json, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Invalid JSON')

    def test_create_student_info_invalid_request_method(self):
        url = reverse('create_student_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Invalid request method')
    




class TestSearchStudent(TestCase):

    def setUp(self):
        self.class_group = ClassGroup.objects.create(
            name='Class 1',
            segment='Primary',
            director='Director 1'
        )
        self.student1 = Student.objects.create(
            name='John Doe',
            age=15,
            gender='Male',
            registry='S123456',
            class_group=self.class_group,
            current_class='9th Grade'
        )
        self.student_info1 = StudentInfo.objects.create(
            student=self.student1,
            allergies='None',
            notes='Regular check-ups'
        )

        self.student2 = Student.objects.create(
            name='Jane Doe',
            age=14,
            gender='Female',
            registry='S654321',
            class_group=self.class_group,
            current_class='8th Grade'
        )
        self.student_info2 = StudentInfo.objects.create(
            student=self.student2,
            allergies='Peanuts',
            notes='Carries EpiPen'
        )

    def test_search_student_success(self):
        response = search_student(name='John Doe', registry='S123456')
        self.assertIsInstance(response, dict)
        self.assertEqual(response['name'], 'John Doe')
        self.assertEqual(response['info']['allergies'], 'None')
        self.assertEqual(response['class_group_name'], 'Class 1')

    def test_search_student_multiple_records(self):
        
        Student.objects.create(
            name='John Doe',
            age=16,
            gender='Male',
            registry='S789012',
            class_group=self.class_group,
            current_class='10th Grade'
        )

        response = search_student(name='John Doe', registry=None)
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['message'], 'More than one record found for the given information.')

    def test_search_student_not_found(self):
        response = search_student(name='Nonexistent Name', registry='NonexistentRegistry')
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'], 'No records found')