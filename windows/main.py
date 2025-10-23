import tkinter as tk

class Main(tk.TK):
      def __init__(self):
            super().__init__()

      self.attributes('-fullscreen',True)
      self.geometry("1000x1000")
      self.title("E-commerce Application")

      outcolour = "black"
      textcolour = "white"

      #Appearance Selector
      def lightMode():
            self.configure(bg="white")
            global outcolour
            global textcolour
            outcolour = "white"
            textcolour = "black"
            self.update()
            self.update_idletasks()

      def darkMode():
            window.configure(bg="black")
            global outcolour
            global textcolour
            outcolour = "black"
            textcolour = "white"
            window.update()
            window.update_idletasks()
      #Login System
      def login():
            userID = loginText.get("1.0", "end-1c")
            customerProfile = Ecommerce.returnCutomerProfileView()
            customerProfileButton = tk.Label(window, text=customerProfile).place(y=500,x=920,width=400,height=400)


      #Kill Window

      def closeWindow():
            window.destroy()

      loginLabel = tk.Label(window, text="Please Enter User ID").place(y=0,x=920)
      loginText = tk.Text(window, height=1, width=20)
      loginText.place(y=25,x=920)
      loginButton = tk.Button(window, text="Login", command=login).place(y=50,x=940)
      lightButton = tk.Radiobutton(window, text="Light Mode", value=1, command=lightMode).pack(side=tk.RIGHT)
      darkButton = tk.Radiobutton(window, text="Dark Mode", value=2, command=darkMode).pack(side=tk.RIGHT)
      closeButton = tk.Button(window, text="Close", command=closeWindow).pack(side=tk.BOTTOM)

