import sqlite3
DB = sqlite3.connect(r"E-commerceDB.db")
cursor = DB.cursor()

tables = ["Basket", "CustomerBasket", "Item", "Customer", "ItemType", "Manufacturer", "FormatType", "PreviousOrder"]

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

#------------------------------------------------------------------ TRIGGERS ------------------------------------------------------------------

#Add stock when user adds item to basket
cursor.execute("""
    CREATE TRIGGER ItemtoBasketTrigger
    AFTER Insert
    ON Basket
    BEGIN
    UPDATE Item
    SET Stock = Stock + (
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


def CustomerBasketPaid(basket_id):
    cursor.execute("""
        UPDATE CustomerBasket
        SET Paid = TRUE
        WHERE BasketID = ?;""",
        (basket_id,))

def CustomerBasketAdd(basket_id):
    cursor.execute("""
        INSERT INTO Basket (BasketID, ItemID, Quantity)
        VALUES (?, 10, 10);""",
        (basket_id,))

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
    #def createCustomerProfileView():
    cursor.executescript("""
    DROP VIEW IF EXISTS CustomerProfile;
    CREATE VIEW CustomerProfile AS
    SELECT Customer.FirstName, Customer.Surname, CustomerBasket.BasketID
    FROM Customer
    LEFT JOIN CustomerBasket ON CustomerBasket.CustomerID = Customer.CustomerID;
    """)

def returnCutomerProfileView():
    cursor.execute("SELECT * FROM CustomerProfile;")
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
    


#----------------------------------------------------------------------------------------------------------------------------------------------








##AI, Manually do it later

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
    (15, "Action Show1", 4, "Description13", 30.00),
    (16, "Pop Album1", 1, "Description14", 20.00),
    (17, "Action Game3", 5, "Description15", 22.50)
]
cursor.executemany("INSERT OR IGNORE INTO Item (ItemID, ItemName, ItemTypeID, ItemDescription, ItemPrice) VALUES (?, ?, ?, ?, ?);", items)


item_types = [
    (1, "Record", 1, 2),
    (2, "CD", 2, 1),
    (3, "DVD", 2, 2),
    (4, "Game", 2, 3),
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
    (3, "Solid State"),
    (4, "Blu-Ray"),
    (5, "Optical")
]
cursor.executemany("INSERT OR IGNORE INTO FormatType (FormatID, StorageType) VALUES (?, ?);", formats)

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












