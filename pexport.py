import csv
from passwordsql import Database
import pgenerator as pg


def import_passwords(passwords: csv, database: Database):
    """
    Imports CSV password files from Chrome or Edge.
    """
    csv_reader = csv.reader(passwords)
    list_of_passwords = []
    for row in csv_reader:
        list_of_passwords.append(row)
    list_of_passwords.pop(0)
    for i in list_of_passwords:
        database.append_password(i)

def export_passwords(database: Database, dir_name: str) -> csv:
    """
    Exports passwords from SQLite database to a CSV file.
    """
    read_database = database.read_query()
    export = [['name', 'url', 'username', 'password']]
    for entry in read_database:
        single_entry = []
        i = 0
        for col in entry:
            if i == 3:
                col = pg.decrypt(col)
            single_entry.append(col)
            i += 1
        single_entry[0] = entry[1]
        export.append(single_entry)
    with open(file=dir_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(export)
