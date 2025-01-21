import json
from functionality import load_data, add_expense, display_expenses, lookup__details, add_participant, record_payment


# Main function to interact with the user
def main():
    load_data()  # Load any saved data at the start

    while True:
        print("\n==================== Expense Tracker ====================")
        display_expenses()
        print("1. Lookup friends detail")
        print("2. Add friends")
        print("3. Add an Expense")
        print("4. Record a payment")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            # ask for input name and addresss
            lookup__details()
        
                
        elif choice == '2':
            # add participant 
            add_participant()

        elif choice == '3':
            # add expenses 
            add_expense()
        elif choice== '4':
            record_payment()

        elif choice == '5':
            print("Data saved. Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
