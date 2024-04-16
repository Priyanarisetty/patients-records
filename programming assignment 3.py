main.py:

from patients import Hospital
from users import authenticate_user
import helpers

def main():
    hospital = helpers.read_patient_data('patients.csv')
    users = helpers.read_credentials('PA3_credentials.csv')

    authenticated_user = None
    while authenticated_user is None:
        username = input("Enter username: ")
        password = input("Enter password: ")
        authenticated_user = authenticate_user(username, password, users)
        if authenticated_user is None:
            print("Invalid credentials. Please try again.")

    if authenticated_user.role == 'admin':
        print("You have admin role. You can perform count_visits.")
        helpers.perform_admin_actions(hospital)
    elif authenticated_user.role in ['clinician', 'nurse']:
        helpers.perform_clinician_nurse_actions(hospital)
    elif authenticated_user.role == 'management':
        helpers.generate_statistics_report(hospital)

if __name__ == "__main__":
    main()
patients.py:

from datetime import datetime
import csv
import random
import string

class Patient:
    def __init__(self, patient_id, gender, race, age, ethnicity, insurance, zip_code):
        self.patient_id = patient_id
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.visits = []
        self.notes = []

    def add_visit(self, visit):
        self.visits.append(visit)

    def add_note(self, note_id, note_type):
        note = Note(note_id, note_type)
        self.notes.append(note)

    def remove_note_by_id(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                return True
        return False

class Visit:
    def __init__(self, visit_id, visit_time, department, chief_complaint):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.department = department
        self.chief_complaint = chief_complaint

class Department:
    def __init__(self, name):
        self.name = name
        self.patients = []

    def add_patient(self, patient):
        self.patients.append(patient)
        print(f"Patient {patient.patient_id} added to {self.name} department.")

    def remove_patient(self, patient_id):
        for patient in self.patients:
            if patient.patient_id == patient_id:
                self.patients.remove(patient)
                print(f"Patient {patient_id} removed from {self.name} department.")
                return True
        print(f"Patient {patient_id} not found in {self.name} department.")
        return False

class Hospital:
    def __init__(self):
        self.departments = {}

    def add_department(self, department_name):
        if department_name not in self.departments:
            self.departments[department_name] = Department(department_name)

    def get_department(self, department_name):
        return self.departments.get(department_name)

    def add_patient_to_department(self, department_name, patient):
        if department_name in self.departments:
            self.departments[department_name].add_patient(patient)
        else:
            print(f"Department '{department_name}' does not exist.")

    def remove_patient_from_department(self, department_name, patient_id):
        if department_name in self.departments:
            return self.departments[department_name].remove_patient(patient_id)
        else:
            print(f"Department '{department_name}' does not exist.")

    def retrieve_patient_info(self, patient_id):
        for department in self.departments.values():
            for patient in department.patients:
                if patient.patient_id == patient_id:
                    return patient
        print(f"Patient {patient_id} not found.")
        return None

    def count_visits_on_date(self, date):
        total_visits = 0
        for department in self.departments.values():
            for patient in department.patients:
                for visit in patient.visits:
                    if visit.visit_time.date() == date.date():
                        total_visits += 1
        return total_visits

def read_patient_data(file_path):
    hospital = Hospital()
    with open(file_path, 'r') as file:
        if file_path.lower().endswith('.csv'):
            reader = csv.DictReader(file)
            for row in reader:
                patient_id = row['Patient_ID']
                if patient_id not in hospital.patients:
                    patient = Patient(patient_id, row['Gender'], row['Race'], int(row['Age']), row['Ethnicity'], row['Insurance'], row['Zip_code'])
                    hospital.add_patient_to_department(row['Visit_department'], patient)
                visit_id = row['Visit_ID']
                visit_time = datetime.strptime(row['Visit_time'], '%Y-%m-%d')
                department = row['Visit_department']
                chief_complaint = row['Chief_complaint']
                visit = Visit(visit_id, visit_time, department, chief_complaint)
                patient = hospital.retrieve_patient_info(patient_id)
                if patient:
                    patient.add_visit(visit)
        else:
            print("Unsupported file format.")
    return hospital

users.py:
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

helpers.py:

from datetime import datetime
import random
import string

def read_credentials(file_path):
    users = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = User(row['username'], row['password'], row['role'])
            users.append(user)
    return users

def authenticate_user(username, password, users):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

def perform_admin_actions(hospital):
    action = input("Choose an action (count_visits): ").strip().lower()
    if action == 'count_visits':
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            total_visits = hospital.count_visits_on_date(date)
            print("Total visits on", date.strftime('%Y-%m-%d'), ":", total_visits)
        except ValueError:
            print("Invalid date format.")

def perform_clinician_nurse_actions(hospital):
    while True:
        action = input("Choose an action (add_patient, remove_patient, retrieve_patient, count_visits, stop): ").strip().lower()

        if action == "stop":
            break
        elif action == "add_patient":
            # Implement add_patient action for clinicians and nurses
            pass
        elif action == "remove_patient":
            # Implement remove_patient action for clinicians and nurses
            pass
        elif action == "retrieve_patient":
            # Implement retrieve_patient action for clinicians and nurses
            pass
        elif action == "count_visits":
            # Implement count_visits action for clinicians and nurses
            pass
        else:
            print("Invalid action.")

def generate_statistics_report(hospital):
    print("You have management role. Generating key statistics report...")
    # Implement key statistics report generation for management role
    pass
