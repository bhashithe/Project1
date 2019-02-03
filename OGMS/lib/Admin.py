import psycopg2 as pg

class Admin():
        """ 
        Handles administrative service
        """

        @staticmethod
        def check_assistantship(sid):
                connection = pg.connect(dbname='llin15', user='llin15')
                with connection.cursor() as cur:
                        try:
                                sql = f"SELECT assistantship FROM oassistantship WHERE sid={sid}"
                                cur.execute(sql)
                                return cur.fetchone()
                        except (Exception, pg.DatabaseError) as e:
                                print(e)

        @staticmethod
        def accepted_student_req(alldata):
                """
                gets the accepted students into database
                """
                connection = pg.connect(dbname='llin15', user='llin15')
                with connection.cursor() as cur:
                        for data in alldata:
                                try:
                                        sql = f"INSERT INTO ostudent (sid, fname, lname) VALUES('{data[0]}', '{data[3]}', '{data[4]}')"
                                        cur.execute(sql)
                                        connection.commit()
                                except (Exception, pg.DatabaseError) as e:
                                        connection.rollback()
                                        print(e)

########### get courses ##############
        @staticmethod
        def accepted_course_req(alldata):
                """
                gets the accepted students into database
                """
                connection = pg.connect(dbname='llin15', user='llin15')
                with connection.cursor() as cur:
                        for data in alldata:
                                try:
                                        sql = f"INSERT INTO ocourse (cprefix, cno, ctitle, hours) VALUES('CSC', '{data[0]}', '{data[1]}', '{data[2]}')"
                                        cur.execute(sql)
                                        connection.commit()
                                except (Exception, pg.DatabaseError) as e:
                                        connection.rollback()
                                        print(e)
########### get enrollment ##############
        @staticmethod
        def accepted_enrollment_req(alldata):
"""
                gets the accepted students into database
                """
                connection = pg.connect(dbname='llin15', user='llin15')
                with connection.cursor() as cur:
                        for data in alldata:
                                try:
                                        sql = f"INSERT INTO oenroll (sid, term, year, crn, grade) VALUES('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}')"
                                        cur.execute(sql)
                                        connection.commit()
                                except (Exception, pg.DatabaseError) as e:
                                        connection.rollback()
                                        print(e)

#### update assistantship ##############
        @staticmethod
        def create_assistantship(sid, term, year, assistantship):
                connection = pg.connect(dbname='llin15', user='llin15')
                with connection.cursor() as cur:
                        try:
                                sql = f"INSERT INTO oassistantship (sid, term, year, assistantship) values ({sid}, '{term}', {year}, '{assistantship}')"
                                cur.execute(sql)
                                connection.commit()
                        except (Exception, pg.DatabaseError) as e:
                                connection.rollback()
                                print(e)

########### update grade ##############
        @staticmethod
        def update_grade(sid, term, year, grade):
                connection = pg.connect(dbname='llin15', user='llin15')
                with connection.cursor() as cur:
                        try:
                                sql = f"UPDATE oenroll SET grade='{grade}' WHERE sid={sid} AND term='{term}' AND year={year}"
                                cur.execute(sql)
                                connection.commit()
                        except (Exception, pg.DatabaseError) as e:
                                connection.rollback()
                                print(e)
