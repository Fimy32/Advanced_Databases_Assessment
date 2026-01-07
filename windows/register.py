import tkinter as tk
import ecommerceDBHandler

class Register(tk.Toplevel):
      def __init__(self, system):
            super().__init__()
            self.ecommerceSystem = system
            self.title("Register")
            self.userNameLabel = tk.Label(self, text="Username")
            self.userNameLabel.pack()
            self.userNameText = tk.Text(self, height=1, width=20)
            self.userNameText.pack()
            self.passwordLabel = tk.Label(self, text="Password")
            self.passwordLabel.pack()
            self.passwordText = tk.Text(self, height=1, width=20)
            self.passwordText.pack()
            self.firstNameLabel = tk.Label(self, text="First Name")
            self.firstNameLabel.pack()
            self.firstNameText = tk.Text(self, height=1, width=20)
            self.firstNameText.pack()
            self.secondNameLabel = tk.Label(self, text="Second Name")
            self.secondNameLabel.pack()
            self.secondNameText = tk.Text(self, height=1, width=20)
            self.secondNameText.pack()
            self.addressLabel = tk.Label(self, text="Address")
            self.addressLabel.pack()
            self.addressText = tk.Text(self, height=1, width=20)
            self.addressText.pack()

            self.registerButton = tk.Button(self, text="Register", command=self.registerUser)
            self.registerButton.pack()

      #The registration proccess, validates the user has not left a field empty. 
      #THis ensures empty fields aren't added to the Database
      def registerUser(self):
            import hashlib
            username = self.userNameText.get("1.0", "end-1c").strip()
            password = self.passwordText.get("1.0", "end-1c").strip()
            firstname = self.firstNameText.get("1.0", "end-1c").strip()
            secondname = self.secondNameText.get("1.0", "end-1c").strip()
            address = self.addressText.get("1.0", "end-1c").strip()
            if not username or not password:
                  self.wrongText.config(text="Username and Password required")
                  self.wrongText.pack()
                  return
            ecommerceDBHandler.register(firstname, secondname, address,hashlib.sha256(username.encode()).hexdigest(),hashlib.sha256(password.encode()).hexdigest())
            self.destroy()





            # userID = self.loginText.get("1.0", "end-1c")
            # customerProfile = Ecommerce.returnCutomerProfileView()
            # customerProfileButton = tk.Label(self, text=customerProfile).place(y=500,x=920,width=400,height=400)



      # closeButton = tk.Button(self, text="Close", command=self.destroy).pack(side=tk.BOTTOM)
            #       loginLabel = tk.Label(self, text="Please Enter User ID").place(y=0,x=920)
            # loginText = tk.Text(self, height=1, width=20)
            # loginText.place(y=25,x=920)
            # loginButton = tk.Button(self, text="Login", command=self.login).place(y=50,x=940)