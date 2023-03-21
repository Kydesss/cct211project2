import csv


def import_passwords(passwords: csv, database):
    """
    Imports CSV password files from Chrome or Edge.
    """
    csv_reader = csv.reader(passwords)
    list_of_passwords = []
    for row in csv_reader:
        list_of_passwords.append(row)
    list_of_passwords.pop(0)
    for i in list_of_passwords:
        database.insert_password(i)

def export_passwords(passwords: list[tuple]) -> csv:
    """
    Exports passwords from SQLite database to a CSV file.
    """
    #TODO
    pass

