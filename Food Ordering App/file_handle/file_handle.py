# This package is for file handling 

# Modules to import
import json


# File Handling class
class file_handle:

    # Constructor
    def __init__(self,file_path):
        self.file_path = file_path

    # Read the file data from file and return the data
    def read_data(self):
        readed_data = open(self.file_path, "r+")
        export_data = json.load(readed_data)
        readed_data.close()
        return export_data

    # create or update the data to file
    def write_data(self,data):
        opened_file = open(self.file_path, "w+")
        export_data = json.dump(data, opened_file)
        opened_file.close()
        return export_data

    # Delete the file data 
    def delete_data(self,key):
        readed_data = open(self.file_path, "r+")
        all_data = json.load(readed_data)
        readed_data.close()
        if key in all_data:
            del all_data[key]
            opened_file = open(self.file_path, "w+")
            json.dump(all_data, opened_file)
            opened_file.close()
            return 1
        return 0

    # Search data in the file 
    def search_data(self,serach_word):
        readed_data = open (self.file_path, "r+")
        all_data = json.load(readed_data)
        readed_data.close()
        if serach_word in all_data:
            return all_data[serach_word]
        return 0

    # Search in key pair values in user information data in the file 
    def search_user_value_data(self,serach_key,search_word):
        readed_data = open (self.file_path, "r+")
        all_data = json.load(readed_data)
        readed_data.close()
        # print(all_data.values())
        for key,value in all_data.items():
            if value[serach_key] == search_word:
                return {key:value}
        return 0
