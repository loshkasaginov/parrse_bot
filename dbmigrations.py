import sqlite3
import logging

places_dict = {1:"москва",2:"санкт-питербург",3:"Екатеринбург",4:"Новосибирск",5:"украина"}
logging.basicConfig(level=logging.INFO, filename="dblogs.log",filemode="w",format="%(asctime)s %(levelname)s %(message)s")

class Db:
    def __init__(self):
        self.connection = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        logging.info("db connected")

    def create_city_table(self):
        self.cursor.execute("create table IF NOT EXISTS city(city_id INTEGER primary key AUTOINCREMENT unique,city varchar(50) not null unique)")
        self.cursor.execute("INSERT INTO city(city_id,city) values (0,'test')")
        logging.info("city table created")

    def create_salarytab_table(self):
        self.cursor.execute("create table IF NOT EXISTS salarytab(vacancy_id INTEGER primary key AUTOINCREMENT unique,vacancy varchar(50) not null,city_id int2 not null references city (city_id),salary numeric)")
        self.cursor.execute("INSERT INTO salarytab(vacancy_id,vacancy,city_id,salary) values (0,'test',0,0)")
        logging.info("salarytab table created")

    def insert_into_city(self, city):
        self.cursor.execute("INSERT INTO city(city) values ('%s')"%(city))
        self.connection.commit()

    def insert_into_salarytab(self, vacancy, city_id, salary):
        self.cursor.execute("INSERT INTO salarytab(vacancy, city_id, salary) values ('%s',%s, %s)" % (vacancy, city_id, salary))
        self.connection.commit()

    def drop_city_table(self):
        self.cursor.execute("drop table city")
        logging.info("city table dropped")

    def drop_salarytab_table(self):
        self.cursor.execute("drop table salarytab")
        logging.info("salary table dropped")

    def get_alldata_from_city(self):
        result=self.cursor.execute("select * from city")
        return result.fetchall()

    def get_alldata_from_salarytab(self):
        result=self.cursor.execute("select * from salarytab")
        return result.fetchall()

    def close_connection(self):
        self.connection.close()
        logging.info("db connection closed")

    def check_vacancy(self, vacancy):
        result = self.cursor.execute("select count(vacancy) from salarytab where vacancy='%s'" % (vacancy))
        test = result.fetchall()[0][0]
        if test == 0:
            return False
        return True

    def get_vacancy_salary(self, vacancy):
        result = self.cursor.execute("select salary from salarytab where vacancy='%s'" % (vacancy))
        return result.fetchall()

def check_vacancy(vacancy):
    db = Db()
    if db.check_vacancy(vacancy):
        db.close_connection()
        return True
    db.close_connection()
    return False

def get_vacancy_salary(vacancy):
    db = Db()
    listof_avg_salary = db.get_vacancy_salary(vacancy)
    db.close_connection()
    return listof_avg_salary

def insert_default_values_to_city(db):
    for i in list(places_dict.values()):
        db.insert_into_city(str(i))
    logging.info("city table was inserted with default data")

def create_db():
    db = Db()
    db.create_city_table()
    db.create_salarytab_table()
    insert_default_values_to_city(db)
    db.close_connection()

def insert_salaries_and_place(vacancy, city_id, salary):
    db = Db()
    db.insert_into_salarytab(vacancy, city_id, salary)
    db.close_connection()

def drop_tables():
    db = Db()
    db.drop_salarytab_table()
    db.drop_city_table()
    db.close_connection()

def get_data_from_db():
    db = Db()
    print(db.get_alldata_from_city())
    print(db.get_alldata_from_salarytab())
    db.close_connection()
