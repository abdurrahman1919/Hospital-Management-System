from appointmentcls import *
from doctorcls import *
from recordcls import *
from medicineManagementcls import *
from billcls import *
from patientcls import *

print('.'*10,'HOSPITAL MANAGEMENT SYSTEM','.'*10)
print('1.Appointment Manager\n2.Doctor\n3.Medicine Manager\n4.Pharmacy\n5.Cashier\n6.Hospital Manager')
you=int(input('Who are you...?(1,2,3,4,5,6)'))

if you==1:
    print('\n==========(Appointment Manager)==========')
    Appointment.get_all_appoinments()
    while True:
        print('1.See all Appoinments\n2.New Appoinment\n3.Search Appoinment\n4.Delete Appoinment\n5.exit')
        choice=int(input('Enter here(1,2,3,4,5):'))
        if choice==1:
            Appointment.view_all_appoinments()
        elif choice==2:
            Appointment.add_appoinment()
        elif choice==3:
            Appointment.search_appoinment()
        elif choice==4:
            Appointment.del_appoinment()
        elif choice==5:
            break
        else:
            print('Invalid Input')
elif you==2:
    print('\n==========(Doctor)==========')
    docid=int(input('Dr, enter your Doctor ID:'))
    Medical_Record.get_all_records()
    Medical_Record.add_checked_nuchk()
    while True:
            print('1.See Checked Appoinments\n2.See NOt Checked Appoinments\n3.Check Patient\n4.exit')
            choice=int(input('Enter here(1,2,3,4):'))
            if choice==1:
                Medical_Record.view_checked_specificDR(docid)
            elif choice==2:
                Medical_Record.view_nochecked_specificDR(docid)
            elif choice==3:
                Medical_Record.add_record(docid)
            elif choice==4:
                break
            else:
                print('Invalid Input')
elif you==3:
    print('\n==========(Medicine Manager)==========')
    Medicine.get_all_medicines()
    while True:
        print('1.View All Medicine\n2.Search Medicine\n3.Update Medicine\n4.Delete Medicine\n5.Add Medicine\n6.exit')
        choice=int(input('Enter here(1,2,3,4,5,6):'))
        if choice==1:
            Medicine.view_all_medicine()
        elif choice==2:
            Medicine.search_medicine()
        elif choice==3:
            Medicine.update_medicine()
        elif choice==4:
            Medicine.del_medicine()
        elif choice==5:
            Medicine.add_medicine()
        elif choice==6:
            break
        else:
            print('Invalid Input')
elif you==4:
    print('\n==========(Pharmacy)==========')
    Medicine.get_all_medicines()
    Medicine.take_medicine_notgive()
    Medicine.take_medicine_give()
    while True:
        print('\n1.See Prescription (Medicine to give)\n2.See done Prescription\n3.Give Medicine to Patient\n4.exit')
        choice=int(input('Enter here(1,2,3,4):'))
        if choice==1:
            Medicine.show_ndoneMrecord()
        elif choice==2:
            Medicine.show_doneMrecord()
        elif choice==3:
            Medicine.give_medicine()
        elif choice==4:
            break
        else:
            print('Invalid Input')
elif you==5:
    print('\n==========(Cashier)==========')
    Bill.get_all_bills()
    while True:
            print('\n1.View all Bills\n2.Search Bill\n3.Delete Bill\n4.View Unpaid Bills\n5.View Paid Bills\n6.Bill Paying\n7.exit')
            choice=int(input('Enter here(1,2,3,4,5,6,7):'))
            if choice==1:
                Bill.view_all_bills()
            elif choice==2:
                Bill.search_bill()
            elif choice==3:
                Bill.del_bill()
            elif choice==4:
                Bill.view_unpaid_bills()
            elif choice==5:
                Bill.view_paid_bills()
            elif choice==6:
                Bill.paying_bill()
            elif choice==7:
                break
            else:
                print('Invalid Input')
elif you==6:
    print('\n==========(Hospital Manager)==========')
    while True:
        Patient.get_all_patients()
        Doctor.get_all_doctors()
        Appointment.get_all_appoinments()
        Medical_Record.get_all_records()
        Medicine.get_all_medicines()
        Medicine.take_medicine_give()
        Medicine.take_medicine_notgive()
        Bill.get_all_bills()
        print('\n1.Patient Section\n2.Doctor Section\n3.Appoinmnet Section\n4.Medical Record Section\n5.Medicine Section\n6.Pharmacy Section\n7.Bill Section\n8.exit')
        choice=int(input('Enter here(1,2,3,4,5,6,7):'))
        if choice==1:
            print('\n..........(Patient Section)..........')
            while True:
                print('\n1.View all Patients\n2.Search Patient\n3.Upadate Patient\n4.Delete Patient\n5.exit')
                sec_choice=int(input('Enter here(1,2,3,4,5):2'))
                if sec_choice==1:
                    Patient.view_all_patient()
                elif sec_choice==2:
                    Patient.search_patient()
                elif sec_choice==3:
                    Patient.update_patient()
                elif sec_choice==4:
                    Patient.del_patient()
                elif sec_choice==5:
                    break
                else:
                    print('Invalid Input')
        elif choice==2:
            print('\n..........(Doctor Section)..........')
            while True:
                print('\n1.View all Doctors\n2.Search Doctor\n3.Upadate Dcotor\n4.Delete Dcotor\n5.Add Doctor\n6.exit')
                sec_choice=int(input('Enter here(1,2,3,4,5,6):'))
                if sec_choice==1:
                    Doctor.view_all_doctors()
                elif sec_choice==2:
                    Doctor.search_doctor()
                elif sec_choice==3:
                    Doctor.update_doctor()
                elif sec_choice==4:
                    Doctor.del_doctor()
                elif sec_choice==5:
                    Doctor.add_doctor()
                elif sec_choice==6:
                    break
                else:
                    print('Invalid Input')
        elif choice==3:
            print('\n..........(Appoinmnet Section)..........')
            while True:
                print('\n1.View all Appoinments\n2.Search Appoinment\n3.Delete Appoinment\n4.exit')
                sec_choice=int(input('Enter here(1,2,3,4):'))
                if sec_choice==1:
                    Appointment.view_all_appoinments()
                elif sec_choice==2:
                    Appointment.search_appoinment()
                elif sec_choice==3:
                    Appointment.del_appoinment()
                elif sec_choice==4:
                    break
                else:
                    print('Invalid Input')
        elif choice==4:
            print('\n..........(Medical Record Section)..........')
            while True:
                print('\n1.View all Medical Records\n2.Search Medical Record\n3.Delete Medical Record\n4.exit')
                sec_choice=int(input('Enter here(1,2,3,4,5):'))
                if sec_choice==1:
                    Medical_Record.view_all_records()
                elif sec_choice==2:
                    Medical_Record.search_record()
                elif sec_choice==3:
                    Medical_Record.del_record()
                elif sec_choice==4:
                    break
                else:
                    print('Invalid Input')
        elif choice==5:
            print('\n..........(Medicine Section)..........')
            while True:
                print('\n1.View all Medicine\n2.Search Medicine\n3.Delete Medicine\n4.Update Medicine\n5.Add Medicine\n6.exit')
                sec_choice=int(input('Enter here(1,2,3,4,5):'))
                if sec_choice==1:
                    Medicine.view_all_medicine()
                elif sec_choice==2:
                    Medicine.search_medicine()
                elif sec_choice==3:
                    Medicine.del_medicine()
                elif sec_choice==4:
                    Medicine.update_medicine()
                elif sec_choice==5:
                    Medicine.add_medicine()
                elif sec_choice==6:
                    break
                else:
                    print('Invalid Input')
        elif choice==6:
            print('\n..........(Pharmacy Section)..........')
            while True:
                print('\n1.View Done Prescription\n2.View not Done Prescription\n3.exit')
                sec_choice=int(input('Enter here(1,2,3,4,5):'))
                if sec_choice==1:
                    Medicine.show_doneMrecord()
                elif sec_choice==2:
                    Medicine.show_ndoneMrecord()
                elif sec_choice==3:
                    break
                else:
                    print('Invalid Input')
        elif choice==7:
            print('\n..........(Bill Section)..........')
            while True:
                print('\n1.View all Bills\n2.Search Bill\n3.Delete Bill\n4.View Paid Bills\n5.View Unpaid Bills\n6.exit')
                sec_choice=int(input('Enter here(1,2,3,4,5):'))
                if sec_choice==1:
                    Bill.view_all_bills()
                elif sec_choice==2:
                    Bill.search_bill()
                elif sec_choice==3:
                    Bill.del_bill()
                elif sec_choice==4:
                    Bill.view_paid_bills()
                elif sec_choice==5:
                    Bill.view_unpaid_bills()
                elif sec_choice==6:
                    break
                else:
                    print('Invalid Input')
        elif choice==8:
            break
        else:
            print('invalid Input')
else:
    print('Invalid Input')