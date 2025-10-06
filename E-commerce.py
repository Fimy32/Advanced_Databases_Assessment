import sqlite3
DB = sqlite3.connect(r"E-commerceDB.db")
cursor = DB.cursor()

tables = ["Basket", "CustomerBasket", "Item", "Customer", "ItemType", "Manufacturer", "FormatType", "PreviousOrder"]

if (input("Do you want to clear the table before starting? Y/N\n") == "Y"):
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
    Time TEXT DEFAULT "September",
    FOREIGN KEY (BasketID) REFERENCES Basket(BasketID)
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
    CREATE TRIGGER PurchaseStockTrigger
    AFTER Update
    ON CustomerBasket
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


##AI, Manually do it later

# -------------------------
# Insert Customer data
# -------------------------
customers = [
    (1, "Forename1", "Surname1", "1 Mainstreet"),
    (2, "Forename2", "Surname2", "2 Mainstreet"),
    (3, "Forename3", "Surname3", "3 Mainstreet"),
    (4, "Forename4", "Surname1", "4 Mainstreet"),
    (5, "Forename2", "Surname5", "1 Mainstreet"),
    (6, "Forename6", "Surname6", "6 Mainstreet")
]
cursor.executemany("INSERT OR IGNORE INTO Customer (CustomerID, FirstName, Surname, ShippingAddress) VALUES (?, ?, ?, ?);", customers)

# -------------------------
# Insert CustomerBasket data
# -------------------------
customer_baskets = [
    (1,1, False),
    (2,2, False),
    (3,3, False),
    (4,4, False),
    (5,5, False),
    (6,6, False)
]
cursor.executemany("INSERT OR IGNORE INTO CustomerBasket (BasketID, CustomerID, Paid) VALUES (?, ?, ?);", customer_baskets)

# -------------------------
# Insert Basket data
# -------------------------
baskets = [
    (1,1,16,1),
    (2,2,17,1),
    (3,3,6,1),
    (4,3,7,50),
    (5,3,9,2),
    (6,9,11,1),
    (7,5,12,1),
    (8,11,13,1),
    (9,12,14,1),
    (10,13,15,2),
    (11,14,16,1),
    (12,15,17,1),
    (13,1,1,1),
    (14,5,3,3)
]
cursor.executemany("INSERT INTO Basket (BasketItemID, BasketID, ItemID, Quantity) VALUES (?, ?, ?, ?);", baskets)

# -------------------------
# Insert Item data
# -------------------------
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


# -------------------------
# Insert ItemType data (with FormatID and ManufacturerID included as per your schema)
# -------------------------
item_types = [
    (1, "Record", 1, 2),
    (2, "CD", 2, 1),
    (3, "DVD", 2, 2),
    (4, "Game", 2, 3),
    (5, "Game", 2, 4),
    (6, "Game", 3, 5)
]
cursor.executemany("INSERT OR IGNORE INTO ItemType (ItemTypeID, TypeName, FormatID, ManufacturerID) VALUES (?, ?, ?, ?);", item_types)

# -------------------------
# Insert Manufacturer data
# -------------------------
manufacturers = [
    (1, "Universal", ""),
    (2, "Sony", ""),
    (3, "Blu-Ray", ""),
    (4, "Xbox", ""),
    (5, "Nintendo", "")
]
cursor.executemany("INSERT OR IGNORE INTO Manufacturer (ManufacturerID, ManufacturerName, ManufacturerDesc) VALUES (?, ?, ?);", manufacturers)

# -------------------------
# Insert FormatType data
# -------------------------
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
while (input("Would you like to simulate a purchase? Y/N\n") == "Y"):
    CustomerBasketPaid(input("Enter BasketID to pay for:\n"))
    DB.commit()


DB.close()
