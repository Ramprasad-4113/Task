''' 
BUDGET_PLANNER
-- Add Income and Expenses
-- Set Monthly budget limits
-- Show variance between budget vs actual expense
-- Export monthly budget report
'''



income=[]  
expenses=[]  
budgets ={}

print('==== Budget Planner ===')

#Adding income and expenses

def add_income(amount):
    income.append({"amount": amount})
    print(f"Income of {amount} is added")
    
def add_expenses(amount, category):
    expenses.append({"amount":amount,"category": category})
    print(f"Expenses of {amount} in {category} is added")
    
def fun1():
    amount=int(input("Enter the amount : "))
    if amount>=0:
        add_income(amount)
    else:
        print("Enter a valid amount")
        
def fun2():
    amount=int(input("Enter the expenses :"))
    category=input("Enter the expenses category here : ")
    add_expenses(amount, category)
    
#Set monthly budget limits

def set_budget():
    category=input('Enter the budget category name: ')
    amount = int(input(f"Enter budget limit for {category}: "))
    if amount>0:
        budgets[category] = amount
        print(f"Budget set for {category} is : {amount}")
    else:
        print("Enter a valid amount")
    
#Show variance between budget vs. actual
def show_variance():
    print("=== Budget vs Actual Expenses ===")
    print("Category         Budget   Spent  Variance  ")
    
    print("-----------------------------------------------")

    for category in budgets:
        budget_limit = budgets[category]
        actual_expense = sum(item['amount'] for item in expenses if item['category'] == category)
        variance = budget_limit - actual_expense
        print(f"{category:<12}  {budget_limit:>8}Rs {actual_expense:>8}Rs {variance:>8}Rs")

#Export monthly budget report

def export_report():
    with open("report.txt", 'w') as file:
        file.write("=== Monthly Budget Report ===")
        
        file.write("Income: ")
        for item in income:
            file.write(f"{item['amount']}")
        file.write("Expenses:")
        for item in expenses:
            file.write(f"{item['amount']} ({item['category']})")
            
        file.write("Budget vs Actual:")
        for category in budgets:
            budget_limit=budgets[category]
            spent=sum(item['amount'] for item in expenses if item ["category"]==category)
            file.write(f"{category}: Budget={budgets}, Spent={spent}")
    print("Report saved to 'report.txt'.")
    
    
    
def main_menu():
    while True:
        print("==== Main Menu ====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Set Budget")
        print("4. Show Variance")
        print("5. Export Report")
        print("6. Exit")
        
        choice = input("Choose an option (1-6): ")
        
        if choice == "1":
            amount = int(input("Enter income amount: "))
            if amount >= 0:
                add_income(amount)
            else:
                print("Amount must be positive.")
        
        elif choice == "2":
            amount = int(input("Enter expense amount: "))
            category = input("Enter category: ")
            if amount >= 0 and category:
                add_expenses(amount, category)
            else:
                print("Invalid input.")
           
        elif choice == "3":
            set_budget()
        
        elif choice == "4":
            if budgets:
                show_variance()
            else:
                print("No budgets set yet.")
        
        elif choice == "5":
            export_report()
        
        elif choice == "6":
            print("___ Operation Stopped ___")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()