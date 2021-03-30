import sqlite3
from datetime import datetime
connection = sqlite3.connect('base.db', check_same_thread=False)
cursor = connection.cursor()


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    cursor.execute(query)
    result = cursor.fetchall()
    return result


class DataBase():
    def delete(self, id, type, item):
        select = "DELETE  FROM " + type + \
            " WHERE id=" + str(id)+" AND text='"+item+"'"
        selectors = execute_read_query(connection, select)

    def load(self, id, type):
        if type == 'status':
            select = "SELECT status.id, status.screen, status.lastscreen FROM status WHERE id=" + \
                str(id)
            selectors = execute_read_query(connection, select)
            return selectors
        if type == 'alarmt':
            select = "SELECT alarms.id, alarms.text, alarms.data, alarms.time FROM alarms WHERE data='" + id+"'"
            selectors = execute_read_query(connection, select)
            return selectors
        if type == 'alarms':
            select = "SELECT alarms.id, alarms.text, alarms.data, alarms.time FROM alarms WHERE id=" + \
                str(id)
            selectors = execute_read_query(connection, select)
            return selectors

        else:
            select = "SELECT "+str(type)+".id, "+str(type)+".text, " + \
                str(type)+".data FROM " + type + " WHERE id=" + str(id)
            selectors = execute_read_query(connection, select)
            return selectors

    def update(self, id, type, stunit):
        if type == 'status':
            query = "UPDATE status SET screen='" + \
                stunit['screen']+"' WHERE id='"+str(id)+"'"
            cursor.execute(query)
            connection.commit()

    def save(self, id, type, sunit):
        if type == 'status':
            query = "INSERT INTO status (id, screen,lastscreen) VALUES ('" + str(
                id) + "','"+sunit['screen'] + "','" + sunit['lastscreen']+"');"
            cursor.execute(query)
            connection.commit()
        if type == 'alarms':
            query = "INSERT INTO "+str(type)+" (id, text,data,time) VALUES ('" + str(id) + \
                "','" + sunit['text'] + "','" + \
                    sunit['data'] + "','" + sunit['time'] + "');"
            cursor.execute(query)
            connection.commit()
        else:
            query = "INSERT INTO "+str(type)+" (id, text,data) VALUES ('" + str(id) + \
                "','" + sunit['text'] + "','" + sunit['data'] + "');"
            cursor.execute(query)
            connection.commit()


# db = DataBase()
# id = 445987860
# select = "DELETE  FROM status"
# selectors = execute_read_query(connection, select)

# print(db.load(1,'status'))
# print(db.load(2,'status'))

# print(selectors)
# db.save
# db.save(1,'status',{'screen':'main','lastscreen':'main','savestatus':"false"})
# db.update(2,'status',{'screen':'mainy'})
# print(db.load(1,'status'))
# print(db.load(2,'status'))


# query = "INSERT INTO status (id, screen, savestatus,lastscreen) VALUES ('"+str(i)+"','alarms','keepF','main');"
# cursor.execute(query)
# connection.commit()

# select = "SELECT status.screen, status.savestatus, status.id  FROM status "
# selectors = execute_read_query(connection, select)
# print(selectors)
# query = "UPDATE status SET screen='main', savestatus='keepT'"
# cursor.execute(query)
# connection.commit()
# select = "SELECT status.screen, status.savestatus, status.id FROM status WHERE id = '4455987860'"
# selectors = execute_read_query(connection, select)
# print(selectors)
# db.update()

# db.save(4455987860,'keeps','good5')
# db.save(4455987860,'keeps','good')
# db.save(4455987860,'keeps','good')
# db.save(4455987860,'keeps','good')
# db.save(4455987860,'keeps','good')
# db.save(4455987860,'keeps','good')
# db.save(4455987860,'keeps','good')
# # print(db.load(4455987860,'keeps'))

# # db.save(4455987860,'keeps','goody')

# select = "DELETE FROM keeps WHERE id ='4455987860' AND text = 'good';"

# selectors = execute_read_query(connection, select)
# connection.commit()
# # print(db.load(4455987860,'keeps'))

# queryke = """
# CREATE TABLE IF NOT EXISTS status (
#   id INTEGER,
#   screen TEXT NOT NULL,
#   lastscreen TEXT NOT NULL
# );
# """
# cursor.execute(queryke)
# queryal = """
# CREATE TABLE IF NOT EXISTS alarms (
#   id INTEGER,
#   text TEXT NOT NULL,
#   data TEXT NOT NULL,
#   time TEXT NOT NULL

# );
# """
# cursor.execute(queryal)
# querykep = """
# CREATE TABLE IF NOT EXISTS keeps (
#   id INTEGER,
#   text TEXT NOT NULL,
#   data INTEGER
# );
# """
# cursor.execute(querykep)

# id = 45698796
# text = "keep"
# querycr = "INSERT INTO keeps (id, text) VALUES ('"+str(id)+"','"+text+"');"
# cursor.execute(querycr)


# id = 45698796
# text = "alarm"
# querycr = "INSERT INTO keeps (id, text) VALUES ('"+str(id)+"','"+text+"');"

# cursor.execute(querycr)
# connection.commit()
