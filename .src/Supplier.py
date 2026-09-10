"""
This module consists of all functions for Supplier Role.
"""

import Administrator
import StockManager

#Task 1: View Orders & Delete CANCELLED orders records if requested
def order_status_menu():
    """
    Displays a selection menu for order statuses and returns the
    corresponding status string based on user input.
    """
    # --- 1. Display Menu Options ---
    print("---ORDER STATUS MENU---")
    print("1. PENDING")
    print("2. DELIVERED")
    print("3. RECEIVED")
    print("4. RETURNED")
    print("5. CANCELLED")
    print("6. EXIT\n")

    # --- 2. Input Validation Loop ---
    while True:
        choice = input("Choose the order status (1-6): ")

        # Mapping numerical choices to specific status strings
        if choice == "1":
            status = "PENDING"
            break
        elif choice == "2":
            status = "DELIVERED"
            break
        elif choice == "3":
            status = "RECEIVED"
            break
        elif choice == "4":
            status = "RETURNED"
            break
        elif choice == "5":
            status = "CANCELLED"
            break
        elif choice == "6":
            # Handle the exit case by returning None
            print("Exiting the menu...")
            status = None
            break
        else:
            # Handle non-numerical or out-of-range inputs
            print("Invalid choice. Try again.")

    # Return the chosen status string to the calling function
    return status
def view_orders_by_status(status, status_date=None):
    """
    Searches and displays orders based on their status and an optional date.
    If 'CANCELLED' is selected, it offers an option to purge those records.
    """
    # --- 1. Load Order Records ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("Orders file not found.")
        return

    # Define the separator used to identify individual order blocks
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)
    order_found = False

    # --- 2. Filter and Search Logic ---
    for order_detail in order_details_list:
        if order_detail.strip():  # Skip empty strings resulting from the split
            line_details = order_detail.split("\n")

            # Iterate backwards [::-1] because status is usually at the end of the block
            for line in line_details[::-1]:
                if line.startswith("Order Status"):
                    # Extract status text, e.g., "RECEIVED (30/12/2025)"
                    order_status_with_date = line.split(":")[1].strip()

                    # Scenario A: Search by Status only
                    if not status_date:
                        if status in order_status_with_date:
                            order_found = True
                            full_order_detail = line_to_split + order_detail.strip() + "\n"
                            print(full_order_detail)

                    # Scenario B: Search by Status AND specific Date
                    else:
                        if f"{status} ({status_date})" in order_status_with_date:
                            order_found = True
                            full_order_detail = line_to_split + order_detail.strip() + "\n"
                            print(full_order_detail)
                    break  # Stop searching this block once status line is processed

    # --- 3. Final Results and Cleanup ---
    if not order_found:
        print("No orders with input status found. ")
        return

    # Special Admin feature: Delete records that are marked as CANCELLED
    if status == "CANCELLED":
        choice = input("Would you like to delete all CANCELLED orders (Y/N)?\n"
                       "Cautious: Must be approved by ADMIN! ").upper()
        if choice == "Y":
            print("Deleting all CANCELLED orders...")
            # Calls external function to rewrite the file without cancelled records
            delete_order_record()
            print("CANCELLED orders records deleted. ")
def view_orders_by_date(date_to_find):
    """
    Searches the orders file and prints all order records that
    match a specific order placement date.
    """
    # --- 1. Read the Orders File ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        # Handle cases where no orders have been placed yet
        print("No orders file found.")
        return

    # --- 2. Split the File into Blocks ---
    # The separator identifies the start of each unique order entry
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)

    # Flag to check if any matches were found
    order_found = False

    # --- 3. Iterative Search Logic ---
    for order_details in order_details_list:
        # Split the current block into individual lines
        line_details = order_details.split("\n")

        for line in line_details:
            # Look for the specific header "Order Date"
            if line.startswith("Order Date"):
                # Extract the date value after the colon (e.g., "30/12/2025")
                date = line.split(":")[1].strip()

                # Compare the extracted date with the user's input
                if date == date_to_find:
                    order_found = True
                    # Reconstruct the receipt with the header for better readability
                    full_order = line_to_split + order_details.strip()
                    print(full_order, end="\n")

                # Once 'Order Date' is found, move to the next order block
                break

    # --- 4. Final Verification ---
    if not order_found:
        print("Date not found.")
def view_orders_by_sup_id(sup_id_to_find):
    """
    Filters and displays all order records from 'orders.txt'
    that match a specific Supplier ID.
    """
    # --- 1. Access the Orders Database ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        # Error handling for missing files
        print("No orders file found.")
        return

    # --- 2. Segment the File into Individual Orders ---
    # The separator string used to identify the start of each order block
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)

    # Flag to track if at least one matching order is discovered
    order_found = False

    # --- 3. Parsing and Matching Logic ---
    for order_details in order_details_list:
        # Split the current block into lines to look for the Supplier ID field
        line_details = order_details.split("\n")
        for line in line_details:
            # Check for the specific header "Supplier ID"
            if line.startswith("Supplier ID"):
                # Extract the ID value (e.g., "S001") after the colon
                sup_id = line.split(":")[1].strip()

                # Check if the extracted ID matches the user's search criteria
                if sup_id == sup_id_to_find:
                    order_found = True
                    # Reconstruct the original formatted order block for the console
                    full_order = line_to_split + order_details.strip()
                    print(full_order, end="\n")

                # Stop checking lines in this block once the Supplier ID is processed
                break

    # --- 4. Search Result Feedback ---
    if not order_found:
        print("Supplier ID not found.")
def delete_order_record():
    """
    Removes all orders with 'CANCELLED' status from orders.txt and
    decrements the corresponding totals in the supplier file.
    """
    # --- 1. Load Order Records ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("Orders file not found")
        return

    # Define the separator used to identify individual order blocks
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)
    new_order_details_list = []

    # --- 2. Filter Orders and Update Suppliers ---
    for order_detail in order_details_list:
        if order_detail:  # Skip empty entries
            order_to_delete = False
            line_details = order_detail.split("\n")

            # Check the status line (usually near the end of the block)
            for line in line_details[::-1]:
                if line.startswith("Order Status"):
                    # Extract status (e.g., "CANCELLED (30/12/2025)")
                    order_status_with_date = line.split(":")[1].strip()
                    # Remove the date part " (DD/MM/YYYY)" to get just the status word
                    order_status = order_status_with_date[:-12].strip()

                    if order_status != "CANCELLED":
                        # If not cancelled, preserve the order for the new file
                        full_order_detail = line_to_split + order_detail
                        new_order_details_list.append(full_order_detail)
                    else:
                        # Flag this order for deletion logic
                        order_to_delete = True
                    break

            # --- 3. Synchronize with Supplier File ---
            if order_to_delete:
                supplier_id = ""
                total_item_qty = 0
                # Scan the block to get necessary details for the supplier update
                for line in line_details:
                    if line.startswith("Supplier ID"):
                        supplier_id = line.split(":")[1].strip()
                    if line.startswith("Total Items Quantity"):
                        total_item_qty = int(line.split(":")[1].strip())

                # Deduct these quantities from the supplier's history
                StockManager.delete_order_to_supplier_file(supplier_id, total_item_qty)

    # --- 4. Overwrite Orders File ---
    # Reassemble the preserved orders into a single string
    new_order_contents = "".join(new_order_details_list)
    with open("orders.txt", "w") as file:
        file.write(new_order_contents)

#Task 2: Update Order Status
def update_order_status(current_date_list):
    """
    Manages the lifecycle of an order by updating its status, enforcing logical
    state transitions, and triggering inventory or payment adjustments.
    """
    # --- 1. Load Orders ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("Orders file not found")
        return

    # --- 2. Setup Search Parameters ---
    OrderID = input("Enter Order ID to update status: ").upper().strip()
    current_date = current_date_list[0]
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)
    new_order_details_list = []
    order_id_found = False

    # --- 3. Iterate Through Orders to Find a Match ---
    for order_detail in order_details_list:
        if order_detail.strip():
            line_details = order_detail.strip().split("\n")
            new_line_details = line_details.copy()

            # Identify if this block belongs to the Order ID we want
            for line in line_details:
                if line.startswith("Order ID"):
                    order_id = line.split(":")[1].strip()
                    if order_id == OrderID:
                        order_id_found = True
                        break

            full_order_detail = line_to_split + order_detail

            # --- 4. Process the Status Update ---
            if order_id_found:
                print(full_order_detail)

                # Get the new desired status from the predefined menu
                print(f"Choose a new order status for {OrderID}:")
                updated_status = order_status_menu()
                if not updated_status:  # If user chose 'Exit' in menu
                    return

                # Check the current (last) status to validate the transition
                for line in line_details[::-1]:
                    if line.startswith("Order Status"):
                        last_status_with_date = line.split(":")[1].strip()
                        last_status = last_status_with_date[:-12].strip()
                        last_date = last_status_with_date[-11:-1].strip()

                        print(f"Last Updated Status for {OrderID}: {last_status_with_date}")

                        # Date Validation: Ensure we aren't updating to a date in the past
                        result_date = Administrator.check_later_date(last_date, current_date)
                        if result_date == last_date and last_date != current_date:
                            print(f"Invalid: Current date {current_date} is earlier than last date {last_date}.")
                            return

                        # --- 5. Business Logic & State Transitions ---
                        if last_status != updated_status:
                            # Logic for orders currently in PENDING
                            if last_status == "PENDING":
                                if updated_status == "RETURNED":
                                    print("Order cannot be returned before received.")
                                    return

                                new_status_line = f"Order Status: {updated_status} ({current_date})"
                                new_line_details.append(new_status_line)

                                if updated_status == "CANCELLED":
                                    remark = input("Enter reason for cancellation: ").capitalize()
                                    new_line_details.append(f"Remarks: {remark}")

                            # Logic for orders currently in DELIVERED
                            elif last_status == "DELIVERED":
                                if updated_status in ["PENDING", "RETURNED"]:
                                    print(f"Invalid transition from DELIVERED to {updated_status}.")
                                    return

                                new_status_line = f"Order Status: {updated_status} ({current_date})"
                                new_line_details.append(new_status_line)
                                if updated_status == "CANCELLED":
                                    remark = input("Enter reason for cancellation: ").capitalize()
                                    new_line_details.append(f"Remarks: {remark}")

                            # Logic for orders currently in RECEIVED (Stock already in inventory)
                            elif last_status == "RECEIVED":
                                if updated_status in ["PENDING", "CANCELLED"]:
                                    print("Received orders cannot be moved to Pending or Cancelled.")
                                    return

                                new_status_line = f"Order Status: {updated_status} ({current_date})"
                                new_line_details.append(new_status_line)
                                remark = input("Enter reason for return: ").capitalize()
                                new_line_details.append(f"Remarks: {remark}")

                                # Crucial: If returning after receiving, remove stock from inventory
                                StockManager.return_stock_to_supplier(OrderID)

                            # Finality check: Cancelled or Returned orders cannot be reopened
                            elif last_status in ["RETURNED", "CANCELLED"]:
                                print("Closed orders cannot be changed. Please place a new order.")
                                return

                            print(f"Order {OrderID} updated to {updated_status}.")
                        else:
                            print(f"Status is already {last_status}.")
                        break

                # --- 6. Final Formatting and External Module Integration ---
                new_order_detail = "\n".join(new_line_details)
                new_full_order_detail = line_to_split + new_order_detail + "\n"
                new_order_details_list.append(new_full_order_detail)

                # Receive Stock: Add items to inventory if status is now RECEIVED
                if updated_status == "RECEIVED":
                    StockManager.receive_stock(OrderID)
                    choice = input(f"Would you like to pay for order {OrderID} now (Y/N): ").upper().strip()
                    if choice == "Y":
                        make_payment(current_date, OrderID)
                    else:
                        print(f"Order {OrderID} recorded as unpaid.")

                # Refund logic: If order is cancelled/returned after some financial action
                if updated_status in ["RETURNED", "CANCELLED"]:
                    refund_payment(current_date, OrderID)
            else:
                # If Order ID doesn't match, keep the original record
                new_order_details_list.append(full_order_detail)

    # --- 7. Save Changes ---
    if order_id_found:
        with open("orders.txt", "w") as file:
            file.write("".join(new_order_details_list))
        print("Changes recorded successfully.")
    else:
        print("Order ID not found.")

#Task 3: Add payments (UNPAID) once orders are created. Let user choose to pay manually or autopay when orders RECEIVED
#Refund payments when Order Status: Others -> CANCELLED
def payment_status_menu():
    """
    Displays a selection menu for payment statuses and returns the
    corresponding string. This ensures uniform naming conventions across
    the payment ledger.
    """
    # --- 1. Display Menu Options ---
    print("---PAYMENT STATUS MENU---")
    print("1. Unpaid")
    print("2. Paid")
    print("3. Refunded")
    print("4. Exit\n")

    # --- 2. Input Validation Loop ---
    # Continuously prompt the user until a valid numeric choice is made
    while True:
        choice = input("Choose the payment status (1-3): ")

        # Map the numeric input to the specific status string
        if choice == "1":
            status = "Unpaid"
            break
        elif choice == "2":
            status = "Paid"
            break
        elif choice == "3":
            status = "Refunded"
            break
        elif choice == "4":
            # Handle the exit/cancel scenario
            print("Exiting the menu...")
            status = None
            break
        else:
            # Error handling for inputs that aren't 1, 2, 3, or 4
            print("Invalid choice. Try again.")

    # Return the resulting status string to the calling function
    return status
def record_unpaid_payment(order_date, order_id_input):
    """
    Creates a new payment record in 'payments.txt' by pulling relevant
    financial data from the 'orders.txt' file for a specific Order ID.
    """
    # --- 1. Load Order Source Data ---
    try:
        with open("orders.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("Orders file not found")
        return

    # Split the file into individual order blocks
    line_to_split = "\n" + "=" * 23 + "ORDER DETAILS" + "=" * 23 + "\n"
    order_details_list = contents.split(line_to_split)

    # Initialize the new payment record header
    payment_details = [
        "\n" + "=" * 10 + "PAYMENT DETAILS" + "=" * 10 + "\n",
        "Order ID: " + order_id_input + "\n"
    ]

    order_id_found = False

    # --- 2. Search and Extract Financial Data ---
    for order_details in order_details_list:
        if order_details.strip():
            line_details = order_details.strip().split("\n")

            # Verify if this block matches the Order ID we are recording for
            for line in line_details:
                if line.startswith("Order ID"):
                    order_id = line.split(":")[1].strip()
                    if order_id == order_id_input:
                        order_id_found = True
                        break

            # Define the specific financial lines we need to copy to the payment ledger
            line_to_append = ["Supplier ID", "Total Items Quantity", "Total Payment Amount (RM)"]

            if order_id_found:
                # Loop through the order block and pluck out the specific lines identified above
                for line in line_details:
                    for item in line_to_append:
                        if item in line:
                            payment_details.append(line.strip() + "\n")

                # Append the initial status as 'Unpaid' with the current date
                payment_details.append(f"Payment Status: Unpaid ({order_date})\n")
                # Exit once the correct order is processed
                break

    # --- 3. Save to Payment Ledger ---
    # Display the constructed payment block in the console
    print("".join(payment_details))

    # Append the record to payments.txt (maintaining a history of all payment states)
    with open("payments.txt", "a") as file:
        file.writelines(payment_details)

    print(f"Unpaid payment for order {order_id_input} successfully recorded. ")
def make_payment(payment_date, order_id_input):
    """
    Finds an unpaid order in the payments file and updates its status to 'Paid'.
    Includes validation to prevent duplicate payments or backdated transactions.
    """
    # --- 1. Load Payment Ledger ---
    try:
        with open("payments.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("No payment file found.")
        return

    # Define the separator used to segment different payment entries
    line_to_split = "\n" + "=" * 10 + "PAYMENT DETAILS" + "=" * 10 + "\n"
    payment_blocks = contents.split(line_to_split)
    new_payment_blocks = []
    payment_found = False

    # --- 2. Search for the Specific Order ---
    for block in payment_blocks:
        if block.strip(): #Check if the block is not empty
            full_payment = line_to_split + block.strip() + '\n'
            line_details = block.split("\n")

            # Check the ID of the current payment block
            for line in line_details:
                if line.strip() and line.startswith("Order ID"):
                    order_id = line.split(":")[1].strip()
                    if order_id == order_id_input:
                        payment_found = True
                        break

            # --- 3. Process and Validate the Payment ---
            if payment_found:
                print(full_payment)

                # Scan lines backwards to find the most recent status
                for line in line_details[::-1]:
                    if line.strip() and line.startswith("Payment Status"):
                        payment_status_with_date = line.split(":")[1].strip()
                        last_payment_status = payment_status_with_date[:-12].strip()

                        # Prevent paying if the status is already 'Paid' or 'Returned'
                        if last_payment_status != "Unpaid":
                            print("The order payment is already paid or refunded.")
                            return

                        # Date Validation: Ensure payment date isn't earlier than the order date
                        last_update_date = payment_status_with_date[-11:-1].strip()
                        result_date = Administrator.check_later_date(last_update_date, payment_date)
                        if result_date == last_update_date and last_update_date != payment_date:
                            print(f"Invalid: The current date to make payment {payment_date} is earlier than last "
                                  f"updated date {last_update_date}.")
                            return
                        break

                # Append the new "Paid" status line to the existing block
                updated_full_receipt = full_payment + f"Payment Status: Paid ({payment_date})\n"
                new_payment_blocks.append(updated_full_receipt)
                print(f"Payment for order {order_id_input} is made successfully.")
                # Reset flag for the next iteration (in case of multiple blocks, though IDs should be unique)
                payment_found = False
            else:
                # If not the target order, keep the block exactly as it was
                new_payment_blocks.append(full_payment)

    # --- 4. Save the Updated Ledger ---
    with open("payments.txt", "w") as file:
        file.writelines(new_payment_blocks)
def refund_payment(date_to_return, order_id_to_return):
    """
    Locates a 'Paid' transaction in the payment ledger and updates it to 'Refunded'.
    Requires a reason for the refund and validates that the refund date is logical.
    """
    # --- 1. Load Payment Ledger ---
    try:
        with open("payments.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("No payment file found.")
        return

    # Define the separator used to identify individual payment entries
    line_to_split = "\n" + "=" * 10 + "PAYMENT DETAILS" + "=" * 10 + "\n"
    payment_blocks = contents.split(line_to_split)
    new_payment_blocks = []
    payment_found = False

    # --- 2. Search for the Target Order ---
    for block in payment_blocks:
        if block.strip():
            full_payment = line_to_split + block.strip() + '\n'
            line_details = block.split("\n")

            # Check if this block matches the Order ID to be refunded
            for line in line_details:
                if line.strip() and line.startswith("Order ID"):
                    order_id = line.split(":")[1].strip()
                    if order_id == order_id_to_return:
                        payment_found = True
                        break

            # --- 3. Process and Validate the Refund ---
            if payment_found:
                print(full_payment)

                # Check the most recent status (must be 'Paid' to be eligible for a refund)
                for line in line_details[::-1]:
                    if line.strip() and line.startswith("Payment Status"):
                        payment_status_with_date = line.split(":")[1].strip()
                        last_payment_status = payment_status_with_date[:-12].strip()

                        # You cannot refund something that was never paid or already refunded
                        if last_payment_status != "Paid":
                            print("The order payment is unpaid or already refunded.")
                            return

                        # Date Validation: Refund cannot happen before the original payment
                        last_payment_date = payment_status_with_date[-11:-1].strip()
                        result_date = Administrator.check_later_date(last_payment_date, date_to_return)
                        if result_date == last_payment_date and last_payment_date != date_to_return:
                            print(f"Invalid: The current date to refund payment {date_to_return} is earlier than payment"
                                  f" date {last_payment_date}.")
                            return
                        break

                # Request justification for the refund
                remarks = input("Enter reasons to refund the payment: ")

                # Append the new status and the remarks to the payment history
                updated_full_receipt = full_payment + (f"Payment Status: Refunded ({date_to_return})\n"
                                                       f"Remarks: {remarks}\n")
                new_payment_blocks.append(updated_full_receipt)

                # Reset flag so subsequent blocks aren't accidentally modified
                payment_found = False
            else:
                # Keep non-matching records unchanged
                new_payment_blocks.append(full_payment)

    # --- 4. Update the Ledger File ---
    with open("payments.txt", "w") as file:
        file.writelines(new_payment_blocks)
    print(f"Payments for order {order_id_to_return} refunded successfully.")
