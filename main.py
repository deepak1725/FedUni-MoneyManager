import tkinter as tk
from tkinter import *
from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import defaultdict
import matplotlib.pyplot as plt
from tkinter import messagebox
from moneymanager import MoneyManager

win = tk.Tk()
#Set window size here to '540 x 640'
win.geometry("540x640")

#Set the window title to 'FedUni Money Manager'
win.title('FedUni MoneyManager')

#The user number and associated variable
user_number_var = tk.StringVar()
#This is set as a default for ease of testing
user_number_var.set('123457')
user_number_entry = tk.Entry(win, textvariable=user_number_var)
user_number_entry.focus_set()

#The pin number entry and associated variables
pin_number_var = tk.StringVar()
#This is set as a default for ease of testing
pin_number_var.set('1234')

#Modify the following to display a series of * rather than the pin ie **** not 1234
user_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var, show="*")

#set the user file by default to an empty string
user_file = ''

# The balance label and associated variable
balance_var = StringVar(win)
balance_label = Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amountVar=StringVar(win)
amount_entry = tk.Entry(win, textvariable=amountVar)

# The transaction text widget holds text of the transactions
transaction_text_widget = tk.Text(win, height=25, width=65)

drop_downVar = tk.StringVar(win)
choices = { 'Rent','Bills','Food','Entertainment','Other'}
drop_downVar.set("Rent")

entry_type=tk.OptionMenu(win, drop_downVar, *choices)


# The money manager object we will work with
user = MoneyManager()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry():
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.''' 
    # Clear the pin number entry here
    pin_number_var.set('')


def clear_deposit_entry():
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.''' 
    # Clear the pin number entry here
    global amountVar
    amountVar.set('')


def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry.'''    
    # Limit to 4 chars in length
    pin_lenght = len(pin_number_var.get())
    if pin_lenght < 4:
    	user_pin_entry.insert(pin_lenght, event.widget["text"])
    # Set the new pin number on the pin_number_var

def log_in():
    '''Function to log in to the banking system using a known user number and PIN.'''
    global user
    global pin_number_var
    global user_file
    global user_num_entry
    user_num_entry = user_number_entry
    # Create the filename from the entered account number with '.txt' on the end
    filename = user_num_entry.get()+".txt"

    # Try to open the account file for reading
    # Open the account file for reading
    global user_file
    try:
        with open(filename, 'r') as user_file:
            # First line is account number
            user_number = read_line_from_user_file()
            user.user_number = user_number
            # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read 
            user_pin = read_line_from_user_file()
            assert( user_pin == pin_number_var.get())
            user.pin_number = user_pin
            # Read third and fourth lines (balance and interest rate) 
            user_balance = read_line_from_user_file()
            user_balance = float(user_balance)
            user.user_balance = user_balance
            user.transaction_list = []
            _ = read_line_from_user_file()
            while True:
                trans_type = read_line_from_user_file()
                trans_amount = read_line_from_user_file()
                if trans_amount!='' and trans_type!='':
                    user.transaction_list.append((trans_type, trans_amount))
                else: break
                    
    except AssertionError as a:
        messagebox.showinfo("Alert", "Invalid Pin. Please Try again.")
        return ""

    except (FileNotFoundError) as e:
        # Show error messagebox and & reset BankAccount object to default...
        messagebox.showinfo("Alert", "Invalid User. Please Try again.")
        user = MoneyManager()
        return ""

    finally:
        #  ...also clear PIN entry and change focus to account number entry
        clear_pin_entry()
        user_number_entry.focus_set()
    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
    remove_all_widgets()
    create_user_screen()

# ---------- Button Handlers for User Screen ----------
# ---------- Button Handlers for User Screen ----------

def save_and_log_out():
    '''Function  to overwrite the user file with the current state of
       the user object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global user
    global user_number_var
    global pin_number_var

    # Save the account with any new transactions
    
    # Reset the bank acount object
    user = MoneyManager()

    # Reset the account number and pin to blank
    user_number_var.set('')
    pin_number_var.set('')

    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()

def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       user's transaction list.'''
    global user    
    global amount_entry
    global balance_label
    global balance_var
    global amountVar
    # Try to increase the account balance and append the deposit to the account file
    
    # Get the cash amount to deposit. Note: We check legality inside account's deposit method

    # Deposit funds
    user = user.deposit_funds(amount_entry.get(), user)
    if user is None:
        return
            
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
    add_to_transactions(amount_entry.get(), "Deposit")
    # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
    #       contents, and finally configure back to state='disabled' so it cannot be user edited.

    # Change the balance label to reflect the new balance
    balance_var.set('Balance: $'+str(user.user_balance))
    user.save_to_file(user, "Deposit", amount_entry.get())
    # Clear the amount entry
    clear_deposit_entry()
    # Update the interest graph with our new balance

    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception

def perform_transaction():
    '''Function to add the entry the amount in the amount entry from the user balance and add an entry to the transaction list.'''
    global user    
    global amount_entry
    global balance_label
    global amountVar
    global drop_downVar
    global choices

    entry_type = drop_downVar.get()
    amount = amountVar.get()
    userObj = user.add_entry(entry_type, amount, user, choices)
    if userObj is None:
        return
    # Try to decrease the account balance and append the deposit to the account file
    
        # Get the cash amount to use. Note: We check legality inside account's withdraw_funds method

        # Get the type of entry that will be added ie rent etc
        
        # Withdraw funds from the balance      

        # Update the transaction widget with the new transaction by calling user.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.

        # Change the balance label to reflect the new balance
    balance_var.set('Balance: $'+str(user.user_balance))

    add_to_transactions(amount_entry.get(), entry_type)
    user.save_to_file(user, entry_type, amount)

    # Clear the amount entry
    clear_deposit_entry()

    # Catch and display any returned exception as a messagebox 'showerror'

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_user_file():
    '''Function to read a line from the users file but not the last newline character.
       Note: The user_file must be open to read from for this function to succeed.'''
    global user_file
    return user_file.readline()[0:-1]

def plot_spending_graph():
    '''Function to plot the user spending here.'''
    global user
    # YOUR CODE to generate the x and y lists here which will be plotted
    data = defaultdict(list)

    for txType, txAmount in user.transaction_list:
        if not data[txType]:
            data[txType].append(float(txAmount))
            continue
        data[txType].append(data[txType][0]+ float(txAmount))

    #Your code to display the graph on the screen here - do this last
    index = range(0, len(data.items()))
    plt.bar(index, list(map(sum, data.values())) )
    plt.xlabel('Spent Type', fontsize=8)
    plt.ylabel('Amount in $', fontsize=8)
    plt.xticks(index, data.keys(), fontsize=7, rotation=10)
    plt.title('Your Total Spendings', fontsize=8)

    plt.show()




    
# ---------- UI Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''    
    
    # ----- Row 0 -----

    # 'FedUni Money Manager' label here. Font size is 28.
    title1=Label(win,text="FedUni Money Manager" , justify="center",font=("Times New Roman", 28), width=22, height=4)
    title1.grid(row=0,column=0,padx=0,pady=8, columnspan=3)
    
    # ----- Row 1 -----
    # Acount Number / Pin label here
    label1=Label(win,text="User Number/Pin", width=22, height=6)
    label1.grid(row=1,column=0,padx=0,pady=0)

    # Account number entry here
    # ac_entry=Entry(win, textvariable=user_number_var)
    user_number_entry.grid(row=1,column=1,padx=0,pady=0, ipady=15, ipadx=0)
	
    # Account pin entry here
    # pin_entry=Entry(win, text="Pin", show="*", textvariable=pin_number_var)
    # user_pin_entry.config(textvariable=pin_number_var)
    user_pin_entry.grid(row=1,column=2,padx=0,pady=0, ipady=15)

    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button1 = Button(win,text=1, width=22, height=8)
    button1.bind("<Button-1>", handle_pin_button)

    button2 = Button(win,text=2, width=22, height=8)
    button2.bind("<Button-1>", handle_pin_button)

    button3 = Button(win,text=3, width=22, height=8)
    button3.bind("<Button-1>", handle_pin_button)

    button1.grid(row=2,column=0,padx=0,pady=0)
    button2.grid(row=2,column=1,padx=0,pady=0)
    button3.grid(row=2,column=2,padx=0,pady=0)
    

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button4 = Button(win,text=4, width=22, height=8)
    button4.bind("<Button-1>", handle_pin_button)

    button5 = Button(win,text=5, width=22, height=8)
    button5.bind("<Button-1>", handle_pin_button)

    button6 = Button(win,text=6, width=22, height=8)
    button6.bind("<Button-1>", handle_pin_button)

    button4.grid(row=3,column=0,padx=0,pady=0)
    button5.grid(row=3,column=1,padx=0,pady=0)
    button6.grid(row=3,column=2,padx=0,pady=0)
    

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button7 = Button(win,text=7, width=22, height=8)
    button7.bind("<Button-1>", handle_pin_button)

    button8 = Button(win,text=8, width=22, height=8)
    button8.bind("<Button-1>", handle_pin_button)

    button9 = Button(win,text=9, width=22, height=8)
    button9.bind("<Button-1>", handle_pin_button)

    button7.grid(row=4,column=0,padx=0,pady=0)
    button8.grid(row=4,column=1,padx=0,pady=0)
    button9.grid(row=4,column=2,padx=0,pady=0)
    

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    clear=Button(win,text="Cancel / Clear", width=22, height=8, bg="red", activebackground='red', command=clear_pin_entry)
    clear.grid(row=5,column=0,padx=0,pady=0)
    
    # Button 0 here
    button0=Button(win,text="0", width=22, height=8)
    button0.bind("<Button-1>", handle_pin_button)

    button0.grid(row=5,column=1,padx=0,pady=0)

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    login_button=Button(win,text="Log In", width=22, height=8, bg="green", activebackground='green', command=log_in)
    login_button.grid(row=5,column=2,padx=0,pady=0)


    # ----- Set column & row weights -----

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)


def create_user_screen():
    '''Function to create the user screen.'''
    global transaction_text_widget
    global balance_var
    global balance_label
    global user
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    label1 = Label(win, 
			 text="FedUni Money Manager",
			 height=3,
			 width="30",
			 font = "Verdana 24 bold italic")
    label1.grid(row=0, column=0, columnspan="5")


    # ----- Row 1 -----

    # Account number label here
    acc_no=Label(win,text=get_user_number(), justify = CENTER)
    acc_no.grid(row=1,column=0,padx=0,pady=0, ipadx=0,ipady=0)
	
    # Balance label here
    # balance=Label(win, text=get_user_balance())
    balance_label.grid(row=1,column=1,padx=0,pady=0, ipady=0, ipadx=0)

    # Log out button here
    logout=Button(win,text="Log Out", width=8, height=5, command=save_and_log_out)
    logout.grid(row=1,column=2,padx=0,pady=0, ipady=0, ipadx=20)

    # ----- Row 2 -----

    # Amount label here
    amount=Label(win,text="Amount ($): ")
    amount.grid(row=2,column=0,padx=0,pady=0, ipadx=0,ipady=0)
    # Amount entry here
    # amount_entry.config(height=5, width=20)
    amount_entry.grid(row=2, column=1, pady=0, padx=0, ipadx=0, ipady=0)
    balance_var.set('Balance: $'+str(user.user_balance))

    # Deposit button here
    deposit=Button(win,text="Deposit", width=8, height=5, command=perform_deposit)
    deposit.grid(row=2,column=2,padx=0,pady=0, ipady=0, ipadx=20)

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----
    # Entry type label here
    entry_type_label=Label(win,text="Entry Type: ")
    entry_type_label.grid(row=3,column=0,padx=0,pady=0, ipadx=0,ipady=0)

    entry_type.grid(row=3, column=1)

    # Add entry button here
    add_entry=Button(win,text="Add Entry", width=8, height=5, command=perform_transaction)
    add_entry.grid(row=3,column=2,padx=0,pady=0, ipady=0, ipadx=20)

    
    # ----- Row 4 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    text_scrollbar = Scrollbar(win)
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    # result_text = Text(win, height=25, width=65, state='disabled')
    transaction_text_widget.grid(row=4, column=0, pady=0, padx=0, ipadx=0, ipady=0, columnspan=3)
    
    text_scrollbar.grid(column=5, row=4)
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    transaction_text_widget.config(yscrollcommand = text_scrollbar.set)
    view_graph=Button(win,text="View Graph", width=8, height=2, command=plot_spending_graph)
    view_graph.grid(row=5,column=2,padx=0,pady=0, ipady=0, ipadx=0)

    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited
    update_transaction_box()    
    # Now add the scrollbar and set it to change with the yview of the text widget
    text_scrollbar.config(command= transaction_text_widget.yview)


    # ----- Row 5 - Graph -----

    # Call plot_interest_graph() here to display the graph

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 6 rows and 5 columns (numbered 0 through 4 not 1 through 5!)

def update_transaction_box():
    global user
    global transaction_text_widget
    transaction_text_widget.config(state='normal')
    type_index = float(0)
    for txtype, txamount in user.transaction_list:
        transaction_text_widget.insert(str(type_index), txamount+'\n')
        transaction_text_widget.insert(str(type_index), txtype+'\n')
    transaction_text_widget.config(state='disabled')

def add_to_transactions(txamount, txtype):
    transaction_text_widget.config(state='normal')
    type_index = float(0)
    transaction_text_widget.insert(str(type_index), txamount+'\n')
    transaction_text_widget.insert(str(type_index), txtype+'\n')
    transaction_text_widget.config(state='disabled')
    
def get_user_number():
    return "User Number: " + str(user.user_number)




# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
win.mainloop()
