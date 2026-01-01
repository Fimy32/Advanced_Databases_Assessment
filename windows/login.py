import tkinter as tk
from .register import register
from ecommerceDBHandler import *
import hashlib

class Login(tk.Tk):
      def __init__(self, system):
            super().__init__()
            self.ecommerceSystem = system 
            #self.attributes('-fullscreen',True)
            self.title("E-commerce Application")     
            self.userNameLabel = tk.Label(self, text="Username").pack()
            self.userNameText = tk.Text(self, height=1, width=20)
            self.userNameText.pack()
            self.passwordLabel = tk.Label(self, text="Password").pack()
            self.passwordText = tk.Text(self, height=1, width=20)
            self.passwordText.pack()
            self.loginButton = tk.Button(self, text="Login", command=self.login).pack()
            self.registerButton = tk.Button(self, text="Register", command=self.createRegisterWindow).pack()
            self.wrongText = tk.Label(self, text="Invalid Username or Password", fg="red")



      #Login System
      #This verifies that the login uses an existing username and password from the database
      def login(self):
            for ID in returnLoginIDs():
                  print("UserName:",hashlib.sha256(self.userNameText.get("1.0", "end-1c").encode()).hexdigest(), returnLoginDetailsByID(ID)[0], "\nPassword:", hashlib.sha256(self.passwordText.get("1.0", "end-1c").encode()).hexdigest(), returnLoginDetailsByID(ID)[1])
                  if (hashlib.sha256(self.userNameText.get("1.0", "end-1c").encode()).hexdigest() == returnLoginDetailsByID(ID)[0] and 
                  hashlib.sha256(self.passwordText.get("1.0", "end-1c").encode()).hexdigest() == returnLoginDetailsByID(ID)[1]):
                        print("LOG ON SUCCESSFUL")
                        self.ecommerceSystem.currentUserID = ID
                        self.ecommerceSystem.currentUserName = self.userNameText.get("1.0", "end-1c")
                        #main.createMainWindow()
                        self.destroy()
                  else:
                        self.wrongText.pack()

      def createRegisterWindow(self):
            registerWindow = register(self.ecommerceSystem)
            registerWindow.mainloop()




            # userID = self.loginText.get("1.0", "end-1c")
            # customerProfile = Ecommerce.returnCutomerProfileView()
            # customerProfileButton = tk.Label(self, text=customerProfile).place(y=500,x=920,width=400,height=400)



      # closeButton = tk.Button(self, text="Close", command=self.destroy).pack(side=tk.BOTTOM)
            #       loginLabel = tk.Label(self, text="Please Enter User ID").place(y=0,x=920)
            # loginText = tk.Text(self, height=1, width=20)
            # loginText.place(y=25,x=920)
            # loginButton = tk.Button(self, text="Login", command=self.login).place(y=50,x=940)