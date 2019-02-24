from tkinter import messagebox
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import sys

class MoneyManager():

       
    def __init__(self):
        '''Constructor to set username to '', pin_number to an empty string,
           balance to 0.0, and transaction_list to an empty list.'''
        self.balance = 0.0
        self.transaction_list = []
        self.pin_number = ''
        
    def add_entry(self, entry_type, amount, user, valid_choices):
        '''Function to add and entry an amount to the tool. Raises an
        exception if it receives a value for amount that cannot be cast to float. Raises an exception
        if the entry_type is not valid - i.e. not food, rent, bills, entertainment or other'''
        try:
            amount = float(amount)
            if not entry_type in valid_choices:
                raise AssertionError("Invalid Choice")
            if user.user_balance < amount:
                raise RuntimeError("Invalid Amount")
            user.user_balance -= amount
            user.transaction_list.append((entry_type, str(amount)))
            return user 
        
        except ValueError:
            messagebox.showinfo("Transaction Error", "Invalid Amount. Please Try again.")
        
        except RuntimeError:
            messagebox.showinfo("Transaction Error", "Invalid Amount. You dont have much funds. Please Try again.")
        except:
            messagebox.showinfo("Transaction Error", "Invalid Choice. Please Try again.")
        
            

    def deposit_funds(self, amount, user):
        '''Function to deposit an amount to the user balance. Raises an
           exception if it receives a value that cannot be cast to float. '''
        try:
            amount = float(amount)
        except:
            messagebox.showinfo("Transaction Error", "Invalid Amount. Please Try again.")
        user.user_balance += amount
        user.transaction_list.append(("Deposit", str(amount)))
        return user 


        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or the entry type - food etc - on
           the first line, and then the amount deposited or entry amount on the next line.'''
        return self.transaction_list.pop()


    def save_to_file(self, user=None,txType=None, txAmount=None):
        '''Function to overwrite the user text file with the current user
           details. user number, pin number, and balance (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        filename = user.user_number +'.txt'
        self.write_to_file(filename, user, txType, txAmount)
    
    def write_to_file(self, file_path, user, txType, txAmount):
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open(file_path) as old_file:
                for index, line in enumerate(old_file):
                    if index==2:
                        new_file.write(str(user.user_balance))
                        new_file.write('\n')
                    else:
                        new_file.write(line)
                new_file.write(txType+'\n')
                new_file.write(str(txAmount+'\n'))
        remove(file_path)
        move(abs_path, file_path)



        



        
