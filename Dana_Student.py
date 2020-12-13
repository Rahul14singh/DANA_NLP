from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QScrollBar, QSplitter, QTableWidgetItem, QTableWidget, QWidget, QApplication, QPushButton, QHBoxLayout, QRadioButton, QMainWindow, QAction
from PyQt5.QtWidgets import QButtonGroup, QLabel, QLineEdit, QFormLayout, QMessageBox, QComboBox, QVBoxLayout, QGridLayout, QDialog, QTextEdit, QProgressBar, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QImage, QPalette, QBrush, QPixmap, QTextCursor, QTextTableFormat, QTextFrame
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, pyqtSlot, QCoreApplication
from json import dumps, JSONEncoder,loads
from base64 import b64encode, b64decode
import httplib2
import base64
import json
import pymysql
import sys
import time
import datetime


httplib2.debuglevel = 0
http = httplib2.Http()
apiMethod="https://"
apiVersion="/v1/"
apiServer="api.dialogflow.com"
url = apiMethod + apiServer + apiVersion
Headers={
    'Authorization': 'Bearer cb28f1577da7457087c01cff1ee12e84', # This key will change based on your DialogFlow account it is dummy key for now. 
    'Content-Type': 'application/json'
    }
subjectsinpreference=[]
authorsinpreference=[]
titlesinpreference=[]
publicationsinpreference=[]
bookidsinpreference=[]

def trap_exc_during_debug(*args):
    print(args)

sys.excepthook = trap_exc_during_debug

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        return {'_python_object': b64encode(pickle.dumps(obj)).decode('utf-8')}
    
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
        self.setWindowIcon(QIcon('download.png'))
        oImage = QImage("download(1).jpg")
        sImage = oImage.scaled(QSize(1350,750))                   
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.chatinterface=QTextEdit(self)
        self.chatinterface.setReadOnly(True)
        self.chatinterface.setFont(QtGui.QFont("Times", 14))
        
        sendButton=QPushButton('SEND',self)
        sendButton.setFont(QtGui.QFont("Calibri", 13))
        sendButton.clicked.connect(self.sendClicked)
        sendButton.setStyleSheet("background-color: #F7CE16")
        
        self.textasked=QLineEdit(self)
        self.textasked.setFont(QtGui.QFont("Times", 12))
        self.textasked.setPlaceholderText("Enter Here ! ")
        self.textasked.setMinimumHeight(40)
        self.textasked.returnPressed.connect(sendButton.click)
        
        grid = QGridLayout()
        grid.setSpacing(3)
        grid.addWidget(self.chatinterface, 0, 0, 1, 3)
        grid.addWidget(self.textasked, 1, 0, 1, 1)
        grid.addWidget(sendButton, 1, 2)
        grid.setRowStretch(0,1)
        grid.setColumnStretch(0,1)
        self.setLayout(grid)        
        self.show()
    
    def crashingmsg(self):
        crashmsg = QMessageBox()
        crashmsg.setIcon(QMessageBox.Critical)
        crashmsg.setText("SOMETHING IS WRONG !!")
        crashmsg.setDetailedText("Click Ok and try again and If still not working then close the Application and start again")
        crashmsg.setWindowTitle("Application Crashing")
        crashmsg.setWindowIcon(QIcon('download.png'))
        crashmsg.exec()

    def errormsg(self):
        errormsg = QMessageBox()
        errormsg.setIcon(QMessageBox.Warning)
        errormsg.setText("Enter Something in the text field to query !")
        errormsg.setWindowTitle("Error Report")
        errormsg.setWindowIcon(QIcon('download.png'))
        errormsg.exec()

    def listing(self):
        #print("listing")
        if not self.db.open:
            self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
            self.cursor = self.db.cursor()
            print("Database Connected")   
        checkset=0
        sql='SELECT BOOK_ID,AUTHOR,TITLE,PUBLICATION,EDITION,CLASSIFYING_SUBJECT,AVAILABILITY,ROW_NO,COLUMN_NO,PARTITION_NO FROM LIBOT WHERE '
        if len(bookidsinpreference):
            checkset=1
            sql+='BOOK_ID IN (' + ','.join(('"{0}"'.format(str(x)) for x in bookidsinpreference)) + ')'
        if len(authorsinpreference):
            if checkset==1:
                sql+=' OR '
            else:
                checkset=1
            sql+='AUTHOR IN (' + ','.join(('"{0}"'.format(str(x)) for x in authorsinpreference)) + ')'
        if len(titlesinpreference):
            if checkset==1:
                sql+=' OR '
            else:
                checkset=1
            sql+='TITLE IN (' + ','.join(('"{0}"'.format(str(x)) for x in titlesinpreference)) + ')'
        if len(publicationsinpreference):
            if checkset==1:
                sql+=' OR '
            else:
                checkset=1
            sql+='PUBLICATION IN (' + ','.join(('"{0}"'.format(str(x)) for x in publicationsinpreference)) + ')'
        if len(subjectsinpreference):
            if checkset==1:
                sql+=' OR '
            else:
                checkset=1
            sql+='CLASSIFYING_SUBJECT IN (' + ','.join(('"{0}"'.format(str(x)) for x in subjectsinpreference)) + ')'
        #print(sql)
        try:
            if len(bookidsinpreference) or len(authorsinpreference) or len(titlesinpreference) or len(publicationsinpreference) or len(subjectsinpreference):
                if not self.db.open:
                    self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
                    self.cursor = self.db.cursor()
                    print("Database Connected")
                self.cursor.execute(sql)
                answersql = self.cursor.fetchall()
                if len(answersql):
                    entries=['BOOK ID','AUTHOR','TITLE','PUBLICATION','EDITION','SUBJECT','AVAILABILITY','ROW NO','COLUMN NO','PARTITION NO']
                    textBlockFormat = QTextTableFormat()
                    textBlockFormat.setAlignment(Qt.AlignRight)
                    cursor = QTextCursor()
                    self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                    cursor = self.chatinterface.textCursor()
                    cursor.insertTable(len(answersql)+1,10,textBlockFormat)
                    for val in entries:
                        cursor.insertText(str(val))
                        cursor.movePosition(QTextCursor.NextCell)
                    for val in answersql:
                        for value in val:
                            cursor.insertText(str(value))
                            cursor.movePosition(QTextCursor.NextCell)
                else:
                    self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                    self.chatinterface.append(str(" Your search is empty! "))
                    cursor = QTextCursor()
                    cursor = self.chatinterface.textCursor()
                    textBlockFormat = cursor.blockFormat()
                    textBlockFormat.setAlignment(Qt.AlignRight)
                    cursor.mergeBlockFormat(textBlockFormat)
                    self.chatinterface.setTextCursor(cursor)
                    self.chatinterface.append(" ")
            else:
                self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                self.chatinterface.append(str(" Your search is empty! "))
                cursor = QTextCursor()
                cursor = self.chatinterface.textCursor()
                textBlockFormat = cursor.blockFormat()
                textBlockFormat.setAlignment(Qt.AlignRight)
                cursor.mergeBlockFormat(textBlockFormat)
                self.chatinterface.setTextCursor(cursor)
                self.chatinterface.append(" ")
        except:
            self.workerthread = workerThread()
            self.workerthread.signal.connect(self.crashingmsg)
            self.workerthread.start()
        
    def available(self,addthis,dateinquired):
        #print(addthis)
        #print(dateinquired)
        if not self.db.open:
            self.db=pymysql.connect("#IP ADDRESS FOR DB","#USERID","#PASSWORD","#DB_NAME") # Replace your DB details here
            self.cursor = self.db.cursor()
            print("Database Connected")
        for val in addthis:
            sql='SELECT AVAILABILITY FROM LIBOT WHERE BOOK_ID=%s'
            try:
                self.cursor.execute(sql,val)
                availability = self.cursor.fetchone()[0]
                checkavailable=datetime.datetime.strptime(str(dateinquired),'%Y-%m-%d').strftime('%d/%m/%y')
                #print(availability)
                #print(checkavailable)
                listavailability = availability.split('/')
                listavailable = checkavailable.split('/')
                listavailability = [int(x) for x in listavailability]
                listavailable = [int(x) for x in listavailable]
                if listavailable[2] >= listavailability[2]:
                    if listavailable[1] >= listavailability[1]:
                        if listavailable[0] >= listavailability[0]:
                            self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                            self.chatinterface.append("The book is available! ")
                            cursor = QTextCursor()
                            cursor = self.chatinterface.textCursor()
                            textBlockFormat = cursor.blockFormat()
                            textBlockFormat.setAlignment(Qt.AlignRight)
                            cursor.mergeBlockFormat(textBlockFormat)
                            self.chatinterface.setTextCursor(cursor)
                            self.chatinterface.append(" ")
                        else:
                            self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                            self.chatinterface.append("The book is available from " + str(availability))
                            cursor = QTextCursor()
                            cursor = self.chatinterface.textCursor()
                            textBlockFormat = cursor.blockFormat()
                            textBlockFormat.setAlignment(Qt.AlignRight)
                            cursor.mergeBlockFormat(textBlockFormat)
                            self.chatinterface.setTextCursor(cursor)
                            self.chatinterface.append(" ")
                    else:
                        self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                        self.chatinterface.append("The book is available from " + str(availability))
                        cursor = QTextCursor()
                        cursor = self.chatinterface.textCursor()
                        textBlockFormat = cursor.blockFormat()
                        textBlockFormat.setAlignment(Qt.AlignRight)
                        cursor.mergeBlockFormat(textBlockFormat)
                        self.chatinterface.setTextCursor(cursor)
                        self.chatinterface.append(" ")
                else:
                    self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                    self.chatinterface.append("The book is available from " + str(availability))
                    cursor = QTextCursor()
                    cursor = self.chatinterface.textCursor()
                    textBlockFormat = cursor.blockFormat()
                    textBlockFormat.setAlignment(Qt.AlignRight)
                    cursor.mergeBlockFormat(textBlockFormat)
                    self.chatinterface.setTextCursor(cursor)
                    self.chatinterface.append(" ")
            except:
                self.workerthread = workerThread()
                self.workerthread.signal.connect(self.crashingmsg)
                self.workerthread.start()
                
    def sendClicked(self):
        #print("Send clicked")
        askedquery=str((self.textasked).text()).rstrip("/n/0")
        self.textasked.setText("")
        try:
            if askedquery:
                self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                self.chatinterface.setTextColor(Qt.red)
                self.chatinterface.append(askedquery)
                self.chatinterface.setTextColor(Qt.black)
                cursor = QTextCursor()
                cursor = self.chatinterface.textCursor()
                textBlockFormat = cursor.blockFormat()
                textBlockFormat.setAlignment(Qt.AlignLeft)
                cursor.mergeBlockFormat(textBlockFormat)
                self.chatinterface.setTextCursor(cursor)
                self.chatinterface.append(" ")
                
                urlquery = url + "query?v=20150910"
                Body={"query": askedquery,"sessionId": "12345",'lang': 'en'}
                response,content= http.request(urlquery,'POST',headers=Headers,body=dumps(Body,cls=PythonObjectEncoder))
                answerjson = json.loads(content.decode('utf-8'))
                #print(answerjson)
                if (answerjson['status'])['code']==200:
                    answerjsontime=answerjson['timestamp']
                    answerjsonparameters=(answerjson['result'])['parameters']
                    answerjsonspeech=((answerjson['result'])['fulfillment'])['speech']
                    answerjsonintentname=((answerjson['result'])['metadata'])['intentName']
                    answerjsonaction=(answerjson['result'])['action']
                    #print(answerjson)
                    #self.chatinterface.append(str(answerjson))
                    #self.chatinterface.append(str(answerjson['result']))
                    #self.chatinterface.append(str(answerjsontime))
                    #self.chatinterface.append(str(answerjsonparameters))
                    #self.chatinterface.append(str(answerjsonintentname))
                    #self.chatinterface.append(str(answerjsonaction))
                    self.chatinterface.moveCursor(QtGui.QTextCursor.End)
                    self.chatinterface.append(str(answerjsonspeech))

                    cursor = QTextCursor()
                    cursor = self.chatinterface.textCursor()
                    textBlockFormat = cursor.blockFormat()
                    textBlockFormat.setAlignment(Qt.AlignRight)
                    cursor.mergeBlockFormat(textBlockFormat)
                    self.chatinterface.setTextCursor(cursor)
                    self.chatinterface.append(" ")
                    #print(answerjsonparameters)
                    #print(answerjsonintentname)
                    #print(answerjsonaction)
                    
                    if 'SUBJECTS' in answerjsonparameters.keys():
                        addthis = answerjsonparameters['SUBJECTS']
                        for val in addthis:
                            if val not in subjectsinpreference:
                                subjectsinpreference.append(val)
                                
                    if 'AUTHORS' in answerjsonparameters.keys():
                        addthis = answerjsonparameters['AUTHORS']
                        for val in addthis:
                            if val not in authorsinpreference:
                                authorsinpreference.append(val)
                                
                    if 'TITLES' in answerjsonparameters.keys():
                        addthis = answerjsonparameters['TITLES']
                        for val in addthis:
                            if val not in titlesinpreference:
                                titlesinpreference.append(val)
                                
                    if 'PUBLICATIONS' in answerjsonparameters.keys():
                        addthis = answerjsonparameters['PUBLICATIONS']
                        for val in addthis:
                            if val not in publicationsinpreference:
                                publicationsinpreference.append(val)
                                
                    if 'BOOK_IDS' in answerjsonparameters.keys():
                        addthis = answerjsonparameters['BOOK_IDS']
                        for val in addthis:
                            if val not in bookidsinpreference:
                                bookidsinpreference.append(val)
                                
                    if 'List' in answerjsonparameters.keys():
                        if answerjsonparameters['List']:
                            self.listing()
                            
                    if 'BOOK_IDS' in answerjsonparameters.keys() and len(answerjsonparameters['BOOK_IDS']):
                        if 'date' in answerjsonparameters.keys() and len(answerjsonparameters['date']):
                            self.available(answerjsonparameters['BOOK_IDS'],answerjsonparameters['date'])
                        else:
                            self.available(answerjsonparameters['BOOK_IDS'],datetime.datetime.now().date())
                            
                    #print(subjectsinpreference)
                    #print(authorsinpreference)
                    #print(titlesinpreference)
                    #print(publicationsinpreference)
                    #print(bookidsinpreference)
                else:
                    self.workerthread = workerThread()
                    self.workerthread.signal.connect(self.crashingmsg)
                    self.workerthread.start()
            else:
                self.workerthread = workerThread()
                self.workerthread.signal.connect(self.errormsg)
                self.workerthread.start()
        except:
            self.workerthread = workerThread()
            self.workerthread.signal.connect(self.crashingmsg)
            self.workerthread.start()
            
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
