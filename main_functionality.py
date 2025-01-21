import json
from helper import helper



class Functionality : 
    def __init__(self):
        self.participants, self.expenses,self.money_balance, self.owe_list = helper.load_data()
    def save_data(self):
        helper.save_data(self.participants,self.expenses,self.money_balance,self.owe_list)


    # displaying all the expenses 
    def display_expenses(self):
        # Print header row
        print(f"{'Name':<15}{'Balance':<10}")
        print("="*25)
        
        # Print participant data
        for participant in self.participants:
            print(f"{participant['name']:<15}{participant['balance']:<10}")
        
        print("="*25)


    def lookup__details(self):
        # ask for name
        name= input("Enter the name to lookup : ")
        # display who owe who for the name
        
        print(f"{'Name':<15}{'Owe':<15}{'Amount':<15}")
        print("="*40)
        if name in self.owe_list:
            for name_to in self.owe_list[name]: 
                print(f"{name:<15}{name_to:<15} {self.owe_list[name][name_to]:<15} ")
        else:
            name_to_check = name
                    # check if other has the name 
            for name_key, val in self.owe_list.items():
                if name_to_check in val:  # Check if 'Ethel' is in the inner dictionary
                    amount = val[name_to_check]
                    print(f"{name_key:<15}{name_to_check:<15} {amount:<15} ")

        

    # Add a new participant
    def add_participant(self):
        name = input("Enter name: ")
        email = input("Enter email address: ")
        self.participants.append({'name': name, 'email':email, 'balance': 0.0})
        print(f"Added name: {name} email:{email}")
        self.save_data()
        
    # Add an expense
    def add_expense(self):
        payer = input("Enter payer's name: ")
        type = input("What expenses is thuis about: ")
        amount = float(input("Enter total expense amount: "))
        split_list = input("Enter names of participants to split the expense (comma separated): ").split(',')
        expenses_id = helper.get_total_expenses(self.expenses)+ 1 

        if payer not in [p['name'] for p in self.participants]:
            print(f"Error: {payer} is not a valid participant.")
            return
        
        # Calculate the share each person has to pay
        split_amount = amount / len(split_list)
        # Update their balance 
        for participant in self.participants:
            if participant['name'] == payer:
                participant['balance'] += split_amount  # payer gets credited for the full amount
            elif participant['name'] in split_list:
                participant['balance'] -= split_amount  # others owe their share
                self.money_balance.append({'expense':expenses_id,'name': participant['name'], 'payer': payer, 'amount': amount, 'paid': False})
        
        # Record the expense
        self.expenses.append({'expense':expenses_id,'payer': payer, 'amount': amount, 'split_among': split_list, 'type':type})
        print(f"Expense added: {payer} paid ${amount} and split among {', '.join(split_list)}")
        split_list.remove(payer)

        # Update owe list 
        # check if the payer still owe any one then 
        for payee in split_list:
            # the payer owe the payee before 
            if payer in self.owe_list and payee in self.owe_list[payer]:
                # calculate and decute the money 
                prev_amount= self.owe_list[payer][payee]
                split_amount= prev_amount- split_amount
                if split_amount == 0: 
                    # remove the owe list dictionary 
                    self.owe_list[payer].pop(payee)
                elif split_amount > 0: 
                    # upate new amount
                    self.owe_list[payer][payee]= split_amount
                else:
                    # create a new owe list dictionary 
                    helper.create_new_owe_dic(payee, payer, split_amount, self.owe_list)
            else:
                if payee in self.owe_list and payer in self.owe_list[payee] : 
                    split_amount+= self.owe_list[payee][payer]
                    self.owe_list[payee][payer] = split_amount 
                else:
                    helper.create_new_owe_dic(payee, payer, split_amount, self.owe_list)

        self.save_data()



    def record_payment(self):
        name_from = input("Payment Made From: ")
        name_to = input("Payment Made To: ")
        amount= float(input("Payment Amount :"))
        if name_from in self.owe_list :
            if name_to in self.owe_list[name_from]:
                # pay 
                owe_amount= self.owe_list[name_from][name_to]
                new_amount= amount-owe_amount
                if new_amount>=0:
                    print(f"Sucessfully recorded payment done from : {name_from} to : {name_to} for AUD{owe_amount}")
                    # remove from owe list 
                    helper.remove_owe_list(name_from, name_to, self.owe_list)
                else: 
                    new_amount*=-1
                    print(f"Sucessfully recorded payment done from : {name_from} to : {name_to} for AUD{owe_amount}")
                    print(f"Still owe AUD{new_amount}")
                    # record new amount in owe list 
                    self.owe_list[name_from][name_to]= new_amount
                    print(self.owe_list)
            self.save_data()
        else:
            print(f"Unsuccessfull ! Since {name_from} don't owe {name_to} any amount")

                

