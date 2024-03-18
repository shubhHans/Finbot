import tkinter as tk
from tkinter import scrolledtext
import mysql.connector as c

connection = c.connect(host='localhost', user='root', passwd='W7301@jqir#', database='finbot')
cursor = connection.cursor()

# Function for keyword matching
def keyfind(user_input):
    keyword_list = ["house", "vacation", "education", "longterm", "shortterm", "food", "utilities", "tuitionfees",
                    "entertainment", "personal"]

    words = user_input.lower().split()
    for word in words:
        if word in keyword_list:
            return word  # Return the matched keyword
    return None  # Return None if no keyword is found

# Function to connect to the database
def connect_to_db():
    try:
        return c.connect(host='localhost', user='root', passwd='W7301@jqir#', database='finbot')
    except c.Error as err:
        return f"Database Connection Error: {err}"

# Function to update savings information in the database
def update_savings_in_db(keyword, savings):
    con = connect_to_db()
    if isinstance(con, str):
        return con  # Return error message if connection failed
    cursor = con.cursor()
    try:
        update_query = f"UPDATE saving SET response ='{savings}' WHERE keyword='{keyword}'"
        cursor.execute(update_query)
        con.commit()
        return f"According to your income, you need to save {savings} for {keyword}."
    except c.Error as err:
        return f"Database Operation Error: {err}"
    finally:
        con.close()

# Function to update budget information in the database
def update_budget(keyword, budget):
    con = connect_to_db()
    if isinstance(con, str):
        return con  # Return error message if connection failed
    cursor = con.cursor()
    try:
        update_query = f"UPDATE budget SET response ='{budget}' WHERE keyword_budget='{keyword}'"
        cursor.execute(update_query)
        con.commit()
        return f"According to your income, you need to budget {budget} for {keyword}."
    except c.Error as err:
        return f"Database Operation Error: {err}"
    finally:
        con.close()

# Function to update emergency fund information in the database
def update_emergency_fund(emergency_fund):
    con = connect_to_db()
    if isinstance(con, str):
        return con  # Return error message if connection failed
    cursor = con.cursor()
    try:
        update_query = f"UPDATE emergency SET response ='{emergency_fund}' WHERE keyword_emergency='emergency'"
        cursor.execute(update_query)
        con.commit()
        return f"According to your income, you need to save {emergency_fund} for emergency fund."
    except c.Error as err:
        return f"Database Operation Error: {err}"
    finally:
        con.close()

# Function to calculate savings based on income
def calculate_savings(income, percentage_factor):
    percentage = (income * 0.30) * percentage_factor
    return round(percentage, 2)

# Function to calculate vacation savings
def calculate_vacation(income):
    percentage_factor = 0.10  # Adjust as needed for vacation
    return calculate_savings(income, percentage_factor)

# Function to calculate house savings
def calculate_house(income):
    percentage_factor = 0.20  # Adjust as needed for house
    return calculate_savings(income, percentage_factor)

# Function to calculate budget for food
def calculate_bfood(income):
    percentage = (income * 0.60) * 0.25  # Adjust the percentage calculation as needed
    return round(percentage, 2)

# Function to calculate budget for tuition fees
def calculate_btut(income):
    percentage = (income * 0.60) * 0.30  # Adjust the percentage calculation as needed
    return round(percentage, 2)

# Function to calculate budget for utilities
def calculate_buti(income):
    percentage = (income * 0.60) * 0.20  # Adjust the percentage calculation as needed
    return round(percentage, 2)

# Function to calculate budget for personal activities
def calculate_bpact(income):
    percentage = (income * 0.60) * 0.10  # Adjust the percentage calculation as needed
    return round(percentage, 2)

# Function to calculate budget for entertainment
def calculate_bent(income):
    percentage = (income * 0.60) * 0.15  # Adjust the percentage calculation as needed
    return round(percentage, 2)

# Function to calculate emergency fund based on income
def calculate_emergency(income):
    percentage = (income * 0.07)  # Adjust the percentage calculation as needed
    return round(percentage, 2)

# Process user input for budgeting
def process_budget_input(user_input, income):
    keyword_budget = keyfind(user_input)
    if keyword_budget == "food":
        budget = calculate_bfood(income)
        response = update_budget(keyword_budget, budget) if isinstance(budget, (int, float)) else budget
        chat_history.insert(tk.END, response + "\n")
    elif keyword_budget == "tuitionfees":
        budget = calculate_btut(income)
        response = update_budget(keyword_budget, budget) if isinstance(budget, (int, float)) else budget
        chat_history.insert(tk.END, response + "\n")
    elif keyword_budget == "utilities":
        budget = calculate_buti(income)
        response = update_budget(keyword_budget, budget) if isinstance(budget, (int, float)) else budget
        chat_history.insert(tk.END, response + "\n")
    elif keyword_budget == "entertainment":
        budget = calculate_bent(income)
        response = update_budget(keyword_budget, budget) if isinstance(budget, (int, float)) else budget
        chat_history.insert(tk.END, response + "\n")
    elif keyword_budget == "personal ":
        budget = calculate_bpact(income)
        response = update_budget(keyword_budget, budget) if isinstance(budget, (int, float)) else budget
        chat_history.insert(tk.END, response + "\n")
    else:
        chat_history.insert(tk.END, "Invalid budget category. Please enter a valid category.\n")

# Process user input from the chat interface
def process_user_input(user_input):
    if user_input == "savings":
        chat_history.insert(tk.END, "You selected Savings. \nWhat are you trying to save for?\n")
        user_state["awaiting_keyword"] = True

    elif user_input == "investment":
        chat_history.insert(tk.END, "You selected Investments. \nSelect an option by typing the corresponding number:\n"
                                     "1. Long Term\n"
                                     "2. Short Term\n")
        user_state["awaiting_investment_type"] = True

    elif user_input == "budgeting":
        chat_history.insert(tk.END, "You selected Budgeting. \nWhich budgeting category do you want to calculate?\n"
                                     "1. Food\n"
                                     "2. Utilities\n"
                                     "3. Entertainment\n"
                                     "4. Personal Activities\n")
        user_state["awaiting_budget_category"] = True

    elif user_input == "emergency funds":
        chat_history.insert(tk.END, "You selected Emergency Fund. Please enter your monthly income:\n")
        user_state["awaiting_emergency_input"] = True

    elif user_state.get("awaiting_keyword", False):
        keyword = keyfind(user_input)
        if keyword:
            chat_history.insert(tk.END, f"Great! You're saving for {keyword}. Please enter your monthly income:\n")
            user_state["current_keyword"] = keyword
            user_state["awaiting_keyword"] = False
        else:
            chat_history.insert(tk.END, "Invalid savings goal. Please enter a valid goal.\n")

    elif user_state.get("awaiting_investment_type", False):
        keyword_inv = keyfind(user_input)
        if keyword_inv:
            chat_history.insert(tk.END, f"Great! You're saving for {keyword_inv}. Please enter your monthly income:\n")
            user_state["current_investment_type"] = keyword_inv
            user_state["awaiting_investment_type"] = False
        else:
            chat_history.insert(tk.END, "Invalid investment goal. Please enter a valid goal.\n")

    elif user_state.get("awaiting_budget_category", False):
        budget_category = keyfind(user_input)
        if budget_category:
            chat_history.insert(tk.END, f"Great! You're budgeting for {budget_category}. Please enter your monthly income:\n")
            user_state["current_budget_category"] = budget_category
            user_state["awaiting_budget_category"] = False
        else:
            chat_history.insert(tk.END, "Invalid budget category. Please enter a valid category.\n")

    elif user_state.get("awaiting_emergency_input", False) and user_input.isdigit():
        income = int(user_input)
        emergency_fund = calculate_emergency(income)
        response = update_emergency_fund(emergency_fund) if isinstance(emergency_fund, (int, float)) else emergency_fund
        chat_history.insert(tk.END, response + "\n")
        user_state.clear()  # Reset the state after processing
        chat_history.insert(tk.END, menu_options)

    elif user_state.get("current_keyword") and user_input.isdigit():
        keyword = user_state["current_keyword"]
        if keyword == "vacation":
            income = int(user_input)
            savings = calculate_vacation(income)
            response = update_savings_in_db(keyword, savings) if isinstance(savings, (int, float)) else savings
            chat_history.insert(tk.END, response + "\n")
        elif keyword == "house":
            income = int(user_input)
            savings = calculate_house(income)
            response = update_savings_in_db(keyword, savings) if isinstance(savings, (int, float)) else savings
            chat_history.insert(tk.END, response + "\n")
        elif keyword == "education":
            cursor.execute("SELECT response FROM saving WHERE keyword='education'")
            data = cursor.fetchone()
            if data:
                chat_history.insert(tk.END, data[0] + "\n")
        else:
            chat_history.insert(tk.END, "Error: Unsupported goal.\n")
        user_state.clear()  # Reset the state after processing
        chat_history.insert(tk.END, menu_options)

    elif user_state.get("current_investment_type") and user_input.isdigit():
        keyword_inv = user_state["current_investment_type"]
        if keyword_inv == "longterm":
            cursor.execute("SELECT response FROM investment WHERE keyword_investment='longterm'")
            data = cursor.fetchone()
            chat_history.insert(tk.END, data[0] + "\n")
        elif keyword_inv == "shortterm":
            cursor.execute("SELECT response FROM investment WHERE keyword_investment='shortterm'")
            data = cursor.fetchone()
            if data:
                chat_history.insert(tk.END, data[0] + "\n")
        else:
            chat_history.insert(tk.END, "Error: Unsupported goal.\n")
        user_state.clear()  # Reset the state after processing
        chat_history.insert(tk.END, menu_options)

    elif user_state.get("current_budget_category") and user_input.isdigit():
        budget_category = user_state["current_budget_category"]
        income = int(user_input)
        process_budget_input(budget_category, income)
        user_state.clear()  # Reset the state after processing
        chat_history.insert(tk.END, menu_options)
    
    chat_history.see(tk.END)

# Send message to the chat
def send_message(event=None):
    user_input = user_input_entry.get()
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    process_user_input(user_input)
    user_input_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Financial Advisor Chatbot")
root.config(bg="light blue")

Font_tuple = ("BPreplay ", 12,"bold") 

# Chat history area
chat_history = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled')
chat_history.pack(padx=10, pady=10)
chat_history.config(state='normal')
chat_history.config(font=Font_tuple)

# User input field
user_input_entry = tk.Entry(root, width=50)
user_input_entry.pack(padx=10, pady=5)
user_input_entry.bind("<Return>", send_message)
user_input_entry.config(font=Font_tuple)


# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)




# Display menu options in chat history
menu_options = "Select an option by typing the corresponding number:\n1. Savings\n2. Investments\n3. Budgeting\n4. Emergency Fund\n"
chat_history.insert(tk.END,"Bot: "+ menu_options+"\n")
chat_history.see(tk.END)



# Store user state (current keyword)
user_state = {}

# Start the GUI event loop
root.mainloop()