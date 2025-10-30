import tkinter as tk
import Ecommerce
from .login import Login

class MainWindow(tk.Tk):
      def __init__(self, system):
            super().__init__()
            #self.attributes('-fullscreen',True)
            self.geometry("1000x1000")
            self.title("E-commerce Application")
            self.loginbutton = tk.Button(self, text="Login", command=self.createLoginWindow).place(y=50,x=940)
            self.ecommerceSystem = system
            self.data = tk.Label(self, text=Ecommerce.returnSpecificCustomerProfileView(), height=40, width=120).pack()
   
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
      
            



      # closeButton = tk.Button(self, text="Close", command=self.destroy).pack(side=tk.BOTTOM)

