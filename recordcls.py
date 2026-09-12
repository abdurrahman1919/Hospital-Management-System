import pyodbc
from doctorcls import *
from appointmentcls import *
from datetime import *
class Medical_Record(Doctor,Appointment):
    records=[]
    checked=[]
    nochecked=[]
    connect_string=("DRIVER={SQL Server};"
        "SERVER=DESKTOP-F606CCN\\SQLEXPRESS;"
        "DATABASE=Hospital_Management_System_db;"
        "TRUSTED_CONNECTION=YES;"
        "TRUSTSERVERCERTIFICATE=YES;")
    def __init__(self,record_id,patient_id,doctor_id,appointment_id,status,diagnosis,prescrip):
        self.record_id=record_id
        self.patient_id=patient_id
        self.doctor_id=doctor_id
        self.appointment_id=appointment_id
        self.status=status
        self.diagnosis=diagnosis
        self.prescrip=prescrip
        Medical_Record.records.append(self)
        

    def __str__(self):
        '''Return one object data in formated form'''
        return f'Record_ID:{self.record_id}   Patient_ID:{self.patient_id}    DOctor_ID={self.doctor_id}  Appointment_ID:{self.appointment_id}    Status:{self.status}  Diagnosis:{self.diagnosis}  Prescrip:{self.prescrip}\n'
    
    @classmethod
    def view_all_records(cls):
        '''This function show all records in database and all objects informantion'''
        print('\n.....ALL RECORDS LIST.....\n')
        for i in cls.records:
            print(i)
    
    @classmethod
    def search_record(cls):
        '''This function search appoinment record in database'''
        reid=int(input('Enter Record ID to search:'))
        reno=0
        for i in cls.records:
            if reid==i.record_id:
                print(f"\nRecord_ID: {i.record_id}   Patient_ID: {i.patient_id}   Doctor_ID: {i.doctor_id}  Status: {i.status}    Prescrip:{i.prescrip}")
                reno+=1
        else:
            if reno==0:
                print("Not Found")

    @classmethod
    def del_record(cls):
        '''This function delete one record of patient'''
        reid=int(input('Enter record id to delete:'))
        for i in cls.records:
            if i.record_id==reid:
                con=input(f"Are you sure to delete Patient Record,  Record_ID={i.record_id}... y/n : ")
                if con.lower()=='y':
                    cls.records.remove(i)
                    try:
                        with pyodbc.connect(cls.connect_string) as conn:
                            with conn.cursor() as cursor:
                                 cursor.execute('delete from medical_record_tbl where record_id=?',reid)
                        print(f'Record that has id {i.record_id} has been removed..\n')
                    except Exception as e:
                        print(e)
                    break
                else:
                    print(f'Record that has id {i.record_id} not removed.\n')
                    break
        else:
             print('Record not found.....') 

    @classmethod
    def view_nochecked_specificDR(cls,drid):
        if len(cls.nochecked)>0:
            for i in cls.nochecked:
                if i[2]==drid:
                    print(f'\nAppointment_ID:{i[0]}   Patient_ID:{i[1]}   Date:{str(i[3])[:19]}    Reason:{i[5]}  Status:{i[4]}\n')
        else:
            print('\nempty')

    @classmethod
    def view_checked_specificDR(cls,drid):
        if len(cls.checked)>0:
            for i in cls.checked:
                if i[2]==drid:
                    print(f'\nAppointment_ID:{i[0]}   Patient_ID:{i[1]}   Date:{str(i[3])[:19]}    Reason:{i[5]}  Status:{i[4]}\n')
        else:
            print('\nempty')

    @classmethod
    def add_record(cls,drid):
        '''This function add record of patient in databse also make object'''
        cls.view_nochecked_specificDR(drid)
        apid=int(input('Enter appointment id you want to make record:'))
        if len(cls.records)>0:
            record_id=(cls.records[-1].record_id)+1
        else:
            record_id=1
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select patient_id,doctor_id from appoinment_tbl where doctor_id=? and appointment_id=?',drid,apid)
                rec=cursor.fetchall()
        patient_id=rec[0][0]
        doctor_id=rec[0][1]
        status='Medicine not given'
        diagnosis=input('What diagnosis you use for this patient:')
        print('Enter \'-\' after every medicine name\nExample: medicine_name-medicine_name-medicine_name')
        prescrip=input('Enter medicine of this patient(Enter \'-\' after every medicine name\nExample: medicine_name-medicine_name-medicine_name):')
        obj=Medical_Record(record_id,patient_id,doctor_id,apid,status,diagnosis,prescrip)
        try:
            with pyodbc.connect(cls.connect_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("insert into medical_record_tbl values (?,?,?,?,?,?,?)",record_id,patient_id,doctor_id,apid,prescrip,status,diagnosis)
                    cursor.execute("update appoinment_tbl set appointment_status='Checked' where appointment_id=?",apid)
            cls.add_checked_nuchk()
        except Exception as e:
             print(e)
                 
    @classmethod
    def get_all_records(cls):
        '''This function take all appoinments from database also make object of each record'''
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from medical_record_tbl')
                rec=cursor.fetchall()
                for i in range(len(rec)):
                    obj=Medical_Record(rec[i][0],rec[i][1],rec[i][2],rec[i][3],rec[i][5],rec[i][6],rec[i][4])

    @classmethod
    def add_checked_nuchk(cls):
        cls.nochecked=[]
        cls.checked=[]
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from appoinment_tbl')
                rec=cursor.fetchall()
                for i in rec:
                    if i[4]=='Not Checked':
                        cls.nochecked.append(i)
                    else:
                        cls.checked.append(i)

