from Ecommerce import * 
import tkinter as tk

def refresh(self):
    self.destroy()
    self.__init__()

window = tk.Tk()
window.title("E-commerce Application")

outcolour = "black"
textcolour = "white"

#Login System
def login():
      userID = loginText.get("1.0",END)

loginLabel = tk.Label(window, text="Please Enter User ID").pack()
loginText = tk.Text(window, height=1, width=20).pack()
loginButton = tk.Button(window, text="Login", command=login, background=outcolour).pack()

#Appearance Selector
def lightMode():
      window.configure(bg="white")
      global outcolour
      global textcolour
      outcolour = "white"
      textcolour = "black"
      window.update()
      window.update_idletasks()

def darkMode():
      window.configure(bg="black")
      global outcolour
      global textcolour
      outcolour = "black"
      textcolour = "white"
      window.update()
      window.update_idletasks()


lightButton = tk.Radiobutton(window, text="Light Mode", value=1, command=lightMode).pack()
darkButton = tk.Radiobutton(window, text="Dark Mode", value=2, command=darkMode).pack()




window.mainloop()