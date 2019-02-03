from lib.Database import Database, dbl
import hashlib

class Student():
    """
    handles a student for PAWS system
    """
    def __init__(self, sid):
        self.sid = sid
        #self.connection = dbl.connect(database='bhashithe', user='bhashithe')
        self.connection = Database.getconnection()

    def getdata(self):
        """
        returns viewable data of a student
        """
        with self.connection.cursor() as cur:
            try:
                cur.execute(f'SELECT email, fname, lname FROM student WHERE sid={self.sid}')
                #since only one student
                row = cur.fetchone() 
                #ret = {'email':row[0], 'fname':row[1], 'lname':row[2]}
                return row
            except (Exception, dbl.DatabaseError) as e:
                print(e)

    def register(self, password):
        """
        registers a user to the student table
        """
        with self.connection.cursor() as cur:
            #simple password hashing
            password = hashlib.md5(password.encode('utf-8')).hexdigest()
            try:
                cur.execute(f"SELECT us from student where sid = {self.sid}")
                updated = cur.fetchone()
                if updated[0] == 1:
                    return False
                else:
                    cur.execute(f"UPDATE student SET password = '{password}', us = 1 WHERE sid = {self.sid}")
                    self.connection.commit()
                    return True
            except (Exception, dbl.DatabaseError) as e:
                self.connection.rollback()
                print(e)

    def login(self, password):
        """
        logs a user in to the system and the redirect to home
        """
        with self.connection.cursor() as cur:
            password = hashlib.md5(password.encode('utf-8')).hexdigest()
            try:
                cur.execute(f"SELECT password FROM student WHERE sid={self.sid} LIMIT 1")
                fetched_password = cur.fetchone()
                if password == fetched_password[0]:
                    return True
                else:
                    return False
            except (Exception, dbl.DatabaseError) as e:
                print(e)

    def getyears(self):
        """
        gets all the years of the system
        """
        with self.connection.cursor() as cur:
            try:
                cur.execute(f"SELECT DISTINCT year FROM section")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)

    def getsems(self):
        """
        gets all the semesters of the system
        """
        with self.connection.cursor() as cur:
            try:
                cur.execute(f"SELECT DISTINCT term FROM section")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)
    
    def add_course(self, term, year, crn):
        """
        adds a course to a students enrollment
        """
        with self.connection.cursor() as cur:
            try:
                cur.execute(f"INSERT INTO enroll (sid, term, year, crn) VALUES ({self.sid},'{term}',{year},{crn})")
                self.connection.commit()
            except (Exception, dbl.DatabaseError) as e:
                self.connection.rollback()
                print(e)
    
    def drop_course(self, term, year, crn):
        with self.connection.cursor() as cur:
            try:
                cur.execute(f"DELETE FROM enroll WHERE sid= {self.sid} AND term = '{term}' AND year = {year} AND crn = {crn}")
                self.connection.commit()
            except (Exception, dbl.DatabaseError) as e:
                self.connection.rollback()
                print(e)

    def count_courses(self, term, year):
        """
        select all courses that I  have registered
        """
        with self.connection.cursor() as cur:
            try:
                cur.execute(f"SELECT COUNT(crn) FROM enroll WHERE term='{term}' AND year={year} AND sid = {self.sid}")
                return cur.fetchone()
            except (Exception, dbl.DatabaseError) as e:
                print(e)

    def my_courses(self, term, year):
        """
        select all courses that I  have registered
        """
        with self.connection.cursor() as cur:
            try:
                cur.execute(f"SELECT crn FROM enroll WHERE term='{term}' AND year={year} AND sid = {self.sid}")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)

    @staticmethod
    def student_list(dept):
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT sid, email, fname, lname FROM student WHERE majordept LIKE '{dept}%'")
                rows = cur.fetchall()
                rets = []
                for row in rows:
                    columns = ['sid','email','fname','lname']
                    ret = dict(zip(columns, row))
                    rets.append(ret)
                return rets
            except (Exception, dbl.DatabaseError) as e:
                print(e)


    @staticmethod
    def enrollment_list(dept, term):
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT DISTINCT enroll.* FROM enroll INNER JOIN section ON(enroll.crn=section.crn) WHERE section.cprefix LIKE '{dept}%' and enroll.term='{term}'")
                rows = cur.fetchall()
                rets = []
                for row in rows:
                    columns = ['sid','term','year','crn','grade']
                    ret = dict(zip(columns, row))
                    rets.append(ret)
                return rets
            except (Exception, dbl.DatabaseError) as e:
                print(e)
