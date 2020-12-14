from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QRadioButton, QButtonGroup, QLabel, QLineEdit, QFormLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, pyqtSlot
import sys
import time
import os
import datetime
import MFRC522
import RPi.GPIO as GPIO
import signal
import pymysql

GPIO.setwarnings(False)
Blocks=[8,9,10]
KEY = [211, 247, 211, 247, 211, 247]

def trap_exc_during_debug(*args):
    print(args)

sys.excepthook = trap_exc_during_debug

class workerThread(QThread):

    signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.abort = False
        
    @pyqtSlot()
    def run(self):
        #print("yeah yeah ")
        time.sleep(0.1)
        app.processEvents()
        self.signal.emit('Done')
        
    def __del__(self):
        #print("okay okay")
        self.abort = True
        self.wait()
        
class General(QWidget):
    
    def __init__(self):
        super().__init__()
        self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
        self.cursor = self.db.cursor()
        print("Database Connected")
        self.READER = MFRC522.MFRC522()
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(10, 30, 1350, 750)
            
        self.setWindowTitle('RFID READ WRITE CARD')
        
        self.setObjectName('MainWidget')
        self.setStyleSheet("""
            #MainWidget {
                background-color: #333;
            } """)
        
        WriteButton = QPushButton("WRITE",self)
        ReadButton = QPushButton("READ",self)
        ClearButton = QPushButton("CLEAR",self)
        WriteButton.setFont(QtGui.QFont("Calibri", 13))
        ReadButton.setFont(QtGui.QFont("Calibri", 13))
        ClearButton.setFont(QtGui.QFont("Calibri", 13))
        WriteButton.move(100,690)
        ReadButton.move(260,690)
        ClearButton.move(420,690)
        WriteButton.clicked.connect(self.writeClicked)
        ReadButton.clicked.connect(self.readClicked)
        ClearButton.clicked.connect(self.clearClicked)
        WriteButton.setStyleSheet("background-color: #F7CE16")
        ReadButton.setStyleSheet("background-color: #F7CE16")
        ClearButton.setStyleSheet("background-color: #F7CE16")

        headerfont = QtGui.QFont("Cambria", 14, QtGui.QFont.Bold)

        l1 = QLabel("CATEGORY: ")
        l1.setFont(headerfont)
        l1.setMinimumHeight(30)
        l1.setFixedWidth(250)
        l1.setStyleSheet("color: red")
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("STUDENT")
        self.comboBox.addItem("BOOK")
        self.comboBox.setFixedWidth(150)
        self.comboBox.setMinimumHeight(30)
        self.comboBox.setFont(QtGui.QFont("Times", 11))
        self.comboBox.activated[str].connect(self.Dropdown)

        self.l2 = QLabel("ROLL NO. : ")
        self.l2.setFont(headerfont)
        self.l2.setMinimumHeight(30)
        self.l2.setFixedWidth(500)
        self.l2.setStyleSheet("color: red")
        self.text2 = QLineEdit()
        self.text2.setFixedWidth(600)
        self.text2.setMinimumHeight(30)
        self.text2.setPlaceholderText(" EX:140670 ")
        self.text2.setFont(QtGui.QFont("Times", 11))

        self.l3 = QLabel("REGISTRATION NO. : ")
        self.l3.setFont(headerfont)
        self.l3.setMinimumHeight(30)
        self.l3.setFixedWidth(500)
        self.l3.setStyleSheet("color: red")
        self.text3 = QLineEdit()
        self.text3.setDisabled(True)
        self.text3.setFixedWidth(600)
        self.text3.setMinimumHeight(30)
        self.text3.setPlaceholderText(" EX: 2$23#1489 ")
        self.text3.setFont(QtGui.QFont("Times", 11))

        self.l4 = QLabel("NAME: ")
        self.l4.setFont(headerfont)
        self.l4.setMinimumHeight(30)
        self.l4.setFixedWidth(500)
        self.l4.setStyleSheet("color: red")
        self.text4 = QLineEdit()
        self.text4.setDisabled(True)
        self.text4.setFixedWidth(600)
        self.text4.setMinimumHeight(30)
        self.text4.setPlaceholderText(" EX: RAHUL SINGHAM ")
        self.text4.setFont(QtGui.QFont("Times", 11))

        self.l5 = QLabel("MAJOR: ")
        self.l5.setFont(headerfont)
        self.l5.setMinimumHeight(30)
        self.l5.setFixedWidth(500)
        self.l5.setStyleSheet("color: red")
        self.text5 = QLineEdit()
        self.text5.setDisabled(True)
        self.text5.setFixedWidth(250)
        self.text5.setMinimumHeight(30)
        self.text5.setPlaceholderText(" EX: B.TECH ")
        self.text5.setFont(QtGui.QFont("Times", 11))

        self.l6 = QLabel("BRANCH: ")
        self.l6.setFont(headerfont)
        self.l6.setMinimumHeight(30)
        self.l6.setFixedWidth(500)
        self.l6.setStyleSheet("color: red")
        self.text6 = QLineEdit()
        self.text6.setDisabled(True)
        self.text6.setFixedWidth(250)
        self.text6.setMinimumHeight(30)
        self.text6.setPlaceholderText(" EX: CSE ")
        self.text6.setFont(QtGui.QFont("Times", 11))

        self.l7 = QLabel("GENDER: ")
        self.l7.setFont(headerfont)
        self.l7.setMinimumHeight(30)
        self.l7.setFixedWidth(500)
        self.l7.setStyleSheet("color: red")
        self.text7 = QLineEdit()
        self.text7.setDisabled(True)
        self.text7.setFixedWidth(250)
        self.text7.setMinimumHeight(30)
        self.text7.setPlaceholderText(" EX: M,F,O ")
        self.text7.setFont(QtGui.QFont("Times", 11))
        
        fbox = QFormLayout()
        fbox.setVerticalSpacing(60)
        fbox.setHorizontalSpacing(20)
        fbox.addRow(l1,self.comboBox)
        fbox.addRow(self.l2,self.text2)
        fbox.addRow(self.l3,self.text3)
        fbox.addRow(self.l4,self.text4)
        fbox.addRow(self.l5,self.text5)
        fbox.addRow(self.l6,self.text6)
        fbox.addRow(self.l7,self.text7)
        
        self.setLayout(fbox)
        self.lineedits = [self.text2,self.text3,self.text4,self.text5,self.text6,self.text7]
        self.show()

    def crashingmsg(self):
        crashmsg = QMessageBox()
        crashmsg.setIcon(QMessageBox.Critical)
        crashmsg.setText("SOMETHING IS WRONG TRY SAVING AGAIN!!")
        crashmsg.setDetailedText("If still not working then close the Application and start again")
        crashmsg.setWindowTitle("Application Crashing")
        crashmsg.setWindowIcon(QIcon('download.png'))
        crashmsg.exec()

    def errormsg(self):
        errormsg = QMessageBox()
        errormsg.setIcon(QMessageBox.Warning)
        errormsg.setText("Enter a valid Roll Number or Book Id")
        errormsg.setWindowTitle("Error Report")
        errormsg.setWindowIcon(QIcon('download.png'))
        errormsg.exec()

    def savesuccess(self):
        savemsg = QMessageBox()
        savemsg.setIcon(QMessageBox.Information)
        savemsg.setText("Your Enteries Have Been Saved successfully !")
        savemsg.setWindowTitle("SAVED")
        savemsg.setWindowIcon(QIcon('download.png'))
        savemsg.exec()
        
    def errormsgcard(self):
        errormsgdelete = QMessageBox()
        errormsgdelete.setIcon(QMessageBox.Warning)
        errormsgdelete.setText("Place your Card correctly before reader ")
        errormsgdelete.setWindowTitle("Error Report")
        errormsgdelete.setWindowIcon(QIcon('download.png'))
        errormsgdelete.exec()

    def errorrestart(self):
        errorrest = QMessageBox()
        errorrest.setIcon(QMessageBox.Warning)
        errorrest.setText("Please Contact Help Desk Data in this card got corrupted !")
        errorrest.setWindowTitle("Error Report")
        errorrest.setWindowIcon(QIcon('download.png'))
        errorrest.exec()

    def Dropdown(self):
        #print("Dropdown")
        self.text3.setDisabled(True)
        self.text4.setDisabled(True)
        self.text5.setDisabled(True)
        self.text6.setDisabled(True)
        self.text7.setDisabled(True)
        for edit in self.lineedits:
            edit.clear()
        if str(self.comboBox.currentText())=="STUDENT" or str(self.comboBox.currentText())=="CHOOSE":
            val=1
        else:
            val=0
        if val==0:
            self.l2.setText("BOOK ID: ")
            self.text2.setPlaceholderText(" EX: CSE001 ")
            self.l3.setText("CLASSIFYING SUBJECT: ")
            self.text3.setPlaceholderText(" EX: CSE ")
            self.l4.setText("BOOK TITLE: ")
            self.text4.setPlaceholderText(" EX: JAVA ")
            self.l5.setText("BOOK AUTHOR: ")
            self.text5.setPlaceholderText(" EX: SUMITRA ARORA ")
            self.l6.setText("BOOK PUBLICATION: ")
            self.text6.setPlaceholderText(" EX: TMH ")
            self.l7.setText("BOOK EDITION: ")
            self.text7.setPlaceholderText(" EX: 1,2,3 ")
        else:
            self.l2.setText("ROLL NO. : ")
            self.text2.setPlaceholderText(" EX: 140670 ")
            self.l3.setText("REGISTRATION NO. : ")
            self.text3.setPlaceholderText(" EX: 2$23#1489 ")
            self.l4.setText("NAME: ")
            self.text4.setPlaceholderText(" EX: RAHUL SINGHAM ")
            self.l5.setText("MAJOR: ")
            self.text5.setPlaceholderText(" EX: B.TECH ")
            self.l6.setText("BRANCH: ")
            self.text6.setPlaceholderText(" EX: CSE ")
            self.l7.setText("GENDER: ")
            self.text7.setPlaceholderText(" EX: M,F,O ")
            
    def findkeys(self):
        self.keyval={}
        MIFAREReader = MFRC522.MFRC522()
        for sector in range(15):
            for key in MFRC522.MIFARE_CLASSIC_1K_KEYS:
                (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_SelectTag(uid)
                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, sector, key, uid)
                    if status == MIFAREReader.MI_OK:
                        #print(key)
                        #print(sector)
                        self.keyval[sector]=key
                        MIFAREReader.MFRC522_StopCrypto1()
        #print(self.keyval)

    def readClicked(self):
        #print("read")
        try:
            if not self.db.open:
                self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
                self.cursor = self.db.cursor()
                print("Database Connected")
            tex=[]
            print("1")
            try:
                for sector in Blocks:
                    for key in MFRC522.MIFARE_CLASSIC_1K_KEYS:
                        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
                        (status, uid) = self.READER.MFRC522_Anticoll()
                        if status == self.READER.MI_OK:
                            self.READER.MFRC522_SelectTag(uid)
                            status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, sector, key, uid)
                            if status == self.READER.MI_OK:
                                data = self.READER.MFRC522_Read(sector)
                                self.READER.MFRC522_StopCrypto1()
                                textt=""
                                t=data["data"]
                                te=""
                                i=1
                                while i<len(t)-1:
                                    te+=t[i]
                                    i+=1
                                textlist=te.split(",")
                                for val in textlist:
                                    val=int(val)
                                    textt+=chr(val)
                                #print(textlist)
                                tex.append(textt)
            except:
                self.workerthread = workerThread()
                self.workerthread.signal.connect(self.errormsgcard)
                self.workerthread.start()
            #print(tex)
            print("2")
            textt=tex[0].split("==")
            if textt[0]=='S':
                self.comboBox.setCurrentIndex(0)
                sql=("SELECT reg_no, name, major, branch, gender FROM Student WHERE roll_no = %s")
            else:
                self.comboBox.setCurrentIndex(1)
                sql=("SELECT CLASSIFYING_SUBJECT, TITLE, AUTHOR, PUBLICATION, EDITION FROM LIBOT WHERE BOOK_ID = %s")
            print("3")
            self.Dropdown()
            print("4")
            data=textt[1]           
            try:
                self.cursor.execute(sql,data)
            except:
                self.reselectdatabase(sql,data)
            self.text2.setText(str(textt[1]))
            placelist=list(self.cursor.fetchall()[0])
            print(placelist)
            self.text3.setText(str(placelist[0]))
            self.text4.setText(str(placelist[1]))
            self.text5.setText(str(placelist[2]))
            self.text6.setText(str(placelist[3]))
            self.text7.setText(str(placelist[4]))
            self.text3.setDisabled(False)
            self.text4.setDisabled(False)
            self.text5.setDisabled(False)
            self.text6.setDisabled(False)
            self.text7.setDisabled(False)
            print("5")
        except:
            self.workerthread = workerThread()
            self.workerthread.signal.connect(self.crashingmsg)
            self.workerthread.start()
            
    def write(self,datatext,blockaddre):
        #print("write")
        try:
            (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
            if status != self.READER.MI_OK:
                print("Something Wrong!")
            (status, uid) = self.READER.MFRC522_Anticoll()
            if status != self.READER.MI_OK:
                print("Something Wrong!")
            id = self.uid_to_num(uid)
            print(id)
            self.READER.MFRC522_SelectTag(uid)
            status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.keyval[blockaddre], uid)
            self.READER.MFRC522_Read(11)
            if status == self.READER.MI_OK:
                data = bytearray()
                data.extend(bytearray(datatext.ljust(16).encode('ascii')))
                self.READER.MFRC522_Write(blockaddre, data[0:16])
            self.READER.MFRC522_StopCrypto1()
            print("Data written ",end='')
            print(" ",end='')
            print(datatext,end='')
            print(" ",end='')
            print(blockaddre)
            return True
        except:
            if (blockaddre != 9):
                self.workerthread = workerThread()
                self.workerthread.signal.connect(self.errormsgcard)
                self.workerthread.start()
            else:
                print("9th garbage block")
        finally:
            GPIO.cleanup()
            
    def writeClicked(self):
        #print("writeclick")
        if not self.db.open:
            self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
            self.cursor = self.db.cursor()
            print("Database Connected")
        try:
            tex=[]
            for edit in self.lineedits:
                tex.append(str(edit.text()))
            #print(tex)
                
            text8=(str(self.comboBox.currentText())[0])+"=="+str(self.text2.text())
            text9="garbage"
            sql=""
            if (str(self.comboBox.currentText())) == "STUDENT":
                sql=("SELECT password, no_book_issued FROM Student WHERE roll_no = %s")
                data=str(self.text2.text())
                try:
                    self.cursor.execute(sql,data)
                except:
                    self.reselectdatabase(sql,data)
                lis=list(self.cursor.fetchall()[0])
                text10=str(lis[0])
                text8+="=="+str(lis[1])
            else:
                sql=("SELECT ISSUED_STATUS FROM LIBOT WHERE BOOK_ID = %s")
                data=str(self.text2.text())
                try:
                    self.cursor.execute(sql,data)
                except:
                    self.reselectdatabase(sql,data)
                text10=str((list(self.cursor.fetchall())[0])[0])
            try:
                textt=[]
                textt.append(text8)
                textt.append(text9)
                textt.append(text10)
                statuse=False
                self.findkeys()
                i=0
                while i<3:
                    statuse=False
                    statuse = self.write(textt[i],Blocks[i])
                    if statuse == False:
                        break
                    i+=1
                    
                if statuse == True:
                    self.workerthread = workerThread()
                    self.workerthread.signal.connect(self.savesuccess)
                    self.workerthread.start()
                else:
                    self.workerthread = workerThread()
                    self.workerthread.signal.connect(self.errormsg)
                    self.workerthread.start()
            except:
                self.workerthread = workerThread()
                self.workerthread.signal.connect(self.errormsg)
                self.workerthread.start()
        except:
            self.workerthread = workerThread()
            self.workerthread.signal.connect(self.crashingmsg)
            self.workerthread.start()
    
    def reselectdatabase(self,sql,data):
        if not self.db.open:
            self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
            self.cursor = self.db.cursor()
            print("Database Connected")
        try:
            self.cursor.execute(sql,data)
        except:
            print("retried database not going")
            self.errorestart()
            
    def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n
    
    def clearClicked(self):
        for edit in self.lineedits:
            edit.clear()
        self.comboBox.setCurrentIndex(0)
        self.text3.setDisabled(True)
        self.text4.setDisabled(True)
        self.text5.setDisabled(True)
        self.text6.setDisabled(True)
        self.text7.setDisabled(True)
        #print("clear")
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = General()
    sys.exit(app.exec_())
