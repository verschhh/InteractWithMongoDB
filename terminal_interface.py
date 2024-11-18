import pymongo
import os

db_name = "CA2"
col = None
current_col = None
db = None

# CONNECT TO THE DB
def connect_to_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    return db

# LIST EXISTING COLLECTIONS
def display_collection(client):
    collections = client.list_collection_names()
    if not collections:
        print("No collections found please restart the program.")
        exit()
    else:
        for collection in collections:
            print("- " + collection)
    return

# DISPLAY DATA FROM COLLECTION
def display_collection_data(collection):
    for data in collection.find({}, {"_id": 0, "region": {"name": 1}, "poverty_indicator": {"label": 1}}):
        for key, value in data.items():
            print(f"{key}: {value}")
        print("\n")
    input("Press any key to continue...")
    option_menu()

# ADD DATA TO COLLECTION
def add_document_to_col(collection):
    data = {}
    for key in collection.find_one():
        if key == "_id":
            continue
        value = input(f"Enter {key}: ")
        data[key] = value
    collection.insert_one(data)
    print("Data added successfully")
    input("Press any key to continue...")
    option_menu()
    return

# UPDATE DOCUMENT IN COLLECTION
def update_document_to_col(collection):
    filter_key = input("Enter the key to filter (e.g., name): ")
    filter_value = input(f"Enter the value of {filter_key} to filter by: ")
    _filter = {filter_key: filter_value}
    data = {}
    for key in collection.find_one():
        if key == "_id":
            continue
        value = input(f"Enter new value for {key} (leave blank to skip): ")
        if value:
            data[key] = value
    if data:
        collection.update_one(_filter, {"$set": data})
        print("Data updated successfully")
    else:
        print("No data provided to update.")
    input("Press any key to continue...")
    option_menu()

# DELETE A DOCUMENT FROM COLLECTION
def delete_document_from_col(collection):
    filter_key = input("Enter the key to filter (e.g., name): ")
    filter_value = input(f"Enter the value of {filter_key} to filter by: ")
    _filter = {filter_key: filter_value}
    confirmation = input(f"Are you sure you want to delete the document(s) matching {_filter}? (yes/no): ").strip().lower()
    if confirmation == "yes":
        result = collection.delete_one(_filter)
        if result.deleted_count > 0:
            print("Data deleted successfully.")
        else:
            print("No document found matching the provided filter.")
    else:
        print("Deletion canceled.")
    input("Press any key to continue...")
    option_menu()

#FIND AN EXISTING DOCUMENT FROM COLLECTION
def find_document_from_col(collection):
    filter_key = input("Enter the key to filter (e.g., name): ")
    filter_value = input(f"Enter the value of {filter_key} to filter by: ")
    _filter = {filter_key: filter_value}
    result = collection.find(_filter)
    if result:
        for data in result:
            for key, value in data.items():
                print(f"{key}: {value}")
            print("\n")
    else:
        print("No document found matching the provided filter.")
    input("Press any key to continue...")
    option_menu()

# PRINT OPTIONS
def print_options():
    os.system('clear')
    print("\nChoose an option:")
    print(f"1. Display all data from {current_col}")
    print(f"2. Display one specific data from {current_col}")
    print(f"3. Add data to {current_col}")
    print(f"4. Update data in {current_col}")
    print(f"5. Delete data from {current_col}")
    print("6. Switch to another collection")
    print("7. Exit")
    return

# OPTION MENU
def option_menu():
    global db_name, col, db
    print_options()
    choice = input("Enter your choice (1-7): \n")
    if choice == '1':
        display_collection_data(col)
    elif choice == '2':
        find_document_from_col(col)
    elif choice == '3':
        add_document_to_col(col)
    elif choice == '4':
        update_document_to_col(col)
    elif choice == '5':
        delete_document_from_col(col)
    elif choice == '6':
        choose_collection(db)
    elif choice == '7':
        print("Exiting server")
        exit()
    else:
        print("Invalid choice")
        input("Press any key to continue...")
        print_options()

# CHOOSE COLLECTION
def choose_collection(db):
    global col, current_col
    while True:
        print("\nHere is the list of available collections")
        display_collection(db)
        col_name = input("Choose a Collection: ")
        if not col_name:
            print("Error: Collection not found")
            continue
        col = db[col_name]
        current_col = col_name
        option_menu()
        break
    return

# MAIN EXOSKELETON
def run_server():
    global col, current_col, db
    db = connect_to_db()
    if db is None:
        print("Error connecting to database")
        return
    else:
        print("Connected to database: ", db.name)
        # start server loop
        choose_collection(db)
    return

run_server()