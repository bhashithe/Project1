from lib.Database import Database, dbl

class Admin():
	""" 
	Handles administrative service
	"""

	@staticmethod
	def accepted_req(alldata):
		"""
		gets the accepted students into database
		"""
		connection = Database.getconnection()
		with connection.cursor() as cur:
			for data in alldata:
				try:
					sql = f"INSERT INTO student (sid, email, fname, lname, majordept, gradassistant) VALUES({data['sid']}, '{data['email']}', '{data['fname']}', '{data['lname']}', '{data['majordept']}', '{data['gradassistant']}')"
					cur.execute(sql)
					connection.commit()
				except (Exception, dbl.DatabaseError) as e:
					connection.rollback()
					print(e)

	@staticmethod
	def update_update_assistantship(sid, term, year, crn, update_assistantship):
		"""
		update a grade of a given student
		"""
		connection = Database.getconnection()
		with connection.cursor() as cur:
			try:
				sql = f"UPDATE enroll SET update_assistantship='{update_assistantship}' WHERE sid={sid} AND term='{term}' AND year={year} AND crn={crn}"
				cur.execute(sql)
				connection.commit()
			except (Exception, dbl.DatabaseError) as e:
				connection.rollback()
				print(e)

	@staticmethod
	def update_grade(sid, term, year, crn, grade):
		"""
		update a grade of a given student
		"""
		connection = Database.getconnection()
		with connection.cursor() as cur:
			try:
				sql = f"UPDATE enroll SET grade='{grade}' WHERE sid={sid} AND term='{term}' AND year={year} AND crn={crn}"
				cur.execute(sql)
				connection.commit()
			except (Exception, dbl.DatabaseError) as e:
				connection.rollback()
				print(e)

