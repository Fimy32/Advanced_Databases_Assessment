import tkinter as tk
from ecommerceDBHandler import *

class Basket(tk.Tk):
      def __init__(self, system):
            super().__init__()
            self.attributes('-fullscreen', True)
            self.ecommerceSystem = system 
            self.title(self.ecommerceSystem.currentUserName + "'s Basket")
            self.basketId = findBasket(self.ecommerceSystem.currentUserID)
            items = getEachItemInBasket(self.basketId)
            for i, (uniqueid, itemid, name, price, quantity) in enumerate(items):
                  label1 = tk.Label(self, text="Name: " + name + "\n" + "Price: £" + str(price) + "\nQuantity: " + str(quantity))
                  editbutton1 = tk.Button(self, text="+1", command=lambda uid=uniqueid, quant=quantity: self.additem(uid, quant))
                  editbutton2 = tk.Button(self, text="-1", command=lambda uid=uniqueid, quant=quantity: self.removeItem(uid, quant))
                  deletebutton1 = tk.Button(self, text="Delete", command=lambda uid=uniqueid: self.deleteItem(uid))
                  label1.grid(row=i*2, column=1, sticky="w", padx=10, pady=5)
                  editbutton1.grid(row=i*2+1, column=1, sticky="w", padx=10, pady=5)
                  editbutton2.grid(row=i*2+1, column=2, sticky="w", padx=10, pady=5)
                  deletebutton1.grid(row=i*2+1, column=3, sticky="w", padx=10, pady=5)

      def additem(self, uniqueId, currentQuantity):
            CustomerBasketUpdate(uniqueId, currentQuantity + 1)
            self.destroy()
            Basket(self.ecommerceSystem)

      def removeItem(self, uniqueId, currentQuantity):
            CustomerBasketUpdate(uniqueId, currentQuantity - 1)
            self.destroy()
            Basket(self.ecommerceSystem)

      def deleteItem(self, uniqueId):
            CustomerBasketDelete(uniqueId)
            self.destroy()
            Basket(self.ecommerceSystem)
      
