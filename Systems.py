"""
    Documentation:

        In this module, there are four functions-
            
            1) EmployeeManagementSystem()
            2) InventoryManagementSystem()
            3) BankManagementSystem()
            4) dbManagementSystem()

            EmployeeManagementSystem() allows you to-
                >>> Add new employee, delete existing employee.
                >>> Update salary.

            InventoryManagementSystem() allows you to-
                >>> Add new item, delete existing item.
                >>> Recieve goods, and create GRN records.
                >>> Sell goods, and create invoice records.
                >>> Show bill for sold goods.

            BankManagementSystem() allows you to-
                >>> Add new customer, delete existing customer.
                >>> Create new accounts, delete existing accounts.
                >>> Deposit, withdraw, get loans, repay loans.

            dbManagementSystem() allows you to manage you employee database tables(add,delete,rename,change a table or column).

"""

#-- EMPLOYEE MANAGEMENT SYSTEM --#
def EmployeeManagementSystem():
    #IMPORT CONNECTOR
    import mysql.connector

    #SET THE DATABASE AND CURSOR
    mydb = mysql.connector.connect(user='root',
                                   password='Pranav123@MySQL',
                                   host='127.0.0.1',
                                   database='employee_database')

    cur = mydb.cursor()

    print('\n')
    print("===============================================================================")
    print("==============================EMPLOYEE MANAGEMENT==============================")
    print("===============================================================================")
    print('\n')

    #PROGRAM AND QUERY HERE 
    while True:  
        print("Choose from the options below to manage your employee data:\n")
        print('''Options:
            1. Manage your employee data.
            2. View your employee data.
            3. Exit.
        ''')

        menuchoice = int(input("Enter your choice: "))
        if menuchoice == 1:                
            #EMPLOYEE DATA MANAGEMENT
            while True:
                print("Choose from the options below to manage your employee data:\n")
                print('''Options:
                    1. Add a new employee.
                    2. Delete a current existing employee.
                    3. Update the salary.  
                    4. Back to menu.
                ''')         
                option=int(input("\nEnter your Option: "))                        
                
                while True:
                    #add new employee
                    if option==1:
                        print("\nAdd new employee's details-\n")
                        emp_id = input("Enter employee ID: ")
                        emp_name = input("Enter employee name: ")
                        emp_dept_id = input("Enter department ID: ")
                        emp_email = input("Enter employee email-ID: ")
                        emp_mobile = input("Enter employee mobile no.: ")
                        emp_country = input("Enter employee country: ")
                        emp_state = input("Enter employee state: ")
                        emp_city = input("Enter employee city: ")
                        
                        cur.execute('insert into employee_master(emp_id,emp_name,emp_dept_id) values("{}","{}","{}")'.format(emp_id,emp_name,emp_dept_id))
                        
                        cur.execute('insert into employee_data values("{}","{}","{}","{}")'.format(emp_id,emp_name,emp_email,emp_mobile))
                                                    
                        cur.execute('insert into employee_location values("{}","{}","{}","{}","{}")'.format(emp_id,emp_name,emp_country,emp_state,emp_city))
                                                    
                        cur.execute('insert into salary_master(emp_id,dept_id) values("{}","{}")'.format(emp_id,emp_dept_id))
                                                    
                        cur.execute('update employee_master,department_master '
                        'set employee_master.emp_dept_name = department_master.dept_name '
                        'where employee_master.emp_dept_id = department_master.dept_id')

                        print("\nEmployee registered in database successfully!\n")
                        mydb.commit()
                        print("Go to option 3 to update salary immediately\n")
                        print('-'*30)
                        repeat_add_empl=input("Do you want to add another employee? (y/n)")
                        if repeat_add_empl.upper() not in ('Y','YES'):
                            break

                    #delete employee
                    elif option==2:
                        print("\nDelete existing employee-\n")           
                                                                       
                        print("Enter the ID keys of required employees one-by-one and press enter to break loop.")
                        empchoice = []
                        while True:                
                            a = input("Enter employee ID: ")
                            if a=='':
                                break
                            empchoice.append(a)
                            
                        empstring=''
                        for i in empchoice:
                            empstring+=i+','
                        empstring=empstring[:-1]
                        print()
                        
                        cur.execute('delete from salary_master where emp_id in ("{}")'.format(empstring))
                        cur.execute('delete from employee_location where emp_id in ("{}")'.format(empstring))
                        cur.execute('delete from employee_data where emp_id in ("{}")'.format(empstring))
                        cur.execute('delete from employee_master where emp_id in ("{}")'.format(empstring))
                        mydb.commit()
                        print("\nEmployee deleted from database successfully!\n")
                        print('-'*30)

                        repeat_del_empl=input("Do you want to delete another employee? (y/n)")
                        if repeat_del_empl.upper() not in ('Y','YES'):
                            break

                    #salary update
                    elif option==3:
                        print("\nUpdate existing employee's salary-\n")
                        emp_id = input("Enter employee ID to add/update salary: ")     
                        salary = int(input("Enter the salary: "))
                        cur.execute('update salary_master '
                                    'set emp_salary = ' 
                                    '   case '
                                    '       when emp_salary is null then {} '
                                    '       else {} '
                                    '   end '
                                    'where emp_id = "{}"'.format(salary,salary,emp_id))

                        print("\nSalary updated successfully!\n")
                        mydb.commit()
                        print('-'*30)
                        repeat_sal_update=input("Do you want to add another employee's salary? (y/n)")
                        if repeat_sal_update.upper() not in ('Y','YES'):
                            break

                    elif option==4:
                        break
                
                    else:
                        print("Sorry ... wrong entry ... \n")
                        break
                    
                repeat=input("Do you want to change anything else (MAIN MENU) ? (y/n)")
                if repeat.upper() not in ('Y','YES'):
                    break
                    
        elif menuchoice == 2:            
            #EMPLOYEE DATAVIEW                     
            cur.execute('truncate table employee_display')

            cur.execute('insert into employee_display '
                        'select e.emp_id, e.emp_name, e.emp_dept_id, d.dept_name, ed.emp_email, ed.emp_mobile, s.emp_salary, el.emp_country, el.emp_state, el.emp_city '
                        'from employee_master e, salary_master s, employee_data ed, employee_location el, department_master d ' 
                        'where e.emp_id=s.emp_id and e.emp_dept_id=d.dept_id and e.emp_id = ed.emp_id and e.emp_id = el.emp_id')

            mydb.commit()

            while True:
                print("Choose from the options below to select your view form:\n")
                print('''\n
            Do you want to see the data of- 
                    1.  All employees.
                    2.  Specific employees.
                    3.  Except for specific employees.
                    4.  Back to menu.
                ''')
                print()
                viewoption = int(input("Select your view form: "))
                print("\nView employee details-\n")
                                
                #all employees
                if viewoption==1:

                        #what to check
                        cur.execute('desc employee_display')
                        cols=[]
                        for i in cur.fetchall():
                                cols.append(i[0])
                        colsnum=[]
                        for i in range(len(cols)):
                                colsnum.append(i+1)
                        colsdict=dict(zip(colsnum,cols))
                        print("\nAvailable columns are: \n")
                        for i in colsdict:
                                print(i,'\t',colsdict[i])
                        print()
                        
                        print("Enter the column keys one-by-one and press enter to break loop.")
                        colchoice = []
                        while True:                
                                a = input("Enter column key: ")
                                if a=='':
                                        break
                                colchoice.append(a)
                                
                        colstring=''
                        for i in colchoice:
                                colstring+=colsdict[int(i)]+','
                        colstring=colstring[:-1]
                        print()             
                        
                        #display data
                        cur.execute("select {} from employee_display".format(colstring))
                                                
                        for i in cur.fetchall():
                                for j in i:
                                        if len(str(j))>15:
                                            j = j[:13]
                                        print(str(j),end = (' '*(15-len(str(j)))))
                                print('\n')
                        print('\n')

                #specific employees
                elif viewoption==2:

                        #whom to check
                        cur.execute('select * from employee_display')
                        emps=[]
                        for i in cur.fetchall():
                                emps.append(i[0])
                        print("Available employee IDs are: ")
                        for i in emps:
                                print(i)
                        
                        print("Enter the ID keys of required employees one-by-one and press enter to break loop.")
                        empchoice = []
                        while True:                
                                a = input("Enter employee ID: ")
                                if a=='':
                                        break
                                empchoice.append(a)
                                
                        empstring=''
                        for i in empchoice:
                                empstring+=i+','
                        empstring=empstring[:-1]
                        print()

                        #what to check
                        cur.execute('desc employee_display')
                        cols=[]
                        for i in cur.fetchall():
                                cols.append(i[0])
                        colsnum=[]
                        for i in range(len(cols)):
                                colsnum.append(i+1)
                        colsdict=dict(zip(colsnum,cols))
                        print("\nAvailable columns are: \n")
                        for i in colsdict:
                                print(i,'\t',colsdict[i])
                        print()
                        
                        print("Enter the column keys one-by-one and press enter to break loop.")
                        colchoice = []
                        while True:                
                                a = input("Enter column key: ")
                                if a=='':
                                        break
                                colchoice.append(a)
                                
                        colstring=''
                        for i in colchoice:
                                colstring+=colsdict[int(i)]+','
                        colstring=colstring[:-1]
                        print()             

                        #display data
                        cur.execute('select {} from employee_display where emp_id in ("{}")'.format(colstring,empstring))
                                                
                        for i in cur.fetchall():
                                for j in i:
                                        if len(str(j))>15:
                                            j = j[:13]
                                        print(str(j),end = (' '*(15-len(str(j)))))
                                print('\n')
                        print('\n')
                 
                #except specific employees 
                elif viewoption==3:

                        #whom to check
                        cur.execute('select * from employee_display')
                        emps=[]
                        for i in cur.fetchall():
                                emps.append(i[0])
                        print("Available employee IDs are: ")
                        for i in emps:
                                print(i)

                        print("Enter the ID keys of required employees one-by-one and press enter to break loop.")
                        empchoice = []
                        while True:                
                                a = input("Enter employee ID: ")
                                if a=='':
                                        break
                                empchoice.append(a)
                                
                        empstring=''
                        for i in empchoice:
                                empstring+=i+','
                        empstring=empstring[:-1]
                        print()

                        #what to check
                        cur.execute('desc employee_display')
                        cols=[]
                        for i in cur.fetchall():
                                cols.append(i[0])
                        colsnum=[]
                        for i in range(len(cols)):
                                colsnum.append(i+1)
                        colsdict=dict(zip(colsnum,cols))
                        print("\nAvailable columns are: \n")
                        for i in colsdict:
                                print(i,'\t',colsdict[i])
                        print()
                        
                        print("Enter the column keys one-by-one and press enter to break loop.")
                        colchoice = []
                        while True:                
                                a = input("Enter column key: ")
                                if a=='':
                                        break
                                colchoice.append(a)
                                
                        colstring=''
                        for i in colchoice:
                                colstring+=colsdict[int(i)]+','
                        colstring=colstring[:-1]
                        print()
                        
                        #display data
                        cur.execute('select {} from employee_display where emp_id not in ("{}")'.format(colstring,empstring))
                                                
                        for i in cur.fetchall():
                                for j in i:
                                        if len(str(j))>15:
                                            j = j[:13]
                                        print(str(j),end = (' '*(15-len(str(j)))))
                                print('\n')
                        print('\n')

                else:
                    print("Sorry ... wrong entry ... \n")
                print('-'*30)           
                repeat_view_employee=input("Do you want to view another employee's data? (y/n)")
                if repeat_view_employee.upper() not in ('Y','YES'):
                        break

            cur.execute('truncate table employee_display')            
        
        elif menuchoice == 3:
            break
        
        else: 
            print("Sorry ... wrong entry ... \n")
            break
            
    #COMMIT THE APPLIED CHANGES AND CLOSE/EXIT THE CURSOR
    print('\n')
    print("===============================================================================")
    print("====================================THANK YOU!=================================")
    print("===============================================================================")
    print('\n')
    mydb.commit()
    cur.close()

#-- INVENTORY MANAGEMENT SYSTEM --#    
def InventoryManagementSystem():
    #IMPORT CONNECTOR
    import mysql.connector

    #SET THE DATABASE AND CURSOR
    mydb = mysql.connector.connect(user='root',
                                   password='Pranav123@MySQL',
                                   host='127.0.0.1',
                                   database='inventory_database')

    cur = mydb.cursor()

    print('\n')
    print("===============================================================================")
    print("==============================INVENTORY MANAGEMENT=============================")
    print("===============================================================================")
    print('\n')

    #PROGRAM AND QUERY HERE
    while True:  
        print("Choose from the options below to manage your employee data:\n")
        print('''Options:
            1. Manage your inventory data.
            2. View your inventory data.
            3. Exit.
        ''')

        menuchoice = int(input("Enter your choice: "))
        if menuchoice == 1:  
            #INVENTORY DATA MANAGEMENT
            while True:
                print("Choose from the options below to manage your employee data:\n")
                print('''Options:
                    1. Add a new item.
                    2. Delete existing item.
                    3. Update the unit price of any item.
                    4. Add goods received.
                    5. Sell goods.
                ''')   
                           
                option=int(input("\nEnter your Option: "))    
                
                while True:
                    #add new item
                    if option==1:
                        print("\nAdd new item's details-\n")
                        item_code = input("Enter item code: ")
                        item_name = input("Enter item name: ")
                        quantity = int(input("Enter item quantity: "))
                        price = float(input("Enter item price: "))

                        cur.execute('insert into item_master values'
                                    '("{}","{}",{},{})'.format(item_code,item_name,quantity,price))                                
                        
                        print()
                        mydb.commit()
                        print('-'*30)

                        repeat_add_empl=input("Do you want to add another item? (y/n)")
                        if repeat_add_empl.upper() not in ('Y','YES'):
                            break

                    #delete item
                    elif option==2:
                        print("\nDelete existing item-\n")
                        
                        print("Enter the codes of not required items one-by-one and press enter to break loop.")
                        itemchoice = []
                        while True:                
                            a = input("Enter item code: ")
                            if a=='':
                                break
                            itemchoice.append(a)
                            
                        itemstring=''
                        for i in itemchoice:
                            itemstring+=i+','
                        itemstring=itemstring[:-1]
                        print()
                        
                        cur.execute('delete from item_master where item_code in ("{}")'.format(itemstring))

                        mydb.commit()
                        print("\nItem deleted from inventory successfully!\n")
                        print('-'*30)

                        repeat_del_empl=input("Do you want to delete another item? (y/n)")
                        if repeat_del_empl.upper() not in ('Y','YES'):
                            break

                    #update price
                    elif option==3:
                        print("\nUpdate existing item's price-\n")
                        item_code = input("Enter item code: ")
                        price = float(input("Enter price: "))
                        cur.execute('update item_master set price = {} where item_code="{}"'.format(price,item_code))

                        mydb.commit()
                        print("\nItem price updated successfully!\n")
                        print('-'*30)

                        repeat_del_empl=input("Do you want to update another item's price? (y/n)")
                        if repeat_del_empl.upper() not in ('Y','YES'):
                            break

                    #receive goods
                    elif option==4:
                        print("\nUpdate received goods-\n")
                        count = int(input("How many goods? "))
                        cur.execute('select item_code from item_master')
                        item_list = []
                        for i in cur.fetchall():
                            item_list.append(i[0])
                        
                        grn_code = input("Enter the GRN code: ")
                        grn_date = input("Enter GRN date in 'YYYY-MM-DD': ")
                        supply_code = input("Enter the supply code: ")
                                
                        cur.execute('insert into grn_master values'
                                    '("{}","{}","{}")'.format(grn_code,grn_date,supply_code))
                        mydb.commit()
                                    
                        for i in range(count):
                            print('\nItem '+str(i+1)+': ')
                            item_code = input("Enter item code: ")
                            
                            if item_code not in item_list:
                                print("Sorry! The item code either wrong or does not exist.")
                                cur.execute('delete from grn_master where grn_code = "{}"'.format(grn_code))
                                mydb.commit()
                                getnext = input("""--   If it is a new item, 
                            press ENTER to add item to inventory, 
                            else press any key to get next item: """)
                                if getnext == "":
                                    print("Go to 'ADD ITEM' ")
                                    break
                                else:
                                    continue
                                    
                            else:
                                quantity = int(input("Enter the quantity: "))
                                cost_price = float(input("Enter cost price: "))
                                          
                                cur.execute('insert into grn_detail values'
                                            '("{}","{}","{}",{},{})'.format(grn_code,grn_date,item_code,quantity,cost_price))
                                            
                                cur.execute('update item_master '
                                            'set quantity = quantity + {} '
                                            'where item_code = "{}"'.format(quantity,item_code))

                                print("\nSupply acquired successfully!\n")
                                            
                        print("Go to inventory to change the selling price of any item, if necessary.")
                        print('-'*30)
                        mydb.commit()
                        
                        repeat_sal_update=input("Do you want to receive more items? (y/n)")
                        if repeat_sal_update.upper() not in ('Y','YES'):
                            break

                    #sell goods
                    elif option==5:
                        print("\nUpdate sold goods-\n")

                        cur.execute("select * from item_master")
                        l = cur.fetchall()
                        
                        itemcode = []
                        itemlist = []
                        quantity = []
                        price = []
                        
                        for x in range(len(l)):
                            itemcode.append(l[x][0])
                            itemlist.append(l[x][1])
                            quantity.append(l[x][2])
                            price.append(l[x][3])
                            
                        inv_code = input("Enter the invoice code: ")
                        inv_date = input("Enter invoice date in 'YYYY-MM-DD': ")
                        cust_code = input("Enter the customer code: ")
                        
                        cur.execute('insert into invoice_master values'
                                    '("{}","{}","{}")'.format(inv_code,inv_date,cust_code))
                        mydb.commit()                                              
                        
                        i="y" 
                        while i=="y":
                            print('\nItem: ')
                            item_code = input("Enter item code: ")                                        
                            
                            if item_code not in itemcode:
                                print("Sorry! The item code either wrong or does not exist.")
                                continue
                                
                            else:
                                needed = int(input("Enter the quantity: "))
                                
                                item_index = itemcode.index(item_code)
                                av_quantity = quantity[item_index]
                                
                                if needed > av_quantity:
                                    print("Not enough quantity!\n")
                                    continue                          

                                else:
                                    cur.execute('insert into invoice_detail values'
                                                '("{}","{}","{}",{})'.format(inv_code,inv_date,item_code,needed))
                                                
                                    cur.execute('update item_master '
                                                'set quantity = quantity - {} '
                                                'where item_code = "{}"'.format(needed,item_code))
                            i = input("Do you want to continue? (y/n)").lower()
                                    
                        print("Go to inventory to change the selling price of any item, if necessary.")
                        mydb.commit()    
                        print("\nItems sold successfully!\n")
                        print('-'*30)

                        bill = input("Do you want bill? (y/n)")
                        if bill.upper() not in ('Y','YES'):
                            break
                        else:
                            cur.execute('select i.item_name as ITEM, r.quantity as QUANTITY, i.price as PRICE, (r.quantity * i.price) as AMOUNT '
                                        'from item_master i, invoice_detail r '
                                        'where r.item_code = i.item_code and inv_code="{}"'.format(inv_code))

                            print()
                            print("ITEM NAME      QUANTITY       PRICE          AMOUNT")
                            print()

                            total = 0
                            for x in cur.fetchall():
                                for j in x:
                                    print(str(j),end = (' '*(15-len(str(j)))))
                                print()
                                total += x[3]
                            print("\nTOTAL = ",total)

                            input('Waiting for payment...(if customer paid,press any key)')

                            print("Thank You!")
                            print('-'*30)
                        
                        repeat_sal_update=input("Do you want to sell more items? (y/n)")
                        if repeat_sal_update.upper() not in ('Y','YES'):
                            break
                            
                        mydb.commit()

                    elif option==6:
                    	break
                    	        
                    else:
                        print("Sorry ... wrong entry ... \n")
                        break
                    
                repeat=input("Do you want to change anything else? (y/n)")
                if repeat.upper() not in ('Y','YES'):
                    break

                    
        elif menuchoice == 2:            
            #INVENTORY DATAVIEW                     
            
            cur.execute('select * from item_master')
            
            print()
            print("ITEM CODE      ITEM NAME      QUANTITY       PRICE")
            print()

            for i in cur.fetchall():
                for j in i:
                    print(str(j),end = (' '*(15-len(str(j)))))
                print()              
            print()
            
        elif menuchoice == 3:
            break
        
        else: 
            print("Sorry ... wrong entry ... \n")
            break

        repeat_course = input("Do you want to do anything else (MAIN MENU) ? (y/n)")
        print()
        if repeat_course.upper() not in ('Y','YES'):
            break    
        
    #COMMIT THE APPLIED CHANGES AND CLOSE/EXIT THE CURSOR
    print('\n')
    print("===============================================================================")
    print("====================================THANK YOU!=================================")
    print("===============================================================================")
    print('\n')
    mydb.commit()
    cur.close()

#-- BANK MANAGEMENT SYSTEM --#
def BankManagementSystem():
    #IMPORTS
    import random
    import mysql.connector

    #SET THE DATABASE AND CURSOR
    mydb = mysql.connector.connect(user='root',
                                   password='Pranav123@MySQL',
                                   host='127.0.0.1',
                                   database='bank_database')

    cur = mydb.cursor()

    print('\n')
    print("===============================================================================")
    print("================================== PYTHONBANK =================================")
    print("===============================================================================")
    print('\n')

    #CLASS DEFINITION
    class BankAccount:
        
        """
            This class creates 'bank accounts' as objects!
        """
        
        def __init__(self):
            self.balance = 0
            
        def Deposit(self,amt):
            self.balance = self.balance + amt 
            return self.balance
            
        def Withdraw(self,amt):
            if amt > self.balance:
                print("Balance Insufficient!")
            else:
                self.balance = self.balance - amt   
            return self.balance	

    #REQUIRED SEQUENCES
    security = '1234567890'

    #EXECUTIONS
    accounts = {}
    cur.execute('select * from accounts')
    acdata = cur.fetchall()
    aclist = []
    ulist = []
    acbal = []
    for i in acdata:
        aclist.append(i[0])
        ulist.append(i[1])
        acbal.append(i[2])

    while True:
        print("""Choose from the options below:
    1. Manage your bank customer data.
    2. View bank customer data.
    3. Exit.
        """)

        main_option= int(input("Enter your choice: "))
        
        if main_option == 1:
            #BANK DATA MANAGEMENT
            for i in range(len(acdata)):
                accounts.update(
                                    {
                                        aclist[i] : {ulist[i]:BankAccount()}
                                    }
                               )
                accounts[aclist[i]][ulist[i]].balance = acbal[i]

            while True:
                print("""
Choose from the options below:
    1. Customers.
    2. Accounts.
    3. Exit.
                """)
                    
                option1 = int(input("Enter your choice: "))

                #CUSTOMERS
                if option1 == 1:
                    
                    while True:
                        print("""
Choose from the options below:
    1. New customer.
    2. Existing customer.
    3. Delete Customer.
    4. Main Menu.
                        """)
                        
                        option2 = int(input("Enter your choice: "))

                        #NEW CUSTOMER
                        if option2 == 1:
                        
                            customer_id = 'CID'
                            for i in range(4):
                                customer_id += random.choice(security)
                            cust_name = input("Enter your name: ")
                            cur.execute('insert into customers values'
                                        '("{}","{}")'.format(customer_id,cust_name))

                            print(customer_id,'is your customer ID')
                            
                            print("""
Go to main menu option 2 to create an account.\n
                            """)
                            print('-'*80)

                        #EXISTING CUSTOMER  
                        elif option2 == 2:
                            
                            customer = input("Enter customer ID: ")
                            cur.execute('select * from customers')
                            l = cur.fetchall()
                            ids = []
                            customers = []
                            for i in l:
                                ids.append(i[0])
                                customers.append(i[1])
                            if customer in ids:
                                print("\nWelcome,",customers[ids.index(customer)])
                                print("Go to Accounts to manage your accounts.")
                                print('-'*80)
                                break
                            else:
                                print("\nSorry! You are not a customer. Go to option 1 to register yourself.\n")
                                print('-'*80)
                            mydb.commit()

                        #DELETE CUSTOMER  
                        elif option2 == 3:
                            
                            customer = input("Enter customer ID: ")
                            cur.execute('select * from customers')
                            l = cur.fetchall()
                            ids = []
                            customers = []
                            for i in l:
                                ids.append(i[0])
                                customers.append(i[1])
                            if customer in ids:
                                cur.execute('delete from accounts where cust_id="{}"'.format(customer))
                                cur.execute('delete from customers where cust_id="{}"'.format(customer))
                                print("Customer deleted successfully!")
                                print('-'*80,'\n')
                                break
                            else:
                                print("\nSorry! You are not a customer. Go to option 1 to register yourself.\n")
                                print('-'*80)
                            mydb.commit()

                        #BACK TO MAIN MENU
                        elif option2 == 4:
                            
                            break

                        else:
                            
                            print("Thank You !!!")
                            break

                #ACCOUNTS
                elif option1 == 2:

                    while True:
                        print("""
Choose from the options below:
    1. New Account.
    2. Existing Account.
    3. Main Menu.
                        """)
                        
                        option2 = int(input("Enter your choice: "))

                        #NEW ACCOUNT
                        if option2 == 1:

                            customer = input("Enter customer ID: ")
                            cur.execute('select * from customers')
                            l = cur.fetchall()
                            ids = []
                            customers = []
                            for i in l:
                                ids.append(i[0])
                                customers.append(i[1])
                            if customer in ids:
                                print("\nWelcome,",customers[ids.index(customer)],'\n')
                            else:
                                print("\nSorry! You are not a customer. Go to option 1 to register yourself.\n")
                                print('-'*80)
                                break

                            ac_id = 'AC0000'
                            for i in range(10):
                                ac_id += random.choice(security)

                            print(ac_id,'is your account ID.\n')

                            cur.execute('select * from accounts')
                            acdata = cur.fetchall()
                            aclist = []
                            ulist = []
                            for i in acdata:
                                aclist.append(i[0])
                                ulist.append(i[1])
                                
                            accounts.update(
                                                {
                                                    ac_id : {customer:BankAccount()}
                                                }
                                           )
                            
                            default_deposit = input("Do you want to deposit default amount? (y/n): ")
                            if default_deposit.upper() in ('Y','YES'):
                                
                                amt = float(input("Amount: "))
                                accounts[ac_id][customer].balance = amt                    
                                
                            else:
                                accounts[ac_id][customer].balance = 0
                                
                            cur.execute('insert into accounts values'
                                        '("{}","{}",{},"standard")'.format(ac_id,customer,accounts[ac_id][customer].balance))

                            print("Account created successfully!")
                            mydb.commit()
                            print('-'*80,'\n')
                            break

                        #EXISTING ACCOUNT    
                        elif option2 == 2:

                            customer = input("Enter customer ID: ")
                            cur.execute('select * from customers')
                            l = cur.fetchall()
                            ids = []
                            customers = []
                            for i in l:
                                ids.append(i[0])
                                customers.append(i[1])
                            if customer in ids:
                                print("\nWelcome,",customers[ids.index(customer)],'\n')
                            else:
                                print("\nSorry! You are not a customer. Go to option 1 to register yourself.\n")
                                print('-'*80)
                                break

                            ac_id = input("Enter your Account ID: ")
                            cur.execute('select * from accounts')
                            acdata = cur.fetchall()
                            aclist = []
                            ulist = []
                            for i in acdata:
                                aclist.append(i[0])
                                ulist.append(i[1])

                            if ac_id in aclist:
                                if ulist[aclist.index(ac_id)] == customer:
                                    while True:
                                        print("""
Choose from the options below:
    1. Deposit.
    2. Withdraw.
    3. Check Balance.
    4. Loan.
    5. Repayment.
    6. Back to Previous Menu.
                                """)

                                        option3 = int(input("Enter your choice: "))

                                        #deposit
                                        if option3 == 1:
                                            depamt = float(input("How much to deposit? "))
                                            accounts[ac_id][customer].Deposit(depamt)
                                            cur.execute('update accounts '
                                                        'set balance = {} '
                                                        'where ac_id = "{}"'.format(accounts[ac_id][customer].balance,ac_id))

                                            print("Amount deposited successfully!")
                                            print('-'*30)
                                            mydb.commit()

                                        #withdraw
                                        elif option3 == 2:
                                            withamt = float(input("How much to withdraw? "))
                                            accounts[ac_id][customer].Withdraw(withamt)
                                            cur.execute('update accounts '
                                                        'set balance = {} '
                                                        'where ac_id = "{}"'.format(accounts[ac_id][customer].balance,ac_id))

                                            print("Amount withdrawn successfully!")
                                            print('-'*30)
                                            mydb.commit()

                                        #balance
                                        elif option3 == 3:                              
                                                                                
                                            print("\nWelcome,",customers[ids.index(customer)],'\n')
                                            print("Your balance is: ",accounts[ac_id][customer].balance)                                             
                                            mydb.commit()
                                            print('-'*30)

                                        #loan
                                        elif option3 == 4:
                                            l_ac_id = 'ACL000'
                                            for i in range(10):
                                                l_ac_id += random.choice(security)
                                            print(l_ac_id,'is your loan account ID.')

                                            ac_id = input("Enter an account ID to debit repayment amount from: ")

                                            if ac_id in accounts:

                                                loanamt = float(input("How much amount for loan? "))
                                                accounts.update(
                                                                    {
                                                                        l_ac_id : {customer:BankAccount()}
                                                                    }
                                                               )
                                                accounts[l_ac_id][customer].balance = loanamt
                                            
                                                cur.execute('insert into accounts values'
                                                            '("{}","{}",{},"loan")'.format(l_ac_id,customer,accounts[l_ac_id][customer].balance))

                                                print("Loan created successfully!")
                                                print('-'*30)

                                            else:
                                                print("Account does not exist.")
                                                print('-'*30)
                                                break
                                            mydb.commit()
                                            
                                        #repayment
                                        elif option3 == 5:
                                            l_ac_id = input("Enter loan account ID: ")
                                            if l_ac_id in accounts:
                                                
                                                print("You have",accounts[l_ac_id][customer].balance," remaining in loan")

                                                repamt = float(input("How much do you want to repay? "))
                                                while repamt > accounts[l_ac_id][customer].balance:
                                                    print("Repayment amount is more than loan pending.")
                                                    repamt = float(input("How much do you want to repay? "))

                                                accounts[l_ac_id][customer].balance = accounts[l_ac_id][customer].balance - repamt
                                                accounts[ac_id][customer].balance = accounts[ac_id][customer].balance - repamt
                                                
                                                cur.execute('update accounts '
                                                            'set balance = {} '
                                                            'where ac_id = "{}"'.format(accounts[l_ac_id][customer].balance,l_ac_id))
                                                cur.execute('update accounts '
                                                            'set balance = {} '
                                                            'where ac_id = "{}"'.format(accounts[ac_id][customer].balance,ac_id))
                                                
                                                if accounts[l_ac_id][customer].balance == 0:
                                                    print("Loan repayed successfully!")
                                                    cur.execute('delete from accounts where ac_id="{}"'.format(l_ac_id))
                                                    print('-'*30)
                                                else:
                                                    print("Amount repayed successfully!")
                                                    print('-'*30)
                                                mydb.commit()
                                            else:
                                                print("Account does not exist.")
                                                print('-'*30)
                                                break

                                        #prev_menu
                                        elif option3 == 6: 
                                            break
                                        else:
                                            print("Choose a correct option!")
                                            break
                                else:
                                    print("Wrong account number/customer. Values do not match.")
                                    print('-'*30)
                            else:
                                print("Wrong account number/customer. Values do not match.") 
                                print('-'*30)               
                            
                            print('-'*30)            

                        #BACK TO MAIN MENU
                        elif option2 == 4:
                            break

                        else:
                            print("Choose a correct option!")
                            break

                else:
                    print('\n')
                    break
                    
        #BANK DATAVIEW
        elif main_option == 2:
            cur.execute('select c.cust_id, c.cust_name, a.ac_id, a.balance, a.ac_type '
                        'from customers c, accounts a where c.cust_id = a.cust_id')

            print('\n')
            print('CUSTOMER ID         CUSTOMER NAME       ACCOUNT ID          ACCOUNT BALANCE     ACCOUNT TYPE')

            for i in cur.fetchall():
                for j in i:
                    print(str(j),end = (' '*(20-len(str(j)))))
                print()              
            print()  
            print('-'*30) 

        elif main_option == 3:
            break 
            
    print('\n')
    print("===============================================================================")
    print("====================================THANK YOU!=================================")
    print("===============================================================================")
    print('\n')

    #COMMIT CHANGES
    mydb.commit()
    cur.close()

#-- DATABASE MANAGEMENT --#
def dbManagementSystem():
    import mysql.connector

    db = input("Enter database to make changes: ")

    #SET THE DATABASE AND CURSOR
    mydb = mysql.connector.connect(user='root',
                                   password='Pranav123@MySQL',
                                   host='127.0.0.1',
                                   database=db)

    cur = mydb.cursor()

    print('\n')
    print("===============================================================================")
    print("========================== DATABASE MANAGEMENT SYSTEM =========================")
    print("===============================================================================")
    print('\n')

    while True:
        print("Choose from the options below to manage your employee database:\n")
        print('''Options:
            1. Add/Create a table or column.
            2. Delete a table or column.
            3. Rename a table or column.
            4. Change the datatype of a column in a table.
            5. Exit
        ''')  
        
        option1 = int(input("Enter your operation's number: "))

        if option1 == 1:
            print("Choose what to add from the options below:\n")
            print('''Options:
                1. Table.
                2. Column.            
            ''')   
           
            option2 = int(input("Enter your selection: "))
            if option2 == 1:
                tablename = input("Enter the tablename: ")
                print()
                count = int(input("How many columns? "))
                print()

                colstring=''
                for i in range(count):
                    colname = input("Enter column "+str(i+1)+" name: ")+' '
                    coldata = input("Enter column "+str(i+1)+" datatype: ")+' '
                    colcons = input("Enter column "+str(i+1)+" constraint: ")+' '
                    colstring += colname + coldata + colcons + ', '
                colstring = colstring[:-2]
                
                cur.execute('create table {} ({})'.format(tablename,colstring))
                mydb.commit()                
                print("\nTable '{}' created successfully!".format(tablename))
                
            elif option2 == 2:
                tablename = input("Enter the tablename: ")
                
                colstring=''
                colname = input("Enter column name: ")+' '
                coldata = input("Enter column datatype: ")+' '
                colcons = input("Enter column constraint: ")+' '
                print()
                
                colstring += colname + coldata + colcons
                cur.execute('alter table {} add {} '.format(tablename,colstring))
                mydb.commit()
                print("\nColumn '{}' added successfully!".format(colname))
                                
            else:
                print("Sorry ... wrong entry ... \n")
                break
        
        elif option1 == 2:
            print("Choose what to add from the options below:\n")
            print('''Options:
                1. Table.
                2. Column.            
            ''')
            
            option2 = int(input("Enter your selection: "))
            if option2 == 1:
                tablename = input("Enter the tablename: ")
                print()
                cur.execute('drop table {}'.format(tablename))
                mydb.commit()                
                print("\nTable '{}' dropped successfully!".format(tablename))
                    
            elif option2 == 2:
                tablename = input("Enter the tablename: ")
                colname = input("Enter the column name: ")
                print()
                cur.execute('alter table {} drop column {}'.format(tablename,colname))
                mydb.commit()                
                print("\nColumn '{}' dropped successfully!".format(colname))
            else:
                print("\nSorry ... wrong entry ... \n")
                break
                
        elif option1 == 3:
            print("Choose what to add from the options below:\n")
            print('''Options:
                1. Table.
                2. Column.            
            ''')
        
            option2 = int(input("Enter your selection: "))
            if option2 == 1:
                tablename = input("Enter the existing tablename: ")
                new = input("Enter the new tablename: ")
                print()
                cur.execute('alter table {} rename to {}'.format(tablename,new))
                mydb.commit()                
                print("\nTable '{}' renamed successfully as '{}'!".format(tablename,new))
                    
            elif option2 == 2:
                tablename = input("Enter the tablename: ")
                colname = input("Enter the existing column name: ")
                new = input("Enter the new column name: ")
                datatype = input("Enter the datatype: ")

                print()
                cur.execute('alter table {} change column {} {} {}'.format(tablename,colname,new,datatype))
                mydb.commit()                
                print("\nColumn '{}' renamed successfully as '{}'!".format(colname,new))
                    
            else:
                print("\nSorry ... wrong entry ... \n")
                break

        elif option1 == 4:
            tablename = input("Enter the tablename: ")
            colname = input("Enter the existing column name: ")
            datatype = input("Enter the new datatype: ")
            constraint = input("Constraint: ")

            print()
            cur.execute('alter table {} modify column {} {} {}'.format(tablename,colname,datatype,constraint))
            mydb.commit()
            print("\ndatatype changed for {} successfully!".format(colname))

        elif option1 == 5:
            break
                   
        else:
            print("\nSorry ... wrong entry ... \n")
            break

        repeat_table_modify = input("Do you want to change anything else (MAIN MENU) ? (y/n)")
        if repeat_table_modify.upper() not in ('Y','YES'):
            break

    print("\n")
    print("===============================================================================")
    print("====================================THANK YOU!=================================")
    print("===============================================================================")
    print("\n")

    mydb.commit()
    cur.close()
