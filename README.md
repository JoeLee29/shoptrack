# ShopTrack - Inventory and Sales Management System

## Overview
ShopTrack is a Python-based Inventory and Sales Management System (ISMS) designed for small retail stores. It automates inventory tracking, sales processing, supplier management, and report generation, transitioning traditional paper-based recording into a robust digital solution. 

## Key Features by Role
ShopTrack provides a role-based menu system featuring five distinct user modules, each tailored to specific operational needs:

### 1. Administrator
- View and manage the complete inventory overview.
- Add, remove, or update item details and pricing dynamically.
- Generate and view automated daily operational and financial reports.

### 2. Cashier
- Process sales transactions and calculate totals, including discounts.
- View previous receipts via Transaction ID or Date.
- Process return transactions with a built-in 14-day policy validation.

### 3. Accountant
- Track and view supplier payments (Unpaid, Paid, Refunded).
- Generate comprehensive monthly financial reports tracking Gross Sales, Procurement, and Profit Variances.

### 4. Stock Manager
- Maintain and update supplier details.
- Monitor stock levels and generate automated restock requests when stock falls below target quantities.
- Coordinate order placement with auto-generated sequential Order IDs.

### 5. Supplier
- View incoming orders filtered by status, date, or Supplier ID.
- Update order statuses through a controlled pipeline (`PENDING` -> `DELIVERED` -> `RECEIVED`).
- Manage order payments and process refunds for cancelled/returned orders.

## Technical Architecture
- **Language:** Python
- **Data Storage:** Flat text files (`.txt`) with fixed-width formatting to ensure readability and easy parsing.
  - `inventory.txt`, `sales.txt`, `orders.txt`, `payments.txt`, `supplier.txt`, `daily_report.txt`, `monthly_report.txt`
- **Core Programming Concepts:**
  - Standardized string parsing and list management.
  - Comprehensive `Try-Except` error handling and strict input validation (e.g., standardizing ID formats, checking numerical constraints).
  - Multi-level control structures and custom date handling without relying on external libraries.

## Requirements
- Python 3.x (no external/third-party packages required — standard library only)

## How to Run
1. Execute the main Python script.
2. Upon startup, input the current system date (`DD/MM/YYYY`). The system strictly operates on this entered date for all transactions and validations.
3. Select a role from the Main Menu (`1-6`) to access the designated task menu — there is no login step, the menu goes straight into the chosen role.
4. Follow the intuitive command-line interface (CLI) prompts to manage store operations.

*Note: Exiting the program automatically triggers the generation and update of the day's `daily_report.txt`.*

**First run:** The `.txt` data files (`inventory.txt`, `sales.txt`, `orders.txt`, `payments.txt`, `supplier.txt`, `daily_report.txt`, `monthly_report.txt`) are created automatically if they don't already exist — no manual setup is needed before launching.

## Screenshots / Demo
*(Add screenshots or a short GIF of the CLI in action here, e.g. the Main Menu and a sample transaction flow.)*

## Known Issues & Limitations
- Single-user only — the system does not support concurrent access to the data files by multiple users at the same time.

## Project Details
- **Institution:** Asia Pacific University of Technology & Innovation (APU)
- **Module:** CT108-3-1-PYP Programming with Python
- **Group:** 27
- **Team Members:** E Joe Lee, Yai Hoo In, Addy Ling How Yun, Royce Ling Wan Hao, Hiroki Nishiyama
