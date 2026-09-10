"""
This module consists of all functions for Accountant Role.
"""

#Task 1: View Supplier Payments
def view_payments_by_status(status, status_date=None):
    """
    Print the whole payment details if the last updated status of the payment is the given status.
    Default value of date is None, means all payments with the given status are printed.
    """
    #Check if the file exists.
    try:
        with open("payments.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("Payments file not found.")
        return

    #Split the payments using headers.
    line_to_split = "\n" + "=" * 10 + "PAYMENT DETAILS" + "=" * 10 + "\n"
    payment_details_list = contents.split(line_to_split)
    payment_found = False
    for payment_detail in payment_details_list:
        if payment_detail.strip(): #prevent code executing error if the order_detail is empty
            line_details = payment_detail.split("\n")
            #Check every line in the payment details from the bottom, so last updated status of the payment is obtained
            for line in line_details[::-1]:
                if line.startswith("Payment Status"):
                    #When first "Payment Status" from the bottom is met, break the loop, only the last status is tracked.
                    payment_status_with_date = line.split(":")[1].strip()
                    if not status_date: #If None, print all results (If the last status is the given status)
                        if status in payment_status_with_date:
                            payment_found = True
                            full_payment_detail = line_to_split + payment_detail.strip() + "\n"
                            print(full_payment_detail)
                    else: #If the date is specific, check whether the given status with given date is in the tracked line
                        if f"{status} ({status_date})" in payment_status_with_date:
                            payment_found = True
                            full_payment_detail = line_to_split + payment_detail.strip() + "\n"
                            print(full_payment_detail)
                    break
    #If still not found after checking all payments, print the message.
    if not payment_found:
        print("No payments with input status found. ")
        return
def view_payments_by_order_id(order_id_to_find):
    """
    Print the whole payment details with the given order ID.
    """
    #Check if the file exists.
    try:
        with open("payments.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("No payment file found.")
        return

    #Split the payment using headers.
    payment_separator = "\n" + "=" * 10 + "PAYMENT DETAILS" + "=" * 10 + "\n"
    payment_blocks = contents.split(payment_separator)
    payment_found = False
    for block in payment_blocks:
        line_details = block.split("\n")
        for line in line_details:
            #If the target line consists of the given order ID, print the full payment
            if line.startswith("Order ID"):
                order_id = line.split(":")[1].strip()
                if order_id == order_id_to_find:
                    payment_found = True
                    full_payment = payment_separator + block.strip()
                    print(full_payment, end="\n")

    if not payment_found:
        print("Order ID not found.")

#Task 2: Track Supplier Payments
# Customer Payments are tracked in Administrator: track_transaction()
def track_payment(status, current_date=None):
    """
    Obtain data from the payment details with given status and date.
    Calculate the total payment quantity with amount of all payment with the given condition.
    Status: Paid, Refunded, Unpaid
    """
    #Declare the variables.
    total_payment_qty = 0
    total_payment_amount = 0.00
    total_paid_item_qty = 0

    #Check if the file exists.
    try:
        with open("payments.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        return total_payment_amount, total_payment_qty, total_paid_item_qty

    #Split the payment using headers.
    payment_separator = "\n" + "=" * 10 + "PAYMENT DETAILS" + "=" * 10 + "\n"
    # Use strip() to remove leading/trailing whitespace before splitting
    payment_blocks = contents.strip().split(payment_separator)
    target_payments_list = []
    for block in payment_blocks:
        if not block.strip():
            continue #Skip the empty blocks

        line_details = block.split("\n")
        #Check every line of the payment from the bottom.
        for line in line_details[::-1]:
            #If the first "Payment Status" met, break the loop, access to the last updated status in the payment
            if current_date: #If the date is specific, check whether the given status with given date is in the tracked line
                if f"{status} ({current_date})" in line:
                    full_payment = payment_separator + block.strip() + "\n"
                    target_payments_list.append(full_payment)
                    break
            else: #If None, check only the given status, and append into list if found
                if line.startswith("Payment Status"):
                    if status in line:
                        full_payment = payment_separator + block.strip() + "\n"
                        target_payments_list.append(full_payment)
                    break

    for payment in target_payments_list:
        #For every target payment in the list, if payment not empty, track all data and calculate totals
        if payment.strip():
            total_payment_qty += 1
            line_details = payment.split("\n")
            for line in line_details:
                if "Total Payment Amount (RM)" in line:
                    payment_amount = float(line.split(":")[1].strip())
                    total_payment_amount += payment_amount
                if "Total Items Quantity" in line:
                    paid_item_qty = int(line.split(":")[1].strip())
                    total_paid_item_qty += paid_item_qty

    return total_payment_amount, total_payment_qty,  total_paid_item_qty

#Task 3: Generate Daily Financial Report
def generate_daily_financial_report(current_date, financial_data):
    """
    Obtain sales data from function in Administrator.
    Obtain order payment data from track_payment function.
    Generate the daily financial report by format and append into the master list in Administrator.
    """
    #Declare the variables and assign values, then calculate the values of other variables.
    gross_sales = financial_data[0]
    sales_return = financial_data[1]
    net_sales = financial_data[2]
    sales_variance = financial_data[3]
    gross_payment, paid_payment_qty, paid_item_qty = track_payment("Paid", current_date)
    payment_refunded, refund_payment_qty, refund_item_qty = track_payment("Refunded", current_date)
    net_procurement = gross_payment - payment_refunded
    net_profit = net_sales - net_procurement
    payment_unpaid, unpaid_payment_qty, unpaid_item_qty = track_payment("Unpaid")
    #Generate the list of financial report.
    report_details = [
        "-" * 42 + "\n",
        f"{"SECTION B: FINANCIAL REPORT".center(42)}" + "\n",
        "-" * 42 + "\n",
        f"{"Gross Sales".ljust(28)}: RM {gross_sales:.2f}\n",
        f"{"(-) Sales Returns".ljust(28)}: RM {sales_return:.2f}\n",
        f"{"NET SALES".ljust(28)}: RM {net_sales:.2f} ({sales_variance}%)\n\n",
        f"{"(-) Gross Order Payments".ljust(28)}: RM {gross_payment:.2f} ({paid_payment_qty} payments: {paid_item_qty} units)\n",
        f"{"Order Payments Refunded".ljust(28)}: RM {payment_refunded:.2f} ({refund_payment_qty} payments: {refund_item_qty} units)\n",
        f"{"(-) NET PROCUREMENT".ljust(28)}: RM {net_procurement:.2f}\n\n",
        f"{"DAILY NET PROFITS".ljust(28)}: RM {net_profit:.2f}\n",
        f"{"Unpaid Supplier Balance".ljust(28)}: RM {payment_unpaid:.2f} ({unpaid_payment_qty} payments: {unpaid_item_qty} units)\n"
    ]

    return report_details

#Task 4: Generate Monthly Financial Report
def calculate_monthly_report_data(daily_reports_list):
    """
    Aggregates data from a list of daily reports to calculate monthly totals
    for sales, returns, order payments, and refunds.
    """
    #Initialize Monthly Accumulators
    monthly_gross_sales = 0.00
    monthly_item_sold_qty = 0
    monthly_sales_return = 0.00
    monthly_item_returned_qty = 0
    monthly_gross_payment = 0.00
    monthly_paid_payment_qty = 0
    monthly_paid_item_qty = 0
    monthly_payment_refunded = 0.00
    monthly_refund_payment_qty = 0
    monthly_refund_item_qty = 0

    #Iterate Through Each Daily Report
    for report in daily_reports_list:
        # Break the report block into individual lines for processing
        line_details = report.split("\n")
        for line in line_details:
            try:
                # Obtain Sales Data
                if "Gross Sales" in line:
                    # Extracts currency value after ": RM"
                    gross_sales = float(line.split(": RM")[1].strip())
                    monthly_gross_sales += gross_sales

                if "Total Transactions" in line:
                    # Slices text between "(" and "units" to get the quantity
                    starting_index = line.index("(")
                    ending_index = line.index("units")
                    item_sold_qty = int(line[starting_index + 1:ending_index].strip())
                    monthly_item_sold_qty += item_sold_qty

                #Obtain Return Data
                if "Sales Returns" in line:
                    sales_return = float(line.split(": RM")[1].strip())
                    monthly_sales_return += sales_return

                if "Customer Returns" in line:
                    # Logic identical to 'Total Transactions' parsing
                    starting_index = line.index("(")
                    ending_index = line.index("units")
                    item_returned_qty = int(line[starting_index + 1:ending_index].strip())
                    monthly_item_returned_qty += item_returned_qty

                # Obtain Gross Order Payments
                if "Gross Order Payments" in line:
                    payment_amount_with_qty = line.split(": RM")[1].strip()

                    # Identify positions of delimiters for slicing
                    first_index = payment_amount_with_qty.index("(")
                    second_index = payment_amount_with_qty.index("payments:")
                    third_index = payment_amount_with_qty.index("units")

                    # Extract and convert values based on calculated indices
                    gross_payment = float(payment_amount_with_qty[:first_index].strip())
                    paid_payment_qty = int(payment_amount_with_qty[first_index + 1:second_index].strip())
                    paid_item_qty = int(payment_amount_with_qty[second_index + 9:third_index].strip())

                    # Add daily values to monthly totals
                    monthly_gross_payment += gross_payment
                    monthly_paid_payment_qty += paid_payment_qty
                    monthly_paid_item_qty += paid_item_qty

                # Parsing Refunded Order Payments
                # Follows the same slicing logic as Gross Order Payments
                if "Order Payments Refunded" in line:
                    payment_amount_with_qty = line.split(": RM")[1].strip()
                    first_index = payment_amount_with_qty.index("(")
                    second_index = payment_amount_with_qty.index("payments:")
                    third_index = payment_amount_with_qty.index("units")
                    payment_refunded = float(payment_amount_with_qty[:first_index].strip())
                    refund_payment_qty = int(payment_amount_with_qty[first_index + 1:second_index].strip())
                    refund_item_qty = int(payment_amount_with_qty[second_index + 9:third_index].strip())
                    monthly_payment_refunded += payment_refunded
                    monthly_refund_payment_qty += refund_payment_qty
                    monthly_refund_item_qty += refund_item_qty

            except (ValueError, IndexError):
                # If a line is malformed, skip it instead of crashing the whole month
                continue

    # Compile and Return the Data
    # Pack all aggregated totals into a single list for the calling function
    monthly_financial_data = [monthly_gross_sales, monthly_item_sold_qty, monthly_sales_return,
                              monthly_item_returned_qty, monthly_gross_payment, monthly_paid_payment_qty,
                              monthly_paid_item_qty, monthly_payment_refunded, monthly_refund_payment_qty,
                              monthly_refund_item_qty]
    return monthly_financial_data
def check_variance_vs_last_month(last_month_name, last_month_year, current_net_sales, current_net_procurement,
                                 current_net_profit):
    """
    Compares current month performance against a specific previous month's data
    retrieved from 'monthly_report.txt'. Calculates percentage and amount variances.
    """
    #Check if the file exists. If no, return 0
    try:
        with open("monthly_report.txt", "r") as file:
            contents = file.read()
    except FileNotFoundError:
        return 0, 0, 0, 0, 0

    #Split the report using headers.
    report_separator = "\n" + "=" * 15 + "MONTHLY REPORT" + "=" * 15 + "\n"
    report_details = contents.split(report_separator)

    # Initialize variables for the data we need to find
    last_month_report_found = False
    last_month_net_sales = 0.00
    last_month_net_procurement = 0.00
    last_month_net_profit = 0.00

    # Search for the Target Month's Data
    for report in report_details:
        # Check if this specific block matches the target month and year
        if f"Report Month: {last_month_name} {last_month_year}" in report:
            last_month_report_found = True
            line_details = report.split("\n")
            for line in line_details:
                # Obtain all datas by checking every line.
                # As some lines involve multiple data, using slicing to find target data.
                if "NET SALES" in line:
                    net_sales_details = line.split(": RM")[1].strip()
                    last_month_net_sales = float(net_sales_details[:net_sales_details.index("(")].strip())

                if "NET PROCUREMENT" in line:
                    net_procurement_details = line.split(": RM")[1].strip()
                    last_month_net_procurement = float(net_procurement_details[:net_procurement_details.index("(")].strip())

                if f"NET PROFIT ({last_month_name} {last_month_year})" in line:
                    last_month_net_profit = float(line.split(": RM")[1].strip())
            break

    #Validate Results
    if not last_month_report_found:
        print("Last month's report not found. Cannot generate variance.")
        return 0, 0, 0, 0, 0

    #Calculation of Variances using Formulas
    if float(last_month_net_sales) == 0:
        last_month_sales_variance = 0
    else:
        last_month_sales_variance = int(((float(current_net_sales) - float(last_month_net_sales))
                                         /float(last_month_net_sales)) * 100)

    if float(last_month_net_procurement) == 0:
        last_month_procurement_variance = 0
    else:
        last_month_procurement_variance = int(((float(current_net_procurement) - float(last_month_net_procurement))
                                           /float(last_month_net_procurement)) * 100)

    profit_variance_amount = float(current_net_profit) - float(last_month_net_profit)

    if float(last_month_net_profit) == 0:
        profit_variance_percentage = 0
    else:
        profit_variance_percentage = int(((float(current_net_profit) - float(last_month_net_profit))
                                          /float(last_month_net_profit)) * 100)

    return (last_month_sales_variance, last_month_procurement_variance, last_month_net_profit, profit_variance_amount,
            profit_variance_percentage)
def generate_monthly_financial_report(current_date, current_month, current_year):
    """
    Orchestrates the creation of a monthly financial summary by filtering daily reports,
    calculating net totals, and comparing performance against the previous month.
    """
    import Administrator

    # Identify Reporting Periods
    current_month_name = Administrator.determine_month_name(int(current_month))
    # Calculate the previous month's name and handle the year rollover (January -> December)
    last_month_name = Administrator.determine_month_name(int(current_month) - 1)
    if int(current_month) - 1 == 0:
        last_month_year = int(current_year) - 1
        #Convert the integer year into formatted strings.
        if 0 < last_month_year <= 9:
            last_month_year = "000" + str(last_month_year)
        elif 10 <= last_month_year <= 99:
            last_month_year = "00" + str(last_month_year)
        elif 100 <= last_month_year <= 999:
            last_month_year = "0" + str(last_month_year)
        else:
            last_month_year = str(last_month_year)
    else:
        last_month_year = current_year

    # Retrieve Daily Report Data
    try:
        with open("daily_report.txt", "r") as report_file:
            report_data = report_file.read()
    except FileNotFoundError:
        print(f"Daily reports for {current_month_name} {current_year} not found.\n")
        return []

    # Filter Daily Reports for the Target Month
    report_separator = "\n" + "=" * 15 + "DAILY REPORT" + "=" * 15 + "\n"
    report_list = report_data.split(report_separator)
    target_report_list = []
    for report in report_list:
        line_details = report.split("\n")
        for line in line_details:
            if "Report Date" in line:
                report_date = line.split(":")[1].strip()
                report_month = report_date.split("/")[1]
                report_year = report_date.split("/")[2].strip()

                # Only collect reports matching the month and year requested
                if report_month == current_month and report_year == current_year:
                    full_report = report_separator + report.strip() + "\n"
                    target_report_list.append(full_report)
                break

    # Exit if no matching data is found for that specific month
    if not target_report_list:
        print(f"Daily reports for {current_month_name} {current_year} not found.\n")
        return []

    #Financial Calculations
    #Using formula to obtain raw data
    (monthly_gross_sales, monthly_item_sold_qty, monthly_sales_return, monthly_item_returned_qty,
     monthly_gross_payment, monthly_paid_payment_qty, monthly_paid_item_qty, monthly_payment_refunded,
     monthly_refund_payment_qty, monthly_refund_item_qty) = calculate_monthly_report_data(target_report_list)

    #Calculate net figures
    monthly_net_sales = float(monthly_gross_sales - monthly_sales_return)
    monthly_net_procurement = float(monthly_gross_payment - monthly_payment_refunded)
    monthly_net_profit = monthly_net_sales - monthly_net_procurement

    #Calculate Variances
    (last_month_sales_variance, last_month_procurement_variance, last_month_net_profit, profit_variance_amount,
    profit_variance_percentage) = check_variance_vs_last_month(last_month_name, last_month_year, monthly_net_sales,
                                                               monthly_net_procurement, monthly_net_profit)
    #Formatting Final Report
    monthly_report_details = [
        "\n" + "=" * 15 + "MONTHLY REPORT" + "=" * 15 + "\n",
        f"Report Month: {current_month_name} {current_year}\n",
        f"Date Generated: {current_date}\n",
        "-" * 44 + "\n",
        f"{"Gross Sales".ljust(30)}: RM {monthly_gross_sales:.2f} ({monthly_item_sold_qty} units)\n",
        f"{"(-) Sales Returns".ljust(30)}: RM {monthly_sales_return:.2f} ({monthly_item_returned_qty} units)\n",
        f"{"NET SALES".ljust(30)}: RM {monthly_net_sales:.2f} ({last_month_sales_variance}% vs {last_month_name} "
        f"{last_month_year})\n\n",
        f"{"(-) Gross Order Payments".ljust(30)}: RM {monthly_gross_payment:.2f} ({monthly_paid_payment_qty} payments: "
        f"{monthly_paid_item_qty} units)\n",
        f"{"Order Payments Refunded".ljust(30)}: RM {monthly_payment_refunded:.2f} ({monthly_refund_payment_qty} payments: "
        f"{monthly_refund_item_qty} units)\n",
        f"{"(-) NET PROCUREMENT".ljust(30)}: RM {monthly_net_procurement:.2f} ({last_month_procurement_variance}% vs "
        f"{last_month_name} {last_month_year})\n\n",
        f"{f"NET PROFIT ({current_month_name} {current_year})".ljust(30)}: RM {monthly_net_profit:.2f}\n",
        f"{f"NET PROFIT ({last_month_name} {last_month_year})".ljust(30)}: RM {last_month_net_profit:.2f}\n",
        f"{f"Profits Variance".ljust(30)}: RM {profit_variance_amount:.2f} ({profit_variance_percentage}%)\n",
    ]

    #Print the whole report
    print("".join(monthly_report_details))

    #Append the whole report to file
    with open("monthly_report.txt", "a") as report_file:
        report_file.writelines(monthly_report_details)
    print(f"Monthly report for {current_month_name} {current_year} recorded successfully.\n")

    return monthly_report_details
def check_monthly_report_generated(current_date, current_month, current_year):
    """
    Checks if a report for the current month already exists.
    If not, it generates one. If it does, it updates the existing entry
    to ensure the data is current.
    Same as function check_daily_report_generated.
    """
    import Administrator

    #Check if the file exists.
    try:
        with open("monthly_report.txt", "r") as report_file:
            report_data = report_file.read()
    except FileNotFoundError:
        # If the file doesn't exist, generate a new one
        generate_monthly_financial_report(current_date, current_month, current_year)
        return

    current_month_name = Administrator.determine_month_name(current_month)
    #If the string with given month and year not in the report, generate a new one.
    if not f"Report Month: {current_month_name} {current_year}" in report_data:
        print("Generating monthly financial report...\n")
        generate_monthly_financial_report(current_date, current_month, current_year)
    else:
        #If exists, update a new report.
        print("Updating this month's report...\n")

        #Split all reports in the file using headers.
        report_separator = "\n" + "=" * 15 + "MONTHLY REPORT" + "=" * 15 + "\n"
        report_list = report_data.split(report_separator)
        new_report_list = []

        for report in report_list:
            if report.strip():
                # If this specific block is the one we are looking for
                if f"Report Month: {current_month_name} {current_year}" in report:
                    # Regenerate the data and get the fresh list of report lines
                    new_report_details = generate_monthly_financial_report(current_date, current_month, current_year)
                    new_report = "".join(new_report_details)

                    # Add the NEW version of the report to our list
                    new_report_list.append(new_report)
                else:
                    # For other months, keep the data exactly as it was
                    full_report = report_separator + report.strip() + "\n"
                    new_report_list.append(full_report)
        #Save changes into the file
        with open("monthly_report.txt", "w") as report_file:
            report_file.writelines(new_report_list)
