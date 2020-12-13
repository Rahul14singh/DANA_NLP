from json import dumps, JSONEncoder,loads
from base64 import b64encode, b64decode
import httplib2
import base64
import json
import pymysql
import requests

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        return {'_python_object': b64encode(pickle.dumps(obj)).decode('utf-8')}

httplib2.debuglevel = 0
http = httplib2.Http()
apiMethod="https://"
apiVersion="/v1"
apiServer="api.dialogflow.com"
book_ids=[]
authors=[]
titles=[]
publications=[]
subjects=[]
entitychecklist={}
entries_entityname={}
url = apiMethod + apiServer + apiVersion+ "/entities?v=20150910"
Headers={
    'Authorization': 'Bearer 01576825c1dc48fa9844a71dc19394a8',
    'Content-Type': 'application/json'
    }
print("Bot training initiating ..........")
response,content= http.request(url,'GET',headers=Headers)
#print (response)
#print (content)
entities = json.loads(content.decode('utf-8'))
#print(entities)
entitylist=[]
for val in entities:
    entitylist.append((val['name'],val['id']))
#print(entitylist)
for val in entitylist:
    if val[0]=="BOOK_IDS":
        urli=apiMethod + apiServer + apiVersion+ "/entities/" + val[1] +"?v=20150910"
        response,content= http.request(urli,'GET',headers=Headers)
        #print(response)
        #print(content)
        book_id_details = json.loads(content.decode('utf-8'))
        templist=[]
        for term in book_id_details['entries']:
            templist2=term['synonyms']
            templist.append(term['value'])
            for term2 in templist2:
                if term2 not in templist:
                    templist.append(term2)
        #print(book_id_details)
        entitychecklist['BOOK_IDS']=templist
        entries_entityname['BOOK_IDS']=book_id_details['entries']
    else:
        if val[0]=="AUTHORS":
            urli=apiMethod + apiServer + apiVersion+ "/entities/" + val[1] +"?v=20150910"
            response,content= http.request(urli,'GET',headers=Headers)
            #print(response)
            #print(content)
            authors_details = json.loads(content.decode('utf-8'))
            templist=[]
            for term in authors_details['entries']:
                templist2=term['synonyms']
                templist.append(term['value'])
                for term2 in templist2:
                    if term2 not in templist:
                        templist.append(term2)
            #print(authors_details)
            entitychecklist['AUTHORS']=templist
            entries_entityname['AUTHORS']=authors_details['entries']
        else:
            if val[0]=="TITLES":
                urli=apiMethod + apiServer + apiVersion+ "/entities/" + val[1] +"?v=20150910"
                response,content= http.request(urli,'GET',headers=Headers)
                #print(response)
                #print(content)
                titles_details = json.loads(content.decode('utf-8'))
                templist=[]
                for term in titles_details['entries']:
                    templist2=term['synonyms']
                    templist.append(term['value'])
                    for term2 in templist2:
                        if term2 not in templist:
                            templist.append(term2)
                #print(titles_details)
                entitychecklist['TITLES']=templist
                entries_entityname['TITLES']=titles_details['entries']
            else:
                if val[0]=="PUBLICATIONS":
                    urli=apiMethod + apiServer + apiVersion+ "/entities/" + val[1] +"?v=20150910"
                    response,content= http.request(urli,'GET',headers=Headers)
                    #print(response)
                    #print(content)
                    publications_details = json.loads(content.decode('utf-8'))
                    templist=[]
                    for term in publications_details['entries']:
                        templist2=term['synonyms']
                        templist.append(term['value'])
                        for term2 in templist2:
                            if term2 not in templist:
                                templist.append(term2)
                    #print(publications_details)
                    entitychecklist['PUBLICATIONS']=templist
                    entries_entityname['PUBLICATIONS']=publications_details['entries']
                else:
                    if val[0]=="SUBJECTS":
                        urli=apiMethod + apiServer + apiVersion+ "/entities/" + val[1] +"?v=20150910"
                        response,content= http.request(urli,'GET',headers=Headers)
                        #print(response)
                        #print(content)
                        subjects_details = json.loads(content.decode('utf-8'))
                        templist=[]
                        for term in subjects_details['entries']:
                            templist2=term['synonyms']
                            templist.append(term['value'])
                            for term2 in templist2:
                                if term2 not in templist:
                                    templist.append(term2)
                        #print(subjects_details)
                        entitychecklist['SUBJECTS']=templist
                        entries_entityname['SUBJECTS']=subjects_details['entries']

#print(entitychecklist)
#print(entries_entityname)
db=pymysql.connect("192.185.78.17","lifeisio_Rahul","lifeisiot","lifeisio_LIBNLP")
cursor = db.cursor()
#print("Database Connected")

def getvaluesentities():
    sql=("SELECT BOOK_ID FROM LIBOT")
    cursor.execute(sql)
    idi=cursor.fetchall()
    #print(idi)
    book_id=list(idi)
    #print(book_id)
    i=0
    while i<len(book_id):
        book_id[i]=(list(book_id[i]))[0]
        i+=1
    #print(book_id)
    book_ids.append(book_id)
    
    sql=("SELECT DISTINCT AUTHOR FROM LIBOT")
    cursor.execute(sql)
    auth=cursor.fetchall()
    #print(auth)
    author=list(auth)
    #print(author)
    i=0
    while i<len(author):
        author[i]=(list(author[i]))[0]
        i+=1
    #print(author)
    authors.append(author)

    sql=("SELECT DISTINCT TITLE FROM LIBOT")
    cursor.execute(sql)
    title=cursor.fetchall()
    #print(title)
    titless=list(title)
    #print(titless)
    i=0
    while i<len(titless):
        titless[i]=(list(titless[i]))[0]
        i+=1
    #print(titless)
    titles.append(titless)

    sql=("SELECT DISTINCT PUBLICATION FROM LIBOT")
    cursor.execute(sql)
    publication=cursor.fetchall()
    #print(publication)
    publicationss=list(publication)
    #print(publicationss)
    i=0
    while i<len(publicationss):
        publicationss[i]=(list(publicationss[i]))[0]
        i+=1
    #print(publicationss)
    publications.append(publicationss)

    sql=("SELECT DISTINCT CLASSIFYING_SUBJECT FROM LIBOT")
    cursor.execute(sql)
    sub=cursor.fetchall()
    #print(sub)
    subjectss=list(sub)
    #print(subjectss)
    i=0
    while i<len(subjectss):
        subjectss[i]=(list(subjectss[i]))[0]
        i+=1
    #print(subjectss)
    subjects.append(subjectss)

getvaluesentities()
#print(book_ids[0])
#print(authors[0])
#print(titles[0])
#print(publications[0])
#print(subjects[0])

urlintent=apiMethod + apiServer + apiVersion+ "/intents?v=20150910"
response,content= http.request(urlintent,'GET',headers=Headers)
#print(response)
#print(content)
intentjsondict={}
intentjson=json.loads(content.decode('utf-8'))
#print(intentjson)
for val in intentjson:
    intentjsondict[val['name']]=val['id']
#print(intentjsondict)

if book_ids[0]:
    urliintent=apiMethod + apiServer + apiVersion + "/intents/" + intentjsondict['Intent Book IDS'] + "?v=20150910"
    response,content= http.request(urliintent,'GET',headers=Headers)
    #print(response)
    #print(content)
    urliintentjsonBody=json.loads(content.decode('utf-8'))
    urliintentjson_changethis=urliintentjsonBody['userSays']
    for val in book_ids[0]:
        if val not in entitychecklist['BOOK_IDS']:
            values={}
            valuelist=[]
            valuelist.append(str(val))
            values['synonyms']=valuelist
            values['value']=val
            entries_entityname['BOOK_IDS'].append(values)
        usersaysdict={}
        usersaysdict['count']=0
        usersaysdict['isTemplate']=False
        usersaysdict['isAuto']=False
        usersaysdict['data']=[{'text': str(val), 'alias': 'BOOK_IDS', 'meta': '@BOOK_IDS', 'userDefined': True}]
        urliintentjson_changethis.append(usersaysdict)
    urliintentjsonBody['userSays']=urliintentjson_changethis
    for val in entitylist:
        if val[0]=="BOOK_IDS":
            ID=val[1]
    #print(entries_entityname['BOOK_IDS'])
    urlentityjson=apiMethod + apiServer + apiVersion + '/entities/' + ID +'?v=20150910'
    Body={'entries':entries_entityname['BOOK_IDS'],'name':'BOOK_IDS'}
    response,content= http.request(urlentityjson,'PUT',headers=Headers,body=dumps(Body,cls=PythonObjectEncoder))
    #print(response)
    #print(content)
    response,content= http.request(urliintent,'PUT',headers=Headers,body=dumps(urliintentjsonBody,cls=PythonObjectEncoder))
    #print(response)
    #print(content)
    
if authors[0]:
    urliintent=apiMethod + apiServer + apiVersion + "/intents/" + intentjsondict['Intent Author'] + "?v=20150910"
    response,content= http.request(urliintent,'GET',headers=Headers)
    #print(response)
    #print(content)
    urliintentjsonBody=json.loads(content.decode('utf-8'))
    urliintentjson_changethis=urliintentjsonBody['userSays']
    for val in authors[0]:
        if val not in entitychecklist['AUTHORS']:
            values={}
            valuelist=[]
            valuelist.append(str(val))
            values['synonyms']=valuelist
            values['value']=val
            entries_entityname['AUTHORS'].append(values)
        usersaysdict={}
        usersaysdict['count']=0
        usersaysdict['isTemplate']=False
        usersaysdict['isAuto']=False
        usersaysdict['data']=[{'text': str(val), 'alias': 'AUTHORS', 'meta': '@AUTHORS', 'userDefined': True}]
        urliintentjson_changethis.append(usersaysdict)
    urliintentjsonBody['userSays']=urliintentjson_changethis
    for val in entitylist:
        if val[0]=="AUTHORS":
            ID=val[1]
    #print(entries_entityname['AUTHORS'])
    urlentityjson=apiMethod + apiServer + apiVersion + '/entities/' + ID +'?v=20150910'
    Body={'entries':entries_entityname['AUTHORS'],'name':'AUTHORS'}
    response,content= http.request(urlentityjson,'PUT',headers=Headers,body=dumps(Body,cls=PythonObjectEncoder))
    #print(response)
    #print(content)
    response,content= http.request(urliintent,'PUT',headers=Headers,body=dumps(urliintentjsonBody,cls=PythonObjectEncoder))
    #print(response)
    #print(content)
    
if titles[0]:
    urliintent=apiMethod + apiServer + apiVersion + "/intents/" + intentjsondict['Intent Titles'] + "?v=20150910"
    response,content= http.request(urliintent,'GET',headers=Headers)
    #print(response)
    #print(content)
    urliintentjsonBody=json.loads(content.decode('utf-8'))
    urliintentjson_changethis=urliintentjsonBody['userSays']
    for val in titles[0]:
        if val not in entitychecklist['TITLES']:
            values={}
            valuelist=[]
            valuelist.append(str(val))
            values['synonyms']=valuelist
            values['value']=val
            entries_entityname['TITLES'].append(values)
        usersaysdict={}
        usersaysdict['count']=0
        usersaysdict['isTemplate']=False
        usersaysdict['isAuto']=False
        usersaysdict['data']=[{'text': str(val), 'alias': 'TITLES', 'meta': '@TITLES', 'userDefined': True}]
        urliintentjson_changethis.append(usersaysdict)
    urliintentjsonBody['userSays']=urliintentjson_changethis
    for val in entitylist:
        if val[0]=="TITLES":
            ID=val[1]
    #print(entries_entityname['TITLES'])
    urlentityjson=apiMethod + apiServer + apiVersion + '/entities/' + ID +'?v=20150910'
    Body={'entries':entries_entityname['TITLES'],'name':'TITLES'}
    response,content= http.request(urlentityjson,'PUT',headers=Headers,body=dumps(Body,cls=PythonObjectEncoder))
    #print(response)
    #print(content)
    response,content= http.request(urliintent,'PUT',headers=Headers,body=dumps(urliintentjsonBody,cls=PythonObjectEncoder))
    #print(response)
    #print(content)

if publications[0]:
    urliintent=apiMethod + apiServer + apiVersion + "/intents/" + intentjsondict['Intent Publication'] + "?v=20150910"
    response,content= http.request(urliintent,'GET',headers=Headers)
    #print(response)
    #print(content)
    urliintentjsonBody=json.loads(content.decode('utf-8'))
    urliintentjson_changethis=urliintentjsonBody['userSays']
    for val in publications[0]:
        if val not in entitychecklist['PUBLICATIONS']:
            values={}
            valuelist=[]
            valuelist.append(str(val))
            values['synonyms']=valuelist
            values['value']=val
            entries_entityname['PUBLICATIONS'].append(values)
        usersaysdict['count']=0
        usersaysdict['isTemplate']=False
        usersaysdict['isAuto']=False
        usersaysdict['data']=[{'text': str(val), 'alias': 'PUBLICATIONS', 'meta': '@PUBLICATIONS', 'userDefined': True}]
        urliintentjson_changethis.append(usersaysdict)
    urliintentjsonBody['userSays']=urliintentjson_changethis
    for val in entitylist:
        if val[0]=="PUBLICATIONS":
            ID=val[1]
    #print(entries_entityname['PUBLICATIONS'])
    urlentityjson=apiMethod + apiServer + apiVersion + '/entities/' + ID +'?v=20150910'
    Body={'entries':entries_entityname['PUBLICATIONS'],'name':'PUBLICATIONS'}
    response,content= http.request(urlentityjson,'PUT',headers=Headers,body=dumps(Body,cls=PythonObjectEncoder))
    #print(response)
    #print(content)
    response,content= http.request(urliintent,'PUT',headers=Headers,body=dumps(urliintentjsonBody,cls=PythonObjectEncoder))
    #print(response)
    #print(content)

if subjects[0]:
    urliintent=apiMethod + apiServer + apiVersion + "/intents/" + intentjsondict['Intent Subjects'] + "?v=20150910"
    response,content= http.request(urliintent,'GET',headers=Headers)
    #print(response)
    #print(content)
    urliintentjsonBody=json.loads(content.decode('utf-8'))
    urliintentjson_changethis=urliintentjsonBody['userSays']
    for val in subjects[0]:
        if val not in entitychecklist['SUBJECTS']:
            values={}
            valuelist=[]
            valuelist.append(str(val))
            values['synonyms']=valuelist
            values['value']=val
            entries_entityname['SUBJECTS'].append(values)
        usersaysdict['count']=0
        usersaysdict['isTemplate']=False
        usersaysdict['isAuto']=False
        usersaysdict['data']=[{'text': str(val), 'alias': 'SUBJECTS', 'meta': '@SUBJECTS', 'userDefined': True}]
        urliintentjson_changethis.append(usersaysdict)
    urliintentjsonBody['userSays']=urliintentjson_changethis
    for val in entitylist:
        if val[0]=="SUBJECTS":
            ID=val[1]
    #print(entries_entityname['SUBJECTS'])
    urlentityjson=apiMethod + apiServer + apiVersion + '/entities/' + ID +'?v=20150910'
    Body={'entries':entries_entityname['SUBJECTS'],'name':'SUBJECTS'}
    response,content= http.request(urlentityjson,'PUT',headers=Headers,body=dumps(Body,cls=PythonObjectEncoder))
    #print(response)
    #print(content)
    response,content= http.request(urliintent,'PUT',headers=Headers,body=dumps(urliintentjsonBody,cls=PythonObjectEncoder))
    #print(response)
    #print(content)
print("Bot training completed !")
