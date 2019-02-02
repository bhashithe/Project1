from lib.Database import Database, dbl

class Department():
    """
    handles department related REST
    """

    def __init__(self):
        self.connection = Database.getconnection()

    def get_course_info(self, crns):
        with self.connection.cursor() as cur:
            try:
                rets = []
                for crn in crns:
                    cur.execute(f"SELECT course.cno, course.ctitle, course.chours, section.days, section.starttime, section.endtime FROM course INNER JOIN section ON(course.cno=section.cno) WHERE crn={crn}")
                    row = cur.fetchone()
                    columns = ['cno','title','hours','day','start','end']
                    ret = dict(zip(columns,row))
                    rets.append(ret)
                return rets
            except (Exception, dbl.DatabaseError) as e:
                print(e)

    @staticmethod
    def get_home_data(term, year, dept):
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
                rows = cur.fetchall()
                rets = []
                for row in rows:
                    columns = ['cno','ctitle','chours']
                    ret = dict(zip(columns, row))
                    rets.append(ret)
                return rets
            except (Exception, dbl.DatabaseError) as e:
                print(e)
