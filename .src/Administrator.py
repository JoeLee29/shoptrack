"""
This module consists of all functions for Administrator Role.
Some validation functions used in the whole program is also in this module.
"""

# Date & Time Adjustments
def validate_days_in_month(month, year):
    """
    According to the input month and year, determine the total number of days in this month and year.
    """
    # Declare the variable
    days_in_month = 0
    # Use match-case to set the value of the variable
    match month:
        case 1 | 3 | 5 | 7 | 8 | 10 | 12:
            days_in_month = 31
        case 4 | 6 | 9 | 11:
            days_in_month = 30
        case 2:
        # Check for leap year
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                days_in_month = 29
            else:
                days_in_month = 28
        case _: #Using other input will show the message and return 0
            print("Invalid month.")
            days_in_month = 0
    return days_in_month
def request_time():
    """
    Prompt the user to enter the time in hour and minutes and return the formatted time.
    """
    hour = int(input("Enter hour (0-23): "))
    minute = int(input("Enter minute (0-59): "))

    #Check whether the input hour is in AM or PM and set the value of formatted hour.
    if 0 <= hour <= 12:
        period = "AM"
        formatted_hour = hour
    elif 13 <= hour <= 23:
        period = "PM"
        formatted_hour = hour - 12
    else:
        raise ValueError #if the input is not in range, raise ValueError and use try-except outside this function.

    if not 0 <= minute <= 59:
        raise ValueError

    #Convert the value to formatted strings.
    if 0 <= formatted_hour <= 9:
        formatted_hour = "0" + str(formatted_hour)
    else:
        formatted_hour = str(formatted_hour)

    if 0 <= hour <= 9:
        hour = "0" + str(hour)
    else:
        hour = str(hour)

    if 0 <= minute <= 9:
        minute = "0" + str(minute)
    else:
        minute = str(minute)

    #Format the time.
    #Store all value into a list and return it (Easier to obtain details of the time for further usage).
    formatted_time = f'{formatted_hour}:{minute} {period}'
    time_list = [formatted_time, hour, minute]
    return time_list
def request_date():
    """
    Prompt the user to enter the date in year, month and day and return the formatted date.
    """
    year = int(input("Enter year: "))
    month = int(input("Enter month (1-12): "))
    day = int(input("Enter day (1-31): "))

    # If the input is not in range, raise ValueError and use try-except outside this function.
    if not 0 < year <= 9999:
        raise ValueError("The input year is out of range")

    days_in_month = validate_days_in_month(month, year)
    if not 1 <= day <= days_in_month:
        raise ValueError("The input day is out of range.")

    #Convert the value to formatted strings.
    if 0 < year <= 9:
        year = "000" + str(year)
    elif 10 <= year <= 99:
        year = "00" + str(year)
    elif 100 <= year <= 999:
        year = "0" + str(year)
    else:
        year = str(year)

    if 0 <= month <= 9:
        month = "0" + str(month)
    else:
        month = str(month)

    if 0 <= day <= 9:
        day = "0" + str(day)
    else:
        day = str(day)

    # Format the date.
    # Store all value into a list and return it (Easier to obtain details of the date for further usage).
    formatted_date = f'{day}/{month}/{year}'
    date_list = [formatted_date, year, month, day]
    return date_list
def find_valid_return_dates(formatted_start_date):
    """
    The valid period to return transactions is 14 days after the transaction date.
    Use this function to return the list of all valid dates to return certain transactions.
    """
    #Obtain the three data from the input formatted date.
    date_details = formatted_start_date.strip().split('/')
    day = int(date_details[0])
    month = int(date_details[1])
    year = int(date_details[2])

    #Check the total number of days in the month.
    days_in_the_month = validate_days_in_month(month, year)
    valid_return_date_list = [] #Store all valid dates in the new list.
    #For every iteration of this loop, generate the new dates with formats.
    for i in range(14):
        #Check date validation. Uses same algorithm with the function request_date().
        return_day = day + i
        if return_day > days_in_the_month:
            return_month = month + 1
            return_day -= days_in_the_month
            if return_month > 12:
                return_year = year + 1
                return_month -= 12
            else:
                return_year = year
        else:
            return_month = month
            return_year = year

        #Convert the details into strings.
        if 0 < return_year <= 9:
            return_year = "000" + str(return_year)
        elif 10 <= return_year <= 99:
            return_year = "00" + str(return_year)
        elif 100 <= return_year <= 999:
            return_year = "0" + str(return_year)
        else:
            return_year = str(return_year)

        if 0 <= return_month <= 9:
            return_month = "0" + str(return_month)
        else:
            return_month = str(return_month)

        if 0 <= return_day <= 9:
            return_day = "0" + str(return_day)
        else:
            return_day = str(return_day)

        formatted_return_date = f'{return_day}/{return_month}/{return_year}'
        valid_return_date_list.append(formatted_return_date)
    return valid_return_date_list
def check_later_date(first_date, second_date):
    """
    Compare two dates input and determine the earlier and later date.
    Uses this function when updating status. To prevent logic error.
    """
    #Obtain the three data from the two input formatted dates.
    first_date_details = first_date.strip().split('/')
    day1 = int(first_date_details[0])
    month1 = int(first_date_details[1])
    year1 = int(first_date_details[2])

    second_date_details = second_date.strip().split('/')
    day2 = int(second_date_details[0])
    month2 = int(second_date_details[1])
    year2 = int(second_date_details[2])

    #Compare the year of two dates first, then compare month and day.
    if year1 > year2:
        return first_date
    elif year1 < year2:
        return second_date
    else:
        if month1 > month2:
            return first_date
        elif month1 < month2:
            return second_date
        else:
            if day1 > day2:
                return first_date
            elif day1 < day2:
                return second_date
            else: #If the day1 and day2 are the same, return the second date.
                return second_date
def find_yesterday(formatted_date_input):
    """
    Determine the formatted date of last day according to the input formatted date.
    Uses this function to find variance in daily reports.
    """
    #Obtain the details from formatted date.
    date_details = formatted_date_input.strip().split('/')
    day = int(date_details[0])
    month = int(date_details[1])
    year = int(date_details[2])

    yesterday = day - 1
    #Validation: If yesterday is 0, jump to previous month. If previous month is 0, jump to previous year.
    if yesterday == 0:
        month -= 1
        if month == 0:
            year -= 1
            month = 12
        #If jump to previous month, the day value is the last day of the previous month.
        yesterday = validate_days_in_month(month, year)

    #Format the strings.
    if 0 < year <= 9:
        year = "000" + str(year)
    elif 10 <= year <= 99:
        year = "00" + str(year)
    elif 100 <= year <= 999:
        year = "0" + str(year)
    else:
        year = str(year)

    if 0 <= month <= 9:
        month = "0" + str(month)
    else:
        month = str(month)

    if 0 <= yesterday <= 9:
        yesterday = "0" + str(yesterday)
    else:
        yesterday = str(yesterday)

    #Return the new date with format.
    formatted_yesterday_date = f'{yesterday}/{month}/{year}'
    return formatted_yesterday_date
def determine_month_name(month_number):
    """
    According to the input number of month, return the month name.
    """
    #Check whether the input is an integer or not.
    try:
        month_number = int(month_number)
    except ValueError:
        print("Invalid month number")
        return None

    #Return the month name by its number.
    if month_number == 0:
        return "December"
    elif month_number == 1:
        return "January"
    elif month_number == 2:
        return "February"
    elif month_number == 3:
        return "March"
    elif month_number == 4:
        return "April"
    elif month_number == 5:
        return "May"
    elif month_number == 6:
        return "June"
    elif month_number == 7:
        return "July"
    elif month_number == 8:
        return "August"
    elif month_number == 9:
        return "September"
    elif month_number == 10:
        return "October"
    elif month_number == 11:
        return "November"
    elif month_number == 12:
        return "December"
    else:
        print("Invalid month number")
        return None

# Inventory Details Validation
def validate_code(code_input):
    """
    Checks if the input code is 1 letter followed by 3 numbers.
    Raises ValueError on invalid format.
    """
    #Check the total length of the item code
    if len(code_input) != 4:
        raise ValueError("Code must be exactly 4 characters long.")

    #Check the first character (must be capital letters)
    first_char = code_input[0]
    if not "A" <= first_char <= "Z":
        raise ValueError("The first character must be a capital letter (A-Z).")

    #Check the remaining four characters (must be numbers)
    number_part = code_input[1:]
    try:
        #Raise ValueError when fail to convert all characters into integers
        int(number_part)
    except ValueError:
        raise ValueError("The last 3 characters must be numbers (0-9).")

    #If all checks pass, return the valid code
    return code_input
def validate_price(price_input):
    """
    Check if the input price is float numbers.
    """
    #Raise ValueError if the input price is not a float.
    try:
        price_float = float(price_input)

        if price_float < 0: #Check if the input is not positive.
            raise ValueError("The input price must be equal to or greater than 0.")

    except ValueError:
        raise ValueError("The price must be integer or float.")

    return price_float  # Return the float value if valid.
def validate_quantity(quantity_input):
    """
    Check if the input quantity is integer.
    """
    # Raise ValueError if the input price is not an integer.
    try:
        quantity_int = int(quantity_input)

        if quantity_int < 0:
            raise ValueError("The input quantity must be equal to or greater than 0.")

    except ValueError:
        raise ValueError("The quantity must be an integer.")

    return quantity_int # Return the input value if no error.

# Parse Lines to Obtain Accurate Details
def parse_inventory_line(line):
    """
    Parses a fixed-width inventory details line using string slicing.
    Use this function instead of split() to get the details.
    """
    # Slice the string based on the defined widths and strip whitespaces
    item_code = line[0:10].strip()  # Width 10
    item_name = line[10:40].strip()  # Width 30
    item_price = line[40:54].strip()  # Width 14
    quantity = line[54:62].strip()  # Width 8

    # Return the clean data and store in a list
    return [item_code, item_name, item_price, quantity]
def parse_sales_item_line(line):
    """
    Parses a fixed-width sales item details line using string slicing.
    Use this function instead of split() to get the details.
    """
    # Slice the string based on the defined widths and strip whitespaces
    item_code = line[0:10].strip()  # Width 10
    item_name = line[10:40].strip()  # Width 30
    unit_price = line[40:54].strip()  # Width 14
    sold_quantity = line[54:62].strip()  # Width 8
    discount = line[62:74].strip()  #Width 12
    total_price_per_item = line[74:84].strip()  #Width 10

    # Return the clean data and store in a list
    return [item_code, item_name, unit_price, sold_quantity, discount, total_price_per_item]
def parse_supplier_line(line):
    """
    Parses a fixed-width supplier detail line using string slicing.
    Use this function instead of split() to get the details and store in a list.
    """
    #Slice the string based on the defined widths and strip whitespace
    sup_id = line[0:6].strip()  # Width 6
    company_name = line[6:26].strip()  # Width 20
    contact_name = line[26:42].strip()  # Width 16
    contact_number = line[42:54].strip()  # Width 12
    contact_email = line[54:74].strip()  # Width 20
    order_qty = line[74:84].strip()  # Width 10
    #Skip the single space at index 84
    item_qty = line[85:95].strip()  # Width 10

    #Return the clean data in list
    return [sup_id, company_name, contact_name, contact_number, contact_email, order_qty, item_qty]
def parse_order_item_line(line):
    """
    Parses a fixed-width order item detail line using string slicing.
    Use this function instead of split() to get the details and store in a list.
    """
    #Slice the string based on the defined widths and strip whitespace
    item_code = line[0:8].strip()  # Width 8
    item_name = line[8:28].strip()  # Width 20
    item_cost = line[28:42].strip()  # Width 14
    request_quantity = line[42:50].strip()  # Width 8
    total_cost = line[50:60].strip()  # Width 10

    #Return the clean data in list
    return [item_code, item_name, item_cost, request_quantity, total_cost]

#Task 1: View Inventory Overview
def create_inventory_file():
    """
    Create a new inventory overview only for primary setup or when all stocks become empty
    """
    with open("inventory.txt", "w") as file:
        # Set up the primary format of the inventory overview
        heading = [
            "-" * 22 + "Inventory Overview" + "-" * 22 + "\n",
            f"{"ItemCode".center(10)}{"ItemName".center(30)}{"ItemPrice(RM)".center(14)}{"Quantity".center(8)}\n",
            "-" * 62 + "\n"
        ]
        # Add the heading into the empty inventory file
        file.writelines(heading)
    view_inventory()
def view_inventory():
    """
    View inventory overview.
    Auto-run this function only when changes made.
    User also can manually run this function.
    """
    #Read and print all contents in the inventory file.
    try:
        with open("inventory.txt", "r") as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError: #if the file is not found, create it with headings.
        create_inventory_file()

#Task 2: Add New Items or Remove Existing Items
def add_item():
    """
    Add an item to the inventory.
    Add ItemCode, ItemName, ItemPrice (per unit), Quantity in a single line.
    Use validate functions to check inputs.
    """
    # Keep running the while loop until the user stop adding items.
    adding_item = True
    while adding_item:
        while True:
            InputCode = input("Enter the Item Code to be added: ").strip().upper() #remove whitespaces
            # Validate the input code, if valid, assign to ItemCode, if not, try again
            try:
                ItemCode = validate_code(InputCode)
                # Check if the inventory file exists. If inventory does not exist, create the file with heading.
                # If the input item code already exists, try again. If not, break the input code loop.
                try:
                    with open("inventory.txt", "r") as file:
                        contents = file.read()
                    if ItemCode in contents:
                        print("The Item Code already exists. Please use a new code.")
                        continue
                except FileNotFoundError:
                    create_inventory_file()
                break
            except ValueError as e:
                print("Invalid Item Code. Try again.")
                print(e)
                choice = input("Would you like to input another item code (Y/N): ").strip().upper()
                if choice != "Y":
                    return

        ItemName = input("Enter the Item Name (Max 30 characters): ").strip().title() #remove whitespaces and capitalize every word
        InputPrice = input("Enter the Item Price (RM): ")
        try: #Check if the input price is valid, if valid, assign to ItemPrice by string
            validated_price = validate_price(InputPrice)
            ItemPrice = f"{validated_price:.2f}"
        except ValueError as e:
            print("Invalid price. Try again.")
            print(e)
            continue

        Quantity = "0"
        # Add all details into single line and \n to enter new line
        ItemDetails = f"{ItemCode.center(10)}{ItemName.center(30)}{ItemPrice.center(14)}{Quantity.rjust(8)}\n"

        # Append the detail line into inventory file.
        with open("inventory.txt", "a") as file:
            file.write(ItemDetails)
        print(f"Item code {ItemCode} successfully added!")

        # Ask user whether continue adding another item or not.
        choice = input("Would you like to add another item? (Y/N): ").upper()
        if choice != "Y":
            #If not, change adding_item False to stop the while loop.
            adding_item = False

    #Finally, view inventory again and exit the process.
    view_inventory()
    print("Exiting item addition process...\n")
def remove_item():
    """
    Remove an item from the inventory.
    Remove the whole line of the details of the item.
    """
    # Keep running the while loop until the user stop removing items.
    removing_item = True
    while removing_item:
        ItemCode = input("Enter the Item Code to be removed: ").strip().upper()
        #If the inventory file not exists, stop the function.
        try:
            with open("inventory.txt", "r") as file:
                contents = file.readlines()
        except FileNotFoundError:
            print("Inventory file not found.")
            return

        # Change to True only when the item successfully removed.
        item_removed = False
        new_contents = []
        # Use enumerate function to return the index number of every line and its contents
        for line_index, line_content in enumerate(contents):
            #Add the heading lines with no item details
            if line_index < 3:
                new_contents.append(line_content)
                continue

            #Skip the line which starts with the item code required.
            if line_content.startswith(f"{ItemCode.center(10)}"):
                item_removed = True
            #Append other unrelated item details.
            else:
                new_contents.append(line_content)

        #If the line is removed, write the new contents to inventory
        if item_removed:
            with open("inventory.txt", "w") as file:
                file.writelines(new_contents)
            print(f"Item code {ItemCode} successfully removed!")
        #If item_removed = False, means the line starts with the required code is not found.
        else:
            print(f"Item code {ItemCode} is not found in the inventory.")

        # Ask user whether continue removing another item or not.
        choice = input("Would you like to remove another item? (Y/N): ").upper()
        if choice != "Y":
            # If not, change removing_item False to stop the while loop.
            removing_item = False
    #Finally, view inventory again and exit the process.
    view_inventory()
    print("Exiting item removal process...")

#Task 3: Update Item Details (Price & Quantity)
def update_price():
    """
    Update the unit price of an item manually from the inventory.
    Read the line starting with required code and change its details, then append again into new contents.
    """
    view_inventory()
    # Keep running the while loop until the user stop changing details.
    updating_price = True
    while updating_price:
        ItemCode = input("Enter the Item Code which its price to be changed: ").strip().upper()
        #If the inventory file not exists, stop the function.
        try:
            with open("inventory.txt", "r") as file:
                contents = file.readlines()
        except FileNotFoundError:
            print("Inventory file not found.")
            return

        # Change to True only when the price successfully changed.
        price_updated = False
        #Define variables first.
        new_contents = []
        OriginalPrice = 0
        NewItemPrice = 0
        # Use enumerate function to return the index number of every line and its contents
        for line_index, line_content in enumerate(contents):
            #Add the heading lines with no item details
            if line_index < 3:
                new_contents.append(line_content)
                continue

            #Change the price in the line which starts with the item code required.
            if line_content.startswith(f"{ItemCode.center(10)}"):
                ItemDetail = parse_inventory_line(line_content)
                OriginalPrice = float(ItemDetail[2])
                print(f"The original price of the item {ItemCode} is RM {OriginalPrice:.2f}.")
                while True:
                    NewInputPrice = input("Enter the New Item Price (RM): ")
                    try:
                        #Attempt validation to input price
                        validated_price = validate_price(NewInputPrice)
                        #If valid, assign the value to NewItemPrice by string
                        NewItemPrice = f"{validated_price:.2f}"
                        break
                    except ValueError as e:
                        print("Invalid price. Try again.")
                        print(e)

                #Arrange the new details in a new single line and append to the inventory
                NewItemDetails = (f"{ItemDetail[0].center(10)}{ItemDetail[1].center(30)}{NewItemPrice.center(14)}"
                                  f"{ItemDetail[3].rjust(8)}\n")
                new_contents.append(NewItemDetails)
                price_updated = True
            else:
                # Append other unrelated item details.
                new_contents.append(line_content)

        #If the price is changed, write the new contents to inventory
        if price_updated:
            with open("inventory.txt", "w") as file:
                file.writelines(new_contents)
            print(f"Item price with item code {ItemCode} successfully changed "
                  f"from RM {OriginalPrice:.2f} to RM {NewItemPrice}!")
        else:
            # If False, means the line starts with the required code is not found.
            print(f"Item code {ItemCode} is not found in the inventory.")

        # Ask user whether continue changing another price or not.
        choice = input("Would you like to change price of another item? (Y/N): ").upper()
        if choice != "Y":
            # If not, change False to stop the while loop.
            updating_price = False
    #Finally, view inventory again and exit the process.
    view_inventory()
    print("Exiting price changing process...")
def update_quantity():
    """
    Update the quantity of an item manually from the inventory.
    Read the line starting with required code and change its details, then append again into new contents.
    """
    view_inventory()
    # Keep running the while loop until the user stop changing details.
    updating_quantity = True
    while updating_quantity:
        ItemCode = input("Enter the Item Code which its quantity to be changed: ").strip().upper()
        #If the inventory file not exists, stop the function.
        try:
            with open("inventory.txt", "r") as file:
                contents = file.readlines()
        except FileNotFoundError:
            print("Inventory file not found.")
            return

        # Change to True only when the quantity successfully changed.
        quantity_updated = False
        #Define variables first.
        new_contents = []
        OriginalQuantity = 0
        NewQuantity = 0
        # Use enumerate function to return the index number of every line and its contents
        for line_index, line_content in enumerate(contents):
            #Add the heading lines with no item details
            if line_index < 3:
                new_contents.append(line_content)
                continue

            #Change the quantity in the line which starts with the item code required.
            if line_content.startswith(f"{ItemCode.center(10)}"):
                ItemDetail = parse_inventory_line(line_content)
                OriginalQuantity = int(ItemDetail[3])
                print(f"Original quantity of the item {ItemCode} is {OriginalQuantity}.")

                while True: #Check the input quantity, if valid, assign to NewQuantity and end the loop
                    NewInputQuantity = input("Enter the New Item Quantity: ")
                    try:
                        validated_quantity = validate_quantity(NewInputQuantity)
                        NewQuantity = str(validated_quantity)
                        break
                    except ValueError as e:
                        print("Invalid quantity. Try again.")
                        print(e)

                #Arrange the new details in a new single line and append to the inventory
                NewItemDetails = (f"{ItemDetail[0].center(10)}{ItemDetail[1].center(30)}{ItemDetail[2].center(14)}"
                                  f"{NewQuantity.rjust(8)}\n")
                new_contents.append(NewItemDetails)
                quantity_updated = True
            else:
                # Append other unrelated item details.
                new_contents.append(line_content)

        #If the quantity is changed, write the new contents to inventory
        if quantity_updated:
            with open("inventory.txt", "w") as file:
                file.writelines(new_contents)
            print(f"Item quantity with item code {ItemCode} successfully changed "
                  f"from {OriginalQuantity} to {NewQuantity}!")
        else:
            # If False, means the line starts with the required code is not found.
            print(f"Item code {ItemCode} is not found in the inventory.")

        # Ask user whether continue changing another quantity or not.
        choice = input("Would you like to change quantity of another item? (Y/N): ").upper()
        if choice != "Y":
            # If not, change False to stop the while loop.
            updating_quantity = False
    #Finally, view inventory again and exit the process.
    view_inventory()
    print("Exiting quantity changing process...")

#Task 4: Generate Daily Reports (Combine with Accountant)
def track_transaction(current_date, paid_or_return):
    """
    To track the total transactions, total items sold and total sales in the given date.
    paid_or_return must be 0 or 1.
    """
    #Declare the variables.
    total_transaction = 0
    total_items_sold = 0
    total_sales = 0.00

    #Check if the file exists.
    try:
        with open("sales.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        return total_transaction, total_items_sold, total_sales

    #Separate all receipts in the data into a list using the receipt header.
    receipt_separator = '\n' + '=' * 38 + 'Receipt' + '=' * 38 + '\n'
    receipt_blocks = contents.split(receipt_separator)
    #Append the target receipt into new list.
    target_transactions_list = []
    for block in receipt_blocks:
        #For paid receipts (paid_or_return == 1)
        if paid_or_return:
            #Separate the whole receipts into lines.
            line_details = block.split("\n")
            for line in line_details:
                #Check the target line, if the value in the line equals the target date, append to the new list.
                if line.startswith("Date:"):
                    date = line.split(":")[1].strip()
                    if date == current_date:
                        full_receipt = receipt_separator + block.strip() + "\n"
                        target_transactions_list.append(full_receipt)
        #For return receipts (paid_or_return == 0)
        else:
            #Check if the whole line in the receipt, if yes, append it.
            if f"Status: Returned ({current_date})" in block:
                full_receipt = receipt_separator + block.strip() + "\n"
                target_transactions_list.append(full_receipt)

    #For all receipts in the list, find the target data in the target line, and calculate totals for every receipt.
    for transaction in target_transactions_list:
        if transaction.strip():
            total_transaction += 1
            line_details = transaction.split("\n")
            for line in line_details:
                if "Total Quantity Sold" in line:
                    item_quantity = int(line.split(":")[1].strip())
                    total_items_sold += item_quantity
                if "Total Payment Amount" in line:
                    transaction_sales = float(line.split(": RM")[1].strip())
                    total_sales += transaction_sales

    return total_transaction, total_items_sold, total_sales
def check_variance_vs_yesterday(current_report_date, current_transaction_qty, current_items_sold, current_net_sales):
    """
    Obtain the data from the yesterday's daily report, and calculate variances according to the today's data.
    """
    #Determine the yesterday's formatted date using the validation function.
    yesterday_date = find_yesterday(current_report_date)
    #Check if the file exists, if not, return 0 for all variables.
    try:
        with open("daily_report.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        return 0, 0, 0

    #Split all reports into list using the header.
    report_separator = "\n" + "=" * 15 + "DAILY REPORT" + "=" * 15 + "\n"
    report_details = contents.split(report_separator)
    #Declare the variables.
    yesterday_report_found = False
    yesterday_transaction_qty = 0
    yesterday_items_sold = 0
    yesterday_net_sales = 0.00
    for report in report_details:
        #Check if the line included in the report, if yes, calculate data required and break
        if f"Report Date: {yesterday_date}" in report:
            yesterday_report_found = True
            line_details = report.split("\n")
            for line in line_details:
                    #Obtain all datas by checking every line.
                    #As some lines involve multiple data, using slicing to find target data.
                    if "Total Transactions" in line:
                        transaction_details = line.split(":")[1].strip()

                        yesterday_transaction_qty = int(transaction_details[:transaction_details.index("(")].strip())
                        yesterday_items_sold = int(transaction_details[transaction_details.index("(")+1:
                                                                       transaction_details.index("units")].strip())
                    if "NET SALES" in line:
                        sales_details = line.split(": RM")[1].strip()
                        yesterday_net_sales = float(sales_details[:sales_details.index("(")].strip())
            break

    #If yesterday's report not generated yet in the txt file, return 0
    if not yesterday_report_found:
        print("Yesterday's report not found.")
        return 0, 0, 0

    #Calculate the variance by formulas. Check whether all values are in specific types. (int and float)
    transaction_variance = int(current_transaction_qty) - int(yesterday_transaction_qty)
    items_sold_variance = int(current_items_sold) - int(yesterday_items_sold)
    try:
        sales_variance_percentage = int(((float(current_net_sales) - float(yesterday_net_sales))/
                                         float(yesterday_net_sales)) * 100)
    except ZeroDivisionError:
        sales_variance_percentage = 0

    return transaction_variance, items_sold_variance, sales_variance_percentage
def track_order(current_date, status):
    """
    Obtain the total number of orders and items ordered according to the given date and status.
    """
    #Check if the file exists.
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        return 0, 0

    #Separate all orders in the file into list using the header.
    order_separator = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_blocks = contents.split(order_separator)
    target_orders_list = []
    for block in order_blocks:
        line_details = block.split("\n")
        for line in line_details[::-1]:
            #Check if the line refers to the given date and status. If yes, append to new list and stop checking other lines.
            if f"{status} ({current_date})" in line:
                full_order = order_separator + block.strip() + "\n"
                target_orders_list.append(full_order)
                break

    total_order = 0
    total_items_ordered = 0
    for order in target_orders_list:
        #For every targeted order in the list, obtain the target data and calculate the totals.
        if order.strip():
            total_order += 1
            line_details = order.split("\n")
            for line in line_details:
                if "Total Items Quantity" in line:
                    item_quantity = int(line.split(":")[1].strip())
                    total_items_ordered += item_quantity

    return total_order, total_items_ordered
def calculate_total_stock():
    """
    Refer to inventory.txt, calculate the total number of stock and items.
    """
    #Check if the file exists.
    try:
        with open("inventory.txt", "r") as file:
            line_contents = file.readlines()
    except FileNotFoundError: #If the file is not found, create it with heading, and return 0
        create_inventory_file()
        return 0, 0

    item_code_qty = 0
    total_stock_qty = 0
    #Skip the headings, and parse every line into details, track the target details and calculate totals.
    for item in line_contents[3:]:
        if item.strip():
            item_details = parse_inventory_line(item)
            item_quantity = int(item_details[3])
            total_stock_qty += item_quantity
            item_code_qty += 1

    return total_stock_qty, item_code_qty
def generate_stock_level(total_stock_qty):
    """
    Track the total quantity of every item in the inventory.txt, and using the total stock quantity input to calculate
    the stock level percentage.
    Generate the stock level demonstration using histogram.
    Return the whole histogram by list and append it to the daily report.
    """
    #Generate the heading of histogram
    stock_level_histogram = [
        "Stock Level Histogram:\n",
    ]

    #If total stock is 0, we can't calculate percentages
    if not total_stock_qty or int(total_stock_qty) == 0:
        stock_level_histogram.append("Current Total Stock is 0. Cannot generate levels.\n")
        return stock_level_histogram

    #Check if the file exists.
    try:
        with open("inventory.txt", "r") as file:
            line_contents = file.readlines()
    except FileNotFoundError: #if the file is not found, create it with headings.
        create_inventory_file()
        #Add the message display no data into the histogram list and add into daily report
        stock_level_histogram.append("Current Total Stock is 0. Cannot generate levels.\n")
        return stock_level_histogram

    #Skip the inventory header, track the quantity of every item.
    for item in line_contents[3:]:
        #If the line is not empty.
        if item.strip():
            #Parse the line into details, track the item code and quantity, and calculate the percentage
            item_details = parse_inventory_line(item)
            item_code = item_details[0]
            item_quantity = int(item_details[3])
            stock_level_percentage = int(item_quantity / int(total_stock_qty) * 100)

            #Formatting the histogram.
            max_capacity = 20
            quantity_of_symbol = int(stock_level_percentage / 100 * max_capacity)
            item_stock_level = quantity_of_symbol * "#"
            formatted_histogram_display = (f"{item_code} | {item_stock_level.ljust(max_capacity)} "
                                           f"| {stock_level_percentage}%\n")
            stock_level_histogram.append(formatted_histogram_display)

    return stock_level_histogram
def generate_operational_report(current_date):
    """
    Generate Section A of the daily report.
    Using the datas returned using the formulas to generate the operational report.
    The operational report is then returned using list and extend in the daily report.
    """
    #Using the formulas to generate the data needed. Calculate other variables by formulas.
    transaction_qty, total_items_sold, gross_sales = track_transaction(current_date, 1)
    return_transaction_qty, items_returned, sales_return = track_transaction(current_date, 0)
    net_sales = float(gross_sales) - float(sales_return)
    transaction_variance, item_sold_variance, sales_variance = (
        check_variance_vs_yesterday(current_date, transaction_qty, total_items_sold, net_sales))
    order_qty_received, stock_received = track_order(current_date, "RECEIVED")
    order_qty_returned, stock_returned = track_order(current_date, "RETURNED")
    stock_qty, item_code_qty = calculate_total_stock()
    stock_added = items_returned + stock_received
    stock_deducted = total_items_sold + stock_returned
    stock_level = generate_stock_level(stock_qty)

    #Using all datas to generate the report by format and store into list.
    report_details = [
        "-" * 42 + "\n",
        f"{"SECTION A: OPERATIONAL REPORT".center(42)}" + "\n",
        "-" * 42 + "\n",
        f"{"Total Transactions".ljust(28)}: {transaction_qty} ({total_items_sold} units)\n",
        f"{"Customer Returns".ljust(28)}: {return_transaction_qty} ({items_returned} units)\n",
        f"{"Variance (vs Yesterday) ".ljust(28)}: {transaction_variance} ({item_sold_variance} units)\n\n",
        f"{"Total Orders Received".ljust(28)}: {order_qty_received} ({stock_received} units)\n",
        f"{"Total Orders Returned".ljust(28)}: {order_qty_returned} ({stock_returned} units)\n\n",
        f"{"Total Stock".ljust(28)}: {stock_qty} ({item_code_qty} items)\n",
        f"{"Total Stock Added".ljust(28)}: {stock_added}\n",
        f"{"Total Stock Deducted".ljust(28)}: {stock_deducted}\n"
    ]
    #Add the list of stock level
    report_details.extend(stock_level)
    #Return the operational report and also financial data obtained from formulas as they are used in financial report.
    financial_details = [gross_sales, sales_return, net_sales, sales_variance]

    return report_details, financial_details
def generate_daily_report(current_date):
    """
    Add operational and financial reports together with the headings into a master list.
    Print out the whole daily report and store into the daily_report.txt file.
    """
    import Accountant

    report_details = [
        "\n" + "=" * 15 + "DAILY REPORT" + "=" * 15 + "\n",
        "Report Date: " + current_date + "\n"
    ]
    #Obtain the operational report and extend into the list. Use the financial data to generate financial report.
    #Then, extend the financial report generated into the master list.
    operational_report, financial_data = generate_operational_report(current_date)
    report_details.extend(operational_report)
    financial_report = Accountant.generate_daily_financial_report(current_date, financial_data)
    report_details.extend(financial_report)

    #Print the whole report and store into the txt file.
    print("".join(report_details))
    with open("daily_report.txt", "a") as report_file:
        report_file.writelines(report_details)
    print(f"Daily Report for {current_date} recorded successfully.\n")

    #Return the list of report as it is used when updating the new daily report.
    return report_details
def check_daily_report_generated(current_date):
    """
    Check whether the daily report with the given date is generated.
    If no, generate it. If yes, update it with the new data.
    Replace the old report with the new one and store again in the file.
    Uses this function when user ask to generate report manually, or auto generate when quiting the system.
    """
    #Check if the file exists, if no, generate report with given date.
    try:
        with open("daily_report.txt", "r") as report_file:
            report_data = report_file.read()
    except FileNotFoundError:
        print("Generating daily report...\n")
        generate_daily_report(current_date)
        return

    #If file exists, but report with given date is not in the file, also generate it.
    if not current_date in report_data:
        print("Generating daily report...\n")
        generate_daily_report(current_date)
    else:
        print("Updating today's daily report...\n")
        #Separate all reports into list using headers.
        report_separator = "\n" + "=" * 15 + "DAILY REPORT" + "=" * 15 + "\n"
        report_list = report_data.split(report_separator)
        new_report_list = []
        for report in report_list:
            if report.strip():
                #If the report is not empty and refer to the given date, update a new one and append into the new list.
                if current_date in report:
                    new_report_details = generate_daily_report(current_date)
                    new_report = "".join(new_report_details)
                    new_report_list.append(new_report)
                #If current report not refers to the given date, just append it.
                else:
                    full_report = report_separator + report.strip() + "\n"
                    new_report_list.append(full_report)

        #Write the new list into the file.
        with open("daily_report.txt", "w") as report_file:
            report_file.writelines(new_report_list)

#Task 5: View Previous Reports
def view_daily_report(date_to_find):
    """
    Print the whole daily report with the given date.
    """
    #Check if the file exists.
    try:
        with open("daily_report.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("No daily report file found.")
        return

    #Split all reports into list using headers.
    report_separator = "\n" + "=" * 15 + "DAILY REPORT" + "=" * 15 + "\n"
    report_blocks = contents.split(report_separator)
    report_found = False
    for block in report_blocks:
        #If the certain line exists in the report, record as report found and print the whole report.
        if f"Report Date: {date_to_find}" in block:
            report_found = True
            full_report = report_separator + block.strip() + "\n"
            print(full_report)

    #If report with given date is not in the file, print the message.
    if not report_found:
        print(f"Daily report for {date_to_find} not found.")
def view_monthly_financial_report(month_num_to_find, year_to_find):
    """
    Print the whole monthly financial report with the given month and year.
    """
    #Check if the file exists.
    try:
        with open("monthly_report.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("No monthly report file found.")
        return

    year_to_find = int(year_to_find)
    if 0 < year_to_find <= 9:
        year_to_find = "000" + str(year_to_find)
    elif 10 <= year_to_find <= 99:
        year_to_find = "00" + str(year_to_find)
    elif 100 <= year_to_find <= 999:
        year_to_find = "0" + str(year_to_find)
    else:
        year_to_find = str(year_to_find)

    month_name_to_find = determine_month_name(int(month_num_to_find))
    #Split all reports into list using headers.
    report_separator = "\n" + "=" * 15 + "MONTHLY REPORT" + "=" * 15 + "\n"
    report_blocks = contents.split(report_separator)
    report_found = False
    for block in report_blocks:
        #If the certain line exists in the report, record as report found and print the whole report.
        if f"Report Month: {month_name_to_find} {year_to_find}" in block:
            report_found = True
            full_report = report_separator + block.strip() + "\n"
            print(full_report)

    #If report with given month and year is not in the file, print the message.
    if not report_found:
        print(f"Monthly report for {month_name_to_find} {year_to_find} not found.")

