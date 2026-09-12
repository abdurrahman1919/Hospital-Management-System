import pyodbc

class Doctor:
    doctors=[]
    connect_string=("DRIVER={SQL Server};"
        "SERVER=DESKTOP-F606CCN\\SQLEXPRESS;"
        "DATABASE=Hospital_Management_System_db;"
        "TRUSTED_CONNECTION=YES;"
        "TRUSTSERVERCERTIFICATE=YES;")
    def __init__(self,doctor_id,name,specialization,phone,fee,availability):
        self.doctor_id=doctor_id
        self.name=name
        self.specialization=specialization
        self.phone=phone
        self.fee=fee
        self.availability=availability
        Doctor.doctors.append(self)
        

    def __str__(self):
        '''Return one object data in formated form'''
        return f'Dr_ID:{self.doctor_id}   Name:{self.name}    specialization:{self.specialization}      Phone:{self.phone}  Fee:{self.fee}  availability:{self.availability}\n'
    
    @classmethod
    def view_all_doctors(cls):
        '''This function show all doctors in database and all objects informantion'''
        print('\n.....ALL Doctors LIST.....\n')
        for i in cls.doctors:
            print(i)
    
    @classmethod
    def search_doctor(cls):
        '''This function search doctor record in database'''
        dnm=input('Enter Doctor name to search:')
        dno=0
        for i in cls.doctors:
            if dnm.capitalize()==i.name:
                print(f"ID:{i.doctor_id}   Name:{i.name}")
                dno+=1
        else:
            if dno==0:
                print("Not Found")

    @classmethod
    def update_doctor(cls):
        '''This function update availabel doctors data in database'''
        did=input('\nEnter Doctor ID to Update:')
        while True:
            edit=input("\nname , specialization , phone , fee , availability\nwhat you want to edit and enter \'exit\' to Exit from here:")
            if edit.lower() in [ 'doctor_id', 'name', 'specialization', 'phone', 'fee' , 'availability']:
                 with pyodbc.connect(cls.connect_string) as conn:
                    with conn.cursor() as cursor:
                        for i in cls.doctors:
                            if int(did)==i.doctor_id:
                                val=input(f'Enter new value of {edit} of Doctor {i.name} has ID {i.doctor_id}:')
                                if edit=="name":
                                    i.name=val
                                    cursor.execute('update doctor_tbl set doctor_name=? where doctor_id=?',val.capitalize(),did)
                                elif edit=="specialization":
                                    i.specialization=val
                                    cursor.execute('update doctor_tbl set specialization=? where doctor_id=?',val.capitalize(),did)
                                elif edit=="fee":
                                    i.fee=val
                                elif edit=="phone":
                                    i.phone=val
                                    cursor.execute('update doctor_tbl set phone=? where doctor_id=?',val.capitalize(),did)
            elif edit=='exit':
                return
            else:
                print('\n.....invalid input.....\n')

    @classmethod
    def del_doctor(cls):
        '''This function delete record of one doctor'''
        did=int(input('Enter Doctor id to delete:'))
        for i in cls.doctors:
            if i.doctor_id==did:
                con=input(f"Are you sure to delete doctor name:{i.name},ID={i.doctor_id}... y/n : ")
                if con.lower()=='y':
                    cls.doctors.remove(i)
                    try:
                        with pyodbc.connect(cls.connect_string) as conn:
                            with conn.cursor() as cursor:
                                 cursor.execute('delete from medical_record_tbl where doctor_id=?',did)
                                 cursor.execute('delete from appoinment_tbl where doctor_id=?',did)
                                 cursor.execute('delete from doctor_tbl where doctor_id=?',did)
                        print(f'Doctor that has id {i.doctor_id} has been removed..\n')
                    except Exception as e:
                        print(e)
                    break
                else:
                    print(f'Doctor that has id {i.doctor_id} not removed.\n')
                    break
        else:
             print('Record not found.....') 

    @classmethod
    def add_doctor(cls):
        '''This function add doctor to databse also make object'''
        if len(Doctor.doctors)>0:
            doctor_id=(Doctor.doctors[-1].doctor_id)+1
        else:
            doctor_id=1
        name=input("Enter Doctor name:")
        specialization=input("Enter Doctor specialization:")
        phone=input("Enter Doctor phone no:")
        fee=input("Enter Doctor fee:")
        availability=input('Enter Doctor availability:')
        p=Doctor(doctor_id, name, specialization, phone, fee,availability)
        try:
            with pyodbc.connect(cls.connect_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("insert into doctor_tbl values (?,?,?,?,?,?)",doctor_id,name.capitalize(),specialization.capitalize(),phone,fee,availability.capitalize())
        except Exception as e:
             print(e)
                          
    @classmethod
    def get_all_doctors(cls):
        '''This function take all data of doctors from database also make object of each record'''
        with pyodbc.connect(cls.connect_string) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute('select * from doctor_tbl')
                        rec=cursor.fetchall()
                        for i in range(len(rec)):
                            obj=Doctor(rec[i][0],rec[i][1],rec[i][2],rec[i][3],rec[i][4],rec[i][5])

