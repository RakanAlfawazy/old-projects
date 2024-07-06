from typing import NoReturn
from .database import ReportGenerator, Database
from .models import User, Transaction


class ConsoleGUI:
    def __init__(self, db: Database) -> None:
        self.db: Database = db
        self.report_generator: ReportGenerator = ReportGenerator(db)
        self.current_user_id: int = None
        self.current_username: str = None

    def main_menu(self) -> NoReturn:
        while True:
            print("\n--- Main Menu ---")
            if self.current_username:
                print(f"Logged in as: {self.current_username}")
            print("[1] Add User")
            print("[2] Add Transaction")
            print("[3] Generate Report")
            print("[4] Exit")
            choice: str = input("Choose an option: ")

            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.add_transaction()
            elif choice == '3':
                self.generate_report_menu()
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

    def add_user(self) -> None:
        username: str = input("Enter user's username: ")
        user: User = User(username)
        try:
            self.db.add_user(user)
            print(f"User '{username}' added.")
            self.current_user_id = self.db.get_user_id(username)
            self.current_username = username
            print(f"You are now logged in as {username}.")
        except Exception as e:
            print(f"Failed to add user: {e}")

    def add_transaction(self) -> None:
        if not self.current_user_id:
            print("No user logged in. Please log in or add a user first.")
            return

        print(f"Adding transaction for {self.current_username}.")

        try:
            amount: float = float(input("Enter the amount: "))
            category: str = input("Enter category: ")
            date: str = input("Enter date (YYYY-MM-DD): ")
            t_type: str = input("Enter type (expense/income): ")
            transaction: Transaction = Transaction(self.current_user_id, amount, category, date, t_type)
            self.db.add_transaction(transaction)
            print("Transaction added successfully.")
        except ValueError:
            print("Invalid input. Please ensure all inputs are correctly formatted.")

    def generate_report_menu(self) -> None:
        while True:
            print("\n--- Generate Report ---")
            print("[1] Total expenses")
            print("[2] Total income")
            print("[3] Spending by category")
            print("[4] Transactions in each category")
            print("[5] Average transaction value by category")
            print("[6] Go back")
            choice: str = input("Select a report to generate: ")

            if choice == '6':
                break
            else:
                self.display_report(choice)

    def display_report(self, report_type: str) -> None:
        if not self.current_user_id:
            print("No user logged in. Please log in to generate a report.")
            return

        try:
            if report_type == '1':
                print(f"Total expenses: {self.report_generator.total_expenses(self.current_user_id)}")
            elif report_type == '2':
                print(f"Total income: {self.report_generator.total_income(self.current_user_id)}")
            elif report_type == '3':
                print("Spending by category:")
                for category, amount in self.report_generator.spending_by_category(self.current_user_id).items():
                    print(f"  {category}: {amount}")
            elif report_type == '4':
                print("Transactions by category:")
                for category, count in self.report_generator.transactions_by_category(self.current_user_id).items():
                    print(f"  {category}: {count}")
            elif report_type == '5':
                print("Average transaction value by category:")
                for category, avg_value in self.report_generator.average_transaction_value_by_category(self.current_user_id).items():
                    print(f"  {category}: {avg_value}")
            else:
                print("Invalid report type selected. Please try again.")
        except Exception as e:
            print(f"Failed to generate report: {e}")

