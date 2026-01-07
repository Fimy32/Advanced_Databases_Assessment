#John Password1 IS A USER


#A GUI for the application. It uses TK inter to generate windows and
#gives functionality for the user to interact with using widgets
from tkinter import *
import tkinter as tk
from ecommerceDBHandler import *
from .login import Login
from .stock import Stock
from .basket import Basket
import matplotlib.pyplot as plt
from xmlHandler import *
from PIL import Image, ImageTk
import io


class MainWindow(tk.Tk):
      def __init__(self, system):
            super().__init__()
            #self.attributes('-fullscreen',True)
            self.geometry("1000x1000")
            self.title("E-commerce Application")
            self.closeButton = tk.Button(self, text="Close", command=self.destroy).grid(row = 0, column = 1, sticky = W, pady = 2)
            self.loginbutton = tk.Button(self, text="Login", command=self.createLoginWindow).grid(row = 0, column = 2, sticky = W, pady = 2)
            self.stockbutton = tk.Button(self, text="Stock", command=self.createStockGrapth)
            self.stockbutton.grid(row = 0, column = 3, sticky = W, pady = 2)
            self.resetButton = tk.Button(self, text="RESET DB\n(THIS IS FINAL)", command=self.dbReset).grid(row = 0, column = 15, sticky = W, pady = 2)
            self.saveIcons = tk.Button(self, text="SAVE THE ICONS FILE TO DATABASE", command=self.saveMedia).grid(row = 0, column = 11, sticky = W, pady = 2)
            self.loadIcons = tk.Button(self, text="LOAD ICONS FROM DATABASE", command=self.loadMedia).grid(row = 0, column = 12, sticky = W, pady = 2)
            self.ecommerceSystem = system
            self.basketButton = tk.Button(self, text="Your Basket", command=self.basket).grid(row = 0, column = 4, sticky = W, pady = 2)
            if self.ecommerceSystem.currentUserName != None:
                  self.usertext = tk.Label(self, self.ecommerceSystem.currentUserName).grid(row = 0, column = 10, sticky = W, pady = 3)
            self.currentItemID = None
            self.xmlsave = tk.Button(self, text="Convert To XML", command=self.savexml).grid(row = 1, column = 11, sticky = W, pady = 2)
            self.xmlload = tk.Button(self, text="XML to DB", command=self.loadxml).grid(row = 1, column = 12, sticky = W, pady = 2)
            
            for i in range(len(returnAllItems()[0])):
                  item_id = returnAllItems()[2][i]
                  if returnAllItems()[4][i] > 0:
                        l1 = Button(self, text = returnAllItems()[0][i] + "\n£" + str(returnAllItems()[1][i]) + "\nAdd To Basket", command=lambda iid=item_id: self.addToBasket(iid))
                  else:
                        l1 = Button(self, text = returnAllItems()[0][i] + "\n£" + str(returnAllItems()[1][i]) + "\nOut of Stock")
                  l1.grid(row = i//5 + 1, column = i%5 + 1, sticky = W, pady = 2)

   
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
      #This grapth shows inovation by generating a couple different grapths
      #This is an effective way for an admin to use data visualisation to see stock levels
      #and the amount of stock in baskets
      def createStockGrapth(self):
            plt.xticks(rotation=90)
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

      def saveMedia(self):
            send_media_to_sql()
      
      def loadMedia(self,):
            for i in range(1,4):
                  Get_media_from_sql(i)

      def basket(self):
                  if not self.ecommerceSystem.currentUserID:
                        if self.ecommerceSystem.currentUserID == None:
                              self.notLoggedInLabel = tk.Label(self, text="You must be logged in to view your basket.", fg="red")
                              self.notLoggedInLabel.grid(row=1, column=10, sticky='w', pady=5)
                        return
                  basketWindow = Basket(self.ecommerceSystem)
                  basketWindow.mainloop()

      def dbReset(self):
            resetDB()

      def addToBasket(self, item_id):
            CustomerBasketAdd(findBasket(self.ecommerceSystem.currentUserID), item_id)

      def savexml(self):
            loginsToXml()
      
      def loadxml(self):
            xmltologins()
            





