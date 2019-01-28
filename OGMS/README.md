OGMS - Lina

This is the departmental graduate student portal. This website maintains a database ogms.sql that records data about students, assistantships, courses, and enrollments. This website has the following functionality:

Graduate Director retrieves students from PAWS for the department
Graduate Director retrieves courses from PAWS for the department
Graduate Director retrieves enrollments from PAWS for the department
Graduate Director awards assistantship to student (this should also submit this information to the PAWS system by calling the REST service there).
Graduate Director requests department level statistics (you may hard code "GSU" and "CSC"; Allow user to choose term and year from pull down list; no login required for this option as well)
Faculty member submits grade for a student (sends data to REST service at PAWS); Faculty member need not have a login.
OGMS should provide the following REST Web service:
Given sid, return assistantship ('yes' or 'no').


## Functions to creaete

- [ ] Graduate Director retrieves students from PAWS for the department
- [ ] Graduate Director retrieves courses from PAWS for the department
- [ ] Graduate Director retrieves enrollments from PAWS for the department
- [ ] Graduate Director awards assistantship to student (this should also submit this information to the PAWS system by calling the REST service there).
- [ ] Graduate Director requests department level statistics (you may hard code "GSU" and "CSC"; Allow user to choose term and year from pull down list; no login required for this option as well)
- [ ] Faculty member submits grade for a student (sends data to REST service at PAWS); Faculty member need not have a login.


## Services to create

- [ ] Given sid, return assistantship ('yes' or 'no').
	- `tinman.cs.gsu.edu:5013/students/CSC/` PUT
