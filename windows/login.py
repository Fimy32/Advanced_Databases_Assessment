import tkinter as tk
import Ecommerce

class Login(tk.Tk):
      def __init__(self, system):
            super().__init__()
            self.ecommerceSystem = system 
            #self.attributes('-fullscreen',True)
            self.title("E-commerce Application")     
            userNameLabel = tk.Label(self, text="Username").pack()
            userNameText = tk.Text(self, height=1, width=20)
            userNameText.pack()
            passwordLabel = tk.Label(self, text="Password").pack()
            passwordText = tk.Text(self, height=1, width=20)
            passwordText.pack()
            loginButton = tk.Button(self, text="Login", command=self.login).pack()

            userNameLabel2 = tk.Label(self, text="----------").pack()
            userNameLabel2 = tk.Label(self, text="Username").pack()
            userNameText2 = tk.Text(self, height=1, width=20)
            userNameText2.pack()
            passwordLabel2 = tk.Label(self, text="Password").pack()
            passwordText2 = tk.Text(self, height=1, width=20)
            passwordText2.pack()
            loginButton2 = tk.Button(self, text="Register", command=self.login).pack()

      #Login System
      def login(self):
            for ID in self.ecommerceSystem.users:
                  if self.loginText.get("1.0", "end-1c") in ID[0] and self.passwordText.get("1.0", "end-1c") in ID[1]:
                        self.destroy()





            # userID = self.loginText.get("1.0", "end-1c")
            # customerProfile = Ecommerce.returnCutomerProfileView()
            # customerProfileButton = tk.Label(self, text=customerProfile).place(y=500,x=920,width=400,height=400)



      # closeButton = tk.Button(self, text="Close", command=self.destroy).pack(side=tk.BOTTOM)
            #       loginLabel = tk.Label(self, text="Please Enter User ID").place(y=0,x=920)
            # loginText = tk.Text(self, height=1, width=20)
            # loginText.place(y=25,x=920)
            # loginButton = tk.Button(self, text="Login", command=self.login).place(y=50,x=940)