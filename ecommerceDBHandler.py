import sqlite3
import hashlib
DB = sqlite3.connect(r"EcommerceDB.db")
cursor = DB.cursor()

tables = ["Basket", "CustomerBasket", "Item", "Customer", "ItemType", "Manufacturer", "FormatType", "PreviousOrder", "Logins", "Icons"]

#if (input("Do you want to clear the table before starting? Y/N\n") == "Y"):
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table};")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT,
    Surname TEXT,
    ShippingAddress TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS CustomerBasket (
    BasketID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    Paid BOOL DEFAULT FALSE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Basket (
    BasketItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    BasketID INTEGER,
    ItemID INTEGER,
    Quantity INTEGER,
    FOREIGN KEY (BasketID) REFERENCES CustomerBasket(BasketID),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PreviousOrder (
    BasketID INTEGER PRIMARY KEY,
    Time TEXT DEFAULT 'September',
    FOREIGN KEY (BasketID) REFERENCES CustomerBasket(BasketID)
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS Item (
    ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName TEXT,
    ItemTypeID INTEGER,
    ItemDescription TEXT,
    ItemPrice REAL DEFAULT 0.00,
    Stock INTEGER DEFAULT 100,
    FOREIGN KEY (ItemTypeID) REFERENCES ItemType(ItemTypeID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ItemType (
    ItemTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeName TEXT,
    FormatID INTEGER,
    ManufacturerID INTEGER,
    FOREIGN KEY (FormatID) REFERENCES FormatType(FormatID),
    FOREIGN KEY (ManufacturerID) REFERENCES Manufacturer(ManufacturerID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Manufacturer (
    ManufacturerID INTEGER PRIMARY KEY AUTOINCREMENT,
    ManufacturerName TEXT,
    ManufacturerDesc TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS FormatType (
    FormatID INTEGER PRIMARY KEY AUTOINCREMENT,
    StorageType TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Logins (
    LoginID INTEGER PRIMARY KEY,
    Username TEXT,
    Password TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Icons (
    file_path_name TEXT NOT NULL,
    file_blob BLOB NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

""")

#------------------------------------------------------------------ TRIGGERS ------------------------------------------------------------------

#Add stock when user adds item to basket
cursor.execute("""
    CREATE TRIGGER ItemtoBasketTrigger
    AFTER Insert
    ON Basket
    BEGIN
    UPDATE Item
    SET Stock = Stock - (
        SELECT Quantity
        FROM Basket
        WHERE Basket.BasketID = NEW.BasketID
        AND Basket.ItemID = Item.ItemID
    )
    WHERE Item.ItemID IN (
        SELECT ItemID
        FROM Basket
        WHERE Basket.BasketID = NEW.BasketID
    );
    END;
""")

#Edit stock when user updates basket
cursor.execute("""
    CREATE TRIGGER UpdateItemInBasketTrigger
    AFTER Update
    ON Basket
    BEGIN
    UPDATE Item
    SET Stock = Stock - (
        SELECT Quantity
        FROM Basket
        WHERE Basket.BasketID = NEW.BasketID
        AND Basket.ItemID = Item.ItemID
    )
    WHERE Item.ItemID IN (
        SELECT ItemID
        FROM Basket
        WHERE Basket.BasketID = NEW.BasketID
    );
    END;
""")

#Return stock when user removes item from basket
cursor.execute("""
    CREATE TRIGGER ReturnItem
    AFTER Delete
    ON Basket
    BEGIN
    UPDATE Item
    SET Stock = Stock + (
        SELECT Quantity
        FROM Basket
        WHERE Basket.BasketID = OLD.BasketID
        AND Basket.ItemID = Item.ItemID
    )
    WHERE Item.ItemID IN (
        SELECT ItemID
        FROM Basket
        WHERE Basket.BasketID = OLD.BasketID
    );
    END;
""")

#Basket goes on to orders when user buys basket
cursor.execute("""
    CREATE TRIGGER PurchaseOrderTrigger
    AFTER Update
    ON CustomerBasket
    BEGIN
    INSERT INTO PreviousOrder (BasketID, Time)
    VALUES (NEW.BasketID, datetime('now'));
    END;
""")

DB.commit()

def CustomerBasketPaid(basket_id):
    cursor.execute("""
        UPDATE CustomerBasket
        SET Paid = TRUE
        WHERE BasketID = ?;""",
        (basket_id,))
    DB.commit()

def CustomerBasketAdd(basket_id):
    cursor.execute("""
        INSERT INTO Basket (BasketID, ItemID, Quantity)
        VALUES (?, 10, 10);""",
        (basket_id,))
    DB.commit()

def CustomerBasketUpdate(basket_item_id, new_quantity):
    cursor.execute("""
        UPDATE Basket
        SET Quantity = ? 
        WHERE BasketItemID = ?;""",
        (new_quantity, basket_item_id))
    
def CustomerBasketDelete(basket_item_id):
    cursor.execute("""
        DELETE FROM Basket
        WHERE BasketItemID = ?;""",
        (basket_item_id,))
    


def createCustomerProfileView():
    cursor.executescript("""
    DROP VIEW IF EXISTS CustomerProfile;
    CREATE VIEW CustomerProfile AS
    SELECT Customer.FirstName, Customer.Surname, CustomerBasket.BasketID
    FROM Customer
    LEFT JOIN CustomerBasket ON CustomerBasket.CustomerID = Customer.CustomerID;
    """)

def returnCustomerProfileView():
    cursor.execute("SELECT * FROM CustomerProfile;")
    return cursor.fetchone()

def specificCustomerProfileView(customer_id):
    cursor.executescript("""
    DROP VIEW IF EXISTS SpecificCustomerProfile;
    CREATE VIEW SpecificCustomerProfile AS
    SELECT Customer.FirstName, Customer.Surname, CustomerBasket.BasketID, CustomerBasket.Paid
    FROM Customer
    LEFT JOIN CustomerBasket ON CustomerBasket.CustomerID = Customer.CustomerID
    WHERE Customer.CustomerID = ?;
    """, ( customer_id, ))

def returnSpecificCustomerProfileView():
    cursor.execute("SELECT * FROM SpecificCustomerProfile;")
    return cursor.fetchone()

def createDeliveredItemsView():
    cursor.execute("""
        DROP VIEW IF EXISTS DeliveredItems;

        CREATE VIEW DeliveredItems AS
        SELECT Item.ItemName, Item.ItemDescription, Item.ItemPrice, Basket.Quantity
        FROM Basket
        LEFT JOIN Item ON Item.ItemID = Basket.ItemID
        LEFT JOIN CustomerBasket ON CustomerBasket.BasketID = Basket.BasketID
        WHERE CustomerBasket.Paid = 1;

        SELECT *
        FROM DeliveredItems;""")

def createTotalSoldView():
    cursor.execute("""
        DROP VIEW IF EXISTS TotalSold;

        CREATE VIEW TotalSold AS
        SELECT COUNT(Basket.Quantity) AS [Total Items Sold], 
            COUNT(Basket.Quantity) * Item.ItemPrice AS [Total Profts]
        FROM Basket
        LEFT JOIN Item ON Item.ItemID = Basket.ItemID
        LEFT JOIN CustomerBasket ON CustomerBasket.BasketID = Basket.BasketID
        WHERE CustomerBasket.Paid = 1;

        SELECT *
        FROM TotalSold;""")

def createTotalItemSoldView():
    cursor.execute("""
        DROP VIEW IF EXISTS TotalItemSold;

        CREATE VIEW TotalItemSold AS
        SELECT Item.ItemName,
            SUM(Basket.Quantity),
            SUM(Basket.Quantity) * Item.ItemPrice AS [Total Profits]
        FROM Item
        RIGHT JOIN Basket ON Basket.ItemID = Item.ItemID
        GROUP BY Item.ItemID;

        SELECT *
        FROM TotalItemSold;""")
    
def generateUserID():
    cursor.execute("SELECT MAX(CustomerID) FROM Customer;")
    max_id = cursor.fetchone()[0]
    if max_id is None:
        return 1
    else:
        return max_id + 1
    
def returnLoginIDs():
    cursor.execute("SELECT LoginID FROM Logins")
    rows = cursor.fetchall()
    IDs = []
    for loginID in rows:
        IDs.append(loginID[0])
    return IDs

def returnLoginDetailsByID(ID):
    rows = cursor.execute("""SELECT Username, Password FROM Logins WHERE LoginID = ?;""", ( ID,))
    for row in rows:
        return row

def returnStock():
    cursor.execute("SELECT ItemName FROM item")
    items = cursor.fetchall()
    row1 = []
    for item in items:
        row1.append(item[0])

    cursor.execute("SELECT Stock FROM item")
    stocks = cursor.fetchall()
    row2 = []
    for stock in stocks:
        row2.append(stock[0])

    rows = [row1, row2]
    print(rows[0], "\n", rows[1])
    return rows

def returnBaskets():
    cursor.execute("SELECT BasketID FROM basket")
    ids = cursor.fetchall()
    row1 = []
    for id in ids:
        row1.append(id[0])

    cursor.execute("SELECT Quantity FROM basket")
    quantity = cursor.fetchall()
    row2 = []
    for num in quantity:
        row2.append(num[0])

    rows = [row1, row2]
    print(rows[0], "\n", rows[1])
    return rows

def returnAllItems():
    cursor.execute("SELECT ItemName FROM Item")
    names = cursor.fetchall()
    row1 = []
    for name in names:
        row1.append(name[0])
    
    cursor.execute("SELECT ItemPrice FROM Item")
    names = cursor.fetchall()
    row2 = []
    for name in names:
        row2.append(name[0])
    
    cursor.execute("SELECT ItemID FROM Item")
    names = cursor.fetchall()
    row3 = []
    for name in names:
        row3.append(name[0])
    
    cursor.execute("SELECT ItemTypeID FROM Item")
    names = cursor.fetchall()
    row4 = []
    for name in names:
        row4.append(name[0])
    
    rows = [row1, row2, row3, row4]
    print(rows[0], "\n", rows[1], "\n", rows[2], "\n", rows[3])
    return rows



def simulatePurchases():
    CustomerBasketAdd(1)
    CustomerBasketAdd(7)
    CustomerBasketAdd(12)
    CustomerBasketAdd(13)
    CustomerBasketPaid(1)
    CustomerBasketPaid(7)
    CustomerBasketPaid(12)
    CustomerBasketPaid(13)
    DB.commit()

def send_media_to_sql_user(filePath):
    #To open a file in binary format, add 'b' to the mode parameter and "rb" mode opens the file in binary format for reading.
    with open(filePath, 'rb') as file:
        file_blob = file.read()
    #to see file in BLOB values
    print("[INFO] : the last 100 characters of blob = ", file_blob[:100]) 

    #to insert file_path_name and BLOB to database audio_table
    sql_insert_file_query = "INSERT INTO audio_table(filePath, file_blob)VALUES(?, ?)"

    cursor.execute(sql_insert_file_query, (filePath, file_blob, ))
    DB.commit()
    #message to test
    print("[INFO] : The blob for ", filePath, " sent and saved in the database audio_table.") 

def send_media_to_sql():
        paths = ["./icons/music.png", "./icons/movie.png", "./icons/game.png"]
        for path in paths:
            #To open a file in binary format, add 'b' to the mode parameter and "rb" mode opens the file in binary format for reading.
            with open(path, 'rb') as file:
                file_blob = file.read()
            #to see file in BLOB values
            print("[INFO] : the last 100 characters of blob = ", file_blob[:100]) 
            #to insert file_path_name and BLOB to database audio_table
            sql_insert_file_query = "INSERT INTO Icons(file_path_name, file_blob)VALUES(?, ?)"
            cursor.execute(sql_insert_file_query, (path, file_blob, ))
            DB.commit()
            #message to test
            print("[INFO] : The blob for ", path, " sent and saved in the database audio_table.") 

send_media_to_sql()

def Get_media_from_sql(iconID):
        print("[INFO] : Connected to SQLite to read_blob_data")
        cursor.execute("""SELECT * from Icons where id = ?;""", (iconID,))                        
        record = cursor.fetchall()
        for row in record:
            converted_file_name = row[0]
            media_binarycode  = row[1]
            last_slash_index = converted_file_name.rfind("/") + 1 
            final_file_name = converted_file_name[last_slash_index:] 
            print("[DATA] : media file successfully stored on disk. Check the project directory. \n")
        with open(final_file_name, 'wb') as file:
                file.write(media_binarycode)

        
Get_media_from_sql(1)
Get_media_from_sql(2)
Get_media_from_sql(3)




#----------------------------------------------------------------------------------------------------------------------------------------------










customers = [
    (1, "Forename1", "Surname1", "1 Mainstreet"),
    (2, "Forename2", "Surname2", "2 Mainstreet"),
    (3, "Forename3", "Surname3", "3 Mainstreet"),
    (4, "Forename4", "Surname1", "4 Mainstreet"),
    (5, "Forename2", "Surname5", "1 Mainstreet"),
    (6, "Forename6", "Surname6", "6 Mainstreet")
]
cursor.executemany("INSERT OR IGNORE INTO Customer (CustomerID, FirstName, Surname, ShippingAddress) VALUES (?, ?, ?, ?);", customers)

customer_baskets = [
    (1,1, False),
    (2,2, False),
    (3,3, False),
    (4,4, False),
    (5,5, False),
    (6,6, False),
    (7,1, False),
    (8,4, False),


]
cursor.executemany("INSERT OR IGNORE INTO CustomerBasket (BasketID, CustomerID, Paid) VALUES (?, ?, ?);", customer_baskets)

baskets = [
    (1,1,16,1),
    (2,1,2,1),
    (3,1,3,1),
    (4,1,4,50),
    (5,2,17,2),
    (6,3,6,1),
    (7,3,7,1),
    (8,3,3,1),
    (9,4,9,1),
    (10,4,5,2),
    (11,4,11,1),
    (12,5,12,1),
    (13,5,13,1),
    (14,5,14,3),
    (15,5,15,1),
    (16,6,1,1),
    (17,6,5,3),
    (18,7,1,100),
    (19,8,5,1)
]
cursor.executemany("INSERT INTO Basket (BasketItemID, BasketID, ItemID, Quantity) VALUES (?, ?, ?, ?);", baskets)

items = [
    (1, "Pop Album1", 2, "Description1", 15.00),
    (2, "Pop Album2", 2, "Description2", 20.00),
    (3, "Comedy Movie1", 4, "Description3", 9.50),
    (4, "Rock Album2", 2, "Description4", 12.00),
    (5, "Action Game3", 6, "Description5", 30.00),
    (6, "Romance Show1", 3, "Description6", 40.00),
    (7, "Country Album2", 2, "Description7", 5.00),
    (9, "Action Game2", 5, "Description8", 35.00),
    (11, "Action Game1", 6, "Description9", 15.00),
    (12, "2D Game2", 5, "Description10", 60.00),
    (13, "Country Album1", 2, "Description11", 50.00),
    (14, "2D Game1", 6, "Description12", 25.00),
    (15, "Game Show1", 4, "Description13", 150.00),
    (16, "Jungle Album1", 1, "Description14", 80.00),
    (17, "Educational Software1", 5, "Description15", 5.00),
    (18, "Comedy Movie2", 4, "Description16", 9.50),
    (19, "Jungle Album2", 2, "Description17", 8.99),
    (20, "Action Game4", 6, "Description18", 30.00),
    (21, "Animated Show1", 3, "Description19", 19.99),
    (22, "Country Album3", 2, "Description20", 5.00),
    (23, "Game Show2", 5, "Description21", 35.00),
    (24, "Action Game5", 6, "Description22", 15.00),
    (25, "2D Game3", 5, "Description23", 60.00),
    (26, "Dubstep Album1", 2, "Description24", 5.00),
    (27, "Collector's Game1", 6, "Description25", 999.50),
    (28, "Animated Show2", 4, "Description26", 30.99),
    (29, "Kpop Album1", 1, "Description27", 15.99),
    (30, "Collector's Game2", 5, "Description28", 500.00)
]
cursor.executemany("INSERT OR IGNORE INTO Item (ItemID, ItemName, ItemTypeID, ItemDescription, ItemPrice) VALUES (?, ?, ?, ?, ?);", items)


item_types = [
    (1, "Record", 1, 1),
    (2, "CD", 2, 2),
    (3, "DVD", 2, 2),
    (4, "Blu-Ray", 2, 3),
    (5, "Game", 2, 4),
    (6, "Game", 3, 5)
]
cursor.executemany("INSERT OR IGNORE INTO ItemType (ItemTypeID, TypeName, FormatID, ManufacturerID) VALUES (?, ?, ?, ?);", item_types)


manufacturers = [
    (1, "Universal", ""),
    (2, "Sony", ""),
    (3, "Blu-Ray", ""),
    (4, "Xbox", ""),
    (5, "Nintendo", "")
]
cursor.executemany("INSERT OR IGNORE INTO Manufacturer (ManufacturerID, ManufacturerName, ManufacturerDesc) VALUES (?, ?, ?);", manufacturers)

formats = [
    (1, "Analogue"),
    (2, "Optical"),
    (3, "Solid State")
]
cursor.executemany("INSERT OR IGNORE INTO FormatType (FormatID, StorageType) VALUES (?, ?);", formats)

logins = [
    (1, "John", "Password1"),
    (5, "CoolUser123", "basketball!"),
    (11, "Jane", "Password3")
]

encrypted_logins = []

for login in logins:
    encrypted_logins.append((login[0],
        str(hashlib.sha256(login[1].encode()).hexdigest()),
        str(hashlib.sha256(login[2].encode()).hexdigest()),
       ))                                   

cursor.executemany("INSERT OR IGNORE INTO Logins (LoginID, Username, Password) VALUES (?, ?, ?);", encrypted_logins)

import datetime

# Insert BasketID into PreviousOrder for paid customer baskets
cursor.execute("SELECT BasketID FROM CustomerBasket WHERE Paid=1;")
paid_baskets = cursor.fetchall()
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for (basket_id,) in paid_baskets:
    cursor.execute(
        "INSERT OR IGNORE INTO PreviousOrder (BasketID, Time) VALUES (?, ?);",
        (basket_id, current_time)
    )

DB.commit()

def text_program():
    while (input("Would you like to simulate a purchase? Y/N\n") == "Y"):
        CustomerBasketPaid(input("Enter BasketID to pay for:\n"))
        DB.commit()
    while (input("Would you like to add to a basket? Y/N\n") == "Y"):
        CustomerBasketAdd(input("Enter BasketID to add to:\n"))
        DB.commit()
    while (input("Would you like to Update a purchase? Y/N\n") == "Y"):
        CustomerBasketUpdate(input("Enter BasketItemID to update:\n"),input("Enter Quantity to update with:\n"))
        DB.commit()
    while (input("Would you like to delete an item in your basket? Y/N\n") == "Y"):
        CustomerBasketDelete(input("Enter BasketItemID to delete?:\n"))

    DB.commit()


createCustomerProfileView()
#createDeliveredItemsView()
#createTotalSoldView()
#createTotalItemSoldView()












