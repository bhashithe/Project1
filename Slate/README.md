## Slate - Student Application portal

Following are the functionalities of this portal:

* Register
* Login/Logout
* Update Profile
* Apply
* Graduate Director Accept/Reject application

## And provides the following REST services

- [X] List of accepted applicants
* {Sample URL} - tinman.cs.gsu.edu:5015/acceptedStudents/GSU
- { "students": [ { "fname": "Tony", "lname": "Romo", "email": "a1@gmail.com", "aid": 1000, "dname": "CSC" }, { "fname": "Michael", "lname": "Stone", "email": "a2@gmail.com", "aid": 1001, "dname": "CSC" } ] }
- [X] University level statistics of applicants
* {Sample URL} - tinman.cs.gsu.edu:5015/universityStats/GSU/FA/2019
- { "GSU students": [ { "dname": "CSC", "program": "MS", "accepted": 2, "rejected": 0, "pending": 0, "total": 2 }, { "dname": "CSC", "program": "PhD", "accepted": 0, "rejected": 0, "pending": 1, "total": 1 } ] }
- [X] Department level statistics of applicants
* {Sample URL} - tinman.cs.gsu.edu:5015/departmentStats/GSU/CSC/FA/2019
- { "CSC students": [ { "program": "MS", "accepted": 2, "rejected": 0, "pending": 0, "total": 2 }, { "program": "PhD", "accepted": 0, "rejected": 0, "pending": 1, "total": 1 } ] }

