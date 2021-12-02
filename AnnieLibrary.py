import hashlib
import secrets
import csv


def masterHashComapare(password):
    master = open(MASTER_HASH_FILE)
    masterLines = master.read().splitlines()
    salt = masterLines[0]
    hash = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
    if (hash == masterLines[1]):
        return True
    else:
        return False


def createMasterHashFile(password):
    with open(CSV_FILE, mode='w') as password_file:
        password_writer = csv.writer(password_file, delimiter=',', quotechar='"')
        password_writer.writerow(["site", "username", "salt", "hash"])
    master = open(MASTER_HASH_FILE, 'w')
    salt = secrets.token_hex(64)
    hash = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
    master.write("%s\n" % salt)
    master.write("%s\n" % hash)
    master.close()


def hashPassword(password, length):
    salt = secrets.token_hex(64)
    hash = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
    hash = hash[:length]
    return salt, hash


def writeCsv(site, username, salt, hash):
    try:
        readCsv("site")
    except FileNotFoundError:
        with open(CSV_FILE, mode='a') as password_file:
            password_writer = csv.writer(password_file, delimiter=',', quotechar='"')
            password_writer.writerow(["site", "username", "salt", "hash"])
    with open(CSV_FILE, mode='a') as password_file:
        password_writer = csv.writer(password_file, delimiter=',', quotechar='"')
        password_writer.writerow([site, username, salt, hash])


def readCsv(site):
    with open(CSV_FILE) as password_file:
        password_reader = csv.reader(password_file, delimiter=',')
        line_count = 0
        for row in password_reader:
            if (line_count != 0):
                if (row[0] == site):
                    return row
            line_count += 1


def deleteCsv(site):
    changes = list()
    with open(CSV_FILE) as password_file:
        password_reader = csv.reader(password_file, delimiter=',')
        for row in password_reader:
            if (row[0] != site):
                changes.append(row)

    with open(CSV_FILE, mode="w") as password_file:
        password_writer = csv.writer(password_file, delimiter=',', quotechar='"')
        password_writer.writerows(changes)


def listSites():
    with open(CSV_FILE) as password_file:
        password_reader = csv.reader(password_file, delimiter=',')
        sites = list()
        line_count = 0
        for row in password_reader:
            if (line_count != 0):
                sites.append(row[0])
            line_count += 1
    return sites


def menu():
    print("BENN'S PASSWORD MANAGER")
    print("-----------------------")
    print("1. Create password")
    print("2. Retrive password")
    print("3. Delete password")
    print("4. List Sites")
    print("5. Quit")
    print("-----------------------\n")

    userInput = int(input("Enter option: "))
    return userInput

