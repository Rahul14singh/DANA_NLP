# DANA_NLP

Dana (Pronounced Diana) is an NLP powered virtual librarian. She is capable of answering all books related queries in a library with a GUI based application and can also be integrated with Facebook messenger for a more user-friendly experience.

## Usage:

There are 3 parts of the whole system.
  1. Management Interface   : GUI interface where the entry for every existing book and any new book is done to be stored on DB such that Dana can be trained out of this DB and she knows all the books and specifics of books in the library. ` Dana_Manage_sql.py `
  2. Student Interface      : GUI interface which is used by students to chit-chat with Dana and find the queries answered. Queries can be Books specific and general things. It's same as talking like a 6 to 7 yrs kid. Alternatively, if Facebook is integrated that can be used instead of this interface. ` Dana_Student.py `
  3. Library Exit Interface : GUI interface Running on a Raspberry Pi installed at the exit of the library so that students can issue the books, return the books without any trouble and human interference. Students will come to the library to study or issue books only after checking the availability of same using the Student Interface. Thus an efficient and time-saving experience for students. Books will only be issued after proper authentication. ` gui_issue_return.py `
  4. Intermediate Script    : This is an intermediate script called by Dana_Manage_sql.py to train Dana with the current/new database. ` intermediate_bot_train.py `

## Requirements:

1. Python 3 or later 
2. DialogFlow account (api.dialogflow.com) or similar. It's free and can be made from the given link below. 
3. Some Images you want to set in the background of your GUI Window. I have attached the default ones that I used.
4. A Hosting so that you can connect and maintain the database (Here I used MySql) for the Library Database storing data of books & Student Database storing data of students and books issued by students.
5. Some other necessary supporting libraries as per code.

Install  [Python](https://www.python.org/downloads/) . Do install Python3 or later.

if facing difficulty in installing libraries here is the link for the HELP:

1. [DialogFlow](https://dialogflow.cloud.google.com/)

> Do note down the userName and password of the DialogFlow account that you made. We will need in the code.

## Instructions and Setup Environment:

-  Raspberry should have code ` gui_issue_return.py `.
-  The code ` Dana_Manage_sql.py `, ` Dana_Student.py `, ` intermediate_bot_train.py ` and the images (Background Image & Icon Image) should be in the same directory or make changes as per the directory structure in the code.
-  First ` Dana_Manage_sql.py ` should be run to create/update records of books in the database. A similar database should be made for student records having a count of books issued. Details can be seen in the code and video posted below.
-  Then Dana should be trained from the same interface as above for all the new entries and updates in the database. This will internally run ` intermediate_bot_train.py ` automatically. 
-  Now ` Dana_Student.py ` should be used for general chit-chat and queries by students. Alternatively, Messenger can also be used here.
-  ` gui_issue_return.py ` should be run on Raspberry Pi and the setup with RFID Card reader and GUI should be setup at the exit of the Library.
-  Each student will need to show RFID Cards to get out of the library with issued books or return books. Both books and students will have their respective RFID cards will they will have to show during exit from the library. 

## Run:

```
  python Dana_Manage_sql.py
  python Dana_Student.py
  python gui_issue_return.py // this one is on Raspberry Pi
```
## Vedio:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/dmeZ23E9hss/0.jpg)](https://youtu.be/dmeZ23E9hss)

