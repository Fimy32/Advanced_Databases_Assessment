#This file converts the login details from the database into an XML file
import xml.etree.cElementTree as ET
import sqlite3


root = ET.Element("root")
doc = ET.SubElement(root, "doc")


tree = ET.ElementTree(root)
tree.write("logins.xml")



def loginsToXml():
      DB = sqlite3.connect(r"EcommerceDB.db")
      cursor = DB.cursor()
      cursor.execute("SELECT * FROM Logins;")
      get_login_details = cursor.fetchall()

      data = ET.Element('user')

      login = ET.SubElement(data, 'login_details')
      root = ET.Element('users')
      for row in get_login_details:
            s_elem1 = ET.SubElement(login, 'LoginID')
            s_elem2 = ET.SubElement(login, 'Username')
            s_elem3 = ET.SubElement(login, 'Password')
            s_elem1.text = row[0]
            s_elem2.text = row[1]
            s_elem3.text = row[2]

      b_xml = ET.tostring(data)

      with open("logins.xml", "wb") as f:
            f.write(b_xml)


