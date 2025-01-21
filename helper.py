import json


class helper:
    # Load data from a JSON file to persist
    def load_data():
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                participants = data.get('participants', [])
                expenses = data.get('expenses', [])
                money_balance = data.get('money_balance', [])
                owe_list = data.get('owe_list', {})
                return participants, expenses,money_balance, owe_list

        except FileNotFoundError:
            print("No data file found. Starting fresh.")

    # Save data to a JSON file to persist
    def save_data(participants, expenses,money_balance, owe_list ):
        with open('data.json', 'w') as f:
            json.dump({'participants':participants, 'expenses':expenses,'money_balance':money_balance, 'owe_list':owe_list}, f)


        
    def get_total_expenses(expenses ):
        return len(expenses)



    def create_new_owe_dic(name, name_owe, amount, owe_list):
        owe_list[name]= {
            name_owe:amount 
        }


    def remove_owe_list(name_from, name_to, owe_list):
        owe_list[name_from].pop(name_to)
        if not owe_list[name_from]:
            owe_list.pop(name_from)


