import tkinter as tk
from ecommerceDBHandler import *

class Basket(tk.Tk):
      def __init__(self, system):
            super().__init__()
            self.ecommerceSystem = system 
            self.title(self.ecommerceSystem.currentUserName + "'s Basket")

            for i in range(len(returnBaskets(self.ecommerceSystem.currentUserID)[0])):
                  l1 = tk.Label(self, text = "Basket ID: " + str(returnBaskets(self.ecommerceSystem.currentUserID)[0][i]) + " Item ID: " + str(returnBaskets(self.ecommerceSystem.currentUserID)[1][i]) + " Quantity: " + str(returnBaskets(self.ecommerceSystem.currentUserID)[2][i]))
                  l1.pack()