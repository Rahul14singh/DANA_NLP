from PyQt5 import QtGui, QtWidgets, QtCore 
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QRadioButton, QButtonGroup, QLabel, QLineEdit, QFormLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, pyqtSlot
import pymysql
import sys
import time
import datetime

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
        self.initUI()
        
    def initUI(self):
        
        try:
            self.setWindowState(QtCore.Qt.WindowMaximized)
        except:
            self.setGeometry(10, 30, 1350, 750)
            
        self.setWindowTitle('Dana')
        
        self.setWindowIcon(QIcon('download.png')) # Have this png at same directory as this code is. Icon Image
        
        oImage = QImage("download(1).jpg") # Have this png at same directory as this code is. Background Image
        sImage = oImage.scaled(QSize(1350,750))                   
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        
        saveButton = QPushButton("ADD/MODIFY",self)
        deleteButton = QPushButton("DELETE",self)
        clearButton = QPushButton("CLEAR",self)
        TrainButton = QPushButton("Train DANA",self)
        saveButton.setFont(QtGui.QFont("Calibri", 13))
        deleteButton.setFont(QtGui.QFont("Calibri", 13))
        clearButton.setFont(QtGui.QFont("Calibri", 13))
        TrainButton.setFont(QtGui.QFont("Calibri", 13))
        saveButton.move(100,690)
        clearButton.move(260,690)
        TrainButton.move(420,690)
        saveButton.clicked.connect(self.saveClicked)
        deleteButton.clicked.connect(self.deleteClicked)
        clearButton.clicked.connect(self.clearClicked)
        TrainButton.clicked.connect(self.TrainClicked)
        saveButton.setStyleSheet("background-color: #F7CE16")
        deleteButton.setStyleSheet("background-color: #F7CE16")
        clearButton.setStyleSheet("background-color: #F7CE16")
        TrainButton.setStyleSheet("background-color: #F7CE16")

        headerfont = QtGui.QFont("Cambria", 13, QtGui.QFont.Bold)

        l1 = QLabel("BOOK ID: ")
        l1.setFont(headerfont)
        l1.setMinimumHeight(30)
        l1.setFixedWidth(180)
        text1 = QLineEdit()
        text1.setFixedWidth(250)
        text1.setMinimumHeight(30)
        text1.setPlaceholderText("The Library Book ID ")
        text1.setFont(QtGui.QFont("Times", 11))

        l2 = QLabel("AUTHOR: ")
        l2.setFont(headerfont)
        l2.setMinimumHeight(30)
        l2.setFixedWidth(180)
        text2 = QLineEdit()
        text2.setFixedWidth(600)
        text2.setMinimumHeight(30)
        text2.setPlaceholderText(" EX: Sumitra Arora ")
        text2.setFont(QtGui.QFont("Times", 11))

        l3 = QLabel("TITLE: ")
        l3.setFont(headerfont)
        l3.setMinimumHeight(30)
        l3.setFixedWidth(180)
        text3 = QLineEdit()
        text3.setFixedWidth(600)
        text3.setMinimumHeight(30)
        text3.setPlaceholderText(" EX: Artificial Intelligence,C,C++ ")
        text3.setFont(QtGui.QFont("Times", 11))

        l4 = QLabel("PUBLICATION: ")
        l4.setFont(headerfont)
        l4.setMinimumHeight(30)
        l4.setFixedWidth(180)
        text4 = QLineEdit()
        text4.setFixedWidth(600)
        text4.setMinimumHeight(30)
        text4.setPlaceholderText(" EX: TATA MCGRAW HILL ")
        text4.setFont(QtGui.QFont("Times", 11))

        l5 = QLabel("EDITION: ")
        l5.setFont(headerfont)
        l5.setMinimumHeight(30)
        l5.setFixedWidth(180)
        text5 = QLineEdit()
        text5.setFixedWidth(250)
        text5.setMinimumHeight(30)
        text5.setPlaceholderText(" EX: 1,2,3 ")
        text5.setFont(QtGui.QFont("Times", 11))

        l6 = QLabel("ISSUE STATUS: ")
        l6.setFont(headerfont)
        l6.setMinimumHeight(30)
        l6.setFixedWidth(200)

        hboxperiod = QHBoxLayout()
        hboxperiod.setSpacing(70)
        r1 = QRadioButton("BOOK ISSUED")
        r1.setFont(QtGui.QFont("Calibri", 9, QtGui.QFont.Bold))
        r1.setMinimumHeight(30)
        r2 = QRadioButton("NOT ISSUED")
        r2.setFont(QtGui.QFont("Calibri", 9, QtGui.QFont.Bold))
        r2.setMinimumHeight(30)
        r2.setChecked(True)
        widgetperiod=QWidget(self)
        groupperiod=QButtonGroup(widgetperiod)
        groupperiod.addButton(r1)
        groupperiod.addButton(r2)
        hboxperiod.addWidget(r1)
        hboxperiod.addWidget(r2)
        hboxperiod.addStretch()
        

        l7 = QLabel("PRICE: ")
        l7.setFont(headerfont)
        l7.setMinimumHeight(30)
        l7.setFixedWidth(200)
        text7 = QLineEdit()
        text7.setFixedWidth(250)
        text7.setMinimumHeight(30)
        text7.setPlaceholderText("Price of the Book")
        text7.setFont(QtGui.QFont("Times", 11))
        
        l8 = QLabel("ROW NUMBER: ")
        l8.setFont(headerfont)
        l8.setMinimumHeight(30)
        l8.setFixedWidth(200)
        text8 = QLineEdit()
        text8.setFixedWidth(250)
        text8.setMinimumHeight(30)
        text8.setPlaceholderText("Start counting from Door")
        text8.setFont(QtGui.QFont("Times", 11))

        l9 = QLabel("COLUMN NUMBER: ")
        l9.setFont(headerfont)
        l9.setMinimumHeight(30)
        l9.setFixedWidth(200)
        text9 = QLineEdit()
        text9.setFixedWidth(250)
        text9.setMinimumHeight(30)
        text9.setPlaceholderText("Start counting from the Help Desk")
        text9.setFont(QtGui.QFont("Times", 11))

        l10 = QLabel("SHELF PARTION NUMBER: ")
        l10.setFont(headerfont)
        l10.setMinimumHeight(30)
        l10.setFixedWidth(200)
        text10 = QLineEdit()
        text10.setFixedWidth(250)
        text10.setMinimumHeight(30)
        text10.setPlaceholderText("Start counting from top of the shelf")
        text10.setFont(QtGui.QFont("Times", 11))

        l11 = QLabel("CLASSIFYING SUBJECT: ")
        l11.setFont(headerfont)
        l11.setMinimumHeight(30)
        l11.setFixedWidth(180)
        text11 = QLineEdit()
        text11.setFixedWidth(600)
        text11.setMinimumHeight(30)
        text11.setPlaceholderText(" EX: Mathematics/Science/Computer Science or others.")
        text11.setFont(QtGui.QFont("Times", 11))

        text12 = QLineEdit()
        text12.setFixedWidth(600)
        text12.setMinimumHeight(30)
        text12.setPlaceholderText(" Enter the BOOK ID and Press the Delete Button to delete the data of the book")
        text12.setFont(QtGui.QFont("Times", 11))
        
        fbox = QFormLayout()
        fbox.setVerticalSpacing(27)
        fbox.setHorizontalSpacing(30)
        fbox.addRow(l1,text1)
        fbox.addRow(l2,text2)
        fbox.addRow(l3,text3)
        fbox.addRow(l4,text4)
        fbox.addRow(l5,text5)
        fbox.addRow(l11,text11)
        fbox.addRow(l6,hboxperiod)
        fbox.addRow(l7,text7)
        fbox.addRow(l8,text8)
        fbox.addRow(l9,text9)
        fbox.addRow(l10,text10)
        fbox.addRow(deleteButton,text12)
        
        self.setLayout(fbox)
        self.lineedits = [text1,text2,text3,text4,text5,text7,text8,text9,text10,text11]
        self.deletelineedit=[text12]
        self.radiobutton=[r1,r2]
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
        errormsg.setText("All Fields are not properly Mentioned")
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
        
    def errormsgdelete(self):
        errormsgdelete = QMessageBox()
        errormsgdelete.setIcon(QMessageBox.Warning)
        errormsgdelete.setText("Delete Book ID Field is NULL")
        errormsgdelete.setWindowTitle("Error Report")
        errormsgdelete.setWindowIcon(QIcon('download.png'))
        errormsgdelete.exec()

    def deletesuccess(self):
        deletemsg = QMessageBox()
        deletemsg.setIcon(QMessageBox.Information)
        deletemsg.setText("The Details Of Book is deleted !")
        deletemsg.setWindowTitle("DELETED")
        deletemsg.setWindowIcon(QIcon('download.png'))
        deletemsg.exec()

    def Trainsuccess(self):
        deletemsg = QMessageBox()
        deletemsg.setIcon(QMessageBox.Information)
        deletemsg.setText("Dana training Initiated !")
        deletemsg.setWindowTitle("TRAINING INITIATED")
        deletemsg.setWindowIcon(QIcon('download.png'))
        deletemsg.exec()

    def TrainClicked(self):
        print("Training Dana............")
        self.workerthread = workerThread()
        self.workerthread.signal.connect(self.Trainsuccess)
        self.workerthread.start()
        
    def deleteClicked(self):
        if not self.db.open:
            self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
            self.cursor = self.db.cursor()
            print("Database Connected")
        try:
            deletingbookid=str((self.deletelineedit)[0].text())
            #print(deletingbookid)
            if deletingbookid:
                sql=("DELETE FROM LIBOT WHERE BOOK_ID=%s")
                try:
                    self.cursor.execute(sql,deletingbookid)
                    self.db.commit()
                    self.workerthread = workerThread()
                    self.workerthread.signal.connect(self.deletesuccess)
                    self.workerthread.start()
                except:
                    self.db.rollback()
                    self.workerthread = workerThread()
                    self.workerthread.signal.connect(self.crashingmsg)
                    self.workerthread.start()
            else:
                self.workerthread = workerThread()
                self.workerthread.signal.connect(self.errormsgdelete)
                self.workerthread.start()
        except:
            self.workerthread = workerThread()
            self.workerthread.signal.connect(self.crashingmsg)
            self.workerthread.start()
            
    def saveClicked(self):
        if not self.db.open:
            self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
            self.cursor = self.db.cursor()
            print("Database Connected")
            
        try:
            tex=[]
            for edit in self.lineedits:
                tex.append(str(edit.text()))
            #print(tex)
                
            yes=0
            for each in tex:
                if each=='':
                    yes=1
                    self.workerthread = workerThread()
                    self.workerthread.signal.connect(self.errormsg)
                    self.workerthread.start()
                    break
                
            if yes==0:
                issue=0
                if self.radiobutton[0].isChecked():
                    issue=1
                if issue==1:
                    available=datetime.datetime.now().date()+datetime.timedelta(days=10)
                else:
                    available=datetime.datetime.now().date()
                available=datetime.datetime.strptime(str(available),'%Y-%m-%d').strftime('%d/%m/%y')
                available=str(available)
                #print(available)

                sql=("SELECT COUNT(1) FROM LIBOT WHERE BOOK_ID = %s")
                data=tex[0]
                self.cursor.execute(sql,data)
                
                if self.cursor.fetchone()[0]:
                    
                    #print("Yeah")
                    
                    sql=("UPDATE LIBOT SET AUTHOR=%s,TITLE=%s,PUBLICATION=%s,CLASSIFYING_SUBJECT=%s, EDITION=%s,ISSUED_STATUS=%s,ROW_NO=%s,COLUMN_NO=%s,PARTITION_NO=%s,PRICE=%s WHERE BOOK_ID=%s")
                    data=(tex[1],tex[2],tex[3],tex[9],int(eval(str(tex[4]))),issue,int(eval(str(tex[6]))),int(eval(str(tex[7]))),int(eval(str(tex[8]))),int(eval(str(tex[5]))),tex[0])

                    try:
                       self.cursor.execute(sql,data)
                       self.db.commit()
                    except:
                       self.db.rollback()
                else:
                    
                    #print("No")
                    
                    sql=("INSERT INTO LIBOT"
                         "(BOOK_ID,AUTHOR,TITLE,PUBLICATION,EDITION,CLASSIFYING_SUBJECT,ISSUED_STATUS,ISSUED_TO,AVAILABILITY,ROW_NO,COLUMN_NO,PARTITION_NO,PRICE)"
                         "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    data=(tex[0],tex[1],tex[2],tex[3],int(eval(str(tex[4]))),tex[9],issue,0,available,int(eval(str(tex[6]))),int(eval(str(tex[7]))),int(eval(str(tex[8]))),int(eval(str(tex[5]))))

                    #print(data)
                    try:
                       self.cursor.execute(sql,data)
                       self.db.commit()
                    except:
                       self.db.rollback()
                    
                self.workerthread = workerThread()
                self.workerthread.signal.connect(self.savesuccess)
                self.workerthread.start()
                #print("saved")
        except:
            self.workerthread = workerThread()
            self.workerthread.signal.connect(self.crashingmsg)
            self.workerthread.start()

    def clearClicked(self):
        for edit in self.lineedits:
            edit.clear()
        self.deletelineedit[0].clear()
        self.radiobutton[1].setChecked(True)
        #print("clear")
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.db.close()
        else:
            event.ignore()
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = General()
    sys.exit(app.exec_())
