import json

class helper:
    """
    A helper class containing utility methods for managing participants, expenses, and owe lists.
    """

    @staticmethod
    def load_data():
        """
        Load data from a JSON file to persist participants, expenses, money balance, and owe list.

        Returns:
            tuple: A tuple containing participants (list), expenses (list), money_balance (list), and owe_list (dict).
            If the file is not found, returns empty structures for all.
        """
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                participants = data.get('participants', [])
                expenses = data.get('expenses', [])
                money_balance = data.get('money_balance', [])
                owe_list = data.get('owe_list', {})
                return participants, expenses, money_balance, owe_list
        except FileNotFoundError:
            print("No data file found. Starting fresh.")
            return [], [], [], {}

    @staticmethod
    def save_data(participants, expenses, money_balance, owe_list):
        """
        Save data to a JSON file to persist participants, expenses, money balance, and owe list.

        Args:
            participants (list): A list of participants.
            expenses (list): A list of expenses.
            money_balance (list): A list of money balance records.
            owe_list (dict): A dictionary containing owe relationships.
        """
        with open('data.json', 'w') as f:
            json.dump({'participants': participants, 'expenses': expenses, 
                       'money_balance': money_balance, 'owe_list': owe_list}, f)

    @staticmethod
    def get_total_expenses(expenses):
        """
        Get the total number of expenses recorded.

        Args:
            expenses (list): A list of expenses.

        Returns:
            int: The number of expenses in the list.
        """
        return len(expenses)

    @staticmethod
    def create_new_owe_dic(name, name_owe, amount, owe_list):
        """
        Create a new owe relationship in the owe list.

        Args:
            name (str): The name of the person who owes money.
            name_owe (str): The name of the person to whom money is owed.
            amount (float): The amount of money owed.
            owe_list (dict): The dictionary storing owe relationships.
        """
        owe_list[name] = {name_owe: amount}

    @staticmethod
    def remove_owe_list(name_from, name_to, owe_list):
        """
        Remove an owe relationship from the owe list.

        Args:
            name_from (str): The name of the person who owes money.
            name_to (str): The name of the person to whom money is owed.
            owe_list (dict): The dictionary storing owe relationships.

        Notes:
            If the owe list for `name_from` becomes empty after removal, the entry for `name_from` is also removed.
        """
        owe_list[name_from].pop(name_to)
        if not owe_list[name_from]:  # Check if the dictionary for `name_from` is empty
            owe_list.pop(name_from)
    
    @staticmethod
    def print_table(headers, rows):
        """
        Print a formatted table with headers and rows, ensuring proper alignment.

        Args:
            headers (list): A list of column headers (strings) for the table.
            rows (list of lists): A list where each element is a list representing a row of table data.

        Notes:
            - The column widths are dynamically determined based on the longest item in each column,
            including the headers and rows.
            - Rows are left-aligned for consistent formatting.
        """
        # Calculate the maximum width of each column
        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
        
        # Format and print the header row
        header_row = "  ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
        separator = "=" * len(header_row)
        print(header_row)
        print(separator)
        
        # Format and print each data row
        for row in rows:
            print("  ".join(f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row)))
        print(separator)
