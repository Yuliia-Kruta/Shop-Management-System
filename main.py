import csv
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Global variables
inventory = []
cart = []
inventory_file = "inventory.csv"

# GUI global variables
aisle_number = None
product_entry = None
aisle_products = None


def load_inventory():
    """Loads the content of inventory file into the list"""
    global inventory
    try:
        with open(inventory_file, "r") as file:
            reader = csv.reader(file)
            inventory = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Error", "Inventory file not found.")


def display_inventory(aisle):
    """Determines the items from the specified aisle.
        :param aisle: name or number of the aisle
        :returns: list of lists, that include product name, price and their quantity in stock"""
    items = []
    for item in inventory:
        if item[2].lower() == aisle.lower().strip():
            item_info = [item[0], item[1], item[3]]
            items.append(item_info)
    return items


def add_to_cart(item_name):
    """Adds the product to the cart if it is available in stock"""
    global cart
    for item in inventory:
        if item[0].lower() == item_name.lower().strip():
            if int(item[3]) > 0:
                cart.append(item)
                item[3] = str(int(item[3]) - 1)
                messagebox.showinfo("Success", "Item added to cart.")
                if aisle_number is not None and aisle_number.get() != "":
                    on_display_button_click()
            else:
                messagebox.showwarning("Out of Stock", "Item is out of stock.")
            return
    messagebox.showerror("Error", "Item not found.")


def checkout():
    """Clears the cart, updates the inventory file to reflect the decrease of stock"""
    cart.clear()
    update_inventory_file()
    messagebox.showinfo("Checkout", "Purchase completed successfully.")


def on_view_cart_button_click():
    """Shows information about the items in the cart and their total cost"""
    total = 0
    items = ""
    for item in cart:
        items += item[0] + "\t" + item[1] + "$AUD\n"
        total += float("{:.2f}".format(float(item[1])))
    messagebox.showinfo("Your cart:", "Items:\n" + items + "\nTotal amount payable: {:.2f}$AUD".format(total))
    if items != "":
        result = messagebox.askquestion("Cart Summary", "Do you want to proceed to checkout?")
        if result == "yes":
            checkout()


def update_inventory_file():
    """Updates the inventory file"""
    with open(inventory_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(inventory)


def on_display_button_click():
    """Shows the items from a specified aisle in the GUI"""
    aisle = aisle_number.get()
    items = display_inventory(aisle)
    if items:
        aisle_products.delete(*aisle_products.get_children())  # Clear previous data
        for item in items:
            aisle_products.insert("", tk.END, values=item)
    else:
        messagebox.showerror("Error", "No such aisle.")


def on_cancel_order_button_click():
    """Clears the cart if it is not already empty"""
    if not cart:
        messagebox.showinfo("Info", "Your cart is empty")
    else:
        result = messagebox.askquestion("Cart Summary", "Would you like to cancel the order?",
                                        icon="warning", type=messagebox.YESNO, default=messagebox.YES)
        if result == "yes":
            cart.clear()
            messagebox.showinfo("Order Canceled", "The order has been canceled.")
            load_inventory()
            if aisle_number.get() != "":
                on_display_button_click()


def on_add_button_click():
    """Triggers function that adds the product to the cart"""
    item_name = product_entry.get()
    add_to_cart(item_name)


def main():
    global aisle_number, product_entry, aisle_products
    # Loads the inventory list
    load_inventory()

    # Creates GUI for the app
    # Main Window
    window = tk.Tk()
    window.title("Shop Management System")
    window.configure(borderwidth=10)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 370
    window_height = 450
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    # Placing window in the center of the screen
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Adding other GUI components, using grid as a layout

    aisle_label = tk.Label(window, text="Please enter the aisle number:")
    aisle_label.grid(row=0, column=0, sticky="W", pady=5)
    aisle_number = tk.Entry(window, width=10)
    aisle_number.grid(row=1, column=0, sticky="W", pady=5)

    display_button = tk.Button(window, text="Display Items", command=on_display_button_click)
    display_button.grid(row=1, column=1, pady=5, sticky="W")

    aisle_label = tk.Label(window, text="Products in the aisle:")
    aisle_label.grid(row=2, column=0, sticky="W", pady=5)

    # Displaying the products from the specified aisle in the neat format
    aisle_products = ttk.Treeview(window, columns=("Item", "Price", "Stock"), show="headings")
    aisle_products.heading("Item", text="Item")
    aisle_products.heading("Price", text="Price")
    aisle_products.heading("Stock", text="Stock")
    aisle_products.column("Item", width=100, anchor="center")
    aisle_products.column("Price", width=100, anchor="center")
    aisle_products.column("Stock", width=100, anchor="center")
    aisle_products.grid(row=3, column=0, columnspan=2, sticky="W", pady=5)

    item_label = tk.Label(window, text="Please enter the name of the product:")
    item_label.grid(row=4, column=0, sticky="W", pady=5)
    product_entry = tk.Entry(window)
    product_entry.grid(row=5, column=0, sticky="W", pady=5)

    add_button = tk.Button(window, text="Add to Cart", command=on_add_button_click)
    add_button.grid(row=5, column=1, pady=5, sticky="W")

    view_cart_button = tk.Button(window, text="View Cart", command=on_view_cart_button_click)
    view_cart_button.grid(row=6, column=0, pady=5)

    cancel_order_button = tk.Button(window, text="Cancel Order", command=on_cancel_order_button_click)
    cancel_order_button.grid(row=6, column=1, pady=5)

    window.mainloop()


if __name__ == "__main__":
    main()


def assert_equals(expected_value, actual_value):
    line_num = sys._getframe(1).f_lineno
    if expected_value == actual_value:
        print("\n  Passed test at line " + str(line_num) + " with " + str(actual_value))
    else:
        print("ERROR: test at line " + str(line_num) + " failed.  Expected "
              + str(expected_value) + " but got " + str(actual_value), file=sys.stderr)


# Unit tests

# def test_display_inventory():
#     load_inventory()
#     assert_equals([["Cake", "5", "6"]], display_inventory("19"))
#     assert_equals([["Rice", "2.99", "8"], ["Pasta", "1.49", "6"], ["Flour", "1.99", "5"]], display_inventory("15"))
#     assert_equals([["Mango", "2.99", "0"], ["Big Mango", "4.00", "1"]], display_inventory("2"))
#     assert_equals([["Tomato", "0.79", "3"]], display_inventory("Vegetables"))
#     assert_equals([["Tomato", "0.79", "3"]], display_inventory("  vegetables"))
#     assert_equals([], display_inventory("20"))
#     assert_equals([], display_inventory(""))
#
#
# def test_add_to_cart():
#     expected_values = [["Apple", "1.99", "1", "3"]]
#     for i in range(1, 5):
#         load_inventory()
#         global cart
#         cart = []
#
#         if i == 1:
#             add_to_cart("Apple")
#             assert_equals(cart, expected_values)
#         if i == 2:
#             add_to_cart("apple")
#             assert_equals(cart, expected_values)
#         if i == 3:
#             add_to_cart("watermelon")
#             assert_equals(cart, [])
#         if i == 4:
#             add_to_cart("noneExist")
#             assert_equals(cart, [])
#
#
# def test_update_inventory_file():
#     global inventory
#     inventory[1][0] = "Apple Pink Lady"
#     update_inventory_file()
#     load_inventory()
#     assert_equals("Apple Pink Lady", inventory[1][0])