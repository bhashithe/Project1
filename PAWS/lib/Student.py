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
                cur.execute(f"UPDATE student SET password = '{password}' WHERE sid = {self.sid}")
                self.connection.commit()
            except (Exception, dbl.DatabaseError) as e:
                self.connection.rollback()
                print(e)
    
    @staticmethod
    def student_list(dept):
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT sid FROM student WHERE majordept LIKE '{dept}'")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)
