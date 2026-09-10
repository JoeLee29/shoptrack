"""
This module consists of all functions for Cashier Role.
"""

import Administrator

#Task 1: Process Sales Transaction & Generate Receipt
def deduct_quantity(item_code, quantity_to_deduct):
    """
    Find the given item code in the inventory and deduct its quantity by the quantity given.
    Uses this function when transaction made and order returned.
    """
    #Check if the file exists.
    try:
        with open("inventory.txt", "r") as file:
            contents = file.readlines()
    except FileNotFoundError:
        print("Inventory file not found.")
        return

    new_contents = []
    # Use enumerate function to return the index number of every line and its contents
    for line_index, line_content in enumerate(contents):
        # Add the heading lines with no item details
        if line_index < 3:
            new_contents.append(line_content)
            continue

        # Change the quantity in the line which starts with the item code required.
        if line_content.startswith(f"{item_code.center(10)}"):
            ItemDetail = Administrator.parse_inventory_line(line_content)
            OriginalQuantity = int(ItemDetail[3])
            NewQuantity = OriginalQuantity - int(quantity_to_deduct)
            if NewQuantity < 0:
                print(f"Unable to deduct quantity of {item_code} from {OriginalQuantity} to {NewQuantity}.")
                return
            # Arrange the new details in a new single line and append to the inventory
            NewItemDetails = (f"{ItemDetail[0].center(10)}{ItemDetail[1].center(30)}{ItemDetail[2].center(14)}"
                              f"{str(NewQuantity).rjust(8)}\n")
            new_contents.append(NewItemDetails)
            print(f"Quantity of {item_code} deducted from {OriginalQuantity} to {NewQuantity}. ")
        else:
            # Append other unrelated item details.
            new_contents.append(line_content)

    #Write the new contents into the file.
    with open("inventory.txt", "w") as file:
        file.writelines(new_contents)
def sales_transaction(date_list):
    """
    Prompt user to enter details of customer name and items to buy with its discounts.
    Print the receipts and store in sales.txt
    """
    #Obtain the data from the given list.
    formatted_date = date_list[0]
    date = date_list[1] + date_list[2] + date_list[3]

    #Request the current time from user. Declare the variables and store the values.
    try:
        print("Please enter the time of the transaction:")
        time_list = Administrator.request_time()
        formatted_time = time_list[0]
        time = time_list[1] + time_list[2]
    except ValueError:
        print("Invalid time. Please try again.")
        return

    #Format the ID and prompt the user to input customer name.
    transaction_id = "TX" + date + time
    CustName = input("Enter Customer Name: ")
    #Form the receipt headings.
    receipt_heading = [
        '\n' + '=' * 38 + 'Receipt' + '=' * 38 + '\n',
        f'Transaction ID: {transaction_id}\n',
        f'Date: {formatted_date}\n',
        f'Time: {formatted_time}\n',
        f'Customer: {CustName}\n',
        '-' * 84 + '\n',
        f'{"ItemCode".center(10)}{"ItemName".center(30)}{"UnitPrice(RM)".center(14)}{"SoldQty".center(8)}'
        f'{"Discount(%)".center(12)}{"Total(RM)".center(10)}\n'
    ]

    item_count = 0
    total_quantity = 0
    total_sales = 0
    sales_item_list = []
    adding_sales_item = True
    #Let the user keep adding item to be sold
    while adding_sales_item:
        #Check if the file exists.
        try:
            with open("inventory.txt", "r") as file:
                contents = file.readlines()
        except FileNotFoundError:
            print("Inventory file not found.")
            return

        #Prompt the user to enter the item code to buy
        ItemCode = input("Enter Item Code to buy: ").strip().upper()

        #Calculate total quantity of the item code input that is confirmed to be sold in the receipt earlier
        #To deduct item quantity in stock for primary usage
        total_item_qty_in_receipt = 0
        for item in sales_item_list:
            if ItemCode in item:
                item_details = Administrator.parse_sales_item_line(item)
                item_qty_in_receipt = int(item_details[3])
                total_item_qty_in_receipt += item_qty_in_receipt

        item_found = False
        for line in contents:
            if line.startswith(f"{ItemCode.center(10)}"):
                item_found = True
                #When the line with the code is tracked, parse the line into list and print the details of the item
                item_details = Administrator.parse_inventory_line(line)
                item_price = float(item_details[2])
                #Calculate total quantity in stock excluding the quantity in the same receipt
                item_quantity_in_stock = int(item_details[3]) - total_item_qty_in_receipt
                print(f"Item Name: {item_details[1]} | Item Price: RM {item_price:.2f} "
                      f"| Quantity In Stock: {item_quantity_in_stock}")
                #Check if the item quantity is valid to buy or not in inventory
                if item_quantity_in_stock <= 0:
                    print("The item is not available.")
                    break

                #Cannot buy the item with quantity more than the quantity in stock.
                quantity_to_buy = int(input("Enter Quantity to Buy: "))
                if quantity_to_buy <= 0:
                    print("Invalid Quantity. Please try again.")
                    break
                if quantity_to_buy > item_quantity_in_stock:
                    print("Not enough quantity to buy. Try again. ")
                    break

                #Prompt user to input discount and calculate amount after discount
                discount = int(input("Discount(%): "))
                discount_amount = item_price * (discount/100)
                total_price_per_unit = item_price - discount_amount
                total_price_per_item = total_price_per_unit * quantity_to_buy
                print(f"""
Sales Details for this item:
Item Code: {ItemCode}
Item Name: {item_details[1]}
Unit Price: RM {item_price:.2f}
Quantity to Buy: {quantity_to_buy}
Discount Amount (per unit): RM {discount_amount:.2f} ({discount}%)
Total amount after discount: RM {total_price_per_unit:.2f} * {quantity_to_buy} = RM {total_price_per_item:.2f}""")

                #Prompt the user to confirm the purchase details of the item
                confirm_message = input("Are you confirm to add this to receipt (Y/N): ").upper()
                #If no, ask to enter another buying items
                if confirm_message != "Y":
                    print("Aborted.")
                    break
                #If yes, add the item sold details into the list and calculate the total item quantity and sales amount
                item_sold_details = (f'{ItemCode.center(10)}{item_details[1].center(30)}{f"{item_price:.2f}".center(14)}'
                                     f'{f"{quantity_to_buy}".center(8)}{f"{discount}".center(12)}'
                                     f'{f"{total_price_per_item:.2f}".rjust(10)}\n')
                sales_item_list.append(item_sold_details)
                item_count += 1
                total_quantity += quantity_to_buy
                total_sales += total_price_per_item

        #After searching all items in the file, if still not found the item, try again.
        if not item_found:
            print("Item code not found. Try again.")

        #Prompt user to choose to add another item
        choice = input("Do you want to continue (Y/N): ").upper()
        if choice != "Y":
            adding_sales_item = False
            print("Generating the receipt...")

    #After finished adding items, add ending and print the whole receipts
    receipt_ending = [
        '-' * 84 + '\n',
        'Total Quantity Sold: ' + str(total_quantity) + '\n',
        'Total Payment Amount: RM ' + f'{total_sales:.2f}' + '\n'
    ]

    receipt_details = receipt_heading + sales_item_list + receipt_ending
    print("".join(receipt_details))

    # If no items are added in the receipt, return the function
    if item_count == 0:
        print("No items are sold. Payment failed.\n")
        return

    #If user decide to make payment, deduct quantity of all sold items from inventory, and add status
    payment_status = input("Would you like to make payment (Y/N): ").upper()
    if payment_status == "Y":
        for i in range(7, 7 + item_count):
            item_details_to_deduct_quantity = Administrator.parse_sales_item_line(receipt_details[i])
            item_code_to_deduct_quantity = item_details_to_deduct_quantity[0]
            quantity_to_deduct = int(item_details_to_deduct_quantity[3])
            deduct_quantity(item_code_to_deduct_quantity, quantity_to_deduct)
        print("Quantity sold successfully deducted from inventory. ")

        receipt_details.append("Status: Paid\n\n")
        with open("sales.txt", "a") as file:
            file.writelines(receipt_details)
        print("Payment successful!")

    else:
        print("Payment failed.")

#Task 2: View Previous Receipts
def view_sales_by_id(transaction_id):
    """
    Print the receipt for the given transaction ID.
    """
    #Check if the file exists.
    try:
        with open("sales.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("No receipt file found.")
        return None

    #Separate all receipts into list using separator.
    receipt_separator = '\n' + '=' * 38 + 'Receipt' + '=' * 38 + '\n'
    receipt_blocks = contents.split(receipt_separator)
    receipt_content_to_view = []
    transaction_found = False
    for block in receipt_blocks:
        full_receipt = receipt_separator + block.strip() + '\n'
        #Check if the transaction ID is in the receipt
        if transaction_id in full_receipt:
            transaction_found = True
            #Multiple receipts may have same ID, so append all target receipts into list first
            receipt_content_to_view.append(full_receipt)

    #If at least one transaction found, print all receipts and return the receipt list
    if transaction_found:
        print("".join(receipt_content_to_view))
        return receipt_content_to_view
    #If no transaction found, print the message
    else:
        print("Transaction ID not found.")
        return None
def view_sales_by_date(date_to_find):
    """
    Print the receipt for the given date
    """
    #Check if the file exists.
    try:
        with open("sales.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("No receipt file found.")
        return

    #Separate all receipts into list using separator.
    receipt_separator = '\n' + '=' * 38 + 'Receipt' + '=' * 38 + '\n'
    receipt_blocks = contents.split(receipt_separator)
    transaction_found = False
    for block in receipt_blocks:
        line_details = block.split("\n")
        for line in line_details:
            # Check if the target line consists of given date
            if line.startswith("Date:"):
                date = line.split(":")[1].strip()
                if date == date_to_find:
                    #If yes, print the full receipt.
                    transaction_found = True
                    full_receipt = receipt_separator + block.strip() + "\n"
                    print(full_receipt)

    #If no transaction found, print the message.
    if not transaction_found:
        print("Date not found.")

#Task 3: Return Transactions (Change status & Add Inventory)
def add_quantity(item_code, quantity_to_add):
    """
    According to the given item code, add the given quantity to inventory.
    Uses this function when transaction is returned or order is received.
    """
    try:
        with open("inventory.txt", "r") as file:
            contents = file.readlines()
    except FileNotFoundError:
        print("Inventory file not found.")
        return

    new_contents = []
    # Use enumerate function to return the index number of every line and its contents
    for line_index, line_content in enumerate(contents):
        # Add the heading lines with no item details
        if line_index < 3:
            new_contents.append(line_content)
            continue

        # Change the quantity in the line which starts with the item code required.
        if line_content.startswith(f"{item_code.center(10)}"):
            ItemDetail = Administrator.parse_inventory_line(line_content)
            OriginalQuantity = int(ItemDetail[3])
            NewQuantity = OriginalQuantity + int(quantity_to_add)
            # Arrange the new details in a new single line and append to the inventory
            NewItemDetails = (f"{ItemDetail[0].center(10)}{ItemDetail[1].center(30)}{ItemDetail[2].center(14)}"
                              f"{str(NewQuantity).rjust(8)}\n")
            new_contents.append(NewItemDetails)
            print(f"Quantity of {item_code} added from {OriginalQuantity} to {NewQuantity}. ")
        else:
            # Append other unrelated item details.
            new_contents.append(line_content)

        with open("inventory.txt", "w") as file:
            file.writelines(new_contents)
def return_transaction(current_date_list):
    """
    Handles the process of returning a transaction, updating inventory,
    and marking the transaction status as 'Returned' in the sales record.
    """
    #Get Transaction Details
    transaction_id_to_return = input("Enter Transaction ID to return: ").upper().strip()
    #Retrieve the list of receipts matching the ID
    receipt_content_list = view_sales_by_id(transaction_id_to_return)
    transaction_formatted_date = ""

    # Extract the original transaction date from the receipt content
    for receipt in receipt_content_list:
        receipt_lines = receipt.split('\n')
        for line in receipt_lines:
            if line.startswith("Date:"):
                line_detail = line.split(":")
                transaction_formatted_date = line_detail[1].strip()

    #Validate Return Eligibility
    current_date = current_date_list[0]
    if not transaction_formatted_date:
        print("Error")
        return
    else:
        # Calculate allowed return window based on the transaction date
        valid_return_date_list = Administrator.find_valid_return_dates(transaction_formatted_date)
        print(f"Transaction {transaction_id_to_return} Last Return Date: {valid_return_date_list[-1]}")
        # Check if the current system date falls within the valid return window
        if current_date in valid_return_date_list:
            print(f"Transaction {transaction_id_to_return} is valid to return by {current_date}.")
        else:
            print(f"Transaction {transaction_id_to_return} is invalid to return by {current_date}.")
            return

    #User Confirmation and Remarks
    choice = input(f"Would you like to return transaction {transaction_id_to_return}? (Y/N): ").upper()
    if choice != "Y":
        print("Return transaction cancelled.")
        return
    else:
        remarks = input("Enter reasons to return the transaction: ").strip()
        # Add quantity of every items back to inventory
        for receipt in receipt_content_list:
            # Locate the section containing item details (separated by dashes)
            receipt_details_separator = '-' * 84 + '\n'
            receipt_details = receipt.split(receipt_details_separator)

            # Identify the individual item lines
            sold_items_details = receipt_details[1].split('\n')
            for line_index, line_detail in enumerate(sold_items_details):
                # Skip header and footer lines in the items section
                if 0 < line_index < len(sold_items_details) - 1:
                    item_detail = Administrator.parse_sales_item_line(line_detail)
                    sold_item_code = item_detail[0]
                    sold_item_quantity = int(item_detail[3])
                    # Call function to increment stock level in inventory
                    add_quantity(sold_item_code, sold_item_quantity)
        print("Items sold successfully returned to inventory.")

        #Update Sales Record File
        try:
            with open("sales.txt", "r") as file:
                contents = file.read()
        except FileNotFoundError:
            print("No receipt file found.")
            return

        # Split file into individual receipts using the standard separator
        receipt_separator = '\n' + '=' * 38 + 'Receipt' + '=' * 38 + '\n'
        receipt_blocks = contents.split(receipt_separator)
        new_receipt_blocks = []
        for block in receipt_blocks:
            # Reconstruct the receipt block for comparison
            full_receipt = receipt_separator + block.strip() + '\n'
            if block.strip():
                # If this is the receipt being returned, modify its status
                if full_receipt in receipt_content_list:
                    index_to_find = full_receipt.index("Status:")
                    # Append 'Returned' status and the reason to the receipt text
                    updated_full_receipt = (full_receipt[:index_to_find] +
                                            f"Status: Returned ({current_date})\nRemarks: {remarks}\n\n")
                    new_receipt_blocks.append(updated_full_receipt)
                else:
                    # Keep other receipts as they are
                    new_receipt_blocks.append(full_receipt)
        # Write the updated blocks back to the sales file
        with open("sales.txt", "w") as file:
            file.writelines(new_receipt_blocks)

        print(f"Transaction {transaction_id_to_return} returned successfully.") #not deleted but changed status

#Task 4: View Return Receipts
def view_return_transaction_by_date(date_to_find):
    """
    Searches through the sales records to find and display all transactions
    that were marked as 'Returned' on a specific date.
    """
    #Check if the file exists
    try:
        with open("sales.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("No receipt file found.")
        return

    #Split the receipts into list using headers
    receipt_separator = '\n' + '=' * 38 + 'Receipt' + '=' * 38 + '\n'
    receipt_blocks = contents.split(receipt_separator)
    transaction_found = False
    for block in receipt_blocks:
        #Check if the string exists in the receipt, if yes, print the full receipt
        if f"Status: Returned ({date_to_find})" in block:
            transaction_found = True
            full_receipt = receipt_separator + block.strip() + "\n"
            print(full_receipt)
    #If no, print the message
    if not transaction_found:
        print("Date not found.")
