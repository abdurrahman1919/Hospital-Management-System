import pyodbc
class Patient:
    patients=[]
    connect_string=("DRIVER={SQL Server};"
        "SERVER=DESKTOP-F606CCN\\SQLEXPRESS;"
        "DATABASE=Hospital_Management_System_db;"
        "TRUSTED_CONNECTION=YES;"
        "TRUSTSERVERCERTIFICATE=YES;")
    def __init__(self,patient_id,name,age,gender,phone,address,blood_group):
        self.patient_id=patient_id
        self.name=name
        self.age=age
        self.gender=gender
        self.phone=phone
        self.address=address
        self.blood_group=blood_group
        Patient.patients.append(self)
        

    def __str__(self):
        '''Return one object data in formated form'''
        return f'ID:{self.patient_id}   Name:{self.name}    age={self.age}  Gender:{self.gender}    Phone:{self.phone}  Address:{self.address}  Blood_Group:{self.blood_group}\n'
    
    @classmethod
    def view_all_patient(cls):
        '''This function show all patients in database and all objects informantion'''
        print('\n.....ALL PATIENT LIST.....\n')
        for i in cls.patients:
            print(i)
    
    @classmethod
    def search_patient(cls):
        '''This function search patient record in database'''
        pnm=input('Enter Patient name to search:')
        ppno=0
        for i in cls.patients:
            if pnm.capitalize()==i.name:
                print(f"ID:{i.patient_id}   Name:{i.name}")
                ppno+=1
        else:
            if ppno==0:
                print("Not Found")

    @classmethod
    def update_patient(cls):
        '''This function update availabel patient data in database'''
        pid=input('Enter Patient ID to Update:')
        while True:
            edit=input("\nname , age , gender , phone , address , blood_group\nwhat you want to edit and enter \'exit\' to Exit from here:")
            if edit.lower() in [ 'patient_id', 'name', 'age', 'gender', 'phone', 'address' ,'blood_group']:
                 with pyodbc.connect(cls.connect_string) as conn:
                    with conn.cursor() as cursor:
                        for i in cls.patients:
                            if int(pid)==i.patient_id:
                                val=input(f'Enter new value of {edit} of Patient {i.name} has ID {i.patient_id}:')
                                if edit=="name":
                                    i.name=val
                                    cursor.execute('update patient_tbl set patient_name=? where patient_id=?',val.capitalize(),pid)
                                elif edit=="age":
                                    i.age=val
                                    cursor.execute('update patient_tbl set age=? where patient_id=?',int(val),pid)
                                elif edit=="gender":
                                    i.gender=val
                                    cursor.execute('update patient_tbl set gender=? where patient_id=?',val.upper(),pid)
                                elif edit=="phone":
                                    i.phone=val
                                    cursor.execute('update patient_tbl set phone=? where patient_id=?',val,pid)
                                elif edit=="address":
                                    i.address=val
                                    cursor.execute('update patient_tbl set paddress=? where patient_id=?',val.capitalize(),pid)
                                elif edit=="blood_group":
                                    i.blood_group=val
                                    cursor.execute('update patient_tbl set blood_group=? where patient_id=?',val.upper(),pid)
                            
            elif edit=='exit':
                return
            else:
                print('\n.....invalid input.....\n')

    @classmethod
    def del_patient(cls):
        '''This function delete record of one patient'''
        pid=int(input('Enter patient id to delete:'))
        for i in cls.patients:
            if i.patient_id==pid:
                con=input(f"Are you sure to delete patient name:{i.name},ID={i.patient_id}... y/n : ")
                if con.lower()=='y':
                    cls.patients.remove(i)
                    try:
                        with pyodbc.connect(cls.connect_string) as conn:
                            with conn.cursor() as cursor:
                                 cursor.execute('delete from medical_record_tbl where patient_id=?',pid)
                                 cursor.execute('delete from appoinment_tbl where patient_id=?',pid)
                                 cursor.execute('delete from bill_tbl where patient_id=?',pid)
                                 cursor.execute('delete from patient_tbl where patient_id=?',pid)
                        print(f'Patient that has id {i.patient_id} has been removed..\n')
                    except Exception as e:
                        print(e)
                    break
                else:
                    print(f'Patient that has id {i.patient_id} not removed.\n')
                    break
        else:
             print('Record not found.....') 

    @classmethod
    def add_patent(cls):
        '''This function add patient to databse also make object'''
        Patient.patients=[]
        Patient.get_all_patients()
        if len(Patient.patients)>0:
            patient_id=(Patient.patients[-1].patient_id)+1
        else:
            patient_id=1
        name=input("Enter Patient name:")
        age=int(input("Enter Patient age:"))
        gender=input("Enter Patient gender:")
        phone=input("Enter Patient phone no:")
        address=input("Enter Patient address:")
        blood_group=input('Enter Patent blood group:')
        p=Patient(patient_id, name, age, gender, phone, address,blood_group)
        try:
            with pyodbc.connect(cls.connect_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("insert into patient_tbl values (?,?,?,?,?,?,?)",patient_id,name.capitalize(),age,gender.upper(),phone,address.capitalize(),blood_group.upper())
        except Exception as e:
             print(e)
                          
    @classmethod
    def get_all_patients(cls):
        '''This function take all data of patients from database also make object of each record'''
        with pyodbc.connect(cls.connect_string) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute('select * from patient_tbl')
                        rec=cursor.fetchall()
                        for i in range(len(rec)):
                            obj=Patient(rec[i][0],rec[i][1],rec[i][2],rec[i][3],rec[i][4],rec[i][5],rec[i][6])
