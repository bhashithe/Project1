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
                return cur.fetchone() 
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
    
    @staticmethod
    def student_list(dept):
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT * FROM student WHERE majordept LIKE '{dept}%'")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)


    @staticmethod
    def enrollment_list(dept, term):
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT enroll.* FROM enroll INNER JOIN section ON(enroll.crn=section.crn) WHERE section.cprefix LIKE '{dept}%' and section.term='{term}'")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)
