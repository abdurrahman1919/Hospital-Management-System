import pyodbc

class Bill:
    bills=[]
    current_bill=[(1,2),(1,3)]
    connect_string=("DRIVER={SQL Server};"
        "SERVER=DESKTOP-F606CCN\\SQLEXPRESS;"
        "DATABASE=Hospital_Management_System_db;"
        "TRUSTED_CONNECTION=YES;"
        "TRUSTSERVERCERTIFICATE=YES;")
    def __init__(self,bill_id,patient_id,doctor_fee,medicine_charges,discount,total,payment_status):
        self.bill_id=bill_id
        self.patient_id=patient_id
        self.doctor_fee=doctor_fee
        self.medicine_charges=medicine_charges
        self.discount=discount
        self.total=total
        self.payment_status=payment_status
        Bill.bills.append(self)
        

    def __str__(self):
        '''Return one object data in formated form'''
        return f'Bill_ID:{self.bill_id}   Patient_ID:{self.patient_id}    Doctor_fee={self.doctor_fee}  Medicine_Charges:{self.medicine_charges}    Discount:{self.discount}  Total:{self.total}  Payment_Status:{self.payment_status}\n'
    
    @classmethod
    def view_all_bills(cls):
        '''This function show all bills in database and all objects informantion'''
        print('\n.....ALL BILLS LIST.....\n')
        for i in cls.bills:
            print(i)
    
    @classmethod
    def search_bill(cls):
        '''This function search bill record in database'''
        bid=int(input('Enter bill ID to search:'))
        pid=int(input('Enter patient ID to search:'))
        reno=0
        for i in cls.bills:
            if bid==i.bill_id and pid==i.patient_id:
                print(f"\nBill_ID: {i.bill_id}   Patient_ID: {i.patient_id}   Doctor_Fee: {i.doctor_fee}  Medicine_Charges: {i.medicine_charges}    Discount:{i.discount} Total:{i.total} Payment_Status:{i.payment_status}")
                reno+=1
        else:
            if reno==0:
                print("\nNot Found")

    @classmethod
    def del_bill(cls):
        '''This function delete one bill'''
        bid=int(input('Enter bill id to delete:'))
        for i in cls.bills:
            if i.bill_id==bid:
                con=input(f"Are you sure to delete Bill,  Bill_ID={i.bill_id}... y/n : ")
                if con.lower()=='y':
                    cls.bills.remove(i)
                    try:
                        with pyodbc.connect(cls.connect_string) as conn:
                            with conn.cursor() as cursor:
                                 cursor.execute('delete from bill_medicine_tbl where bill_id=?',bid)
                                 cursor.execute('delete from bill_tbl where bill_id=?',bid)
                        print(f'Bill that has id {i.bill_id} and Patietn ID:{i.patient_id} has been removed..\n')
                    except Exception as e:
                        print(e)
                    break
                else:
                    print(f'Bill that has id {i.bill_id} and Patietn ID:{i.patient_id} not removed..\n')                    
                    break
        else:
             print('Record not found.....') 

    @classmethod
    def view_unpaid_bills(cls):
        '''Show all unpaid bills'''
        print()
        if len(Bill.bills)>0:
            for i in Bill.bills:
                if i.payment_status=='Unpaid':
                    print(i)
        else:
            print('empty')
    
    @classmethod
    def view_paid_bills(cls):
        '''Show all paid bills'''
        print()
        if len(Bill.bills)>0:
            for i in Bill.bills:
                if i.payment_status=='Paid':
                    print(i)
        else:
            print('empty')

    @classmethod
    def paying_bill(cls):
        '''changing bill status to paid'''
        cls.view_unpaid_bills()
        bid=int(input('Enter bill id to pay bill:'))
        for i in Bill.bills:
            if i.bill_id==bid:
                print(F'\n\n.........HOSPITAL BILL.........')
                print(f'Bill_ID:{i.bill_id}         Patient_ID:{i.patient_id}\n\t....ITEMS....\n')
                with pyodbc.connect(cls.connect_string) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute('select * from bill_medicine_tbl where bill_id=?',i.bill_id)
                        mrdid=cursor.fetchall()[1]
                        query=f'select * from medicine_tbl where medicine_id in ({'?,'*len(mrdid)})'
                        query=query[:-2]+query[-1]
                        cursor.execute(query,mrdid)
                        rec=cursor.fetchall()
                        itmno=1
                        for j in rec:
                            print(f'{itmno}.{j[1]}')
                            itmno+=1
                        print('\n      ...ALL CHARGES...')
                        print(f'\nDr_Fee:              {i.doctor_fee}\nMedicine_Charges:     {i.medicine_charges}\nDiscount:             {i.discount}\n')
                        print(f'...............................\n    TOTAL BILL:   {i.total}\n...............................\n')
                        choice=input('Enter \'ok\' to pay bill:')
                        if choice.lower()=='ok':
                            cursor.execute("update bill_tbl set payment_status='Paid' where bill_id=?",bid)
                i.payment_status='Paid'         
                print('\nBill has been paid...')

    @classmethod
    def get_all_bills(cls):
        '''This function take all bills from database also make object of each record'''
        with pyodbc.connect(cls.connect_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from bill_tbl')
                rec=cursor.fetchall()
                for i in range(len(rec)):
                    obj=Bill(rec[i][0],rec[i][1],rec[i][2],rec[i][3],rec[i][4],rec[i][5],rec[i][6])
