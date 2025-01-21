import json

# Initialize participants and expenses
participants = []
expenses = []
money_balance = []
owe_list ={}


# Load data from a JSON file to persist
def load_data():
    global participants, expenses, money_balance, owe_list
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            participants = data.get('participants', [])
            expenses = data.get('expenses', [])
            money_balance = data.get('money_balance', [])
            owe_list = data.get('owe_list', {})
            print(owe_list)


    except FileNotFoundError:
        print("No data file found. Starting fresh.")

# Save data to a JSON file to persist
def save_data():
    with open('data.json', 'w') as f:
        json.dump({'participants': participants, 'expenses': expenses, 'money_balance':money_balance , 'owe_list': owe_list}, f)


# displaying all the expenses 
def display_expenses():
    # Print header row
    print(f"{'Name':<15}{'Balance':<10}")
    print("="*25)
    
    # Print participant data
    for participant in participants:
        print(f"{participant['name']:<15}{participant['balance']:<10}")
    
    print("="*25)


def lookup__details():
    # ask for name
    name= input("Enter the name to lookup : ")
    # display who owe who for the name 
    # find the accumulated owe 
    # Print header row
    
    print(f"{'Name':<15}{'Owe':<15}{'Amount':<15}")
    print("="*40)
    if name in owe_list:
        for name_to in owe_list[name]: 
            print(f"{name:<15}{name_to:<15} {owe_list[name][name_to]:<15} ")
    else:
        # check if other has the name 
        for owe in  owe_list.values():
            if name in owe_list[owe]:
                print(f"{owe:<15}{name:<15} {owe_list[owe][name]:<15} ")

        

    
def get_total_expenses():
    return len(expenses)


# Add a new participant
def add_participant():
    name = input("Enter name: ")
    email = input("Enter email address: ")
    participants.append({'name': name, 'email':email, 'balance': 0.0})
    print(f"Added name: {name} email:{email}")
    save_data()
    
# Add an expense
def add_expense():
    payer = input("Enter payer's name: ")
    type = input("What expenses is thuis about: ")
    amount = float(input("Enter total expense amount: "))
    split_list = input("Enter names of participants to split the expense (comma separated): ").split(',')
    expenses_id = get_total_expenses()+ 1 

    if payer not in [p['name'] for p in participants]:
        print(f"Error: {payer} is not a valid participant.")
        return
    
    # Calculate the share each person has to pay
    split_amount = amount / len(split_list)
    # Update their balance 
    for participant in participants:
        if participant['name'] == payer:
            participant['balance'] += split_amount  # payer gets credited for the full amount
        elif participant['name'] in split_list:
            participant['balance'] -= split_amount  # others owe their share
            money_balance.append({'expense':expenses_id,'name': participant['name'], 'payer': payer, 'amount': amount, 'paid': False})
    
    # Record the expense
    expenses.append({'expense':expenses_id,'payer': payer, 'amount': amount, 'split_among': split_list, 'type':type})
    print(f"Expense added: {payer} paid ${amount} and split among {', '.join(split_list)}")
    split_list.remove(payer)

    # Update owe list 
    # check if the payer still owe any one then 
    for payee in split_list:
        # the payer owe the payee before 
        if payer in owe_list and payee in owe_list[payer]:
            # calculate and decute the money 
            prev_amount= owe_list[payer][payee]
            split_amount= prev_amount- split_amount
            if split_amount == 0: 
                # remove the owe list dictionary 
                owe_list[payer].pop(payee)
            elif split_amount > 0: 
                # upate new amount
                owe_list[payer][payee]= split_amount
            else:
                # create a new owe list dictionary 
                create_new_owe_dic(payee, payer, split_amount)
        else:
            if payee in owe_list and payer in owe_list[payee] : 
                split_amount+= owe_list[payee][payer]
                owe_list[payee][payer] = split_amount 
            else:
                create_new_owe_dic(payee, payer, split_amount)
    save_data()    

def create_new_owe_dic(name, name_owe, amount):
    owe_list[name]= {
        name_owe:amount 
    }
    print(owe_list)

# Mark an expense as done
def mark_as_done(expense_id):
    if expense_id < len(expenses):
        expenses[expense_id]['status'] = 'done'
        print(f"Expense {expense_id} marked as done.")
    else:
        print("Invalid expense ID.")

def remove_owe_list(name_from, name_to):
    owe_list[name_from].pop(name_to)
    if not owe_list[name_from]:
        owe_list.pop(name_from)

def record_payment():
    name_from = input("Payment Made From: ")
    name_to = input("Payment Made To: ")
    amount= float(input("Payment Amount :"))
    if name_from in owe_list :
        if name_to in owe_list[name_from]:
            # pay 
            owe_amount= owe_list[name_from][name_to]
            new_amount= amount-owe_amount
            if new_amount>=0:
                print(f"Sucessfully recorded payment done from : {name_from} to : {name_to} for AUD{owe_amount}")
                # remove from owe list 
                remove_owe_list()
            else: 
                new_amount*=-1
                print(f"Sucessfully recorded payment done from : {name_from} to : {name_to} for AUD{owe_amount}")
                print(f"Still owe AUD{new_amount}")
                # record new amount in owe list 
                owe_list[name_from][name_to]= new_amount
                print(owe_list)
            save_data()
    else:
        print(f"Unsuccessfull ! Since {name_from} don't owe {name_to} any amount")

            

