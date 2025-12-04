from tkinter import *
import tkinter as tk
from ecommerceDBHandler import *
from .login import Login
from .stock import Stock
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
            self.loginbutton = tk.Button(self, text="Login", command=self.createLoginWindow).grid(row = 0, column = 0, sticky = W, pady = 2)
            self.stockbutton = tk.Button(self, text="Stock", command=self.createStockGrapth)
            self.stockbutton.grid(row = 0, column = 1, sticky = W, pady = 2)
            self.purchasebutton = tk.Button(self, text="PRESS THIS TO \nSIMULATE PURCHASES \nFOR 4 HARD CODED \nBASKETS", command=self.simulatePurchasesFrontEnd).grid(row = 0, column = 8, sticky = W, pady = 2)
            self.purchasebutton = tk.Button(self, text="SAVE THE ICONS FILE TO DATABASE", command=self.saveMedia).grid(row = 0, column = 2, sticky = W, pady = 2)
            self.purchasebutton = tk.Button(self, text="LOAD ICONS FROM DATABASE", command=self.loadMedia).grid(row = 0, column = 3, sticky = W, pady = 2)
            self.xmlButton = tk.Button(self, text="Write hashed Logins to XML", command=self.loadXml).grid(row = 0, column = 4, sticky = W, pady = 2)
            self.ecommerceSystem = system
            if self.ecommerceSystem.currentUserName != None:
                  self.usertext = tk.Label(self, self.ecommerceSystem.currentUserName).grid(row = 0, column = 5, sticky = W, pady = 3)
            #self.data = tk.Label(self, text=Ecommerce.returnSpecificCustomerProfileView(), height=40, width=120).pack()
            self.closeButton = tk.Button(self, text="Close", command=self.destroy).grid(row = 0, column = 6, sticky = W, pady = 2)


            #Grid for item data
            for i in range(len(returnAllItems()[0])):
                  frame = tk.Frame(self, bg='lightblue', bd=3, cursor='hand2',
                         highlightcolor='red', highlightthickness=2, highlightbackground='black', relief=tk.RAISED)
                  frame.grid(row = i//5 + 1, column = i%5, sticky = W, pady = 2)
                  l1 = Label(frame, text = returnAllItems()[0][i] + "\n£" + str(returnAllItems()[1][i]))
                  l2 = Button(frame, text = "\nAdd To Basket")

                  photo = return_image(returnAllItems()[0][i])
                  fp = io.BytesIO(photo)
                  image = Image.open(fp)
                  render = ImageTk.PhotoImage(image)
                  img = Label(frame, image=render)
                  img.image = render


                  l1.pack()
                  img.pack()
                  l2.pack()
                  
                  # l1.grid(row = i//5 + 1, column = i%5 + 1, sticky = W, pady = 2)
                  # l2.grid(row = i//5 + 1, column = i%5 + 1, sticky = W, pady = 2)

            col_count, row_count = self.grid_size()
            for col in range(col_count):
                  self.grid_columnconfigure(col, weight=1)

            for row in range(row_count):
                  self.grid_rowconfigure(row, weight=1)

   
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
      
      def loadXml(self,):
            loginsToXml()
            





