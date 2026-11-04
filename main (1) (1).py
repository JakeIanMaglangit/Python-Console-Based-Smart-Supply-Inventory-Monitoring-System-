"""
ITE 260 - Computer Programming 1
Period 2 Project Milestone - Group 7

Python Console-Based School Supply Inventory Monitoring System

An offline, console-based inventory system that organizes school supplies
into categories, monitors the stock quantity of each specific item,
updates stock records, identifies supplies that need restocking, and
displays inventory reports.

All data is stored in in-memory Python lists. Records are lost when the
program is closed.
"""

# ---------------------------------------------------------------------------
# INVENTORY DATA (SAMPLE DATA for demonstration only, not actual stock)
#
# Each record is a list:
#   [product_id, category, product_name, quantity, restock_level]
#     product_id    (str) - unique ID of the school supply
#     category      (str) - supply category (example: "Pens", "Papers")
#     product_name  (str) - specific supply type
#     quantity      (int) - current quantity of the supply
#     restock_level (int) - minimum stock level used for monitoring
# ---------------------------------------------------------------------------
supplies = [
    ["P001", "Pens", "Red Pen", 25, 10],
    ["P002", "Pens", "Stylus Pen", 15, 5],
    ["P003", "Pens", "Black Pen", 40, 10],
    ["P004", "Pens", "Sign Pen", 8, 10],
    ["P005", "Papers", "Bond Paper", 50, 10],
    ["P006", "Papers", "Yellow Pad", 12, 15],
    ["P007", "Papers", "Short Bond Paper", 30, 10],
    ["P008", "Papers", "Long Bond Paper", 5, 10],
]

# Stock updates made during the current session (used by Report B).
# Each record: [product_id, product_name, operation, old_quantity, new_quantity]
stock_updates = []


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def get_categories():
    """Return the list of categories that exist in the inventory."""
    categories = []
    for item in supplies:
        if item[1] not in categories:
            categories.append(item[1])
    return categories


def find_supply_by_id(product_id):
    """Return the supply record with the given Product ID, or None."""
    for item in supplies:
        if item[0] == product_id:
            return item
    return None


def find_category(category_name):
    """Return an existing category that matches the name (ignoring case), or None."""
    for existing in get_categories():
        if existing.lower() == category_name.strip().lower():
            return existing
    return None


def find_item_in_category(category, product_name):
    """Return a record with the same name inside the category, or None."""
    for item in supplies:
        if item[1] == category and item[2].lower() == product_name.strip().lower():
            return item
    return None


def get_items_by_category(category):
    """Return all supply records that belong to the given category."""
    items = []
    for item in supplies:
        if item[1] == category:
            items.append(item)
    return items


def stock_status(item):
    """Return RESTOCK if quantity is at or below the restock level, otherwise SUFFICIENT."""
    if item[3] <= item[4]:
        return "RESTOCK"
    return "SUFFICIENT"


def read_nonempty(prompt):
    """Ask until the user enters text that is not empty."""
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("[ERROR] This field cannot be empty. Please try again.")


def read_nonnegative_int(prompt):
    """Ask until the user enters a whole number that is zero or positive."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("[ERROR] Please enter a whole number (examples: 0, 5, 20).")
            continue
        if number < 0:
            print("[ERROR] Value cannot be negative. Please try again.")
            continue
        return number


def display_supply_table(items):
    """Display a list of supply records as an aligned table."""
    if len(items) == 0:
        print("\n[INFO] No inventory records to display.")
        return
    header = (f"{'ID':<8} {'Category':<12} {'Supply Name':<20} "
              f"{'Qty':>6} {'Restock':>8}  {'Status':<10}")
    print("\n" + header)
    print("-" * len(header))
    for item in items:
        status = stock_status(item)
        print(f"{item[0]:<8} {item[1]:<12} {item[2]:<20} "
              f"{item[3]:>6} {item[4]:>8}  {status:<10}")


def display_status_lines(items):
    """Display stock status lines in the style of the original check_status()."""
    if len(items) == 0:
        print("\n[INFO] No inventory records to display.")
        return
    for item in items:
        status = stock_status(item)
        print(f"{item[2]} ({item[1]}, {item[0]}): {item[3]} units - {status}")


def choose_category():
    """Show the categories and return the selected category name, or None to cancel."""
    categories = get_categories()
    if len(categories) == 0:
        print("\n[INFO] There are no categories yet. Add a supply first.")
        return None
    print("\nCategories:")
    for i in range(len(categories)):
        print(f"  {i + 1}. {categories[i]}")
    print("  0. Cancel / Go back")
    while True:
        choice = input("Select category number: ").strip()
        if choice == "0":
            return None
        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(categories):
                return categories[number - 1]
        print("[ERROR] Invalid category selection. Please try again.")


# ---------------------------------------------------------------------------
# FEATURE 1 - ADD SCHOOL SUPPLY
# ---------------------------------------------------------------------------

def add_supply():
    """Add a new, categorized school supply record to the inventory list."""
    print("\n--- ADD SCHOOL SUPPLY ---")

    # 1. Product ID (must be unique)
    product_id = read_nonempty("Enter Product ID: ")
    while find_supply_by_id(product_id) is not None:
        print(f"[ERROR] Product ID '{product_id}' is already registered.")
        product_id = read_nonempty("Enter a different Product ID: ")

    # 2. Category (choose an existing one or create a new one)
    categories = get_categories()
    print("\nAvailable categories:")
    for i in range(len(categories)):
        print(f"  {i + 1}. {categories[i]}")
    print("  0. Create a new category")
    category = None
    while category is None:
        choice = input("Select category number: ").strip()
        if choice == "0":
            new_category = read_nonempty("Enter new category name: ")
            existing = find_category(new_category)
            if existing is None:
                category = new_category
            else:
                print(f"[INFO] Category already exists. Using '{existing}'.")
                category = existing
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
        else:
            print("[ERROR] Invalid selection. Please try again.")

    # 3. Specific supply name (must be unique within the category)
    product_name = read_nonempty("Enter Supply Name: ")
    while find_item_in_category(category, product_name) is not None:
        print(f"[ERROR] '{product_name}' already exists in category '{category}'.")
        product_name = read_nonempty("Enter a different Supply Name: ")

    # 4 and 5. Quantity and restock level
    quantity = read_nonnegative_int("Enter Quantity: ")
    restock_level = read_nonnegative_int("Enter Restock Level: ")

    supplies.append([product_id, category, product_name, quantity, restock_level])
    print("\n[SUCCESS] School supply added successfully.")


# ---------------------------------------------------------------------------
# FEATURE 2 - VIEW INVENTORY
# ---------------------------------------------------------------------------

def view_inventory():
    """Menu for viewing all supplies, supplies by category, or searching."""
    while True:
        print("\n--- VIEW INVENTORY ---")
        print("1. View All Supplies")
        print("2. View Supplies by Category")
        print("3. Search for a Specific Supply")
        print("4. Return to Main Menu")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            display_supply_table(supplies)
        elif choice == "2":
            view_by_category()
        elif choice == "3":
            search_supply()
        elif choice == "4":
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")


def view_by_category():
    """Display only the supplies that belong to a selected category."""
    category = choose_category()
    if category is None:
        return
    items = get_items_by_category(category)
    print(f"\n--- {category.upper()} INVENTORY ---")
    display_supply_table(items)


def search_supply():
    """Find supply records by Product ID or by supply name."""
    print("\n--- SEARCH SUPPLY ---")
    keyword = read_nonempty("Enter Product ID or supply name: ")
    matches = []
    for item in supplies:
        if item[0].lower() == keyword.lower() or keyword.lower() in item[2].lower():
            matches.append(item)
    if len(matches) == 0:
        print(f"[INFO] No supply records matched '{keyword}'.")
    else:
        display_supply_table(matches)


# ---------------------------------------------------------------------------
# FEATURE 3 - UPDATE STOCK
# ---------------------------------------------------------------------------

def update_stock():
    """Update the quantity of one supply: set exact, add stock, or deduct stock."""
    print("\n--- UPDATE STOCK ---")
    product_id = read_nonempty("Enter Product ID to update: ")
    item = find_supply_by_id(product_id)
    if item is None:
        print("[ERROR] Product ID not found.")
        return

    print(f"Selected: {item[2]} ({item[1]}) - Current quantity: {item[3]} units")
    print("\n1. Set Exact Quantity")
    print("2. Add Stock")
    print("3. Deduct Stock")
    print("4. Cancel")
    choice = input("Enter choice: ").strip()

    previous_quantity = item[3]
    if choice == "1":
        new_quantity = read_nonnegative_int("Enter new quantity: ")
        item[3] = new_quantity
        operation = "Set Exact"
    elif choice == "2":
        amount = read_nonnegative_int("Enter quantity to add: ")
        item[3] = item[3] + amount
        operation = "Add Stock"
    elif choice == "3":
        amount = read_nonnegative_int("Enter quantity to deduct: ")
        if amount > item[3]:
            print(f"[ERROR] Cannot deduct {amount}. Only {item[3]} units available.")
            return
        item[3] = item[3] - amount
        operation = "Deduct Stock"
    elif choice == "4":
        print("[INFO] Update cancelled.")
        return
    else:
        print("[ERROR] Invalid choice. Update cancelled.")
        return

    stock_updates.append([item[0], item[2], operation, previous_quantity, item[3]])
    print(f"\n[SUCCESS] Stock updated: {item[2]} changed from "
          f"{previous_quantity} to {item[3]} units.")


# ---------------------------------------------------------------------------
# FEATURE 4 - CHECK STOCK STATUS
# ---------------------------------------------------------------------------

def check_status():
    """Menu for checking stock status of all supplies, by category, or restock list."""
    while True:
        print("\n--- CHECK STOCK STATUS ---")
        print("1. Stock Status of All Supplies")
        print("2. Stock Status by Category")
        print("3. Items Requiring Restock")
        print("4. Return to Main Menu")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            print("\n--- STOCK STATUS ---")
            display_status_lines(supplies)
        elif choice == "2":
            category = choose_category()
            if category is not None:
                print(f"\n--- STOCK STATUS: {category.upper()} ---")
                display_status_lines(get_items_by_category(category))
        elif choice == "3":
            display_restock_items()
        elif choice == "4":
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")


def display_restock_items():
    """Display only the supplies whose quantity is at or below the restock level."""
    restock_items = []
    for item in supplies:
        if item[3] <= item[4]:
            restock_items.append(item)
    print("\n--- ITEMS REQUIRING RESTOCK ---")
    if len(restock_items) == 0:
        print("[INFO] All supplies have sufficient stock.")
        return
    display_supply_table(restock_items)


# ---------------------------------------------------------------------------
# FEATURE 5 - INVENTORY REPORTS
# ---------------------------------------------------------------------------

def show_reports():
    """Menu for the four console-based inventory reports."""
    while True:
        print("\n--- INVENTORY REPORTS ---")
        print("1. Complete Inventory List")
        print("2. Updated Stock Records")
        print("3. Low-Stock Items")
        print("4. Inventory Summary")
        print("5. Return to Main Menu")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            report_complete_inventory()
        elif choice == "2":
            report_updated_stock()
        elif choice == "3":
            report_low_stock()
        elif choice == "4":
            report_summary()
        elif choice == "5":
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")


def report_complete_inventory():
    """Report A: all records, grouped by category."""
    print("\n--- REPORT: COMPLETE INVENTORY LIST ---")
    if len(supplies) == 0:
        print("[INFO] Inventory is empty.")
        return
    for category in get_categories():
        items = get_items_by_category(category)
        print(f"\nCategory: {category} ({len(items)} record(s))")
        display_supply_table(items)


def report_updated_stock():
    """Report B: supplies whose stock was updated during this session."""
    print("\n--- REPORT: UPDATED STOCK RECORDS (THIS SESSION) ---")
    if len(stock_updates) == 0:
        print("[INFO] No stock updates have been made in this session.")
        return
    header = (f"{'ID':<8} {'Supply Name':<20} {'Operation':<12} "
              f"{'Old Qty':>8} {'New Qty':>8}")
    print("\n" + header)
    print("-" * len(header))
    for record in stock_updates:
        print(f"{record[0]:<8} {record[1]:<20} {record[2]:<12} "
              f"{record[3]:>8} {record[4]:>8}")


def report_low_stock():
    """Report C: records where quantity <= restock_level."""
    print("\n--- REPORT: LOW-STOCK ITEMS ---")
    low_items = []
    for item in supplies:
        if item[3] <= item[4]:
            low_items.append(item)
    if len(low_items) == 0:
        print("[INFO] No supplies need restocking.")
        return
    display_supply_table(low_items)


def report_summary():
    """Report D: counts of records, categories, and stock statuses."""
    print("\n--- REPORT: INVENTORY SUMMARY ---")
    categories = get_categories()
    sufficient_count = 0
    restock_count = 0
    for item in supplies:
        if item[3] <= item[4]:
            restock_count += 1
        else:
            sufficient_count += 1
    print(f"Distinct supply records:      {len(supplies)}")
    print(f"Categories:                   {len(categories)}")
    print(f"Items with sufficient stock:  {sufficient_count}")
    print(f"Items requiring restock:      {restock_count}")
    if len(categories) > 0:
        print("\nRecords per category:")
        for category in categories:
            count = len(get_items_by_category(category))
            print(f"  {category}: {count} record(s)")


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------

def main():
    """Run the console menu until the user chooses Exit."""
    while True:
        print("\n====================================")
        print(" SCHOOL SUPPLY INVENTORY SYSTEM")
        print(" ITE 260 - Group 7")
        print("====================================")
        print("1. Add School Supply")
        print("2. View Inventory")
        print("3. Update Stock")
        print("4. Check Stock Status")
        print("5. Inventory Reports")
        print("6. Exit")
        try:
            choice = input("Enter your choice: ").strip()
        except EOFError:
            print("\nThank you for using the system!")
            break
        if choice == "1":
            add_supply()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            check_status()
        elif choice == "5":
            show_reports()
        elif choice == "6":
            print("\nThank you for using the system!")
            break
        else:
            print("[ERROR] Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()