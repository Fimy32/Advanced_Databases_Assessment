#This file converts the login details from the database into an XML file and vice versa
import xml.etree.cElementTree as ET
import sqlite3

def loginsToXml():
      DB = sqlite3.connect(r"EcommerceDB.db")
      cursor = DB.cursor()
      cursor.execute("SELECT * FROM Logins;")
      get_login_details = cursor.fetchall()
      root = ET.Element('users')
      for row in get_login_details:
            login = ET.SubElement(root, 'login_details')
            s_elem1 = ET.SubElement(login, 'LoginID')
            s_elem2 = ET.SubElement(login, 'Username')
            s_elem3 = ET.SubElement(login, 'Password')
            s_elem1.text = str(row[0])
            s_elem2.text = str(row[1])
            s_elem3.text = str(row[2])
      b_xml = ET.tostring(root)
      with open("logins.xml", "wb") as f:
            f.write(b_xml)

def xmltologins():
      tree = ET.parse('logins.xml')
      root = tree.getroot()
      DB = sqlite3.connect(r"EcommerceDB.db")
      cursor = DB.cursor()
      for login_details in root.findall('login_details'):
            login_id = login_details.find('LoginID').text
            username = login_details.find('Username').text
            password = login_details.find('Password').text
            cursor.execute("INSERT OR REPLACE INTO Logins (LoginID, Username, Password) VALUES (?, ?, ?);", (login_id, username, password))
      DB.commit()
      DB.close()


      