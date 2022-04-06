import mysql.connector
import shutil
import os
shutil.rmtree('./1')
shutil.rmtree('./2') 
shutil.rmtree('./3')
os.mkdir('./1')
os.mkdir('./2')
os.mkdir('./3')
connection = mysql.connector.connect(host='192.168.255.205',
                                    user='library',
                                    password='123456789')

cursor = connection.cursor()

# 創建資料庫
#cursor.execute("CREATE DATABASE `database`;")


# 取得所有資料庫名稱



# 選擇資料庫
cursor.execute("USE `demo`;")

def RetrieveBlob(ID):
    SQLstatement2 = "SELECT * FROM detect where number = '{0}'"
    cursor.execute(SQLstatement2.format(str(ID)))
    cab = cursor.fetchone()[1]
    SQLstatement2 = "SELECT * FROM detect where number = '{0}'"
    cursor.execute(SQLstatement2.format(str(ID)))
    Myresult = cursor.fetchone()[2]
    storefilepath = "./"+str(cab)+"/{0}.jpg".format(str(ID)) #存到此路徑下名為1的資料夾內
    with open(storefilepath,"wb") as File:
        File.write(Myresult)
        File.close()
        
        
cursor.execute("select count(*) from detect;")
records = cursor.fetchall()
for r in records:
    print(r)    
a, = r
for i in range(1,a+1):
    RetrieveBlob(i)    
        

   

# 創建表格
# cursor.execute('CREATE TABLE `qq`(qq INT);')

cursor.close()
connection.close()