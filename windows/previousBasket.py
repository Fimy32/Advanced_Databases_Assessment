import tkinter as tk
from ecommerceDBHandler import *

class previousBasket(tk.Tk):
      def __init__(self, system):
            super().__init__()
            self.attributes('-fullscreen', True)
            self.ecommerceSystem = system 
            self.title(self.ecommerceSystem.currentUserName + "'s Previous Orders")
            self.basketIds = findPaidBasket(self.ecommerceSystem.currentUserID)
            self.rowNumber = 0
            for basketId in self.basketIds:
                  label2 = tk.Label(self, text="Order " + str(basketId[0]) + ":")
                  label2.grid(row=0, column=basketId[0], sticky="w", padx=10, pady=5)
                  items = getEachItemInBasket(basketId[0])
                  for i, (uniqueid, itemid, name, price, quantity) in enumerate(items):
                        label1 = tk.Label(self, text="Name: " + name + "\n" + "Price: £" + str(price) + "\nQuantity: " + str(quantity))
                        label1.grid(row=i + 1, column=basketId[0], sticky="w", padx=10, pady=5)
                        self.rowNumber = i
            self.closeButton = tk.Button(self, text="Close", command=self.destroy).grid(row = 1, column = 100, sticky = "W", pady = 2)
