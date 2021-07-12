from flask.globals import current_app
import mysql.connector as mysql

from mysql.connector import errorcode
from database import db, cursor
DB_NAME = ['questionans']

TABLES = {}
TABLES['users'] = (
    "CREATE TABLE `users`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`name` varchar(50) NOT NULL,"
    "`password` varchar(250) NOT NULL,"
    "`expert` BOOLEAN NOT NULL,"
    "`admin` BOOLEAN NOT NULL,"
    "PRIMARY KEY (`id`)"
    ")ENGINE=InnoDB"
)
TABLES['questions'] = (
    "CREATE TABLE `questions`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`question_text` TEXT NOT NULL,"
    "`answer_text` TEXT,"
    "`asked_by_id` int(10) NOT NULL,"
    "`expert_id` int(10) NOT NULL,"
    "PRIMARY KEY(`id`)"
    ")ENGINE=InnoDB"
)


def create_db():
    for name in DB_NAME:
        cursor.execute(f"CREATE DATABASE  IF NOT EXISTS {name}")


def create_table():
    for name in DB_NAME:
        cursor.execute(f"USE {name}")
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                cursor.execute(table_description)
                print(f'{table_name} is created!')
            except mysql.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('table exist')
                else:
                    print(err.msg)


class InsertData:
    def insertData(self, name, password, expert, admin):
        self.sql = (
            "INSERT INTO users (name, password, expert,admin) VALUES(%s,%s,%s,%s)")
        cursor.execute(self.sql, (name, password, expert, admin,))
        db.commit()

    def makeAdmin(self, b, id):
        self.sql = ("UPDATE users SET admin = %s WHERE id = %s")
        cursor.execute(self.sql, (b, id,))
        db.commit()

    def makeExpert(self, id):
        self.sql = ("UPDATE users SET expert = 1 WHERE id = %s")
        cursor.execute(self.sql, (id,))
        db.commit()

    def getExpert(self):
        self.sql = ("SELECT id, name FROM users WHERE expert = 1 ")
        cursor.execute(self.sql,)
        result = cursor.fetchall()
        return result

    def login(self, name):
        self.sql = ("SELECT * FROM users WHERE name= %s")
        cursor.execute(self.sql, (name,))
        result = cursor.fetchone()
        return result

    def getUsers(self):
        self.sql = (" SELECT * FROM users")
        cursor.execute(self.sql,)
        result = cursor.fetchall()
        return result

    def getUserId(self, name):
        self.sql = ("SELECT id FROM users WHERE name=%s")
        cursor.execute(self.sql, (name,))
        result = cursor.fetchone()
        return result


class Question:
    def quesSubmit(self, q, asked_by_id, expert_id):
        self.sql = (
            " INSERT INTO questions ( question_text, asked_by_id, expert_id) VALUES(%s,%s,%s) ")
        cursor.execute(self.sql, (q, asked_by_id, expert_id,))
        db.commit()

    def allQuestions(self, expert):
        self.sql = (
            " SELECT questions.id, questions.question_text, users.name FROM questions JOIN users ON users.id = questions.asked_by_id WHERE questions.answer_text IS NULL AND questions.expert_id = %s ")
        cursor.execute(self.sql, (expert,))
        result = cursor.fetchall()
        return result

    def singleQuestion(self, id):
        self.sql = ("SELECT id, question_text FROM questions WHERE id=%s")
        cursor.execute(self.sql, (id,))
        res = cursor.fetchone()
        return res

    def submitAns(self, ans, id):
        self.sql = (" UPDATE questions SET answer_text=%s WHERE id=%s")
        cursor.execute(self.sql, (ans, id,))
        db.commit()

    def answers(self):
        self.sql = (
            "SELECT questions.id AS question_id, questions.question_text, askers.name AS asker_name, experts.name AS expert_name FROM questions JOIN users AS askers ON askers.id=questions.id JOIN users AS experts ON experts.id=questions.expert_id WHERE questions.answer_text IS NOT NULL")
        cursor.execute(self.sql,)
        result = cursor.fetchall()
        return result

    def question(self, id):
        self.sql = ("SELECT questions.question_text, questions.answer_text, askers.name AS asker_name, experts.name AS expert_name FROM questions JOIN users AS askers ON askers.id=questions.id JOIN users AS experts ON experts.id=questions.expert_id WHERE questions.id=%s")
        cursor.execute(self.sql, (id,))
        res = cursor.fetchone()
        return res


# create_db()
# create_table()
ins = InsertData()
q = Question()
# ins.makeAdmin(1, 2)
# print(ins.getUsers())
# print(ins.login('saif hasan'))
# print(q.allQuestions(3))
# print(q.answers())
# print(q.singleQuestion(2))
