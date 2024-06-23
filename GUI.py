import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox
import pypyodbc as odbc

# Using SQL Server
DRIVER_NAME = 'SQL SERVER'

# in SQL Server, put in 'SELECT @@ServerName' as a query to find SERVER_NAME 
SERVER_NAME = ''
# put in database name
DATABASE_NAME = ''

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

# Create the PyQt application
class PatientEntryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Patient Entry Form')

        self.name_label = QLabel('Patient First Name:', self)
        self.first_name_input = QLineEdit(self)

        self.last_name_label = QLabel('Patient Last Name:', self)
        self.last_name_input = QLineEdit(self)

        self.age_label = QLabel('Patient Age:', self)
        self.age_input = QLineEdit(self)

        self.gender_label = QLabel('Patient Gender:', self)
        self.gender_combo = QComboBox(self)
        self.gender_combo.addItems(['Male', 'Female'])

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.add_patient_to_db)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_combo)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_patient_to_db(self):
        firstname = self.first_name_input.text()
        lastname = self.last_name_input.text()
        age = self.age_input.text()
        gender = self.gender_combo.currentText()

        if not firstname or not lastname or not age.isdigit():
            QMessageBox.warning(self, 'Input Error', 'Please enter a valid name and age.')
            return

        try:
            conn = odbc.connect(connection_string)
            cursor = conn.cursor()

            # Find the current maximum patient_id
            cursor.execute('SELECT MAX(patient_id) FROM myhospital.hospital')
            result = cursor.fetchone()
            max_patient_id = result[0] if result[0] is not None else 0
            new_patient_id = max_patient_id + 1

            cursor.execute('''
                INSERT INTO myhospital.hospital (patient_id, firstname, lastname, age, gender, ethnicity, weight, height, blood_pressure, cholesterol_level, diabetes,
                    heart_disease, smoking_status, alcohol_intake, diagnosis, treatment, outcome, admission_date, discharge_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (new_patient_id, firstname, lastname, int(age), gender, 'U', 0, 0, 'U', 'U', 0,
                  0, 'U', 'U', 'U', 'U', 'U', '2024-01-01', '2024-01-02'))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, 'Success', 'Patient added to database successfully!')
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.age_input.clear()

        except Exception as e:
            QMessageBox.critical(self, 'Database Error', f'Failed to add patient to database.\nError: {e}')
            return


def main():
    app = QApplication(sys.argv)
    ex = PatientEntryApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
