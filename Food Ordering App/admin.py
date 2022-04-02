# file handling module
from file_handle import file_handle as fh  

# Restuarent object created
restuarent_items = fh.file_handle('json_files/items.json') 

# This function will check weather entered vaalue is numeric or not 
def numbered_input(key_value):
    numberd_values = ["Quantity","Price","Discount","Stock"]
    entered_value = input("Enter {} : ".format(key_value))
    if key_value in numberd_values:
        while True:
            try:
                converted_int = int(entered_value)
                return converted_int
            except:
                print("Enter Only number values")
                entered_value = input("Enter {} : ".format(key_value))
    else:
        return entered_value

# This will give admin to select the options
while True:
    print("1.View Items  2.Edit Item  3.Delete Item  4.Add New Item  5.Delete All Items  6.Exit")
    option_val = input("Select One option and click Enter : ")

    # View Items in Restuarent
    if option_val == "1":
        items = restuarent_items.read_data()
        if items:
            for key,item_data in items.items():
                print("\n")
                print("Item Id : {} \n".format(key))
                for name,value in item_data.items():
                    print("{} : {}".format(name,value))
            print("\n")
        else:
            print("\nNo Items In restuarent\n")

    # Edit Items in Restuarent
    elif option_val == "2":
        serach_key = input("Enter Item Id : ")
        serach_data = restuarent_items.search_data(serach_key)
        if serach_data:
            keys_list = [x for x in list(serach_data.keys())][:-1]
            keys = [str(list(serach_data.keys()).index(x)+1)+". "+x for x in keys_list]
            numberd_values = ["Quantity","Price","Discount","Stock"]
            [print(x, end="  ") for x in keys]
            edit_option = int(input("\nEnter number that you want to edit : "))
            edit_option -= 1
            # new_spec_value = input("Enter new {} : ".format(keys_list[edit_option]))
            serach_data[keys_list[edit_option]] = numbered_input(keys_list[edit_option])
            items = restuarent_items.read_data()
            items[serach_key] = serach_data
            restuarent_items.write_data(items)
            print("\nItem updated successfully\n")
        else:
            print("\nNo Item Found With That Id.\n")

    # Delete Items in Restuarent
    elif option_val == "3":
        delete_key = input("Enter Item Id : ")
        delete_status = restuarent_items.delete_data(delete_key)
        if delete_status:
            print("\nItem deleted Succesfully \n")
        else:
            print("\nNo item found with that Id. \n")

    # Add New Item to Restuarent
    elif option_val == "4":
        item_keys = ["Name","Quantity","Price","Discount","Stock","Unit Type (ex: ml or piece or gm)"]
        numberd_values = ["Quantity","Price","Discount","Stock"]
        values = [numbered_input(x) for x in item_keys]

        new_item = {key : values[item_keys.index(key)] for key in item_keys}
        items = restuarent_items.read_data()

        if items:
            first_value = next(iter(items.values()))
            if first_value["custom_id"]:
                new_item['custom_id'] = int(first_value["custom_id"]) + 1
            else:
                new_item['custom_id'] = 1
        else:
            new_item['custom_id'] = 1
        item_id = "Item"+str(new_item['custom_id'])
        new_item = {item_id:new_item}
        restuarent_items.write_data({**new_item,**items})
        print("\nItem Added Sucessfully. \n")

    # Remove all items from restuarent
    elif option_val == "5":
        restuarent_items.write_data({})
        print("All items deleted from restuarent.")

    # Exit from Restuarent
    elif option_val == "6":
        break

    # Default Message
    else:
        print("Please Select Proper Option")