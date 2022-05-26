# This file is for user intraction like order place , login, register , order history and profile update
import re
from file_handle import file_handle as fh  # file handling module

user_data = fh.file_handle('json_files/users.json') # user object created
restuarents_data = fh.file_handle('json_files/items.json') # restuarents object created
orders_history_data = fh.file_handle('json_files/order_history.json') # order history object created

# This function will check validation for different fields.
def details_validation(key):
    if key == "Phone" : # For Phone number validation
        number = input("Enter phone number : ")
        while True:
            try:
                phone_number = int(number)
                if len(number) == 10:
                    return phone_number
                else:
                    print("Enter 10 digit number")
                    number = input("Enter phone number : ")
                    
            except:
                print("Check your number and enter again")
                number = input("Enter phone number : ")
    elif  key == "Email": # For email validation
        email = input("Enter Email : ")
        while not re.fullmatch("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}",email):
            print("Enter proper Email")
            email = input("Enter Email : ")
        return email
    
    elif key == "Password": # For password validation
        password = input("Enter Password : ")
        while not re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$",password):
            print("Password should contain one upper case, one lower case, one special charecter, one numeric digit and minimum 8 charecters.")
            print("ex : Arun19@")
            password = input("Enter password : ")
        return password

    else:
        return input("Enter {} : ".format(key))


# This will give user to select the options
while True:
    print("1.Login  2.Register")
    option_val = input("Select One option and click Enter : ")
    # Options selected 
    if option_val == "1": # If login clicks
        print("Enter email and password.")
        email = input("Enter Email : ")
        user_fields = user_data.search_user_value_data("Email",email)
        if user_fields: # If user find with entered Email
            password = input("Enter Password : ")
            if user_data.search_user_value_data("Password",password): #If Email find then Check with password
                print("\nLogin Sucess\nPlease Select Your Option\n")
                while True: # Loged in user will see this options to select
                    print("1.Edit Profile  2.Place New Order  3.Order History  4.Logout")
                    option_selc = input("Select Option : ")
                    if option_selc == "1": # For edit profile
                        while True:
                            print("Select field to edit : ")
                            field_index = ["1","2","3","4","5"]
                            field_keys = ["Name","Phone","Email","Address","Password"] # For Profile editing options
                            print("1.Name  2.Phone  3.Email  4.Address  5.Password  6.Back")
                            field_option = input("Enter Option Nunmber : ")
                            if field_option in field_index: # if Match the entered value with to update
                                key = [field for field in user_fields]
                                values = user_fields[key[0]]
                                values[field_keys[int(field_option)-1]] = details_validation(field_keys[int(field_option)-1])
                                all_users = user_data.read_data()
                                all_users[key[0]] = values
                                user_data.write_data(all_users)
                                print("\n{} Updated Sucessfully\n".format(field_keys[int(field_option)-1]))
                                break
                            elif field_option == "6": # Back to menu
                                break
                            else: # Default message if other than options selcted from above
                                print("\nEnter valid number\n")
                    elif option_selc == "2": # For placing new order
                        all_items = restuarents_data.read_data() # All items data from menu
                        if all_items: # Checks if items avilable
                            item_count = 0
                            Items_print = ""
                            for item_id,item_field in all_items.items(): # Check if stock avilable then display that item
                                if item_field["Stock"] > 0:
                                    item_count += 1
                                    Items_print += str(item_count)+". "+item_field["Name"]+" ("+str(item_field["Quantity"])+" "+item_field["Unit Type (ex: ml or piece or gm)"]+") [INR "+str(item_field["Price"])+"]\n"
                            if Items_print != "": # If items not empty
                                print(Items_print)
                                while True:
                                    select_items = []
                                    select_items = input("Enter Item numbers seperated by comma : ") # Takes order in comma seprated string
                                    try:
                                        # This try will check weather entered values are present in items or not
                                        select_items = list(map(int,select_items.split(","))) 
                                        loop_count = 0
                                        new_order_items = []
                                        for item_id,item_values in all_items.items():
                                            if item_values["Stock"] > 0:
                                                loop_count+=1
                                                if loop_count in select_items:
                                                    all_items[item_id]["Stock"]-= 1
                                                    restuarents_data.write_data(all_items)
                                                    item_values["Item_id"] = item_id
                                                    new_order_items.append(item_values)
                                                    select_items.remove(loop_count)
                                        if len(select_items) > 0: # If entred values are other than meni items 
                                            print("\nEnter item numbers from Menu only\n")
                                            new_order_items = []
                                        else: # If entred values are correct
                                            user_id = [x for x,y in user_fields.items()]
                                            user_orders = orders_history_data.search_data(user_id[0]) # Check if user have order history
                                            all_order_history = orders_history_data.read_data()
                                            if user_orders: # If user order history present then append new orders to old orders
                                                new_updated_user_history = all_order_history[user_id[0]] # All order history of user
                                                [new_updated_user_history.append(x) for x in new_order_items] # Appending all new orders to order history
                                                all_order_history[user_id[0]] = new_updated_user_history
                                                selected_itmes = ""
                                                for item_field in new_order_items: # Check if stock avilable then display that item
                                                        selected_itmes += item_field["Name"]+" ("+str(item_field["Quantity"])+" "+item_field["Unit Type (ex: ml or piece or gm)"]+") [INR "+str(item_field["Price"])+"]\n"
                                                print("\nSelected Items are : \n{}".format(selected_itmes))
                                                order_cnfrm = input("Place order 1.Yes 2.No : ")
                                                while True: # For order confirmation
                                                    if order_cnfrm == "1":
                                                        orders_history_data.write_data(all_order_history)
                                                        print("\nSuccessfull !!! Your order have been placed. Thank You\n")
                                                        break
                                                    elif order_cnfrm == "2":
                                                        print("\nYour order have been  cancled\n")
                                                        break
                                                    else:
                                                        print("\nPlease enter option numbers only\n")
                                            else: # If order history is not there then new data is created
                                                all_order_history = {**all_order_history,**{user_id[0]:new_order_items}}
                                                print("\nSelected Items are : \n{}".format(selected_itmes))
                                                order_cnfrm = input("Place order 1.Yes 2.No : ")
                                                while True: # For order confirmation
                                                    if order_cnfrm == "1":
                                                        orders_history_data.write_data(all_order_history)
                                                        print("\nSuccessfull !!! Your order have been placed. Thank You\n")
                                                        break
                                                    elif order_cnfrm == "2":
                                                        print("\nYour order have been  cancled\n")
                                                        break
                                                    else:
                                                        print("\nPlease enter option numbers only\n")
                                            break
                                    except:
                                        print("\nEnter Proper Item numbers\n")
                            else:
                                print("No items in menu.")
                        else:
                            print("Items Menu is Empty.")
                    elif option_selc == "3": # For displaying all order History
                        user_id = [x for x,y in user_fields.items()]
                        old_orlders = orders_history_data.search_data(user_id[0])
                        if old_orlders: # Check if order history presents
                            for x in old_orlders:
                                show_fields = ["Name","Price","Discount","Quantity"]
                                for fileds in show_fields:
                                    print("Item {} : {}".format(fileds,x[fileds]))
                                print("\n")
                        else:
                            print("\nNo order history found\n")
                    elif option_selc == "4": # For logout
                        break
                    else: # Default message if wrong input given
                        print("Please Select Proper Option")
            else:
                print("\nPassword Incorrect Please try again\n")
        else: # If user not find with entered Email
            print("No Email Match.")

    elif option_val == "2": # Register new user
        reg_details = ["Name","Phone","Email","Address","Password"] # User input fields
        print("Enter following detials.")
        values = [details_validation(val) for val in reg_details]
        new_user = {key : values[reg_details.index(key)] for key in reg_details}
        users = user_data.read_data()
        if users: # Check if any users exists then increment the user id 
            first_value = next(iter(users.values()))
            if first_value["custom_id"]:
                new_user['custom_id'] = int(first_value["custom_id"]) + 1
            else:
                new_user['custom_id'] = 1
        else: # If user not found then user id will be 1
            new_user['custom_id'] = 1
        user_id = "User"+str(new_user['custom_id'])
        new_user = {user_id:new_user}
        user_data.write_data({**new_user,**users})
        print("Registration Succesfull")
    
    else: # Default Message
        print("Please Select Proper Option")

