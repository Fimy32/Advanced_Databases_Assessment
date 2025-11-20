from tkinter import *
import tkinter as tk
from ecommerceDBHandler import *
from .login import Login
from .stock import Stock
import matplotlib.pyplot as plt


class MainWindow(tk.Tk):
      def __init__(self, system):
            super().__init__()
            #self.attributes('-fullscreen',True)
            self.geometry("1000x1000")
            self.title("E-commerce Application")
            self.loginbutton = tk.Button(self, text="Login", command=self.createLoginWindow).pack()
            self.stockbutton = tk.Button(self, text="Stock", command=self.createStockGrapth)
            self.stockbutton.pack()
            self.purchasebutton = tk.Button(self, text="PRESS THIS TO SIMULATE PURCHASES FOR 4 HARD CODED BASKETS", command=self.simulatePurchasesFrontEnd).pack()
            self.ecommerceSystem = system
            if self.ecommerceSystem.currentUserName != None:
                  self.usertext = tk.Label(self, self.ecommerceSystem.currentUserName).pack()
            #self.data = tk.Label(self, text=Ecommerce.returnSpecificCustomerProfileView(), height=40, width=120).pack()
            self.closeButton = tk.Button(self, text="Close", command=self.destroy).pack(side=tk.BOTTOM)

   
      #Appearance Selector
      def lightMode(self):
            self.configure(bg="white")
            global outcolour
            global textcolour
            outcolour = "white"
            textcolour = "black"
            self.update()
            self.update_idletasks()

      def darkMode(self):
            self.configure(bg="black")
            global outcolour
            global textcolour
            outcolour = "black"
            textcolour = "white"
            self.update()
            self.update_idletasks()
      
      def createLoginWindow(self):
            loginWindow = Login(self.ecommerceSystem)
            loginWindow.mainloop()

      def createStockGrapth(self):
            itemName = returnStock()[0]
            stock = returnStock()[1]
            plt.bar(itemName, stock, color='skyblue')
            plt.xlabel("Item")
            plt.ylabel("Stock Quantities")
            plt.title("Current Stock Count")
            plt.show()

            itemID = returnBaskets()[0]
            quantity = returnBaskets()[1]
            plt.bar(itemID, quantity, color='skyblue')
            plt.xlabel("Basket Number")
            plt.ylabel("Number of an individual item In Basket")
            plt.title("Items held in basket")
            plt.show()
      
      def simulatePurchasesFrontEnd(self):
            simulatePurchases()
            self.purchasebutton.pack_forget()
            





