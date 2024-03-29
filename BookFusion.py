# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Rishav\Desktop\guiBook\dashboard.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import os,sys
import sqlite3
import datetime
import time


import tempfile
import win32api
import win32print


   
 

try:
    os.makedirs("database")
except OSError:
    if not os.path.isdir("database"):
        raise
try:
    # Create target Directory
    os.mkdir("recipts")
except FileExistsError:
    pass

dat= sqlite3.connect('database/data.db')
curs = dat.cursor()
curs.execute('drop table if exists Tempp')
dat.commit()
curs.execute("CREATE TABLE if not exists Tempp (id INTEGER PRIMARY KEY AUTOINCREMENT,title STRING,quantity INTEGER,Price float,amount float,bkid INTEGER)")
dat.commit()
sql1=("CREATE TABLE if not exists BookDet (ID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, Price float);")
curs.execute(sql1)
dat.commit()
sql2=("CREATE TABLE if not exists Inventory (ID INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER, quantity INTEGER, FOREIGN KEY(book_id) REFERENCES BookDet(ID));")
curs.execute(sql2)
dat.commit()
sql3=("CREATE TABLE if not exists Transactions (ID INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER, quantity INTEGER, customer STRING, date text, time text, FOREIGN KEY(book_id) REFERENCES BookDet(ID));")
curs.execute(sql3)
dat.commit()


det_dict = {}
x=0

class Ui_MainWindow(object):
    


    


    def loadBooks(self):
        fetched_books=dat.execute("SELECT a.title,a.Price,b.quantity FROM BookDet a INNER JOIN Inventory b ON b.book_id=a.ID")
        fetched_books_inven=dat.execute("SELECT a.title,a.author,a.Price,b.quantity FROM BookDet a INNER JOIN Inventory b ON b.book_id=a.ID")
        fetched_trans=dat.execute("SELECT b.title,a.quantity,a.customer,a.date,a.time FROM Transactions a INNER JOIN BookDet b ON a.book_id=b.ID ORDER BY a.ID DESC")
        self.ui_table.setRowCount(0)
        self.i_table.setRowCount(0)
        self.i_trnsactions.setRowCount(0)
        
        for row_number, row_data in enumerate(fetched_books):
            self.ui_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui_table.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
                
        for row_number, row_data in enumerate(fetched_books_inven):
            self.i_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.i_table.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        for row_number, row_data in enumerate(fetched_trans):
            self.i_trnsactions.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.i_trnsactions.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
                 


    def addNewBook(self):
        try:
            bk_ttl=self.ui_ab_bnm.text()
            bk_ath=self.ui_ab_ath.text()
            bk_prc=self.ui_ab_pr.text()
            bk_qty=self.ui_ab_qt.text()
            bk_prc=float(bk_prc)
            bk_qty=int(bk_qty)
        
            try:
                curs.execute("INSERT into BookDet(title,author,Price) VALUES (?,?,?);",(bk_ttl,bk_ath,bk_prc))
                dat.commit()
                try:                
                    curs.execute("SELECT ID from BookDet WHERE ID = (SELECT MAX(ID) FROM BookDet);")
                    Id=curs.fetchone()
                    curs.execute("INSERT into Inventory (book_id,quantity) VALUES (?,?);",(Id[0],bk_qty))
                    dat.commit()
                    print("======One Detail Inserted into Database======")
                    self.loadBooks()
                    self.additemCB()
                except:
                    curs.rollback()
                    print("======Some ERROR occured !!!!! ======")                
            except:
                curs.rollback()
                print("======Some ERROR occured !!!!! ======")
        except:
            print("Insufficient data")


        
        
    def additemCB(self):        
        curs.execute("SELECT title FROM BookDet")
        self.ui_ep_bnm.clear()
        self.ui_eq_bnm.clear()
        self.ui_db_bnm.clear()
        self.s_bnm.clear() 
        while True:  
            data=curs.fetchone()
            if data == None:
                break
            self.ui_ep_bnm.addItem(str(data[0]))
            index1 = self.ui_ep_bnm.findData(self.ui_ep_bnm.currentText())
            self.ui_ep_bnm.setCurrentIndex(index1)
            
            self.ui_eq_bnm.addItem(str(data[0]))
            index2 = self.ui_eq_bnm.findData(self.ui_eq_bnm.currentText())
            self.ui_eq_bnm.setCurrentIndex(index2)
            
            self.ui_db_bnm.addItem(str(data[0]))
            index3 = self.ui_db_bnm.findData(self.ui_db_bnm.currentText())
            self.ui_db_bnm.setCurrentIndex(index3)
            
            self.s_bnm.addItem(str(data[0]))
            index4 = self.s_bnm.findData(self.s_bnm.currentText())
            self.s_bnm.setCurrentIndex(index4)
            
                                    

    def EditPrice(self):
        try:
            bk_ttl=self.ui_ep_bnm.currentText()
            bk_prc=self.ui_ep_pr.text()
            bk_prc=float(bk_prc)
            curs.execute("SELECT Price FROM BookDet WHERE title=(?);",(bk_ttl,))
            bk_prc_o=curs.fetchone()                                        
            print("\nCurrent price of the Book is : {}".format(bk_prc_o[0]))
            try:                                            
                curs.execute("UPDATE BookDet SET Price=(?) Where title==(?);",(bk_prc,bk_ttl))
                dat.commit()
                self.loadBooks()
                print('============Price of Book "{}" has Been Updated with new price {}============'.format(bk_ttl,bk_prc))
            except:             
                print("Some Error Occured")
                dat.rollback()
        except:
            print("Some Error Occured")
            
            

    def UpdQty(self):
        try:
            bk_ttl=self.ui_eq_bnm.currentText()
            bk_qty=self.ui_eq_qt.text()
            bk_qty=int(bk_qty)

            try:
                curs.execute("SELECT b.quantity,a.ID FROM BookDet a INNER JOIN Inventory b ON b.book_id=a.ID WHERE a.title=(?);",(bk_ttl,))
                bk_qt_o=curs.fetchone()
                print("\nCurrent Quantity of the Book is : {}".format(bk_qt_o[0]))
                try:
                    
                    curs.execute("UPDATE Inventory SET quantity=quantity+(?) Where book_id==(?);",(bk_qty,bk_qt_o[1]))
                    dat.commit()
                    self.loadBooks()
                    print('\n\n============New Quantity of Book "{}" is {}============'.format(bk_ttl,(bk_qt_o[0]+bk_qty)))
                except:
                    print("Some Error Occured")
                    dat.rollback()
            except:
                print("\nPlease Enter a Valid Name")
        except:
            print("Some Error Occured")

        
    def Delete(self):
        bk_ttl=self.ui_db_bnm.currentText()

        try:
            curs.execute("SELECT ID FROM BookDet WHERE title=(?);",(bk_ttl,))
            bk_qt_o=curs.fetchone()
            
            try:
                curs.execute("DELETE FROM BookDet WHERE title=?;",(bk_ttl,))
                dat.commit()
                try:
                
                    curs.execute("Delete FROM Inventory Where book_id=(?);",(bk_qt_o[0],))
                    dat.commit()
                    self.loadBooks()
                    self.additemCB()
                    print("One Book Deleted")
                
                except:
                    print("Some Error Occured 1")
                    dat.rollback()
            except:
                print("Some Error Occured 2")
                dat.rollback()
                
        except:
            print("\nPlease Enter a Valid Name")

                                                
    def AddItemRecipt(self):
        try:
            fetched_books_rcpt=dat.execute("SELECT title,quantity,Price,amount FROM Tempp")        
            self.s_table.setRowCount(0)
            total_pr=dat.execute("SELECT sum(amount) from Tempp")
            total_pr=total_pr.fetchone()[0]
            total_it=dat.execute("SELECT sum(quantity) from Tempp")
            total_it=total_it.fetchone()[0]
            
            total_pr=float("{0:.2f}".format(total_pr))
            print(total_pr)
            print(total_it)
            for row_number, row_data in enumerate(fetched_books_rcpt):
                self.s_table.insertRow(row_number)
                
                for column_number, data in enumerate(row_data):
                    self.s_table.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
                    
                #self.s_table.setItem(row_number,column_number+1,QtWidgets.QTableWidgetItem(QtWidgets.QPushButton))
                    
                
            self.s_table.insertRow(row_number+1)
            self.s_table.insertRow(row_number+2)
            self.s_table.setItem(row_number+2,0,QtWidgets.QTableWidgetItem(str("Total Item = ")))
            self.s_table.setItem(row_number+2,1,QtWidgets.QTableWidgetItem(str(total_it)))
            self.s_table.setItem(row_number+2,2,QtWidgets.QTableWidgetItem(str("Total Payable = ")))
            self.s_table.setItem(row_number+2,3,QtWidgets.QTableWidgetItem(str(total_pr)))
        except:
            print("Error occured")
            pass
        

    
    def AddItem(self):
        try:
        
            bknm=self.s_bnm.currentText()
            bkqty=self.s_bqty.text()        
            curs.execute("SELECT ID,Price FROM BookDet WHERE title= ?;",(bknm,))
            bkprc=curs.fetchone()
            bkid=bkprc[0]
            bkprc=bkprc[1]
            
            bkid=int(bkid)
            print("book id{}".format(bkid))
            print(bkprc)
            bkamnt=bkprc*float(bkqty)
            print(bkamnt)
            bkamnt=float("{0:.2f}".format(bkamnt))
            print(bkamnt)
            curs.execute("INSERT into Tempp (title,Price,quantity,amount,bkid) VALUES (?,?,?,?,?);",(bknm,bkprc,bkqty,bkamnt,bkid))
            dat.commit()
            print("Done")
            self.AddItemRecipt()
        except:
            print("Error occured")
            pass
        


    def finalrecipt(self):
        
        rcpt_books=curs.execute("SELECT * FROM Tempp")
        rcpt_cust=self.s_cust_name.text()
        
        rcpt_books=rcpt_books.fetchall()
        if(len(rcpt_books) > 0 and rcpt_cust!=""):
            try:
        
                
                data_to_print=[('Book Id','Book Title','Quantity','Rate','Total Price'),]
                total_amount = 0.0
                now = datetime.datetime.now()
                for row_number, row_data in enumerate(rcpt_books):
                    data_to_print.append((row_data[0],row_data[1],row_data[2],row_data[3],row_data[4]))
                    total_amount = total_amount+int(row_data[4])
                    rcpt_qty=row_data[2]
                    rcpt_ttl=row_data[1]
                    rcpt_id=row_data[5]
                    rcpt_qty=int(rcpt_qty)
                    rcpt_id=int(rcpt_id)
                    print("id:\t{}\t{}\t{}".format(rcpt_id,rcpt_ttl,rcpt_qty,))                
                    print("quantity :{}".format(rcpt_qty))
                    print("Title :{}".format(rcpt_ttl))
                   
                    curs.execute("UPDATE Inventory SET quantity=quantity-(?) WHERE book_id=(?);",(rcpt_qty,rcpt_id))
                    curs.execute("INSERT into Transactions (book_id,quantity,customer,date,time) VALUES (?,?,?,date('now'),time('12:00', 'localtime'));",(rcpt_id,rcpt_qty,rcpt_cust))
                    
                    print("updated book {}".format(row_number+1))
                dat.commit()

                
                dir_path = os.path.dirname(os.path.realpath(__file__))
                timestamp = str(time.time()*1000.0)
                recipt_name = dir_path+'/recipts/'+rcpt_cust+timestamp+".txt"
                file= open(recipt_name,"w+")
                col_width = max(len(str(word)) for row in data_to_print for word in row) + 2  # padding
                
                string_to_print = ""
                string_to_print = string_to_print + ("_")*col_width*5+("\nCustomer Name:\t{}\n".format(rcpt_cust))+("_")*col_width*5+"\n"
                for row in data_to_print:
                    string_to_print = string_to_print + ("".join(str(word).ljust(col_width) for word in row))+"\n"
                string_to_print = string_to_print +("_")*col_width*5 +("\n")+ (((" ")*col_width*3)+("Total :").ljust(col_width)+str(total_amount))
                
                print(string_to_print)
                file.write(string_to_print)
                file.close()
                win32api.ShellExecute (
                  0,
                  "print",
                  recipt_name,
                  #
                  # If this is None, the default printer will
                  # be used anyway.
                  #
                  '/d:"%s"' % win32print.GetDefaultPrinter (),
                  ".",
                  0
                )

                
                self.loadBooks()
                self.delrecipt()
            except:
                print("Error")
                pass
        else:
            print("Customer Name/Item not Added")


    
                
    def delrecipt(self):
        curs.execute('drop table if exists Tempp')
        dat.commit()
        curs.execute("CREATE TABLE if not exists Tempp (id INTEGER PRIMARY KEY AUTOINCREMENT,title STRING,quantity INTEGER,Price float,amount float,bkid INTEGER)")
        dat.commit()
        self.s_table.setRowCount(0)
        
    def searchInven(self):
        strn=self.i_in_txt.text()
        strn=str(strn)
        self.i_table.setRowCount(0)
        fetched_books_inven=dat.execute("SELECT a.title,a.author,a.Price,b.quantity FROM BookDet a INNER JOIN Inventory b ON b.book_id=a.ID")
        
        x=0
        for row_number, row_data in enumerate(fetched_books_inven):
            
            if(strn in str(row_data[0]) or strn in str(row_data[1]) or strn in str(row_data[2]) or strn in str(row_data[3])):
                print(row_data[0])
                print(row_data[1])
                
                print(x)
                self.i_table.insertRow(x)
                for column_number, data in enumerate(row_data):                    
                    self.i_table.setItem(x,column_number,QtWidgets.QTableWidgetItem(str(data)))
                x=x+1
                
        strn=None
        x=0
        
                
    def searchTrans(self):
        strn=self.i_tr_txt.text()
        strn=str(strn)
        self.i_trnsactions.setRowCount(0)
        fetched_trans=dat.execute("SELECT b.title,a.quantity,a.customer,a.date,a.time FROM Transactions a INNER JOIN BookDet b ON a.book_id=b.ID ORDER BY a.ID DESC")
        
        x=0
        
        for row_number, row_data in enumerate(fetched_trans):
            
            if(strn in row_data[0] or strn in str(row_data[1]) or strn in row_data[2] or strn in row_data[3] or strn in row_data[4] ):
                
                self.i_trnsactions.insertRow(x)                
                for column_number, data in enumerate(row_data):                    
                    self.i_trnsactions.setItem(x,column_number,QtWidgets.QTableWidgetItem(str(data)))
                x=x+1
        strn=None
        x=0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(972, 635)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.tab = QtWidgets.QTabWidget(self.centralwidget)
        self.tab.setEnabled(True)
        self.tab.setTabPosition(QtWidgets.QTabWidget.North)
        self.tab.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tab.setObjectName("tab")
        self.sellBook = QtWidgets.QWidget()
        self.sellBook.setAccessibleName("")
        self.sellBook.setObjectName("sell Item")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.sellBook)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.splitter = QtWidgets.QSplitter(self.sellBook)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(150, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        spacerItem1 = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.s_bnm = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.s_bnm.setObjectName("s_bnm")

        #Updated
        self.s_bnm.setEditable(True)
        
        self.horizontalLayout_3.addWidget(self.s_bnm)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.s_bqty = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.s_bqty.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.s_bqty.setObjectName("s_bqty")
        self.horizontalLayout_4.addWidget(self.s_bqty)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.s_ok = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.s_ok.setFont(font)
        self.s_ok.setObjectName("s_ok")

         #Updated
        self.s_ok.clicked.connect(self.AddItem)
        self.s_ok.clicked.connect(self.s_bnm.clear)
        self.s_ok.clicked.connect(self.s_bqty.clear)
        self.s_ok.clicked.connect(self.additemCB)

        
        self.horizontalLayout_5.addWidget(self.s_ok)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_21.addLayout(self.verticalLayout_3)
        spacerItem7 = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem7)
        self.verticalLayout_4.addLayout(self.horizontalLayout_21)
        spacerItem8 = QtWidgets.QSpacerItem(150, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_4.addItem(spacerItem8)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem9 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem9)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        spacerItem10 = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem10)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.s_table = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.s_table.setRowCount(50)
        self.s_table.setColumnCount(5)

        #Updated
        self.s_table.setHorizontalHeaderLabels(["Title","Quantity","Price","Amount","Action"])
        
        self.s_table.setObjectName("s_table")        
        self.verticalLayout.addWidget(self.s_table)
        
        #Updated
        self.s_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem11)
        self.label_19 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout.addWidget(self.label_19)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem12)
        self.s_cust_name = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.s_cust_name.setObjectName("s_cust_name")
        self.horizontalLayout.addWidget(self.s_cust_name)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem13)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem14)
        self.s_recipt_ok = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.s_recipt_ok.setFont(font)
        self.s_recipt_ok.setObjectName("s_recipt_ok")

        #Update
        self.s_recipt_ok.clicked.connect(self.finalrecipt)

        self.horizontalLayout_2.addWidget(self.s_recipt_ok)
        self.s_recipt_clear = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.s_recipt_clear.setFont(font)
        self.s_recipt_clear.setObjectName("s_recipt_clear")
        self.horizontalLayout_2.addWidget(self.s_recipt_clear)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem15)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_22.addLayout(self.verticalLayout)
        spacerItem16 = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem16)
        self.verticalLayout_5.addLayout(self.horizontalLayout_22)
        spacerItem17 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem17)
        self.verticalLayout_15.addWidget(self.splitter)
        self.label.raise_()
        self.verticalLayoutWidget.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.tab.addTab(self.sellBook, "")
        self.Inventory = QtWidgets.QWidget()
        self.Inventory.setObjectName("Inventory")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.Inventory)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.splitter_2 = QtWidgets.QSplitter(self.Inventory)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.widget = QtWidgets.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_18 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_16.addWidget(self.label_18)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem18)
        self.label_21 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_26.addWidget(self.label_21)
        spacerItem19 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem19)
        self.i_in_txt = QtWidgets.QLineEdit(self.widget)
        self.i_in_txt.setObjectName("i_in_txt")
        self.horizontalLayout_26.addWidget(self.i_in_txt)
        
        self.i_in_ok = QtWidgets.QPushButton(self.widget)
        self.i_in_ok.setObjectName("i_in_ok")
        #Updated
        self.i_in_ok.clicked.connect(self.searchInven)
        
        self.horizontalLayout_26.addWidget(self.i_in_ok)
        spacerItem20 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem20)

#updated Button

        self.i_in_can = QtWidgets.QPushButton(self.widget)
        self.i_in_can.setObjectName("i_in_can")
        self.horizontalLayout_26.addWidget(self.i_in_can)
        self.i_in_can.clicked.connect(self.loadBooks)
        self.i_in_can.clicked.connect(self.i_in_txt.clear)
        
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem21)
#^updated Button        
        self.verticalLayout_16.addLayout(self.horizontalLayout_26)
        self.i_table = QtWidgets.QTableWidget(self.widget)
        
        self.i_table.setObjectName("i_table")
        
        #updated
        self.i_table.setColumnCount(4)
        self.i_table.setHorizontalHeaderLabels(["Title","Author", "Price", "Quantity"])
        self.i_table.setRowCount(0)
        self.i_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        self.verticalLayout_16.addWidget(self.i_table)
        self.widget1 = QtWidgets.QWidget(self.splitter_2)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_20 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_17.addWidget(self.label_20)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem21)
        self.label_22 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_27.addWidget(self.label_22)
        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem22)
        self.i_tr_txt = QtWidgets.QLineEdit(self.widget1)
        self.i_tr_txt.setObjectName("i_tr_txt")
        self.horizontalLayout_27.addWidget(self.i_tr_txt)
        self.i_tr_ok = QtWidgets.QPushButton(self.widget1)
        self.i_tr_ok.setObjectName("i_tr_ok")
        #Updated
        self.i_tr_ok.clicked.connect(self.searchTrans)
        
        self.horizontalLayout_27.addWidget(self.i_tr_ok)
        spacerItem23 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem23)

        self.i_tr_can = QtWidgets.QPushButton(self.widget1)
        self.i_tr_can.setObjectName("i_tr_can")
        
        #Updated
        self.i_tr_can.clicked.connect(self.i_tr_txt.clear)
        self.i_tr_can.clicked.connect(self.loadBooks)

                                    
        self.horizontalLayout_27.addWidget(self.i_tr_can)
        self.i_tr_can.clicked.connect(self.loadBooks)
        
        spacerItem25 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem25)

        
        self.verticalLayout_17.addLayout(self.horizontalLayout_27)
        self.i_trnsactions = QtWidgets.QTableWidget(self.widget1)
        
        self.i_trnsactions.setObjectName("i_trnsactions")
        self.i_trnsactions.setColumnCount(5)

        #updated
        self.i_trnsactions.setHorizontalHeaderLabels(["Title","Quantity", "Customer", "Date","Time"])
        
        self.i_trnsactions.setRowCount(0)
        self.verticalLayout_17.addWidget(self.i_trnsactions)
        self.verticalLayout_18.addWidget(self.splitter_2)
        self.tab.addTab(self.Inventory, "")
        self.updateinventory = QtWidgets.QWidget()
        self.updateinventory.setObjectName("updateinventory")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.updateinventory)
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem24 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem24)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem25 = QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem25)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.updateinventory)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(True)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.ui_table = QtWidgets.QTableWidget(self.updateinventory)
        self.ui_table.setRowCount(50)
        self.ui_table.setColumnCount(3)
        
        #Updated
        self.ui_table.setHorizontalHeaderLabels(["Title", "Price", "Quantity"])
        
        self.ui_table.setObjectName("ui_table")
        self.verticalLayout_2.addWidget(self.ui_table)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        spacerItem26 = QtWidgets.QSpacerItem(50, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem26)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        spacerItem27 = QtWidgets.QSpacerItem(2, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem27)
        self.horizontalLayout_25.addLayout(self.verticalLayout_6)
        spacerItem28 = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem28)
        self.splitter_4 = QtWidgets.QSplitter(self.updateinventory)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.widget2 = QtWidgets.QWidget(self.splitter_4)
        self.widget2.setObjectName("widget2")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_6 = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_13.addWidget(self.label_6)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.ui_ep_bnm = QtWidgets.QComboBox(self.widget2)
        self.ui_ep_bnm.setObjectName("ui_ep_bnm")

        
        #Updated
        self.ui_ep_bnm.setEditable(True)
        
        self.horizontalLayout_6.addWidget(self.ui_ep_bnm)
        self.verticalLayout_13.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        spacerItem29 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem29)
        self.ui_ep_pr = QtWidgets.QLineEdit(self.widget2)
        self.ui_ep_pr.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.ui_ep_pr.setObjectName("ui_ep_pr")
        self.horizontalLayout_8.addWidget(self.ui_ep_pr)
        self.verticalLayout_13.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.ui_ep_ok = QtWidgets.QPushButton(self.widget2)
        self.ui_ep_ok.setObjectName("ui_ep_ok")

        #Updated        
        self.ui_ep_ok.clicked.connect(self.EditPrice)
        
        self.horizontalLayout_24.addWidget(self.ui_ep_ok)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_24.addWidget(self.pushButton_6)
        self.verticalLayout_13.addLayout(self.horizontalLayout_24)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.splitter_4)
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        spacerItem30 = QtWidgets.QSpacerItem(13, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_12.addItem(spacerItem30)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        spacerItem31 = QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem31)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_11.addWidget(self.label_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.ui_eq_bnm = QtWidgets.QComboBox(self.verticalLayoutWidget_6)
        self.ui_eq_bnm.setObjectName("ui_eq_bnm")

        #updated
        self.ui_eq_bnm.setEditable(True)
        
        self.horizontalLayout_9.addWidget(self.ui_eq_bnm)
        self.verticalLayout_11.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        spacerItem32 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem32)
        self.ui_eq_qt = QtWidgets.QLineEdit(self.verticalLayoutWidget_6)
        self.ui_eq_qt.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.ui_eq_qt.setObjectName("ui_eq_qt")
        self.horizontalLayout_10.addWidget(self.ui_eq_qt)
        self.verticalLayout_11.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.ui_eq_ok = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.ui_eq_ok.setObjectName("ui_eq_ok")

        #updated
        self.ui_eq_ok.clicked.connect(self.UpdQty)

        self.horizontalLayout_11.addWidget(self.ui_eq_ok)
        self.pushButton_8 = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_11.addWidget(self.pushButton_8)
        self.verticalLayout_11.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_23.addLayout(self.verticalLayout_11)
        spacerItem33 = QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem33)
        self.verticalLayout_12.addLayout(self.horizontalLayout_23)
        spacerItem34 = QtWidgets.QSpacerItem(13, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_12.addItem(spacerItem34)
        self.horizontalLayout_25.addWidget(self.splitter_4)
        spacerItem35 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem35)
        self.splitter_3 = QtWidgets.QSplitter(self.updateinventory)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.splitter_3)
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem36 = QtWidgets.QSpacerItem(13, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem36)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        spacerItem37 = QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem37)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_8.addWidget(self.label_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_12.addWidget(self.label_12)
        self.ui_ab_bnm = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.ui_ab_bnm.setObjectName("ui_ab_bnm")
        self.horizontalLayout_12.addWidget(self.ui_ab_bnm)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_13.addWidget(self.label_13)
        spacerItem38 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem38)
        self.ui_ab_ath = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.ui_ab_ath.setObjectName("ui_ab_ath")
        self.horizontalLayout_13.addWidget(self.ui_ab_ath)
        self.verticalLayout_8.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_14 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_14.addWidget(self.label_14)
        spacerItem39 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem39)
        self.ui_ab_pr = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.ui_ab_pr.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.ui_ab_pr.setObjectName("ui_ab_pr")
        self.horizontalLayout_14.addWidget(self.ui_ab_pr)
        self.verticalLayout_8.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_15 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_15.addWidget(self.label_15)
        self.ui_ab_qt = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.ui_ab_qt.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.ui_ab_qt.setObjectName("ui_ab_qt")
        self.horizontalLayout_15.addWidget(self.ui_ab_qt)
        self.verticalLayout_8.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.ui_ab_ok = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.ui_ab_ok.setObjectName("ui_ab_ok")

        #Updated
        self.ui_ab_ok.clicked.connect(self.addNewBook)
        
        self.horizontalLayout_16.addWidget(self.ui_ab_ok)
        self.pushButton_10 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_16.addWidget(self.pushButton_10)
        self.verticalLayout_8.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_19.addLayout(self.verticalLayout_8)
        spacerItem40 = QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem40)
        self.verticalLayout_7.addLayout(self.horizontalLayout_19)
        spacerItem41 = QtWidgets.QSpacerItem(13, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem41)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.splitter_3)
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        spacerItem42 = QtWidgets.QSpacerItem(13, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_9.addItem(spacerItem42)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        spacerItem43 = QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem43)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_16 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_10.addWidget(self.label_16)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_17 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_17.addWidget(self.label_17)
        self.ui_db_bnm = QtWidgets.QComboBox(self.verticalLayoutWidget_5)
        self.ui_db_bnm.setObjectName("ui_db_bnm")

         #Updated
        self.ui_db_bnm.setEditable(True)
        
        self.horizontalLayout_17.addWidget(self.ui_db_bnm)
        self.verticalLayout_10.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.ui_db_ok = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.ui_db_ok.setObjectName("ui_db_ok")
        
        #Updated
        self.ui_db_ok.clicked.connect(self.Delete)
        
        self.horizontalLayout_18.addWidget(self.ui_db_ok)        
        self.pushButton_12 = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout_18.addWidget(self.pushButton_12)
        self.verticalLayout_10.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_20.addLayout(self.verticalLayout_10)
        spacerItem44 = QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem44)
        self.verticalLayout_9.addLayout(self.horizontalLayout_20)
        spacerItem45 = QtWidgets.QSpacerItem(13, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_9.addItem(spacerItem45)
        self.horizontalLayout_25.addWidget(self.splitter_3)
        spacerItem46 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem46)
        self.tab.addTab(self.updateinventory, "")
        self.verticalLayout_14.addWidget(self.tab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 972, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuUpdate_Inventory = QtWidgets.QMenu(self.menuMenu)
        self.menuUpdate_Inventory.setObjectName("menuUpdate_Inventory")
        self.menuLogout = QtWidgets.QMenu(self.menubar)
        self.menuLogout.setObjectName("menuLogout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSell_Books = QtWidgets.QAction(MainWindow)
        self.actionSell_Books.setObjectName("actionSell_Books")
        self.actionAdd_New_Book = QtWidgets.QAction(MainWindow)
        self.actionAdd_New_Book.setObjectName("actionAdd_New_Book")
        self.actionUpdate_Price = QtWidgets.QAction(MainWindow)
        self.actionUpdate_Price.setObjectName("actionUpdate_Price")
        self.actionUpdate_Quantity = QtWidgets.QAction(MainWindow)
        self.actionUpdate_Quantity.setObjectName("actionUpdate_Quantity")
        self.actionView_Inventory = QtWidgets.QAction(MainWindow)
        self.actionView_Inventory.setObjectName("actionView_Inventory")
        self.menuUpdate_Inventory.addAction(self.actionAdd_New_Book)
        self.menuUpdate_Inventory.addAction(self.actionUpdate_Price)
        self.menuUpdate_Inventory.addAction(self.actionUpdate_Quantity)
        self.menuMenu.addAction(self.actionSell_Books)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.menuUpdate_Inventory.menuAction())
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionView_Inventory)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuLogout.menuAction())
        self.label_3.setBuddy(self.s_bnm)
        self.label_4.setBuddy(self.s_bqty)
        self.label_5.setBuddy(self.ui_ep_bnm)
        self.label_7.setBuddy(self.ui_ep_pr)
        self.label_9.setBuddy(self.ui_eq_bnm)
        self.label_10.setBuddy(self.ui_eq_qt)
        self.label_12.setBuddy(self.ui_ab_bnm)
        self.label_13.setBuddy(self.ui_ab_ath)
        self.label_14.setBuddy(self.ui_ab_pr)
        self.label_15.setBuddy(self.ui_ab_qt)
        self.label_17.setBuddy(self.ui_db_bnm)

        self.retranslateUi(MainWindow)
        self.tab.setCurrentIndex(0)
        self.pushButton_6.clicked.connect(self.ui_ep_bnm.clear)
        self.pushButton_10.clicked.connect(self.ui_ab_pr.clear)
        self.pushButton_12.clicked.connect(self.ui_db_bnm.clear)

        #Updated
        self.pushButton_12.clicked.connect(self.additemCB)
        
        self.pushButton_8.clicked.connect(self.ui_eq_qt.clear)
        self.pushButton_3.clicked.connect(self.s_bnm.clear)
        
        #Updated
        self.pushButton_3.clicked.connect(self.s_bnm.clear)  
        self.pushButton_3.clicked.connect(self.additemCB)
        self.pushButton_3.clicked.connect(self.s_bqty.clear)
        
        self.pushButton_10.clicked.connect(self.ui_ab_qt.clear)
        self.pushButton_10.clicked.connect(self.ui_ab_bnm.clear)
        
        self.pushButton_6.clicked.connect(self.ui_ep_bnm.clear)
        
        #Updated
        self.pushButton_6.clicked.connect(self.additemCB)
        self.pushButton_6.clicked.connect(self.ui_ep_pr.clear)
        
        self.pushButton_10.clicked.connect(self.ui_ab_ath.clear)

        
        self.pushButton_8.clicked.connect(self.ui_eq_qt.clear)
        self.pushButton_8.clicked.connect(self.ui_eq_bnm.clear)
        #Updated
        self.pushButton_8.clicked.connect(self.additemCB)
        
        

        #Updated
        
        self.ui_ab_ok.clicked.connect(self.ui_ab_qt.clear)
        self.ui_ab_ok.clicked.connect(self.ui_ab_pr.clear)
        self.ui_ab_ok.clicked.connect(self.ui_ab_ath.clear)
        self.ui_ab_ok.clicked.connect(self.ui_ab_bnm.clear)
        
        self.ui_ab_ok.clicked.connect(self.ui_ep_bnm.clear)
        self.ui_ab_ok.clicked.connect(self.ui_db_bnm.clear)
        self.ui_ab_ok.clicked.connect(self.ui_eq_bnm.clear)
        self.ui_ab_ok.clicked.connect(self.additemCB)

        self.ui_ep_ok.clicked.connect(self.ui_ep_pr.clear)
        self.ui_ep_ok.clicked.connect(self.ui_ep_bnm.clear)
        self.ui_ep_ok.clicked.connect(self.additemCB)

        self.ui_eq_ok.clicked.connect(self.ui_eq_qt.clear)
        self.ui_eq_ok.clicked.connect(self.ui_eq_bnm.clear)
        self.ui_eq_ok.clicked.connect(self.additemCB)

        self.ui_db_ok.clicked.connect(self.ui_db_bnm.clear)
        self.ui_db_ok.clicked.connect(self.additemCB)



        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.s_bnm, self.s_bqty)
        MainWindow.setTabOrder(self.s_bqty, self.s_ok)
        MainWindow.setTabOrder(self.s_ok, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.s_table)
        MainWindow.setTabOrder(self.s_table, self.s_recipt_ok)
        MainWindow.setTabOrder(self.s_recipt_ok, self.s_recipt_clear)
        MainWindow.setTabOrder(self.s_recipt_clear, self.tab)
        MainWindow.setTabOrder(self.tab, self.ui_table)
        MainWindow.setTabOrder(self.ui_table, self.ui_ep_bnm)
        MainWindow.setTabOrder(self.ui_ep_bnm, self.ui_ep_pr)
        MainWindow.setTabOrder(self.ui_ep_pr, self.ui_ep_ok)
        MainWindow.setTabOrder(self.ui_ep_ok, self.pushButton_6)
        MainWindow.setTabOrder(self.pushButton_6, self.ui_eq_bnm)
        MainWindow.setTabOrder(self.ui_eq_bnm, self.ui_eq_qt)
        MainWindow.setTabOrder(self.ui_eq_qt, self.ui_eq_ok)
        MainWindow.setTabOrder(self.ui_eq_ok, self.pushButton_8)
        MainWindow.setTabOrder(self.pushButton_8, self.ui_ab_bnm)
        MainWindow.setTabOrder(self.ui_ab_bnm, self.ui_ab_ath)
        MainWindow.setTabOrder(self.ui_ab_ath, self.ui_ab_pr)
        MainWindow.setTabOrder(self.ui_ab_pr, self.ui_ab_qt)
        MainWindow.setTabOrder(self.ui_ab_qt, self.ui_ab_ok)
        MainWindow.setTabOrder(self.ui_ab_ok, self.pushButton_10)

        #Updated
        self.loadBooks()
        self.additemCB()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Book Fusion"))
        
        self.label_3.setText(_translate("MainWindow", "Book name :"))
        self.label_4.setText(_translate("MainWindow", "Quantity :"))
        self.s_ok.setText(_translate("MainWindow", "Add item"))
        self.pushButton_3.setText(_translate("MainWindow", "Clear"))
        self.label.setText(_translate("MainWindow", "Recipt"))
        self.label_19.setText(_translate("MainWindow", "Customer Name"))
        self.s_recipt_ok.setText(_translate("MainWindow", "Submit"))
        self.s_recipt_clear.setText(_translate("MainWindow", "Clear"))
        self.tab.setTabText(self.tab.indexOf(self.sellBook), _translate("MainWindow", "Sell Books"))
        self.label_18.setText(_translate("MainWindow", "Inventory"))
        self.label_21.setText(_translate("MainWindow", "Search Directory :"))
        self.i_in_ok.setText(_translate("MainWindow", "Search"))

        #Updated
        self.i_in_can.setText(_translate("MainWindow", "Clear"))
        
        self.label_20.setText(_translate("MainWindow", "Transactions"))
        self.label_22.setText(_translate("MainWindow", "Search Transactions :"))
        self.i_tr_ok.setText(_translate("MainWindow", "Search"))
        
        #Updated
        self.i_tr_can.setText(_translate("MainWindow", "Clear"))

        
        self.tab.setTabText(self.tab.indexOf(self.Inventory), _translate("MainWindow", "Inventory"))
        self.label_2.setText(_translate("MainWindow", "Available Books"))
        self.label_6.setText(_translate("MainWindow", "Edit Book Price"))
        self.label_5.setText(_translate("MainWindow", "Book"))
        self.label_7.setText(_translate("MainWindow", "New Price :"))
        self.ui_ep_ok.setText(_translate("MainWindow", "Update"))
        self.pushButton_6.setText(_translate("MainWindow", "Clear"))
        self.label_8.setText(_translate("MainWindow", "Update Book Quantity"))
        self.label_9.setText(_translate("MainWindow", "Book"))
        self.label_10.setText(_translate("MainWindow", "Added Quantity (20 or -20) :"))
        self.ui_eq_ok.setText(_translate("MainWindow", "Update"))
        self.pushButton_8.setText(_translate("MainWindow", "Clear"))
        self.label_11.setText(_translate("MainWindow", "Add New Book"))
        self.label_12.setText(_translate("MainWindow", "Book Title:"))
        self.label_13.setText(_translate("MainWindow", "Author:"))
        self.label_14.setText(_translate("MainWindow", "Price:"))
        self.label_15.setText(_translate("MainWindow", "Quantity :"))
        self.ui_ab_ok.setText(_translate("MainWindow", "Add"))
        self.pushButton_10.setText(_translate("MainWindow", "Clear"))
        self.label_16.setText(_translate("MainWindow", "Delete Book"))
        self.label_17.setText(_translate("MainWindow", "Book Title:"))
        self.ui_db_ok.setText(_translate("MainWindow", "Delete"))
        self.pushButton_12.setText(_translate("MainWindow", "Clear"))
        self.tab.setTabText(self.tab.indexOf(self.updateinventory), _translate("MainWindow", "Update Inventory"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuUpdate_Inventory.setTitle(_translate("MainWindow", "Update Inventory"))
        self.menuLogout.setTitle(_translate("MainWindow", "Logout"))
        self.actionSell_Books.setText(_translate("MainWindow", "Sell Books"))
        self.actionAdd_New_Book.setText(_translate("MainWindow", "Add New Book"))
        self.actionUpdate_Price.setText(_translate("MainWindow", "Update Price"))
        self.actionUpdate_Quantity.setText(_translate("MainWindow", "Update Quantity"))
        self.actionView_Inventory.setText(_translate("MainWindow", "View Inventory"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())

