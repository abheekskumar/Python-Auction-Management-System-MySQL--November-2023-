# Importing all libraries
import os
import random
import mysql.connector as msc
from mysql.connector import *

# GLOBAL VARIABLES
login_method, login_id, password = "", "", ""


# To convert tuples into string
def convert_tuple_to_string(a):
   res = ''.join(map(str, a))
   return str(res)


# To connect MySQL database
db = msc.connect(
   host='localhost',  # Enter host value
   user='root',  # Enter username
   password="student",  # Enter password
   db='auction',
)

cursor = db.cursor()


# ADMIN LOGIN
def admin_login():
   d1 = False
   d2 = False
   cursor.execute("SELECT * FROM admin_info")
   login_id = input("Enter your Login ID: ")
   password = input("Enter your Password: ")

   for t1 in cursor:
       if t1[1] == login_id:
           d1 = True
       if t1[2] == password:
           d2 = True

   if d1 and d2:
       print(
           "\n----------------------------------------------------------------------------------------------------------------------------\nAdmin login successful!\n")
       adm1, adm2, adm3, adm4, adm5 = "View Auction Items", "Modify Item Value", "View User Data", "Add Auction Items", "Quit"

       print("\n1.", adm1, "\n2.", adm2, "\n3.", adm3, "\n4.", adm4, "\n5.", adm5,
             "\n----------------------------------------------------------------------------------------------------------------------------")
       action = int(input("Which action would you like to perform(1,2,3,4,5): "))  # action chosen by admin
       print(
           "----------------------------------------------------------------------------------------------------------------------------")

       while True:
           if action == 1:
               cursor.execute("SELECT * FROM items")
               s2 = ("Item ID", "Items", "Starting Bid(In Thousand USD)")
               print(s2)
               for t1 in cursor:
                   print(t1)

           elif action == 2:
               edit = (input("Would you like to edit Name(n) or Starting Bid(s) of the item: "))
               if edit.lower() == "n":
                   item_old = input("Enter the old item name: ")
                   item_new = input("Enter the new item name: ")
                   name_update = "UPDATE items SET item_name = '" + item_new + "' WHERE item_name = '" + item_old + "'"
                   cursor.execute(name_update)
                   db.commit()
                   print("The item name has been updated.")

               elif edit.lower() == "s":
                   cost_old = float(input("Enter the starting bid of the old item (In Thousand USD): "))
                   cost_new = float(input("Enter the starting bid of the new item (In Thousand USD): "))
                   cost_update_tuple = "UPDATE items SET starting_bid = '", cost_new, "' WHERE starting_bid = '", cost_old, "'"
                   cost_update = convert_tuple_to_string(cost_update_tuple)
                   cursor.execute(cost_update)
                   db.commit()
                   print("The starting bid has been updated.")

               else:
                   print("Invalid Input.")


           elif action == 3:
               cursor.execute("SELECT * FROM user_info")
               t2 = ("User ID", "Login ID", "Password", "Auction_no")
               print(t2)
               for t1 in cursor:
                   print(t1)

           elif action == 4:
               itemid_new = input("Enter the new Item ID:")
               item_new = input("Enter the new Item Name: ")
               cost_new = float(input("Enter the starting bid of the new item(In Thousand USD): "))
               print(item_new, "worth", cost_new, "thousand USD has been added to the auction list!")
               sql = "INSERT INTO items (item_id,item_name, starting_bid) VALUES (%s, %s, %s)"
               val = (itemid_new, item_new, cost_new)
               cursor.execute(sql, val)
               db.commit()

           elif action == 5:
               print("Thank you!")
               exit()

           else:
               print("Enter a valid option")
               exit()
           break

   else:
       print("Invalid Credentials")
       exit()

   print(
       "----------------------------------------------------------------------------------------------------------------------------")
   exit()


# Login Screen
def login_screen():
   # os.system('clear')

   print(
       "\n\n\n-------------------------------------------Welcome to the auction management system!----------------------------------------\n\n\n")
   login_method = input("Enter your login mode(admin/user): ")

   if login_method.lower() == "admin":
       admin_login()


   elif login_method.lower() == "user":

       s1 = False
       s2 = False
       cursor.execute("SELECT * FROM user_info")
       login_id = input("Enter your Login ID: ")
       password = input("Enter your Password: ")
       for t1 in cursor:
           if t1[1] == login_id:
               s1 = True
           if t1[2] == password:
               s2 = True
       if s1 and s2:
           auctionSystem()
       else:
           print(
               "Invalid Credentials. \n----------------------------------------------------------------------------------------------------------------------------")
           exit()

   else:
       print("Enter a valid login mode")
       exit()


# Assign all variables to the items here Using SQL

cursor.execute("SELECT * FROM items")
itemid_list = []
for t1 in cursor:
   itemid_list.append(t1[0])
cursor.execute("SELECT * FROM items")
itemname_list = []
for t1 in cursor:
   itemname_list.append(t1[1])
cursor.execute("SELECT * FROM items")
costno_list = []
for t1 in cursor:
   costno_list.append(t1[2])



# Main Screen where auction will happen
def auctionSystem():
   print(
       "----------------------------------------------------------------------------------------------------------------------------")
   cursor.execute("SELECT * FROM items")
   s2 = ("Item ID.", "Items", "Starting Bid(In Thousands USD)")
   print(s2)
   for t1 in cursor:
       print(t1)
   chosen_item_id = int(input("Please enter the item you would like to bid on (Item ID.): "))  # Item chosen by user
   index_value = 0
   for i in itemid_list:
       index_value +=1
       if i == chosen_item_id:
           chosen_costno = costno_list[index_value-1]
           chosen_itemname = itemname_list[index_value-1]
   print(        "----------------------------------------------------------------------------------------------------------------------------")

   # --------------------------------------------------------------------------------------------------------------------------------
   # Starting the auction

   # Statement
   if True:
       try:
           print("The starting bid for", chosen_itemname, "is(In Thousand USD):",chosen_costno)
       except UnboundLocalError:
           print("Error! Item ID is not in the auction.")
           exit()
       # Bid 1
       bid1 = float(input("Enter your bid: "))
       counter1 = bid1 + random.randint(0, 10)

       if bid1 > chosen_costno:
           print("The counter bid is:", counter1)

           play1 = input("Would you like to continue bidding(yes/no): ")  # Bid 2
           if play1.lower() == "yes":
               bid2 = float(input("Enter your counter bid: "))
               counter2 = bid2 + random.randint(0, 10)

               if bid2 > counter1:
                   print("The counter bid is: ", counter2)

                   play2 = input("Would you like to continue bidding(yes/no): ")  # Bid 3
                   if play2.lower() == "yes":
                       bid3 = float(input("Enter your counter bid: "))
                       counter3 = bid3 + random.randint(0, 10)

                       if bid3 > counter2:
                           print("The counter bid is: ", counter3)

                           play3 = input("Would you like to continue bidding(yes/no): ")  # Bid 4
                           if play3.lower() == "yes":
                               bid4 = float(input("Enter your counter bid: "))
                               counter4 = bid4 + random.randint(0, 10)

                               if bid4 > counter3:
                                   print("The counter bid is: ", counter4)

                                   play4 = input("Would you like to continue bidding(yes/no): ")  # Bid 5
                                   if play4.lower() == "yes":
                                       bid5 = float(input("Enter your counter bid: "))

                                       if bid5 > counter4:
                                           print(
                                               "There are no other counter bids! You won the item.\n----------------------------------------------------------------------------------------------------------------------------")
                                           sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
                                           cursor.execute(sql1)
                                           db.commit()
                                       elif bid5 < counter4:
                                           print("Your bid cannot be lower than the previous bid. You lost this item.")
                                           sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
                                           cursor.execute(sql1)
                                           db.commit()
                                       else:
                                           print("Please bid correctly...")

                                   elif play4.lower() == "no":
                                       print("Thank you for bidding! You won this item.")
                                       sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
                                       cursor.execute(sql1)
                                       db.commit()
                                   else:
                                       print("Please answer as 'yes' or 'no'")


                               elif bid4 < counter3:
                                   print("Your bid cannot be lower than the previous bid. You lost this item.")
                                   sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
                                   cursor.execute(sql1)
                                   db.commit()
                               else:
                                   print("Please bid correctly...")

                           elif play3.lower() == "n":
                               print("Thank you for bidding! You won this item.")
                               sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
                               cursor.execute(sql1)
                               db.commit()
                           else:
                               print("Please answer as 'yes' or 'no'")


                       elif bid3 < counter2:
                           print("Your bid cannot be lower than the previous bid. You lost this item.")
                           sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
                           cursor.execute(sql1)
                           db.commit()
                       else:
                           print("Please bid correctly...")

                   elif play2.lower() == "no":
                       print("Thank you for bidding! You won this item.")
                       sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
                       cursor.execute(sql1)
                       db.commit()
                   else:
                       print("Please answer as 'yes' or 'no'")

               elif bid2 < counter1:
                   print("Your bid cannot be lower than the previous bid. You lost this item.")
                   sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
                   cursor.execute(sql1)
                   db.commit()
               else:
                   print("Please bid correctly...")

           elif play1.lower() == "no":
               print("Thank you for bidding! You won this item.")
               sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
               cursor.execute(sql1)
               db.commit()
           else:
               print("Please answer as 'yes' or 'no'")

       elif bid1 < chosen_costno:
           print("Your bid cannot be lower than the starting bid. You lost this item.")
           sql1 = "DELETE FROM items WHERE item_name = '" + chosen_itemname + "'"
           cursor.execute(sql1)
           db.commit()
       else:
           print("Please bid correctly...")


# -----------------------------------------------------------------------------------------------------------------------------

login_screen()
db.close()
