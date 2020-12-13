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
        self.db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
        self.cursor = self.db.cursor()
        print("Database Connected")
        self.READER = MFRC522.MFRC522()
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(10, 30, 1350, 740)
            
        self.setWindowTitle('RFID ISSUE RETURN')
        
        self.setObjectName('MainWidget')
        self.setStyleSheet("""
            #MainWidget {
                background-color: #333;
            } """)

        headerfont = QtGui.QFont("Cambria", 16, QtGui.QFont.Bold)

        l1 = QLabel("                           STUDENT DETAILS: ")
        l1.setFont(headerfont)
        l1.setMinimumHeight(50)
        l1.setFixedWidth(500)
        l1.setStyleSheet("color: red")
        self.textedit1=QTextEdit(self)
        self.textedit1.setReadOnly(True)
        self.textedit1.setFont(QtGui.QFont("Times", 14))

        l2 = QLabel("                           BOOK DETAILS: ")
        l2.setFont(headerfont)
        l2.setMinimumHeight(50)
        l2.setFixedWidth(500)
        l2.setStyleSheet("color: red")
        self.textedit2 =QTextEdit(self)
        self.textedit2.setReadOnly(True)
        self.textedit2.setFont(QtGui.QFont("Times", 14))

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(l1, 1, 0)
        grid.addWidget(l2, 1, 1)
        grid.addWidget(self.textedit1, 2, 0)
        grid.addWidget(self.textedit2, 2, 1)
        
        self.setLayout(grid) 
        self.show()
        self.workerthreadcard = workerThread()
        self.workerthreadcard.signal.connect(lambda:self.readClicked(0,"x"))
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
        bookmsg.setText("Now place your book card                 ")
        bookmsg.setWindowTitle("Click OK")
        bookmsg.setWindowIcon(QIcon('download.png'))
        bookmsg.exec()
        
    def wrongpass(self):
        wrongmsg = QMessageBox()
        wrongmsg.setIcon(QMessageBox.Warning)
        wrongmsg.setText("Enter the Password Correctly            ")
        wrongmsg.setWindowTitle("Error Report")
        wrongmsg.setWindowIcon(QIcon('download.png'))
        wrongmsg.exec()
        
    def savesuccess(self):
        savemsg = QMessageBox()
        savemsg.setIcon(QMessageBox.Information)
        savemsg.setText("You have been issued all these books !    ")
        savemsg.setWindowTitle("BOOKS ISSUED")
        savemsg.setWindowIcon(QIcon('download.png'))
        savemsg.exec()

    def savesuccessreturned(self):
        savemsgre = QMessageBox()
        savemsgre.setIcon(QMessageBox.Information)
        savemsgre.setText("All these books are Returned !           ")
        savemsgre.setWindowTitle("BOOKS RETURNED")
        savemsgre.setWindowIcon(QIcon('download.png'))
        savemsgre.exec()
        
    def errormsgcard(self):
        errormsgdelete = QMessageBox()
        errormsgdelete.setIcon(QMessageBox.Warning)
        errormsgdelete.setText("Place the Student RFID                ")
        errormsgdelete.setWindowTitle("Error Report")
        errormsgdelete.setWindowIcon(QIcon('download.png'))
        errormsgdelete.exec()

    def Initialcardmsg(self):
        errormsgdelete = QMessageBox()
        errormsgdelete.setIcon(QMessageBox.Information)
        errormsgdelete.setText("Place the Student RFID                 ")
        errormsgdelete.setWindowTitle("Student Card")
        errormsgdelete.setWindowIcon(QIcon('download.png'))
        errormsgdelete.exec()

    def wrongcard(self):
        wrongcardmsg = QMessageBox()
        wrongcardmsg.setIcon(QMessageBox.Warning)
        wrongcardmsg.setText("Place the Book RFID                       ")
        wrongcardmsg.setWindowTitle("Error Report")
        wrongcardmsg.setWindowIcon(QIcon('download.png'))
        wrongcardmsg.exec()

    def Initialcard(self):
        wrongcardmsg = QMessageBox()
        wrongcardmsg.setIcon(QMessageBox.Warning)
        wrongcardmsg.setText("Check your Internet Connection and retry      ")
        wrongcardmsg.setWindowTitle("Error Report")
        wrongcardmsg.setWindowIcon(QIcon('download.png'))
        wrongcardmsg.exec()

    def errorrestart(self):
        errorrest = QMessageBox()
        errorrest.setIcon(QMessageBox.Warning)
        errorrest.setText("Please Contact Help Desk Data in card got corrupted !")
        errorrest.setWindowTitle("Error Report")
        errorrest.setWindowIcon(QIcon('download.png'))
        errorrest.exec()
        
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

    def readClicked(self,val,rolltobeissued):
        print(val)
        print(rolltobeissued)
        #print("read")
        try:
            while continue_reading:
                if not self.db.open:
                    self.db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
                    self.cursor = self.db.cursor()
                    print("Database Connected")
                if val==0:
                    self.textedit1.clear()
                    self.textedit2.clear()
                    self.Initialcardmsg()
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
                                sql=("SELECT reg_no, name, major, branch, gender, password, no_book_issued FROM Student WHERE roll_no = %s")
                                data=textt[1]
                                try:
                                    self.cursor.execute(sql,data)
                                except:
                                    self.reselectdatabase(sql,data)
                                studata=list(self.cursor.fetchall()[0])
                                if passtext == str(studata[5]):
                                    self.textedit1.moveCursor(QtGui.QTextCursor.End)
                                    self.textedit1.append("")
                                    self.textedit1.append("Registration No. -  "+str(studata[0]))
                                    self.textedit1.append("")
                                    self.textedit1.append("Roll No. -  "+str(textt[1]))
                                    self.textedit1.append("")
                                    self.textedit1.append("Name -  "+str(studata[1]))
                                    self.textedit1.append("")
                                    self.textedit1.append("Course -  "+str(studata[2]))
                                    self.textedit1.append("")
                                    self.textedit1.append("Branch -  "+str(studata[3]))
                                    self.textedit1.append("")
                                    self.textedit1.append("Gender -  "+str(studata[4]))
                                    self.textedit1.append("")
                                    self.textedit1.append("No of Books Already Issued -  "+str(studata[6]))
                                    self.bookcardmsg()
                                    print("11")
                                    self.readClicked(1,rolltoissued)
                                    print("22")
                                else:
                                    self.wrongpass()
                        else:
                            self.wrongcard()
                    else:
                        print("B")
                        if val==0:
                            self.errormsgcard()
                        else:
                            print("33")
                            print(tex)
                            sql=("SELECT AUTHOR, TITLE, PUBLICATION, EDITION, CLASSIFYING_SUBJECT, ROW_NO, COLUMN_NO, PARTITION_NO, PRICE FROM LIBOT WHERE BOOK_ID=%s")
                            data=(str(textt[1]))
                            try:
                                self.cursor.execute(sql,data)
                            except:
                                self.reselectdatabase(sql,data)
                            bookdata=list(self.cursor.fetchall()[0])
                            print(bookdata)
                            
                            self.textedit2.moveCursor(QtGui.QTextCursor.End)
                            self.textedit2.append("")
                            self.textedit2.append("Book ID -  "+str(textt[1]))
                            self.textedit2.append("")
                            self.textedit2.append("Author -  "+str(bookdata[0]))
                            self.textedit2.append("")
                            self.textedit2.append("Title -  "+str(bookdata[1]))
                            self.textedit2.append("")
                            self.textedit2.append("Publication -  "+str(bookdata[2]))
                            self.textedit2.append("")
                            self.textedit2.append("Edition -  "+str(bookdata[3]))
                            self.textedit2.append("")
                            self.textedit2.append("Subject -  "+str(bookdata[4]))
                            self.textedit2.append("")
                            self.textedit2.append("Row No. -  "+str(bookdata[5]))
                            self.textedit2.append("")
                            self.textedit2.append("Column No. -  "+str(bookdata[6]))
                            self.textedit2.append("")
                            self.textedit2.append("Partition No. -  "+str(bookdata[7]))
                            self.textedit2.append("")
                            self.textedit2.append("Price -  "+str(bookdata[8]))
                            
                            issuestatuscard=tex[2].replace(" ","")
                            if issuestatuscard=='0':
                                print("issue book")

                                tempp=False
                                text8=tex[0]
                                text9=""
                                text10="1"
                                texttt=[]
                                texttt.append(text8)
                                texttt.append(text9)
                                texttt.append(text10)
                                statuse=False
                                self.findkeys()
                                i=0
                                while i<3:
                                    statuse=False
                                    statuse = self.write(texttt[i],Blocks[i])
                                    if statuse == False:
                                        break
                                    i+=1
                
                                if statuse == True:
                                    print("BOOK CARD WRITTEN")
                                    self.errormsgcard()
                                    tempp=self.newreadClicked()
                                else:
                                    print("BOOK CARD NOT WRITTEN")
                                
                                if not self.db.open:
                                    self.db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
                                    self.cursor = self.db.cursor()
                                    print("Database Connected")
                                print("Updating Database")
                                sql=("SELECT no_book_issued FROM Student WHERE roll_no=%s")
                                data=(rolltobeissued)
                                try:
                                    self.cursor.execute(sql,data)
                                    booksissued=list(self.cursor.fetchall()[0])[0]
                                    print("booksissued "+str(booksissued))
                                except:
                                    self.reselectdatabase(sql,data)
                                
                                sql=("UPDATE Student SET no_book_issued=%s WHERE roll_no=%s")
                                data=(booksissued+1,rolltobeissued)
                                try:
                                   self.cursor.execute(sql,data)
                                   self.db.commit()
                                   print("Student Database Updated")
                                except:
                                   self.db.rollback()
                                   slef.reupdatedatabase(sql,data)
                                   
                                print(textt[1])
                                sql=("UPDATE LIBOT SET ISSUED_STATUS=1, ISSUED_TO=%s, AVAILABILITY=%s WHERE BOOK_ID=%s")
                                datechecklist=(str(((datetime.datetime.now())+(datetime.timedelta(days=5))).date()).split("-"))
                                newavailable=datechecklist[2]+"/"+datechecklist[1]+"/"+datechecklist[0]
                                data=(rolltobeissued,newavailable,textt[1].replace(' ',''))
                                print(data)
                                try:
                                   self.cursor.execute(sql,data)
                                   self.db.commit()
                                   print("LIBOT Database Updated")
                                except:
                                   self.db.rollback()
                                   self.reupdatedatabase(sql,data)
                                   
                                if tempp:
                                    print("JOB DONE AB password mangna chahiye")
                                break
                            else:
                                print("return book")

                                tempp=False
                                text8=tex[0]
                                text9=""
                                text10="0"
                                texttt=[]
                                texttt.append(text8)
                                texttt.append(text9)
                                texttt.append(text10)
                                statuse=False
                                self.findkeys()
                                i=0
                                while i<3:
                                    statuse=False
                                    statuse = self.write(texttt[i],Blocks[i])
                                    if statuse == False:
                                        break
                                    i+=1
                
                                if statuse == True:
                                    print("BOOK CARD WRITTEN Returned")
                                    self.errormsgcard()
                                    tempp=self.newreadreturnClicked()
                                else:
                                    print("BOOK CARD NOT WRITTEN Returned")
                                
                                if not self.db.open:
                                    self.db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
                                    self.cursor = self.db.cursor()
                                    print("Database Connected")
                                print("Updateing Database return")
                                sql=("SELECT no_book_issued FROM Student WHERE roll_no=%s")
                                data=(rolltobeissued)
                                try:
                                    self.cursor.execute(sql,data)
                                except:
                                    self.reselectdatabase(sql,data)
                                booksissued=list(self.cursor.fetchall()[0])[0]
                                print("booksissued "+str(booksissued))
                                
                                sql=("UPDATE Student SET no_book_issued=%s WHERE roll_no=%s")
                                data=(booksissued-1,rolltobeissued)
                                try:
                                   self.cursor.execute(sql,data)
                                   self.db.commit()
                                   print("Student Database Updated for Return")
                                except:
                                   self.db.rollback()
                                   self.reupdatedatabase(sql,data)
                                    
                                sql=("UPDATE LIBOT SET ISSUED_STATUS=0, ISSUED_TO=0, AVAILABILITY=%s WHERE BOOK_ID=%s")
                                availablitylist=(str(datetime.datetime.now().date()).split("-"))
                                newavailable=availablitylist[2]+"/"+availablitylist[1]+"/"+availablitylist[0]
                                data=(newavailable,textt[1].replace(' ',''))
                                print(data)
                                try:
                                   self.cursor.execute(sql,data)
                                   self.db.commit()
                                   print("LIBOT Database Updated Returned")
                                except:
                                   self.db.rollback()
                                   self.reupdatedatabase(sql,data)
                                   
                                if tempp:
                                    print("JOB DONE Returned AB password mangna chahiye")
                                break
                            print("33return")
        except:
            self.crashingmsg()

    def reupdatedatabase(self,sql,data):
        if not self.db.open:
            self.db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
            self.cursor = self.db.cursor()
            print("Database Connected")
        try:
            self.cursor.execute(sql,data)
            self.db.commit()
        except:
            print("Retried Not going database")
            self.db.rollback()
            self.errorestart()
        
    def reselectdatabase(self,sql,data):
        if not self.db.open:
            self.db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
            self.cursor = self.db.cursor()
            print("Database Connected")
        try:
            self.cursor.execute(sql,data)
        except:
            print("Retried Not going database")
            self.errorestart()
            
    def newreadreturnClicked(self):
        try:
            while continue_reading:
                if not self.db.open:
                    self.db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
                    self.cursor = self.db.cursor()
                    print("Database Connected")
                check,tex=self.cardread()
                if check==True and (len(tex)==3):
                    textt=tex[0].split("==")
                    if textt[0]=='S':
                        print("S")
                        text8=textt[0]+"=="+textt[1]+"=="+str(int(textt[2])-1)
                        text9=""
                        text10=tex[2]
                        texttt=[]
                        texttt.append(text8)
                        texttt.append(text9)
                        texttt.append(text10)
                        statuse=False
                        self.findkeys()
                        i=0
                        while i<3:
                            statuse=False
                            statuse = self.write(texttt[i],Blocks[i])
                            if statuse == False:
                                break
                            i+=1
                
                        if statuse == True:
                            print("STUDENT CARD WRITTEN Returned")
                            self.savesuccessreturned()
                            return True
                        else:
                            print("STUDENT CARD NOT WRITTEN Returned")
                    else:
                        print("B")
                        self.errormsgcard()
        except:
            self.crashingmsg()
                
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
        
    def write(self,datatext,blockaddre):
        print("write")
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
            print("write end")
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
            
    def newreadClicked(self):
        try:
            while continue_reading:
                if not self.db.open:
                    self.db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
                    self.cursor = self.db.cursor()
                    print("Database Connected")
                check,tex=self.cardread()
                if check==True and (len(tex)==3):
                    textt=tex[0].split("==")
                    if textt[0]=='S':
                        print("S")
                        text8=textt[0]+"=="+textt[1]+"=="+str(int(textt[2])+1)
                        text9=""
                        text10=tex[2]
                        texttt=[]
                        texttt.append(text8)
                        texttt.append(text9)
                        texttt.append(text10)
                        statuse=False
                        self.findkeys()
                        i=0
                        while i<3:
                            statuse=False
                            statuse = self.write(texttt[i],Blocks[i])
                            if statuse == False:
                                break
                            i+=1
                
                        if statuse == True:
                            print("STUDENT CARD WRITTEN")
                            self.savesuccess()
                            return True
                        else:
                            print("STUDENT CARD NOT WRITTEN")
                    else:
                        print("B")
                        self.errormsgcard()
        except:
            self.crashingmsg()
        
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
