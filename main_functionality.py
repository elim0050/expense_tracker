import json
from helper import helper


class Functionality:
    """
    A class to manage participants, expenses, balances, and owe lists for expense tracking.
    """

    def __init__(self):
        """
        Initialize the Functionality class by loading data from the JSON file.
        """
        self.participants, self.expenses, self.money_balance, self.owe_list = helper.load_data()

    def save_data(self):
        """
        Save the current state of participants, expenses, balances, and owe lists to the JSON file.
        """
        helper.save_data(self.participants, self.expenses, self.money_balance, self.owe_list)

    def display_expenses(self):
        """
        Display the current balances of all participants in a formatted table.
        """
        if len(self.participants)==0:
            print("No Expenses Yet :)")
        else:
            headers = ["Name", "Balance"]
            rows = [[p['name'], p['balance']] for p in self.participants]
            helper.print_table(headers, rows)

    def lookup__details(self):
        """
        Lookup debt details for a specific participant.

        Prompts the user for a name and displays all debts where the participant
        owes or is owed money. If no debts are found, notifies the user.
        """
        name = input("Enter the name to lookup: ")
        rows = []
        if name in self.owe_list:
            rows.extend([[name, name_to, self.owe_list[name][name_to]] for name_to in self.owe_list[name]])
        else:
            for name_key, val in self.owe_list.items():
                if name in val:
                    rows.append([name_key, name, val[name]])

        if rows:
            helper.print_table(["Name", "Owe", "Amount"], rows)
        else:
            print(f"No debts found for {name}.")

    def add_participant(self):
        """
        Add a new participant to the expense tracker.

        Prompts the user for the participant's name and email address.
        If the name already exists, notifies the user and aborts the operation.
        """
        name = input("Enter name: ")
        if any(p['name'] == name for p in self.participants):
            print(f"Error: Participant with name {name} already exists.")
            return
        email = input("Enter email address: ")
        self.participants.append({'name': name, 'email': email, 'balance': 0.0})
        print(f"Added: {name}, {email}")
        self.save_data()

    def add_expense(self):
        """
        Add a new expense to the tracker.

        Prompts the user for details about the payer, expense type, amount,
        and participants involved. Updates balances, expense records, and owe lists accordingly.
        """
        print("\n--- Add Expense ---")
        payer = input("Enter the name of the payer: ")
        expense_type = input("Enter the type of expense (e.g., groceries, rent): ")
        try:
            amount = float(input("Enter the total expense amount: "))
        except ValueError:
            print("Error: Please enter a valid number for the amount.")
            return

        split_list = input("Enter the names of participants to split the expense (comma-separated): ").split(',')
        split_list = [name.strip() for name in split_list]
        expenses_id = helper.get_total_expenses(self.expenses) + 1

        if payer not in [p['name'] for p in self.participants]:
            print(f"Error: {payer} is not a valid participant. Please add them first.")
            return

        try:
            split_amount = amount / len(split_list)
        except ZeroDivisionError:
            print("Error: No participants provided to split the expense.")
            return

        print("\nSplitting the expense...")
        for participant in self.participants:
            if participant['name'] == payer:
                participant['balance'] += amount
            elif participant['name'] in split_list:
                participant['balance'] -= split_amount
                self.money_balance.append({'expense': expenses_id, 'name': participant['name'], 'payer': payer, 'amount': split_amount, 'paid': False})

        self.expenses.append({
            'expense': expenses_id,
            'payer': payer,
            'amount': amount,
            'split_among': split_list,
            'type': expense_type
        })

        split_list.remove(payer)

        print("\nUpdating owe list...")
        for payee in split_list:
            if payer in self.owe_list and payee in self.owe_list[payer]:
                prev_amount = self.owe_list[payer][payee]
                updated_amount = prev_amount - split_amount
                if updated_amount == 0:
                    self.owe_list[payer].pop(payee)
                elif updated_amount > 0:
                    self.owe_list[payer][payee] = updated_amount
                else:
                    helper.create_new_owe_dic(payee, payer, -updated_amount, self.owe_list)
            else:
                if payee in self.owe_list and payer in self.owe_list[payee]:
                    updated_amount = self.owe_list[payee][payer] + split_amount
                    self.owe_list[payee][payer] = updated_amount
                else:
                    helper.create_new_owe_dic(payee, payer, split_amount, self.owe_list)

        self.save_data()
        print("\nExpense and balances updated successfully!")

    def record_payment(self):
        """
        Record a payment made from one participant to another.

        Prompts the user for the payer, payee, and payment amount.
        Updates balances and the owe list based on the payment.
        """
        name_from = input("Payment Made From: ")
        name_to = input("Payment Made To: ")
        try:
            amount = float(input("Payment Amount: "))
            if name_from in self.owe_list and name_to in self.owe_list[name_from]:
                owe_amount = self.owe_list[name_from][name_to]
                if amount >= owe_amount:
                    helper.remove_owe_list(name_from, name_to, self.owe_list)
                else:
                    self.owe_list[name_from][name_to] = owe_amount - amount
                for participant in self.participants:
                    if participant['name'] == name_from:
                        participant['balance'] += amount
                    elif participant['name'] == name_to:
                        participant['balance'] -= amount
                self.save_data()
            else:
                print(f"Error: {name_from} doesn't owe {name_to} any amount.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
