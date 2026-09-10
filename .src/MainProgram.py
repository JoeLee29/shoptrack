from Administrator import *
from Cashier import *
from Accountant import *
from StockManager import*
from Supplier import *

#Introduction to ShopTrack
print("\nWelcome to ShopTrack!")
print("The ShopTrack system is designed to perform tasks for retail stores ONLY on the current date.")
print("If using the system with another date, kindly exit the program and re-enter.\n")

#Prompt user to input date, if date input is valid, break the loop and enter the menu program
print("First, please input the details of current date.")
while True:
    try:
        current_date_list = request_date()
        current_date = current_date_list[0]
        current_year = current_date_list[1]
        current_month = current_date_list[2]
        break

    #If ValueError, try again by entering next iteration
    except ValueError:
        print("Invalid date. Please try again.")

#Main Menu Program
while True:
    print("\n-----MAIN MENU-----")
    print("1. Administrator")
    print("2. Cashier")
    print("3. Accountant")
    print("4. Stock Manager")
    print("5. Supplier")
    print("6. Exit\n")

    #Prompt user to choose roles
    roles = input("Please enter the current role to perform tasks (1-6): ")
    match roles:
        case "1": #Administrator
            while True:
                print("\n=====Administrator Page=====")
                print("1. View Inventory Overview")
                print("2. Add or Remove Items")
                print("3. Update Item Details")
                print("4. Generate/Update Daily Report")
                print("5. View Previous Reports")
                print("6. Exit to Main\n")

                admin_tasks = input("Enter the task number to perform (1-6): ")
                match admin_tasks:
                    case "1":
                        view_inventory()
                    case "2":
                        #Prompt user to keep adding or removing items using while loop
                        while True:
                            print("\n1. Add Items")
                            print("2. Remove Items")
                            print("3. Exit to Administrator Page\n")

                            choice = input("Choose an option (1-3): ")
                            match choice:
                                case "1":
                                    add_item()
                                case "2":
                                    remove_item()
                                case "3":
                                    #Break the loop when exiting to Administrator Page
                                    print("Exiting to Administrator Page...\n")
                                    break
                    case "3":
                        #Prompt user to keep updating item details using while loop
                        while True:
                            print("\n---Update Item Details---")
                            print("1. Item Price")
                            print("2. Item Quantity")
                            print("3. Exit to Administrator Page\n")

                            choice = input("Choose an option (1-3): ")
                            match choice:
                                case "1":
                                    update_price()
                                case "2":
                                    update_quantity()
                                case "3": #Break the loop when exiting
                                    print("Exiting to Administrator Page...\n")
                                    break
                    case "4":
                        check_daily_report_generated(current_date)
                    case "5":
                        #Prompt user to keep viewing different reports using while loop
                        while True:
                            print("\n-------View Reports-------")
                            print("1. Daily Report")
                            print("2. Monthly Financial Report")
                            print("3. Exit to Administrator Page\n")

                            choice = input("Choose an option (1-3): ")
                            match choice:
                                case "1":
                                    ReportDate = input("Enter Date to view daily report (DD/MM/YYYY): ").strip()
                                    view_daily_report(ReportDate)
                                case "2":
                                    #Keep looping until the input are valid.
                                    while True:
                                        try:
                                            ReportMonth = int(input("Enter month number to view monthly report (1-12): ").strip())
                                            ReportYear = int(input("Enter year to view monthly report: ").strip())
                                            view_monthly_financial_report(ReportMonth, ReportYear)
                                            break
                                        except ValueError:
                                            print("Invalid input. Please try again.")
                                case "3": #Break the loop when exiting
                                    print("Exiting to Administrator Page...\n")
                                    break
                                case _:
                                    print("Invalid choice. Try again.\n")
                    case "6":
                        print("Exiting to Main...\n")
                        break
                    case _:
                        print("Invalid choice. Try again.\n")

        case "2": #Cashier
            while True:
                print("\n========Cashier Page========")
                print("1. Process Sales Transactions")
                print("2. View Previous Receipts")
                print("3. Make Return Transactions")
                print("4. View Return Receipts")
                print("5. Exit to Main\n")

                cashier_tasks = input("Enter the task number to perform (1-5): ")
                match cashier_tasks:
                    case "1":
                        sales_transaction(current_date_list)
                    case "2":
                        #Prompt user to keep viewing different receipts using while loop
                        while True:
                            print("\n---View Receipts by Details---")
                            print("1. Transaction ID")
                            print("2. Transaction Date")
                            print("3. Exit to Cashier Page\n")

                            choice = input("Choose an option (1-3): ")
                            match choice:
                                case "1":
                                    TransactionID = input("Enter Transaction ID to view receipt: ").upper().strip()
                                    view_sales_by_id(TransactionID)
                                case "2":
                                    TransactionDate = input("Enter Date to view receipts (DD/MM/YYYY): ").strip()
                                    view_sales_by_date(TransactionDate)
                                case "3":
                                    print("Exiting to Cashier Page...\n")
                                    break
                                case _:
                                    print("Invalid choice. Try again.\n")
                    case "3":
                        return_transaction(current_date_list)
                    case "4":
                        ReturnDate = input("Enter Date to view returned receipts (DD/MM/YYYY): ").strip()
                        view_return_transaction_by_date(ReturnDate)
                    case "5":
                        print("Exiting to Main...\n")
                        break
                    case _:
                        print("Invalid choice. Try again.\n")

        case "3": #Accountant
            while True:
                #Half of tasks for Accountant are already performed in Administrator Page
                print("\n========Accountant Page========")
                print("1. View Supplier Payments")
                print("2. Generate Monthly Financial Report")
                print("3. Exit to Main\n")

                accountant_tasks = input("Enter the task number to perform (1-3): ")
                match accountant_tasks:
                    case "1":
                        #Prompt user to keep viewing different payments using while loop
                        while True:
                            print("\n---View Payments by Details---")
                            print("1. Last Payment Status")
                            print("2. Order ID")
                            print("3. Exit to Supplier Page\n")

                            choice = input("Choose an option (1-3): ")
                            match choice:
                                case "1":
                                    print("Choose the last updated payment status from menu to view payments:")
                                    #Print the status menu and prompt user to choose
                                    payment_status = payment_status_menu()
                                    choice = input(
                                        "Do you want to specify the date of last updated status (Y/N): ").upper().strip()
                                    if choice == "Y":
                                        status_date = input(
                                            "Enter the specified date of the last updated status (DD/MM/YYYY): ").strip()
                                        view_payments_by_status(payment_status, status_date)
                                    else:
                                        #Print all payments with input status (all dates)
                                        view_payments_by_status(payment_status)
                                case "2":
                                    order_id = input("Enter Order ID to view payments: ").upper().strip()
                                    view_payments_by_order_id(order_id)
                                case "3":
                                    print("Exiting to Supplier Page...\n")
                                    break
                                case _:
                                    print("Invalid choice. Try again.\n")
                    case "2":
                        check_monthly_report_generated(current_date, current_month, current_year)
                    case "3":
                        print("Exiting to Main...\n")
                        break
                    case _:
                        print("Invalid choice. Try again.\n")

        case "4": #Stock Manager
            while True:
                print("\n=====Stock Manager Page=====")
                print("1. View Supplier List")
                print("2. Add Supplier")
                print("3. Manage Supplier Details")
                print("4. Send Restock Request")
                print("5. Exit to Main\n")

                stock_manager_tasks = input("Enter the task number to perform (1-5): ")
                match stock_manager_tasks:
                    case "1":
                        view_supplier()
                    case "2":
                        add_supplier()
                    case "3":
                        edit_supplier()
                    case "4":
                        create_order(current_date_list)
                    case "5":
                        print("Exiting to Main...\n")
                        break
                    case _:
                        print("Invalid choice. Try again.\n")

        case "5": #Supplier
            while True:
                print("\n=====Supplier Page=====")
                print("1. View Orders")
                print("2. Update Order Status")
                print("3. Make Payments")
                print("4. Exit to Main\n")

                supplier_tasks = input("Enter the task number to perform (1-4): ")
                match supplier_tasks:
                    case "1":
                        while True:
                            print("\n---View Orders by Details---")
                            print("1. Last Order Status")
                            print("2. Order Date")
                            print("3. Supplier ID")
                            print("4. Exit to Supplier Page\n")

                            choice = input("Choose an option (1-4): ")
                            match choice:
                                case "1":
                                    print("Choose the last updated order status from menu to view orders:")
                                    #Print the status menu and prompt user to choose
                                    order_status = order_status_menu()
                                    if order_status: #To exclude None value when user choose to exit in menu
                                        choice = input("Do you want to specify the date of last updated status (Y/N): ").upper().strip()
                                        if choice == "Y":
                                            status_date = input("Enter the specified date of the last updated status (DD/MM/YYYY): ").strip()
                                            view_orders_by_status(order_status, status_date)
                                        else:
                                            #Print all payments with input status (all dates)
                                            view_orders_by_status(order_status)
                                case "2":
                                    date_input = input("Enter Order Date to view orders (DD/MM/YYYY): ").strip()
                                    view_orders_by_date(date_input)
                                case "3":
                                    supplier_id = input("Enter Supplier ID to view orders: ").upper().strip()
                                    view_orders_by_sup_id(supplier_id)
                                case "4":
                                    print("Exiting to Supplier Page...\n")
                                    break
                                case _:
                                    print("Invalid choice. Try again.\n")
                    case "2":
                        #Prompt the user to keep updating order status
                        while True:
                            update_order_status(current_date_list)
                            choice = input("Would you like to update another order (Y/N): ").upper().strip()
                            if choice != "Y":
                                print("Exiting to Supplier Page...\n")
                                break
                    case "3":
                        #Prompt the user to keep making payments (Must be approved by Accountant)
                        while True:
                            #Ask the user to confirm to continue making payment
                            print("Please make sure the payments made are approved by Administrator and Accountant.")
                            choice_to_continue = input("Would you like to continue? (Y/N): ").upper().strip()
                            if choice_to_continue != "Y":
                                print("Exiting to Supplier Page...\n")
                                break

                            OrderID_to_pay = input("Enter Order ID to make payment: ").upper().strip()
                            make_payment(current_date, OrderID_to_pay)

                            choice = input("Would you like to make another payment (Y/N): ").upper().strip()
                            if choice != "Y":
                                print("Exiting to Supplier Page...\n")
                                break
                    case "4":
                        print("Exiting to Main...\n")
                        break
                    case _:
                        print("Invalid choice. Try again.\n")

        case "6":
            #Auto generating daily report when quiting the system
            #If the daily report already generated, refresh and update a new one
            check_daily_report_generated(current_date)
            print("\nThank you for using ShopTrack! ")
            break

        #When the input is invalid, continue to next iteration
        case _:
            print("Invalid input. Please try again.\n")
            continue
