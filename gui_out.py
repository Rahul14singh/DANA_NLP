from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout, QButtonGroup, QLabel, QLineEdit, QFormLayout, QMessageBox, QVBoxLayout, QTextEdit, QSplitter, QStyleFactory, QInputDialog
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
continue_reading = True

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
        
        self.setGeometry(10, 30, 1350, 740)
            
        self.setWindowTitle('RFID EXIT')
        
        self.setObjectName('MainWidget')
        self.setStyleSheet("""
            #MainWidget {
                background-color: red;
            } """)

        headerfont = QtGui.QFont("Cambria", 16, QtGui.QFont.Bold)

        l1 = QLabel("ROLL NO. : ")
        l1.setFont(headerfont)
        l1.setMinimumHeight(50)
        l1.setFixedWidth(400)
        l1.setStyleSheet("color: black")
        self.textedit1=QTextEdit(self)
        self.textedit1.setReadOnly(True)
        self.textedit1.setMinimumHeight(10)
        self.textedit1.setFixedWidth(400)
        self.textedit1.setFont(QtGui.QFont("Times", 14))

        l2 = QLabel("BOOK DETAILS : ")
        l2.setFont(headerfont)
        l2.setMinimumHeight(25)
        l2.setFixedWidth(500)
        l2.setStyleSheet("color: black")
        self.textedit2 =QTextEdit(self)
        self.textedit2.setReadOnly(True)
        self.textedit2.setMinimumHeight(100)
        self.textedit2.setFixedWidth(800)
        self.textedit2.setFont(QtGui.QFont("Times", 14))
        self.textedit2.append("The Books you have issued today and are verified for exit are : ")

        l3 = QLabel("TOTAL BOOKS ISSUED TODAY : ")
        l3.setFont(headerfont)
        l3.setMinimumHeight(50)
        l3.setFixedWidth(400)
        l3.setStyleSheet("color: black")
        self.textedit3 =QTextEdit(self)
        self.textedit3.setReadOnly(True)
        self.textedit3.setMinimumHeight(200)
        self.textedit3.setFixedWidth(400)
        self.textedit3.setFont(QtGui.QFont("Times", 14))

        l4 = QLabel("BOOKS YET TO VERIFY : ")
        l4.setFont(headerfont)
        l4.setMinimumHeight(50)
        l4.setFixedWidth(400)
        l4.setStyleSheet("color: black")
        self.textedit4 =QTextEdit(self)
        self.textedit4.setReadOnly(True)
        self.textedit4.setMinimumHeight(200)
        self.textedit4.setFixedWidth(400)
        self.textedit4.setFont(QtGui.QFont("Times", 14))

        fbox1st = QFormLayout()
        fbox1st.addRow(l1)
        fbox1st.addRow(self.textedit1)
        fbox1st.addRow(l3)
        fbox1st.addRow(self.textedit3)
        fbox1st.addRow(l4)
        fbox1st.addRow(self.textedit4)

        fbox = QFormLayout()
        fbox.setVerticalSpacing(20)
        fbox.setHorizontalSpacing(40)
        fbox.addRow(l2)
        fbox.addRow(self.textedit2,fbox1st)
        
        self.setLayout(fbox)
        self.show()
        self.workerthreadcard = workerThread()
        self.workerthreadcard.signal.connect( lambda: self.readClicked(0,"x",['1','2','3']))
        self.workerthreadcard.start()

    def crashingmsg(self):
        crashmsg = QMessageBox()
        crashmsg.setIcon(QMessageBox.Critical)
        crashmsg.setText("SOMETHING IS WRONG TRY SAVING AGAIN!! ")
        crashmsg.setDetailedText("If still not working then close the Application and start again ")
        crashmsg.setWindowTitle("Application Crashing       ")
        crashmsg.setWindowIcon(QIcon('download.png'))
        crashmsg.exec()

    def bookcardmsg(self):
        bookmsg = QMessageBox()
        bookmsg.setIcon(QMessageBox.Information)
        bookmsg.setText("Now place your book cards you issued today        ")
        bookmsg.setWindowTitle("Click OK")
        bookmsg.setWindowIcon(QIcon('download.png'))
        bookmsg.exec()
        
    def wrongpass(self):
        wrongmsg = QMessageBox()
        wrongmsg.setIcon(QMessageBox.Warning)
        wrongmsg.setText("Enter the Password Correctly                     ")
        wrongmsg.setWindowTitle("Error Report")
        wrongmsg.setWindowIcon(QIcon('download.png'))
        wrongmsg.exec()
        
    def savesuccess(self):
        savemsg = QMessageBox()
        savemsg.setIcon(QMessageBox.Information)
        savemsg.setText("You are clear to exit Library                      ")
        savemsg.setWindowTitle("CAN EXIT NOW")
        savemsg.setWindowIcon(QIcon('download.png'))
        savemsg.exec()

    def nextcard(self):
        savemsg = QMessageBox()
        savemsg.setIcon(QMessageBox.Information)
        savemsg.setText("Place the next Book card                           ")
        savemsg.setWindowTitle("NEXT CARD")
        savemsg.setWindowIcon(QIcon('download.png'))
        savemsg.exec()

    def Initialrfid(self):
        savemsgre = QMessageBox()
        savemsgre.setIcon(QMessageBox.Information)
        savemsgre.setText("Show Your RFID to EXIT !                         ")
        savemsgre.setWindowTitle("SHOW STUDENT CARD")
        savemsgre.setWindowIcon(QIcon('download.png'))
        savemsgre.exec()
        
    def errormsgcard(self):
        errormsgdelete = QMessageBox()
        errormsgdelete.setIcon(QMessageBox.Warning)
        errormsgdelete.setText("Place the Student RFID                      ")
        errormsgdelete.setWindowTitle("Error Report")
        errormsgdelete.setWindowIcon(QIcon('download.png'))
        errormsgdelete.exec()

    def wrongcard(self):
        wrongcardmsg = QMessageBox()
        wrongcardmsg.setIcon(QMessageBox.Warning) 
        wrongcardmsg.setText("Place the Book RFID                           ")
        wrongcardmsg.setWindowTitle("Error Report")
        wrongcardmsg.setWindowIcon(QIcon('download.png'))
        wrongcardmsg.exec()

    def errorrestart(self):
        errorrest = QMessageBox()
        errorrest.setIcon(QMessageBox.Warning)
        errorrest.setText("Please Contact Help Desk Data in this card got corrupted !")
        errorrest.setWindowTitle("Error Report")
        errorrest.setWindowIcon(QIcon('download.png'))
        errorrest.exec()

    def notcrrctcard(self):
        errorrest = QMessageBox()
        errorrest.setIcon(QMessageBox.Warning)
        errorrest.setText("Either this is not your Book or this Book was not issued today ")
        errorrest.setWindowTitle("Error Report")
        errorrest.setWindowIcon(QIcon('download.png'))
        errorrest.exec()
    
    def readClicked(self,val,rolltobeissued,bookidslistt):
        try:
            bookidsshown=[]
            while continue_reading:
                if not self.db.open:
                    self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
                    self.cursor = self.db.cursor()
                    print("Database Connected")
                if val==0:
                    self.textedit1.clear()
                    self.textedit2.clear()
                    self.textedit3.clear()
                    self.textedit4.clear()
                    self.setStyleSheet(""" #MainWidget { background-color: red; } """)
                    self.Initialrfid()
                    bookidsshown=[]
                    self.textedit2.moveCursor(QtGui.QTextCursor.End)
                    self.textedit2.append("The Books you have issued today and are verified for exit are : ")
                check,tex=self.cardread()
                if check==True and (len(tex)==3):
                    textt=tex[0].split("==")
                    if textt[0]=='S':
                        print("S")
                        if val==0:
                            passtext,Ok = QInputDialog.getText(self,'Password ', 'Enter your Password here:                            ')
                            if Ok:
                                rolltoissued=textt[1]
                                #print(passtext)
                                sql=("SELECT password, no_book_issued FROM Student WHERE roll_no = %s")
                                data=textt[1]
                                try:
                                    self.cursor.execute(sql,data)
                                except:
                                    self.reselectdatabase(sql,data)
                                studata=list(self.cursor.fetchall()[0])
                                if str(studata[1])==textt[2].replace(" ",""):
                                    if passtext == str(studata[0]):
                                        self.textedit1.moveCursor(QtGui.QTextCursor.End)
                                        self.textedit1.append("Roll No. -  "+str(textt[1]))
                                        if studata[1] ==0 :
                                            self.textedit2.moveCursor(QtGui.QTextCursor.End)
                                            self.textedit2.append("Thanks for your patience visit again. ")
                                            self.setStyleSheet(""" #MainWidget { background-color: green; } """)
                                            self.savesuccess()
                                            self.setStyleSheet(""" #MainWidget { background-color: red; } """)
                                        else:
                                            datechecklist=(str(((datetime.datetime.now())+(datetime.timedelta(days=5))).date()).split("-"))
                                            datecheck=datechecklist[2]+"/"+datechecklist[1]+"/"+datechecklist[0]
                                            sql=("SELECT BOOK_ID FROM LIBOT WHERE ISSUED_TO=%s AND AVAILABILITY=%s")
                                            data=(textt[1],datecheck)
                                            try:
                                                self.cursor.execute(sql,data)
                                            except:
                                                self.reselectdatabase(sql,data)
                                            
                                            bookidlist=[]
                                            for each in self.cursor.fetchall():
                                                bookidlist.append(each[0])
                                            print(bookidlist)
                                            for each in bookidlist:
                                                self.textedit3.moveCursor(QtGui.QTextCursor.End)
                                                self.textedit3.append(each)
                                                self.textedit4.moveCursor(QtGui.QTextCursor.End)
                                                self.textedit4.append(each)
                                            self.bookcardmsg()
                                            print("11")
                                            self.readClicked(1,rolltoissued,bookidlist)
                                            print("22")
                                    else:
                                        self.wrongpass()
                                else:
                                    self.errorrestart()
                        else:
                            self.wrongcard()
                    else:
                        print("B")
                        if val==0:
                            self.errormsgcard()
                        else:
                            print("33")
                            print(textt[1])
                            print(bookidslistt)
                            if (str(textt[1].replace(" ","")) in bookidslistt):
                                if (str(textt[1].replace(" ","")) not in bookidsshown):
                                    sql=("SELECT ISSUED_STATUS, TITLE FROM LIBOT WHERE BOOK_ID = %s")
                                    data=(textt[1])
                                    try:
                                        self.cursor.execute(sql,data)
                                    except:
                                        self.reselectdatabase(sql,data)
                                    currstatusbook=list(self.cursor.fetchall()[0])
                                    print(currstatusbook)
                                    if currstatusbook[0] == int(tex[2].replace(" ","")) and currstatusbook[0] == 1:
                                        bookidsshown.append(str(textt[1].replace(" ","")))
                                        print(bookidsshown)
                                        self.textedit2.moveCursor(QtGui.QTextCursor.End)
                                        self.textedit2.append("Book ID : " + str(textt[1]))
                                        self.textedit2.append("TITLE : "+str(currstatusbook[1]))
                                    
                                        self.textedit4.clear()
                                        textedit4list=[]
                                        for each in bookidslistt:
                                            if each not in bookidsshown:
                                                textedit4list.append(each)
                                        for each in textedit4list:
                                            self.textedit4.moveCursor(QtGui.QTextCursor.End)
                                            self.textedit4.append(each)
                                
                                        if set(bookidsshown)==set(bookidslistt):
                                            self.textedit2.moveCursor(QtGui.QTextCursor.End)
                                            self.textedit2.append("Thanks for your patience visit again. ")
                                            self.setStyleSheet(""" #MainWidget { background-color: green; } """)
                                            self.savesuccess()
                                            self.setStyleSheet(""" #MainWidget { background-color: red; } """)
                                            break
                                        else:
                                            self.textedit2.moveCursor(QtGui.QTextCursor.End)
                                            self.textedit2.append("Next Book")
                                            self.nextcard()
                                    else:
                                        self.errorrestart()
                                else:
                                    self.nextcard()
                            else:
                                self.notcrrctcard()
        except:
            self.crashingmsg()

        
    def reselectdatabase(self,sql,data):
        if not self.db.open:
            self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
            self.cursor = self.db.cursor()
            print("Database Connected")
        try:
            self.cursor.execute(sql,data)
        except:
            print("Retried but database not going")
            self.errorestart()
            
    
    def cardread(self):
        tex=[]
        yes=0
        for sector in Blocks:
            for key in MFRC522.MIFARE_CLASSIC_1K_KEYS:
                (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
                (status, uid) = self.READER.MFRC522_Anticoll()
                if status == self.READER.MI_OK:
                    self.READER.MFRC522_SelectTag(uid)
                    status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, sector, key, uid)
                    if status == self.READER.MI_OK:
                        if sector == Blocks[2]:
                            yes=1
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
        #print(tex)
        if yes==1:
            return True , tex
        else:
            return False ,tex
    
    def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n
        
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
