import pyodbc
from patientcls import *
from doctorcls import *
from datetime import *
class Appointment(Patient):
    appointments=[]
    connect_string=("DRIVER={SQL Server};"
        "SERVER=DESKTOP-F606CCN\\SQLEXPRESS;"
        "DATABASE=Hospital_Management_System_db;"
        "TRUSTED_CONNECTION=YES;"
        "TRUSTSERVERCERTIFICATE=YES;")
    def __init__(self,appointment_id,patient_id,doctor_id,reason,status,dattim):
        self.appointment_id=appointment_id
        self.patient_id=patient_id
        self.doctor_id=doctor_id
        self.date_time=dattim
        self.reason=reason
        self.status=status
        Appointment.appointments.append(self)
        

    def __str__(self):
        '''Return one object data in formated form'''
        return f'ID:{self.appointment_id}   Patient_ID:{self.patient_id}    Doctor_ID={self.doctor_id}  Date:{self.date_time}    Reason:{self.reason}  Status:{self.status}\n'
    
    @classmethod
    def view_all_appoinments(cls):
        '''This function show all appoinments in database and all objects informantion'''
        print('\n.....ALL APPOINTMENTS LIST.....\n')
        for i in cls.appointments:
            print(i)

    @classmethod
    def search_appoinment(cls):
        '''This function search appoinment record in database'''
        apid=int(input('Enter Appoinment ID to search:'))
        apno=0
        for i in cls.appointments:
            if apid==i.appointment_id:
                print(f"\nID: {i.appointment_id}   Patient_ID: {i.patient_id}   Doctor_ID: {i.doctor_id}  Status: {i.status}")
                apno+=1
        else:
            if apno==0:
                print("Not Found")

    @classmethod
    def del_appoinment(cls):
        '''This function delete one appoinment'''
        apid=int(input('Enter appoinment id to delete:'))
        for i in cls.appointments:
            if i.appointment_id==apid:
                con=input(f"Are you sure to delete appoinment  ID={i.appointment_id}... y/n : ")
                if con.lower()=='y':
                    cls.appointments.remove(i)
                    try:
                        with pyodbc.connect(cls.connect_string) as conn:
                            with conn.cursor() as cursor:
                                 cursor.execute('delete from medical_record_tbl where appointment_id=?',apid)
                                 cursor.execute('delete from appoinment_tbl where appointment_id=?',apid)
                        print(f'Appoinment that has id {i.appointment_id} has been removed..\n')
                    except Exception as e:
                        print(e)
                    break
                else:
                    print(f'Appoinment that has id {i.appointment_id} not removed.\n')
                    break
        else:
             print('Record not found.....') 

    @classmethod
    def add_appoinment(cls):
        '''This function add appoinment in databse also make object'''
        if len(Appointment.appointments)>0:
            appoinment_id=(Appointment.appointments[-1].appointment_id)+1
        else:
            appoinment_id=1
        super().add_patent()
        patient_id=super().patients[-1].patient_id
        Doctor.doctors=[]
        Doctor.get_all_doctors()
        Doctor.view_all_doctors()
        doctor_id=int(input("Enter Doctor ID :"))
        reason=input("Enter Reason of Appoinment:")
        status='Not Checked'
        dattim=datetime.now()
        a=Appointment(appoinment_id,patient_id,doctor_id, reason,status,dattim)
        try:
            with pyodbc.connect(cls.connect_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("insert into appoinment_tbl values (?,?,?,?,?,?)",appoinment_id,patient_id,doctor_id,dattim,status,reason)
        except Exception as e:
             print(e)
                          
    @classmethod
    def get_all_appoinments(cls):
        '''This function take all appoinments from database also make object of each record'''
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from appoinment_tbl')
                rec=cursor.fetchall()
                for i in range(len(rec)):
                    obj=Appointment(rec[i][0],rec[i][1],rec[i][2],rec[i][3],rec[i][4],rec[i][5])
