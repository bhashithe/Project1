from lib.Database import Database

class Department():
    """
    handles department related REST
    """

    def __init__(self):
        self.connection = Database.getconnection()

    @staticmethod
    def getcourses(dept):
        connection = Database.getconnection()
        with connection.cursor() as cur:
            try:
                cur.execute(f"SELECT cno, ctitle, chours FROM course WHERE cprefix LIKE '{dept}%'")
                return cur.fetchall()
            except (Exception, dbl.DatabaseError) as e:
                print(e)