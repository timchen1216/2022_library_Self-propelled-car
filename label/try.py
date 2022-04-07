import mysql.connector
import shutil
import os
shutil.rmtree('C:/Users/timch\MyPython/2022_library_Self-propelled-car/1')
shutil.rmtree('C:/Users/timch\MyPython/2022_library_Self-propelled-car/2') 
shutil.rmtree('C:/Users/timch\MyPython/2022_library_Self-propelled-car/3')
os.mkdir('C:/Users/timch\MyPython/2022_library_Self-propelled-car/1')
os.mkdir('C:/Users/timch\MyPython/2022_library_Self-propelled-car/2')
os.mkdir('C:/Users/timch\MyPython/2022_library_Self-propelled-car/3')
total = []
connection = mysql.connector.connect(host='192.168.146.205',
                                    user='library',
                                    password='123456789')

cursor = connection.cursor()

# 創建資料庫
#cursor.execute("CREATE DATABASE `database`;")


# 取得所有資料庫名稱



# 選擇資料庫
cursor.execute("USE `demo`;")

def RetrieveBlob(ID,total):
    SQLstatement2 = "SELECT * FROM detect where number = '{0}'"
    cursor.execute(SQLstatement2.format(str(ID)))
    cab = cursor.fetchone()[1]
    SQLstatement2 = "SELECT * FROM detect where number = '{0}'"
    cursor.execute(SQLstatement2.format(str(ID)))
    Myresult = cursor.fetchone()[2]
    if cab == 1:
        name = ID
    elif cab == 2:
        name = ID - total[0]
    else :
        name = ID - total[0] - total[1]
    storefilepath = "./"+str(cab)+"/{0}.jpg".format(str(name)) #存到此路徑下名為1的資料夾內
    with open(storefilepath,"wb") as File:
            File.write(Myresult)
            File.close()
    
for i in range(1,4):    
   cursor.execute("select count(*) from detect where cabinet ="+str(i)+";")
   records = cursor.fetchall()
   for r in records:
      a, = r
      total.append(a)
      print (total)

cursor.execute("select count(*) from detect;")
records = cursor.fetchall()
for r in records:
   print(r)    
   b, = r
   
for i in range(1,b+1):
    RetrieveBlob(i,total)    
        


# 創建表格
# cursor.execute('CREATE TABLE `qq`(qq INT);')

cursor.close()
connection.close()