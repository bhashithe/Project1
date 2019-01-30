from lib.Database import Database

class Department():
    """
    handles department related REST
    """

    def __init__(self):
        self.connection = Database.getconnection()

    @staticmethod
    def getcourses_data(term, year, dept):
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT crn, cno, days, starttime, endtime, room, cap, instructor FROM section where term = '{term}' AND year = {year} AND cprefix LIKE '{dept}%'")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)

    @staticmethod
    def getdepts():
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT DISTINCT cprefix FROM section")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)

    @staticmethod
    def getcourses(dept):
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT cno, ctitle, chours FROM course WHERE cprefix LIKE '{dept}%'")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)
