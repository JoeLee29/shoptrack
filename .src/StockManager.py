"""
This module consists of all functions for Stock Manager Role.
"""

import Administrator
import Cashier
import Supplier

#Task 1: Add, view and manage suppliers details
def create_supplier_file():
    """
    Create a new supplier details list only for primary setup or when all stocks become empty
    """
    with open("supplier.txt", "w") as file:
        # Set up the primary format of the supplier list
        heading = [
            "-" * 39 + "Supplier Overview" + "-" * 39 + "\n",
            f"{"SupID".center(6)}{"Company".center(20)}{"ContactName".center(16)}{"ContactNo".center(12)}{"Email".center(20)}{"TotalOrder".center(10)} {"TotalItem".rjust(10)}\n",
            "-" * 95 + "\n"
        ]
        # Add the heading into the empty supplier file
        file.writelines(heading)
    view_supplier()
def add_supplier():
    """
    Add details of new supplier into list.
    """
    # Keep running the while loop until the user stop adding supplier.
    adding_supplier = True
    while adding_supplier:
        while True:
            InputID = input("Enter the Supplier ID to be added: ").strip().upper()  # remove whitespaces
            try:
                SupID = Administrator.validate_code(InputID)
                # Check if the supplier file exists. If supplier list does not exist, create the file with heading.
                # If the input supplier ID already exists, try again. If not, break the input ID loop.
                try:
                    with open("supplier.txt", "r") as file:
                        contents = file.read()
                    if SupID in contents:
                        print("Supplier ID already exists. Please enter new ID.")
                        continue
                except FileNotFoundError:
                    create_supplier_file()
                break
            except ValueError as e: # If the input Supplier ID is invalid, print the message and try again.
                print("Please enter a valid supplier ID.")
                print(e)

        CompanyName = input("Enter the Company Name (Max 18 characters): ").strip().title() #remove whitespaces and capitalize every word
        ContactName = input("Enter the Contact Name (Max 14 characters): ").strip().title() #remove whitespaces and capitalize every word
        ContactNumber = input("Enter the Contact Number (Eg. 011-187-7091): ").strip() #remove whitespaces
        ContactEmail = input("Enter the Email Address (Max 18 characters): ").strip() #remove whitespaces
        OrderQty = "0"
        ItemQty = "0"

        # Add all details into single line and \n to enter new line
        SupplierDetails = (f"{SupID.center(6)}{CompanyName.center(20)}{ContactName.center(16)}{ContactNumber.center(12)}"
                           f"{ContactEmail.center(20)}{OrderQty.rjust(10)} {ItemQty.rjust(10)}\n")

        # Append the detail line into supplier file.
        with open("supplier.txt", "a") as file:
            file.write(SupplierDetails)
        print(f"Supplier ID {SupID} successfully added!")

        # Ask user whether continue adding another supplier or not.
        choice = input("Would you like to add another supplier? (Y/N): ").upper()
        if choice != "Y":
            #If not, change adding_supplier False to stop the while loop.
            adding_supplier = False

    #Finally, view supplier list again and exit the process.
    view_supplier()
    print("Exiting supplier addition process...")
def view_supplier():
    """
    View Supplier Overview.
    Auto-run this function only when changes made.
    User also can manually run this function.
    """
    #Read and print all contents in the supplier file.
    try:
        with open("supplier.txt", "r") as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        create_supplier_file()
def edit_supplier():
    """
    Update the details of a supplier manually from the list.
    Read the line starting with required code and change its details, then append again into new contents.
    """
    # Keep running the while loop until the user stop changing details.
    editing_supplier = True
    while editing_supplier:
        SupID = input("Enter the Supplier ID to change its details: ").strip().upper()
        #If the inventory file not exists, stop the function.
        try:
            with open("supplier.txt", "r") as file:
                contents = file.readlines()
        except FileNotFoundError:
            print("Supplier file not found.")
            return

        # Change to True only when the SupID found and details successfully changed.
        supplier_found = False
        new_contents = [] #Define variable first.
        # Use enumerate function to return the index number of every line and its contents
        for line_index, line_content in enumerate(contents):
            #Add the heading lines with no item details
            if line_index < 3:
                new_contents.append(line_content)
                continue

            #Change the details in the line which starts with the SupID required.
            if line_content.startswith(f"{SupID.center(6)}"):
                supplier_found = True
                supplier_details = Administrator.parse_supplier_line(line_content)
                print("-" * 10 + "Current Information" + "-" * 10)
                print(f"Supplier ID: {supplier_details[0]}")
                print(f"Company Name: {supplier_details[1]}")
                print(f"Contact Name: {supplier_details[2]}")
                print(f"Contact Number: {supplier_details[3]}")
                print(f"Contact Email: {supplier_details[4]}\n")
                print("=" * 20 + "Edit Menu" + "=" * 20)
                print("*Press ENTER to Skip*")
                new_CompanyName = input("Enter the new company name (Max 18 characters): ").strip().title()
                new_ContactName = input("Enter the new contact name (Max 14 characters): ").strip().title()
                new_ContactNumber = input("Enter the new contact number (Eg: 012-345-6789): ").strip()
                new_ContactEmail = input("Enter the new contact email (Max 18 characters): ").strip()

                if new_CompanyName == "":  #If user press Enter or input nothing, the previous data remains
                    new_CompanyName = supplier_details[1]
                if new_ContactName == "":
                    new_ContactName = supplier_details[2]
                if new_ContactNumber == "":
                    new_ContactNumber = supplier_details[3]
                if new_ContactEmail == "":
                    new_ContactEmail = supplier_details[4]

                OrderQty = supplier_details[5]
                ItemQty = supplier_details[6]
                #Arrange the new details in a new single line and append to the supplier list
                NewSupplierDetails = f"{SupID.center(6)}{new_CompanyName.center(20)}{new_ContactName.center(16)}{new_ContactNumber.center(12)}{new_ContactEmail.center(20)}{OrderQty.rjust(10)} {ItemQty.rjust(10)}\n"
                new_contents.append(NewSupplierDetails)
            else:
                # Append other unrelated item details.
                new_contents.append(line_content)

        #If required SupID is found, write the new contents to supplier
        if supplier_found:
            with open("supplier.txt", "w") as file:
                file.writelines(new_contents)
            print(f"Details updated for {SupID} supplier!")
        else:
            # If False, means the line starts with the required code is not found.
            print(f"Supplier ID {SupID} not found.")

        # Ask user whether continue changing another details or not.
        choice = input("Would you like to change details of another supplier? (Y/N): ").upper()
        if choice != "Y":
            # If not, change False to stop the while loop.
            editing_supplier = False
    #Finally, view supplier list again and exit the process.
    view_supplier()
    print("Exiting supplier details changing process...")

#Task 2: Generate orders for restock request and make adjustments to supplier.txt
def request_low_stock():
    """
    Identifies low-stock items in the inventory and allows the user
    to create a restock request with specific quantities and costs.
    """
    # --- 1. Set the Low-Stock Threshold ---
    # Loop until the user provides a valid integer for the target quantity threshold
    while True:
        InputTargetQty = input("Enter the target quantity to track items with quantity less than it: ")
        try:
            validated_quantity = Administrator.validate_quantity(InputTargetQty)
            TargetQty = int(validated_quantity)
            break
        except ValueError as e:
            print("Invalid quantity. Try again.")
            print(e)

    # --- 2. Load Inventory Data ---
    print("Scanning through the inventory...\n")
    try:
        with open("inventory.txt", "r") as file:
            contents = file.readlines()
    except FileNotFoundError:
        print("Inventory file not found.")
        return None

    # Initialize tracking variables
    items_to_request_list = []
    total_payment_amount = 0
    total_item_qty = 0
    item_found = False

    # --- 3. Process Each Item in Inventory ---
    for line_index, line_content in enumerate(contents):
        # Skip the first three lines (usually file headers/formatting)
        if line_index >= 3:
            # Extract item details from the line
            ItemDetails = Administrator.parse_inventory_line(line_content)
            ItemCode = ItemDetails[0]
            ItemName = ItemDetails[1]
            ItemPrice = ItemDetails[2]  # This is the selling price
            ItemQuantity = int(ItemDetails[3])

            # --- 4. Filtering Logic ---
            # Check if the item's current stock is below the user-defined threshold
            if ItemQuantity < TargetQty:
                item_found = True
                print(f"Item Code: {ItemCode}")
                print(f"Item Name: {ItemName}")
                print(f"Item Price: RM {ItemPrice}")

                # Get the cost (purchase price) for the restock
                while True:
                    InputCost = input("Enter the cost to buy this item (RM): ")
                    try:
                        validated_cost = Administrator.validate_price(InputCost)
                        ItemCost = f"{validated_cost:.2f}"
                        break
                    except ValueError as e:
                        print("Invalid cost price. Try again.")
                        print(e)

                print(f"Original Quantity: {ItemQuantity}")

                # Get the specific quantity being requested from the supplier
                while True:
                    InputRequestQuantity = input("Enter the item quantity to request: ")
                    try:
                        validated_quantity2 = Administrator.validate_quantity(InputRequestQuantity)
                        RequestQuantity = str(validated_quantity2)
                        break
                    except ValueError as e:
                        print("Invalid request quantity. Try again.")
                        print(e)

                # Calculate the financial impact of this specific line item
                TotalCost = float(ItemCost) * int(RequestQuantity)
                TotalCost = f"{TotalCost:.2f}"

                # Display a summary for user review
                print(f"""
---Order Details---
Item Code: {ItemCode}
Item Name: {ItemName}
Item Price (RM): {ItemPrice}
Unit Cost (RM): {ItemCost}
Original Quantity: {ItemQuantity}
Request Quantity: {RequestQuantity}
Total Cost (RM): {TotalCost}
""")

                # --- 5. Confirmation and Accumulation ---
                choice = input("Are you sure to order this item? (Y/N): ").upper().strip()
                if choice != "Y":
                    print(f"Order item {ItemCode} cancelled. Continue to next item...")
                else:
                    # Format the line for the request list with clean spacing
                    items_to_request_detail = f"{ItemCode.center(8)}{ItemName.center(20)}{ItemCost.center(14)}{RequestQuantity.rjust(8)}{TotalCost.rjust(10)}\n"
                    items_to_request_list.append(items_to_request_detail)

                    # Update the running totals for the entire request session
                    total_item_qty += int(RequestQuantity)
                    total_payment_amount += float(TotalCost)
                    print(f"Order item {ItemCode} completed. Continue to next item...\n")

    # --- 6. Final Return ---
    if not item_found:
        print("No inventory has quantity under the target quantity.")
        return None
    else:
        print("All order items recorded.\n")
        # Return the list of strings and the numerical totals for further processing
        return items_to_request_list, total_item_qty, total_payment_amount
def generate_order_id():
    """
    Scans the 'orders.txt' file to find the highest existing Order ID
    and generates the next sequential ID in the format 'O###'.
    """
    # --- 1. Attempt to Read Existing Orders ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        # If the file doesn't exist, this is the very first order
        return "O001"

    # --- 2. Parse the File for Order IDs ---
    # Define the separator used to distinguish between different order blocks
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)
    order_number_list = []

    for order_details in order_details_list:
        # Split each order block into individual lines
        order_detail = order_details.split("\n")
        for item in order_detail:
            # Look for the line containing the ID (e.g., "Order ID: O005")
            if "Order ID" in item:
                order_id = item.split(":")[1].strip()
                # Remove the 'O' prefix and convert the remaining digits to an integer
                order_id_number = int(order_id[1:])
                order_number_list.append(order_id_number)

    # If the file exists but contains no valid Order IDs, start at O001
    if not order_number_list:
        return "O001"

    # --- 3. Determine the New ID Number ---
    # Find the maximum ID number currently in use
    max_num = 0
    for num in order_number_list:
        if num > max_num:
            max_num = num

    # Increment by 1 for the new order
    new_order_id_number = max_num + 1

    # --- 4. Format with Zero-Padding ---
    # Ensures the ID is always 3 digits long (e.g., 1 becomes 001, 15 becomes 015)
    if 1 <= new_order_id_number <= 9:
        new_order_id_number = "00" + str(new_order_id_number)
    elif 10 <= new_order_id_number <= 99:
        new_order_id_number = "0" + str(new_order_id_number)
    elif 100 <= new_order_id_number <= 999:
        new_order_id_number = str(new_order_id_number)

    # Return the final ID string (e.g., "O006")
    return "O" + new_order_id_number
def record_order_to_supplier_file(supplier_id, item_quantity):
    """
    Updates a specific supplier's historical record by incrementing their
    total number of orders and the total volume of items supplied.
    """
    # --- 1. Read Current Supplier Records ---
    try:
        with open("supplier.txt", "r") as file:
            contents = file.readlines()
    except FileNotFoundError:
        print("Supplier file not found.")
        return

    new_supplier_contents = []

    # --- 2. Iterate and Update Data ---
    for line_content in contents:
        # If the current line does not belong to the target supplier, keep it unchanged
        if not supplier_id in line_content:
            new_supplier_contents.append(line_content)
        else:
            # If the supplier ID matches, parse the line into its specific attributes
            supplier_details = Administrator.parse_supplier_line(line_content)

            # Extract historical totals (assuming last two columns are 'Orders' and 'Total Items')
            original_order_quantity = int(supplier_details[-2])
            original_item_quantity = int(supplier_details[-1])

            # Update values: increment order count by 1 and add the new item quantity
            new_order_quantity = str(original_order_quantity + 1)
            new_item_quantity = str(original_item_quantity + item_quantity)

            # Re-format the supplier line with specific spacing for document consistency
            # Uses .center() for main details and .rjust() for numerical totals
            new_supplier_details = (
                f"{supplier_details[0].center(6)}"
                f"{supplier_details[1].center(20)}"
                f"{supplier_details[2].center(16)}"
                f"{supplier_details[3].center(12)}"
                f"{supplier_details[4].center(20)}"
                f"{new_order_quantity.rjust(10)} "
                f"{new_item_quantity.rjust(10)}\n"
            )

            # Add the updated line to our new content list
            new_supplier_contents.append(new_supplier_details)

    # --- 3. Save Updated Records ---
    # Overwrite the file with the updated list to reflect the new statistics
    with open("supplier.txt", "w") as file:
        file.writelines(new_supplier_contents)
def delete_order_to_supplier_file(supplier_id, item_quantity):
    """
    Adjusts a supplier's record by decrementing their total orders and
    subtracting item quantities, typically used when an order is cancelled.
    Similar to the function record_order_to_supplier_file above.
    """
    # --- 1. Load Supplier Records ---
    try:
        with open("supplier.txt", "r") as file:
            contents = file.readlines()
    except FileNotFoundError:
        print("Supplier file not found.")
        return

    new_supplier_contents = []

    # --- 2. Iterate and Adjust Totals ---
    for line_content in contents:
        # If the line doesn't match the target supplier, keep it as is
        if not supplier_id in line_content:
            new_supplier_contents.append(line_content)
        else:
            # Parse the current stats for the supplier to be updated
            supplier_details = Administrator.parse_supplier_line(line_content)

            # Access the last two columns: total orders and total items
            original_order_quantity = int(supplier_details[-2])
            original_item_quantity = int(supplier_details[-1])

            # Reduce the counts based on the deleted order
            new_order_quantity = str(original_order_quantity - 1)
            new_item_quantity = str(original_item_quantity - item_quantity)

            # Reconstruct the line with the same centering and padding for file consistency
            new_supplier_details = (
                f"{supplier_details[0].center(6)}"
                f"{supplier_details[1].center(20)}"
                f"{supplier_details[2].center(16)}"
                f"{supplier_details[3].center(12)}"
                f"{supplier_details[4].center(20)}"
                f"{new_order_quantity.rjust(10)} "
                f"{new_item_quantity.rjust(10)}\n"
            )
            new_supplier_contents.append(new_supplier_details)

    # --- 3. Save Updated Data ---
    # Overwrite the supplier file with the corrected data
    with open("supplier.txt", "w") as file:
        file.writelines(new_supplier_contents)
def create_order(current_date_list):
    """
    Coordinates the full order placement process: identifying low stock,
    selecting a supplier, generating a unique Order ID, and saving the transaction.
    """

    # --- 1. Identify Items Needing Restock ---
    # Calls request_low_stock to get a list of formatted item strings and totals
    item_to_request_list, total_qty_requested, total_payment = request_low_stock()

    # If no items were selected or stock levels were sufficient, exit
    if not item_to_request_list:
        print("No items to request.")
        return

    # --- 2. Supplier Selection and Validation ---
    # Display available suppliers for the user to choose from
    view_supplier()

    while True:
        supplier_id_input = input("Choose the supplier ID to supply items: ").upper().strip()
        try:
            supplier_id = Administrator.validate_code(supplier_id_input)
            break
        except ValueError as e:
            print("Invalid Supplier ID. Try again.")
            print(e)
            choice = input("Would you like to input another supplier ID (Y/N): ").strip().upper()
            if choice != "Y":
                return

        supplier_found = False
        try:
            with open("supplier.txt", "r") as sup:
                # Validate that the entered Supplier ID exists in the system
                for line in sup:
                    # Matches ID using the same 'center' formatting used in the file
                    if line.startswith(f"{supplier_id.center(6)}"):
                        supplier_found = True
                        break
        except FileNotFoundError:
            print("Supplier file not found.")
            return

        if not supplier_found:
            print("Supplier ID not found. Try again. ")
        else:
            # Valid supplier found; exit the selection loop
            break

    # --- 3. Generate Order Metadata ---
    OrderID = generate_order_id()
    current_date = current_date_list[0]

    # --- 4. Construct the Order Document ---
    # Building the header and item table header
    order_details = [
        "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n",
        f"Order ID: {OrderID}\n",
        f"Order Date: {current_date}\n",
        f"Supplier ID: {supplier_id}\n",
        "-" * 60 + "\n",
        f"{"ItemCode".center(8)}{"ItemName".center(20)}{"ItemCost(RM)".center(14)}{"ReqQty".center(8)}{"Total(RM)".rjust(10)}\n"
    ]
    # Add the specific item lines collected earlier
    order_details.extend(item_to_request_list)

    # Building the footer with summary totals and status
    order_status = "PENDING"
    order_summary = [
        "-" * 60 + "\n",
        f"Total Items Quantity: {total_qty_requested}\n",
        f"Total Payment Amount (RM): {total_payment:.2f}\n",
        f"Order Status: {order_status} ({current_date})\n"
    ]
    order_details.extend(order_summary)

    # --- 5. Final Confirmation and Persistence ---
    # Preview the full order to the user
    print("".join(order_details))

    choice = input("Are you sure to place this order? (Y/N): ").upper().strip()
    if choice != "Y":
        print("Order placement cancelled.")
        return
    else:
        # Append the full order document to the permanent orders file
        with open("orders.txt", "a") as orders:
            orders.writelines(order_details)

        # Update the supplier's history (incrementing order counts/item volumes)
        record_order_to_supplier_file(supplier_id, total_qty_requested)

        print(f"Order {OrderID} recorded. Please check with supplier for further details.")

        # Log the financial liability in the Supplier class records
        Supplier.record_unpaid_payment(current_date, OrderID)

#Task 3: Add quantity to inventory when order RECEIVED
def receive_stock(received_order_id):
    """
    Processes a completed shipment by locating the original order,
    extracting the item quantities, and updating the inventory stock levels.
    """
    # --- 1. Load Order Records ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("Orders file not found")
        return

    # --- 2. Locate the Specific Order ---
    # Split the file into individual order blocks using the standard header separator
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)

    for order_details in order_details_list:
        if order_details.strip():
            line_details = order_details.split("\n")
            for line in line_details:
                # Check if this block matches the ID provided by the user
                if line.startswith("Order ID"):
                    order_id = line.split(":")[1].strip()

                    if order_id == received_order_id:
                        # --- 3. Extract Item Information ---
                        # Use the dashed line separator to find the table of items
                        subline_to_split = "-" * 60 + "\n"
                        # The items are located in the second part of the split block
                        ordered_items_details = order_details.split(subline_to_split)[1]
                        ordered_items_details_list = ordered_items_details.split("\n")

                        for item in ordered_items_details_list:
                            if item.strip():
                                # Ignore the table header (ItemCode, ItemName, etc.)
                                if not item.startswith(f"{"ItemCode".center(8)}"):
                                    # Parse the text line into specific item data
                                    item_details = Administrator.parse_order_item_line(item)
                                    item_code_received = item_details[0]
                                    item_qty_received = int(item_details[3])

                                    # --- 4. Update Inventory Stock ---
                                    # Call the Cashier function to increment the actual stock levels
                                    Cashier.add_quantity(item_code_received, item_qty_received)

                        print(f"Items received from Order {received_order_id} added to inventory.")
                        return  # Exit once the specific order is found and processed
def return_stock_to_supplier(received_order_id):
    """
    Identifies all items associated with a specific Order ID and removes
    those quantities from the current inventory to reflect a return to the supplier.
    """
    # --- 1. Load Order History ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("Orders file not found")
        return

    # --- 2. Parse File to Locate the Specific Order ---
    # Define the primary separator used for individual order blocks
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)

    for order_details in order_details_list:
        if order_details.strip():
            # Break the order block into lines to find the ID
            line_details = order_details.split("\n")
            for line in line_details:
                if line.startswith("Order ID"):
                    # Extract the ID from the line (e.g., "Order ID: O001")
                    order_id = line.split(":")[1].strip()

                    # Check if this matches the ID the user wants to return
                    if order_id == received_order_id:
                        # --- 3. Extract Items for Return ---
                        # Locate the item table section (between the dashed lines)
                        subline_to_split = "-" * 60 + "\n"
                        ordered_items_details = order_details.split(subline_to_split)[1]
                        ordered_items_details_list = ordered_items_details.split("\n")

                        for item in ordered_items_details_list:
                            # Skip empty lines and the table header row
                            if item.strip():
                                if not item.startswith(f"{"ItemCode".center(8)}"):
                                    # Parse text line to get item code and the quantity to remove
                                    item_details = Administrator.parse_order_item_line(item)
                                    item_code_to_return = item_details[0]
                                    item_qty_to_return = int(item_details[3])

                                    # --- 4. Deduct from Inventory ---
                                    # Reduce the stock level in the inventory file
                                    Cashier.deduct_quantity(item_code_to_return, item_qty_to_return)

                        print(f"All items received from Order {received_order_id} returned successfully.")
                        return  # Process complete, exit the function

