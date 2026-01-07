from tkinter import *
import tkinter as tk
from ecommerceDBHandler import *
import hashlib
import matplotlib.pyplot as plt

class Stock(tk.Tk):
      def __init__(self, system):
            super().__init__()
            self.ecommerceSystem = system
            self.title("Stock")
            self.canvas = Canvas(self, width=550, height=820)
            self.canvas.pack()
            start_point_text_x=30
            start_point_text_y=110

            start_point_rect_x=60
            start_point_rect_y=100

            step=30
            count =0
            print(returnStock())
            for row in returnStock():
                  plt.xticks(rotation=90)
                  self.canvas.create_text(start_point_text_x, start_point_text_y+(step*count), text=row[1])
                  a = self.canvas.create_rectangle(start_point_rect_x, start_point_rect_y+(step*count), 60+int(row[2]), 120+(step*count), fill='red')
                  self.canvas.create_text(80+int(row[2]), 110+(step*count),text=str(row[2])+str("%"))
                  count = count+1 
