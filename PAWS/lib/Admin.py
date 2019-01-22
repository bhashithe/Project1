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
					#sid, email, name, lndata['sid'], data['email'], data['name'], data['lname'], data['majordept'], data['gradassistant']
					sql = f"INSERT INTO student (sid, email, fname, lname, majordept, gradassistant) VALUES({data['sid']}, '{data['email']}', '{data['fname']}', '{data['lname']}', '{data['majordept']}', '{data['gradassistant']}')"
					cur.execute(sql)
					connection.commit()
				except (Exception, dbl.DatabaseError) as e:
					connection.rollback()
					print(e)
