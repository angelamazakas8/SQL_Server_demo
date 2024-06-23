import pypyodbc as odbc
import random
from datetime import datetime, timedelta

# Using SQL Server, but also works with other apps
DRIVER_NAME = 'SQL SERVER'
# To find Server name, in SQL Server, put in 'SELECT @@ServerName' as a query
SERVER_NAME = ''
# put in your database's name (created in SQL)
DATABASE_NAME = ''

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

conn = odbc.connect(connection_string)
print(conn)

cursor = conn.cursor()

# Check if schema exists and create it if not
cursor.execute('''
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'myhospital')
BEGIN
    EXEC('CREATE SCHEMA myhospital')
END
''')

# Create the table if it does not exist
# Index is for last name, first name
cursor.execute('''
IF OBJECT_ID('myhospital.hospital', 'U') IS NULL
BEGIN
    CREATE TABLE myhospital.hospital (
        patient_id INTEGER PRIMARY KEY,
        firstname VARCHAR(255),
        lastname VARCHAR(255),
        age INTEGER,
        gender VARCHAR(7),
        ethnicity VARCHAR(20),
        weight DECIMAL(5,1),
        height DECIMAL(5,1),
        blood_pressure VARCHAR(7),
        cholesterol_level VARCHAR(10),
        diabetes BIT,
        heart_disease BIT,
        smoking_status VARCHAR(20),
        alcohol_intake VARCHAR(20),
        diagnosis VARCHAR(30),
        treatment VARCHAR(30),
        outcome VARCHAR(30),
        admission_date DATE,
        discharge_date DATE
    )
               
    -- Create index on (last name, first name)
    CREATE INDEX person_last_name_first_name_idx
    ON myhospital.hospital (lastname, firstname);               
END
''')

# Function to generate random date within a given range
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Sample data for random generation
genders = ['Male', 'Female']

firstnames = ['Liam', 'Noah', 'Oliver', 'Elijah', 'James', 'William', 'Benjamin', 'Lucas', 'Henry', 'Alexander', 
              'Aiden', 'Gabriel', 'Grayson', 'Anthony', 'Matthew', 'Jackson', 'David', 'Joseph', 'Samuel', 'Carter']
lastnames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 

             'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

ethnicities = ['Caucasian', 'Hispanic', 'Asian', 'African American', 'Other']
blood_pressures = ['120/80', '140/90', '110/70', '150/95', '130/85']
cholesterol_levels = ['Normal', 'High', 'Borderline']
smoking_statuses = ['Non-smoker', 'Current smoker', 'Former smoker']
alcohol_intakes = ['Low', 'Moderate', 'High']
diagnoses = ['Hypertension', 'Heart Disease', 'Asthma', 'Diabetes', 'Flu', 'COVID-19']
treatments = ['Medication', 'Surgery', 'Inhaler', 'Insulin', 'Lifestyle changes', 'Antibiotics']
outcomes = ['Stable', 'Improved', 'Unstable']

# Generate 200 rows of data
start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2024-06-01', '%Y-%m-%d')

for patient_id in range(1, 201):
    age = random.randint(18, 90)
    gender = random.choice(genders)
    firstname = random.choice(firstnames)
    lastname = random.choice(lastnames)
    ethnicity = random.choice(ethnicities)
    weight = round(random.uniform(50.0, 100.0), 1)
    height = round(random.uniform(150.0, 190.0), 1)
    blood_pressure = random.choice(blood_pressures)
    cholesterol_level = random.choice(cholesterol_levels)
    diabetes = bool(random.getrandbits(1))
    heart_disease = bool(random.getrandbits(1))
    smoking_status = random.choice(smoking_statuses)
    alcohol_intake = random.choice(alcohol_intakes)
    diagnosis = random.choice(diagnoses)
    treatment = random.choice(treatments)
    outcome = random.choice(outcomes)
    admission_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
    discharge_date = (datetime.strptime(admission_date, '%Y-%m-%d') + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
    
    cursor.execute('''
        INSERT INTO myhospital.hospital (
            patient_id, firstname, lastname, age, gender, ethnicity, weight, height, blood_pressure, cholesterol_level, diabetes,
            heart_disease, smoking_status, alcohol_intake, diagnosis, treatment, outcome, admission_date, discharge_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (patient_id, firstname, lastname, age, gender, ethnicity, weight, height, blood_pressure, cholesterol_level, diabetes,
          heart_disease, smoking_status, alcohol_intake, diagnosis, treatment, outcome, admission_date, discharge_date))


# Create the CBC (complete blood count) table if it does not exist
cursor.execute('''
IF OBJECT_ID('myhospital.cbc', 'U') IS NULL
BEGIN
    CREATE TABLE myhospital.cbc (
        cbc_id INTEGER NOT NULL PRIMARY KEY,
        patient_id INTEGER FOREIGN KEY REFERENCES myhospital.hospital(patient_id),
        wbc DECIMAL(4,1),
        rbc DECIMAL(4,1),
        hgb DECIMAL(4,1),
        hct DECIMAL(4,1),
        platelet_count DECIMAL(6,1),
        created_date DATE
    )
END
''')

# Generate CBC data for 70% of patients, 140 of 200 patients
cbc_patients = random.sample(range(1, 201), k=140)  

# Start cbc_id at 1
cbc_id = 1

for patient_id in cbc_patients:
    wbc = round(random.uniform(2.0, 15.0), 1)
    rbc = round(random.uniform(2.0, 7.5), 1)
    hgb = round(random.uniform(7.0, 19.0), 1)
    hct = round(random.uniform(10.0, 80.0), 1)
    platelet_count = round(random.uniform(50.0, 600.0), 1)
    created_date = random_date(start_date, end_date).strftime('%Y-%m-%d')

    cursor.execute('''
        INSERT INTO myhospital.cbc (
            cbc_id, patient_id, wbc, rbc, hgb, hct, platelet_count, created_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (cbc_id, patient_id, wbc, rbc, hgb, hct, platelet_count, created_date))
    
    # Increment cbc_id
    cbc_id += 1

# Create the liver panel table if it does not exist
cursor.execute('''
IF OBJECT_ID('myhospital.liver_panel', 'U') IS NULL
BEGIN
    CREATE TABLE myhospital.liver_panel (
        liver_panel_id INTEGER NOT NULL PRIMARY KEY,
        patient_id INTEGER FOREIGN KEY REFERENCES myhospital.hospital(patient_id),
        alt DECIMAL(5,1),
        ast DECIMAL(5,1),
        alp DECIMAL(5,1),
        total_bilirubin DECIMAL(5,1),
        direct_bilirubin DECIMAL(5,1),
        created_date DATE
    )
END
''')

liver_panel_id = 1

# create liver panel data for patients with an abnormal CBC
for patient_id in cbc_patients:

    # Check if CBC values are abnormal
    cursor.execute('''
        SELECT wbc, rbc, hgb, hct, platelet_count
        FROM myhospital.cbc
        WHERE patient_id = ?
    ''', (patient_id,))
    cbc_data = cursor.fetchone()

    if cbc_data:
        wbc, rbc, hgb, hct, platelet_count = cbc_data
        if wbc < 3.0 or wbc > 12.0 or rbc < 3.0 or rbc > 7.0 or hgb < 8.0 or hgb > 18.0 or hct < 20.0 or hct > 60.0 or platelet_count < 100.0 or platelet_count > 500.0:

            # CBC values are abnormal, generate liver panel data
            alt = round(random.uniform(5.0, 100.0), 1)
            ast = round(random.uniform(5.0, 100.0), 1)
            alp = round(random.uniform(5.0, 100.0), 1)
            total_bilirubin = round(random.uniform(0.1, 5.0), 1)
            direct_bilirubin = round(random.uniform(0.1, 5.0), 1)
            created_date = random_date(start_date, end_date).strftime('%Y-%m-%d')

            cursor.execute('''
                INSERT INTO myhospital.liver_panel (
                    liver_panel_id, patient_id, alt, ast, alp, total_bilirubin, direct_bilirubin, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (liver_panel_id, patient_id, alt, ast, alp, total_bilirubin, direct_bilirubin, created_date))
            
            # Increment liver_panel_id
            liver_panel_id += 1


# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()
