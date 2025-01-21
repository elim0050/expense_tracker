from main_functionality import Functionality

def main():
    # Create an instance of the Functionality class to use its methods
    functions = Functionality()

    while True:
        # Display the Expense Tracker title

        print("\n=========================================================")
        print("\n==================== Expense Tracker ====================")
        print("\n=========================================================")

        # Display the list of current expenses
        functions.display_expenses()

        # Show the available options to the user
        print("1. Lookup friends detail")
        print("2. Add friends")
        print("3. Add an Expense")
        print("4. Record a payment")
        print("5. Exit")

        # Prompt the user to enter their choice
        choice = input("Enter your choice (1-5): ")

        # Perform actions based on the user's choice
        if choice == '1':
            # Call the function to look up details for a specific participant
            functions.lookup__details()

        elif choice == '2':
            # Call the function to add a new participant to the tracker
            functions.add_participant()

        elif choice == '3':
            # Call the function to add a new expense
            functions.add_expense()

        elif choice == '4':
            # Call the function to record a payment made by a participant
            functions.record_payment()

        elif choice == '5':
            # Save data and exit the program
            print("Data saved. Exiting.")
            break

        else:
            # If the user enters an invalid choice, notify them
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
