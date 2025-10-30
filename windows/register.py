import tkinter as tk
import Ecommerce

class register(tk.Tk):
      def __init__(self, system):
            super().__init__()
            self.ecommerceSystem = system 

            self.userNameLabe = tk.Label(self, text="Username").pack()
            self.userNameText = tk.Text(self, height=1, width=20)
            self.userNameText.pack()
            self.passwordLabe = tk.Label(self, text="Password").pack()
            self.passwordText = tk.Text(self, height=1, width=20)
            self.passwordText.pack()
            self.loginButton = tk.Button(self, text="Register", command=self.register).pack()
            self.wrongText = tk.Label(self, text="Invalid Username or Password", fg="red")

      #Login System
      def register(self):
            for ID in self.ecommerceSystem.users:
                  if len(self.userNameText.get("1.0", "end-1c")) > 0 and len(self.passwordText.get("1.0", "end-1c")) > 0:
                        self.ecommerceSystem.users[(self.userNameText.get("1.0", "end-1c"), self.passwordText.get("1.0", "end-1c"))] = Ecommerce.generateUserID()
                        self.destroy()
                  else:
                        self.wrongText.pack()





            # userID = self.loginText.get("1.0", "end-1c")
            # customerProfile = Ecommerce.returnCutomerProfileView()
            # customerProfileButton = tk.Label(self, text=customerProfile).place(y=500,x=920,width=400,height=400)



      # closeButton = tk.Button(self, text="Close", command=self.destroy).pack(side=tk.BOTTOM)
            #       loginLabel = tk.Label(self, text="Please Enter User ID").place(y=0,x=920)
            # loginText = tk.Text(self, height=1, width=20)
            # loginText.place(y=25,x=920)
            # loginButton = tk.Button(self, text="Login", command=self.login).place(y=50,x=940)