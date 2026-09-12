import pyodbc
from datetime import *
from billcls import *
class Medicine(Bill):
    medicines=[]
    medicinetogive=[]
    medicinegive=[]
    bills=[]
    connect_string=("DRIVER={SQL Server};"
        "SERVER=DESKTOP-F606CCN\\SQLEXPRESS;"
        "DATABASE=Hospital_Management_System_db;"
        "TRUSTED_CONNECTION=YES;"
        "TRUSTSERVERCERTIFICATE=YES;")
    
    def __init__(self,medicine_id,name,category,price,quantity,expiry_date):
        self.medicine_id=medicine_id
        self.name=name
        self.category=category
        self.price=price
        self.quantity=quantity
        self.expiry_date=expiry_date
        Medicine.medicines.append(self)
        

    def __str__(self):
        '''Return one object data in formated form'''
        return f'ID:{self.medicine_id}   Medicine_Name:{self.name}    Category={self.category}  Price:{self.price}    Quantity:{self.quantity}  Expiry_Date:{self.expiry_date}\n'
    
    @classmethod
    def view_all_medicine(cls):
        '''This function show all medicine in database and all objects informantion'''
        print('\n.....ALL MEDICINE LIST.....\n')
        for i in cls.medicines:
            print(i)
    
    @classmethod
    def search_medicine(cls):
        '''This function search medicine record in database'''
        mnm=input('Enter Medicine name to search:')
        mno=0
        cls.medicines=[]
        cls.get_all_medicines()
        for i in cls.medicines:
            if mnm.capitalize()==i.name:
                print(f"\nID:{i.medicine_id}   Name:{i.name}  Quantity:{i.quantity}   Expiry_Date:{i.expiry_date}")
                mno+=1
        else:
            if mno==0:
                print("Not Found")

    @classmethod
    def update_medicine(cls):
        '''This function update availabel medicine data in database'''
        mid=input('Enter Medicine ID to Update:')
        while True:
            edit=input("\nname, category, price, quantity, expiry_date\nwhat you want to edit (enter \'exit\' to Exit from here):")
            if edit.lower() in ['medicine_id', 'name', 'category', 'price', 'quantity','expiry_date']:
                 with pyodbc.connect(cls.connect_string) as conn:
                    with conn.cursor() as cursor:
                        for i in cls.medicines:
                            if int(mid)==i.medicine_id:
                                val=input(f'Enter new value of {edit} of {i.name} has ID {i.medicine_id}:')
                                if edit=="name":
                                    i.name=val
                                    cursor.execute('update medicine_tbl set medicine_name=? where medicine_id=?',val.capitalize(),mid)
                                elif edit=="category":
                                    i.category=val
                                    cursor.execute('update medicine_tbl set category=? where medicine_id=?',val.capitalize(),mid)
                                elif edit=="price":
                                    i.price=int(val)
                                    cursor.execute('update medicine_tbl set price=? where medicine_id=?',int(val),mid)
                                elif edit=="quantity":
                                    i.quantity=int(val)
                                    cursor.execute('update medicine_tbl set quantity=? where medicine_id=?',int(val),mid)
                                elif edit=="expiry_date":
                                    i.expiry_date=val
                                    cursor.execute('update medicine_tbl set medicine_expiry_date=? where medicine_id=?',val,mid)
                            
            elif edit=='exit':
                return
            else:
                print('\n.....invalid input.....\n')

    @classmethod
    def del_medicine(cls):
        '''This function delete record of one medicine'''
        mid=int(input('Enter Medicine id to delete:'))
        for i in cls.medicines:
            if i.medicine_id==mid:
                con=input(f"Are you sure to delete medicine name:{i.name},ID={i.medicine_id}... y/n : ")
                if con.lower()=='y':
                    cls.medicines.remove(i)
                    try:
                        with pyodbc.connect(cls.connect_string) as conn:
                            with conn.cursor() as cursor:
                                 cursor.execute('delete from medicine_tbl where medicine_id=?',mid)
                        print(f'Medicine that has id {i.medicine_id} has been removed..\n')
                    except Exception as e:
                        print(e)
                    break
                else:
                    print(f'Medicine that has id {i.medicine_id} not removed.\n')
                    break
        else:
             print('Record not found.....') 

    @classmethod
    def add_medicine(cls):
        '''This function add medicine to databse also make object'''
        if len(Medicine.medicines)>0:
            medicine_id=(Medicine.medicines[-1].medicine_id)+1
        else:
            medicine_id=1
        name=input("Enter Medicine name:")
        category=input("Enter Medicine category:")
        price=input("Enter Medicine price:")
        quantity=input("Enter Medicine quantity:")
        expiry_date=input("Enter Medicine expiry_date:")
        p=Medicine(medicine_id,name,category,price,quantity,expiry_date)
        try:
            with pyodbc.connect(cls.connect_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("insert into medicine_tbl values (?,?,?,?,?,?)",medicine_id,name.capitalize(),category.capitalize(),price,quantity,expiry_date)
        except Exception as e:
             print(e)

    @classmethod
    def show_ndoneMrecord(cls):
        '''show all prescripts of patient whose medicine we need to give'''
        if len(cls.medicinetogive)>0:
            for i in cls.medicinetogive:
                print(f'\nRecord_ID:{i[0]}   Patient_ID:{i[1]}    DOctor_ID={i[2]}    Status:{i[5]}  Prescrip:{i[4]}')
        else:
            print('\nempty')
            
    @classmethod
    def show_doneMrecord(cls):
        '''show all prescripts of patient whose medicine we need to give'''
        if len(cls.medicinegive)>0:
            for i in cls.medicinegive:
                print(f'\nRecord_ID:{i[0]}   Patient_ID:{i[1]}    DOctor_ID={i[2]}    Status:{i[5]}  Prescrip:{i[4]}')
        else:
            print('\nempty')

    @classmethod
    def add_medicine_inBill(cls,recid,bid):
        '''This fumction calculate medicine price and data for bill medicine table'''
        medicine_charges=0
        Bill.current_bill=[]
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from medical_record_tbl where record_id=?',recid)
                rec=cursor.fetchone()
                med_name=rec[4].split('-')
                query=f'select * from medicine_tbl where medicine_name in ({'?,'*len(med_name)})'
                query=query[:-2]+query[-1]
                cursor.execute(query,med_name)
                medrec=cursor.fetchall()
                print('\n...Give these medicines...')
                for i in medrec:
                    if i[4]>10:
                        if i[5]>str(datetime.now()):
                            print(f"\nMedicine_ID:{i[0]}  Name:{i[1]} Quantity:{i[4]} Expiery_Date:{i[5]}")
                            choice=input('You enter this medicine (y/n) :')
                            if choice.lower()=='y':
                                quantity=int(input(f'Enter quantity of {i[1]}:'))
                                Bill.current_bill.append((bid,i[0]))
                                cursor.execute('update medicine_tbl set quantity=? where medicine_id=?',i[4]-quantity,i[0])
                                for k in Medicine.medicines:
                                    if k.medicine_id==i[0]:
                                        i.quantity-=quantity
                                        break
                                medicine_charges+=(quantity*i[3])
                            else:
                                print('\nMedicine not added....\n')
                        else:
                            print(f"Medicine_ID:{i[0]}  Name:{i[1]} Expiery_Date:{i[5]}")
                            print('Medicine is expired....')
                    else:
                        print(f"Medicine_ID:{i[0]}  Name:{i[1]} Quantity:{i[4]}")
                        print('Medicine out of stock, and less then 10....')
        return medicine_charges
                        
    @classmethod
    def give_medicine(cls):
        '''This function add record of precrip/medicine in bill table and make status of medical record to medicine given'''
        cls.show_ndoneMrecord()
        if len(Medicine.medicinetogive)>0:
            recid=int(input('\nEnter Record ID of those record you want to give medicine:'))
            Bill.bills=[]
            Bill.get_all_bills()
            if len(Bill.bills)>0:
                bill_id=(Bill.bills[-1].bill_id)+1
            else:
                bill_id=1
            with pyodbc.connect(cls.connect_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('select patient_id,doctor_id from medical_record_tbl where record_id=?',recid)
                    pid_did=cursor.fetchone()
                    patient_id=pid_did[0]
                    dcotor_id=pid_did[1]
                    cursor.execute('select fee from doctor_tbl where doctor_id=?',dcotor_id)
                    fee=cursor.fetchone()[0]
                    medicine_charges=cls.add_medicine_inBill(recid,bill_id)
                    payment_status='Unpaid'
                    discount=((int(fee)+medicine_charges)/100)*10
                    total=medicine_charges+int(fee)-discount
                    obj=Bill(bill_id,patient_id,fee,medicine_charges,discount,total,payment_status)
                    cursor.execute('insert into bill_tbl values (?,?,?,?,?,?,?)',bill_id,patient_id,fee,medicine_charges,discount,total,payment_status)
                    cursor.execute("update  medical_record_tbl set mstatus='Medicine given' where record_id=?",recid)
                    for i in Bill.current_bill:
                        cursor.execute('insert into bill_medicine_tbl values (?,?)',i[0],i[1])
            cls.medicinetogive=[]
            cls.medicinegive=[]
            cls.take_medicine_notgive()
            cls.take_medicine_give()
            print('\nMedicine has been given....\n///////////////////////////////////')
            
    @classmethod
    def take_medicine_notgive(cls):
        '''take those medical record whose status is medicine not given'''
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("select * from medical_record_tbl where mstatus='Medicine not given'")
                rec=cursor.fetchall()
                for i in rec:
                    cls.medicinetogive.append(i)

    @classmethod
    def take_medicine_give(cls):
        '''take those medical record whose status is medicine given'''
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("select * from medical_record_tbl where mstatus='Medicine given'")
                rec=cursor.fetchall()
                for i in rec:
                    cls.medicinegive.append(i)

    @classmethod
    def get_all_medicines(cls):
        '''This function take all data of medicines from database also make object of each record'''
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from medicine_tbl')
                rec=cursor.fetchall()
                for i in range(len(rec)):
                    obj=Medicine(rec[i][0],rec[i][1],rec[i][2],rec[i][3],rec[i][4],rec[i][5])
