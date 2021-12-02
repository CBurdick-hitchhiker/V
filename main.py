import hashlib
import secrets
import csv
import AnnieLibrary.py


CSV_FILE = "passwords.csv"
MASTER_HASH_FILE = "master.txt"
passwordAttempts = 0


while (True):
    try:
        password = input("Enter master password: ")
        if (not masterHashComapare(password)):
            if (passwordAttempts > 1):
                print("\n**TOO MANY WRONG ATTEMPTS**\n")
                raise SystemExit(0)
            else:
                print("\n**WRONG PASSWORD**\n")
                passwordAttempts = passwordAttempts + 1
                continue
        else:
            break
    except FileNotFoundError:
        print("\nMaster password file doesn't exist. Creating master file. Initializing Database.\n")
        createMasterHashFile(password)
        break


while (True):
    try:
        choice = menu()
        if (choice < 1 or choice > 5):
            print("\n**INVALID MENU OPTION**\n")
    except ValueError:
        print("\n**INVALID MENU OPTION**\n")
        continue

    if (choice == 1):
        site = input("Enter site name: ")
        if (site == "site"):
            print("\n**INVALID SITE NAME**\n")
            continue
        try:
            if (readCsv(site) != None):
                print("\n**SITE ALREADY EXISTS**\n")
                continue
        except FileNotFoundError:
            pass
        username = input("Enter username for %s: " % site)
        password = input("Enter simple password to be hashed: ")
        try:
            length = int(input("Enter length of hashed password (1-128): "))
        except ValueError:
            print("\n**NO INPUT SETTING LENGTH TO 16**\n")
            length = 16
        hashTuple = hashPassword(password, length)
        writeCsv(site, username, hashTuple[0], hashTuple[1])
        print("\nPASSWORD HASHED AND SAVED SUCCESSFULLY\n")

    if (choice == 2):
        site = input("Enter site to retrive: ")
        if (site == "site"):
            print("\n**INVALID SITE NAME**\n")
            continue
        try:
            if (readCsv(site) == None):
                print("\n**NO SITE FOUND**\n")
                continue
            else:
                csvRow = readCsv(site)
                print("\n")
                print("SITE: %s" % csvRow[0])
                print("USERNAME: %s" % csvRow[1])
                print("PASSWORD: %s" % csvRow[3])
                print("\n")
        except FileNotFoundError:
            print("\n**PASSWORDS FILE DOES NOT EXIST, CREATE A PASSWORD**\n")

    if (choice == 3):
        site = input("Enter site to delete: ")
        if (site == "site"):
            print("\n**INVALID SITE NAME**\n")
            continue
        elif (readCsv(site) == None):
            print("\n**NO SITE FOUND**\n")
            continue
        else:
            deleteCsv(site)
            print("\nSITE DELETED SUCCESSFULLY\n")

    if (choice == 4):
        if (listSites()):
            counter = 1
            print("\n")
            for site in listSites():
                print("%i: %s" % (counter, site))
                counter += 1
            print("\n")
        else:
            print("\nNO SITES IN FILE\n")

    if (choice == 5):
        print("\nGOODBYE! :)\n")
        break
