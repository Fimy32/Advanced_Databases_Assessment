import ecommerceSystem
import windows
import windows.mainWindow

mainEcommerceSystem = ecommerceSystem.EcommerceSystem()

mainWindow = windows.mainWindow.MainWindow(mainEcommerceSystem)
mainWindow.mainloop()
