PAWS - Bhashithe

## Functions to creaete

- [x] Register service 
- [x] Choose semester
- [x] Add drop coursesf
- [ ] View class schedule
- [ ] View fees
- [x] Request students from SLATE
- [ ] Statistics

## Services to create

- [x] List of students of a department
	- `tinman.cs.gsu.edu:5013/students/CSC/` GET
- [x] List of courses of the department
	- `tinman.cs.gsu.edu:5013/courses/CSC/` GET
- [x] List of enrollment in a deparment
	- `tinman.cs.gsu.edu:5013/students/enrolled/CSC/SU` GET
- [x] Update a grade of a student
	- `tinman.cs.gsu.edu:5013/Admin/students/<sid>/grade/10101/` POST
	- {"term":"SU", "year":2005", "grade":"C"}


## Implementation details

When the accepted students were passed down from slate they will be added to `paws` database with an attribute `us` set to be 0. This is to track who has registered and who has not. It is easier to handle the numerical field than the full text password field.
