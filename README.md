Project1
CSc8711 Project 1 will be maintained in this repository

We shall use Python FLASK, REACT and POSTGRES as frameworks and APIs for this project.

 Slate - developed by Cynthia Khan
URL - tinman.cs.gsu.edu:5015/
 Paws - developed by Bhashithe Abeysinghe
URL - tinman.cs.gsu.edu:5001/
 OGMS - developed by Lina Lin
Server side implementation by python, flask
tinman.cs.gsu.edu:5020/
Client side implemented by react
Hosted locally
SLATE
lib
Folder contains the different forms (Registration, Application and Update status) which are used as class instances in Slate.py

template
Contains all html files used to generate the front end interfaces

SQL
Folder contains 2 files

slate.sql which creates database ckhan3 and tables 'department', 'program', 'applicant', 'application' used to store and retrive student application information.
restservices.sql contains sql commands used to complete the three rest service calls.
Execute
to execute use command: python3 Slate.py

PAWS
library
A library with some specific functions for different entities in the system was created. This is located at PAWS/lib/ directory. Library functions related to Admin, Detaprtment, Student and Database are implemented in respective classes. Then these classes are instantiated and used whenever needed.

Database
Database has a static function to get the connection to the database. This makes it easier to call/maintain the function.

Passwords
Passwords in the system is encrypted with md5 just to illustrate that it could be done.

Asynchronous callback functions
In frontend files (located in PAWS/templates) there were instances where we had to make two simultaneous AJAX calls which the second one depends on the output of the first. To get consistent data, callback functions were used.

OGMS
library
In /OGMS/lib/, the library has a main file, Admin.py and other python files with some methods and functions to handle requrements.

Database
It's easier to call funtions by some static function to reach the database.


React
In front end, I create react files and build set of websites by different big components, Student, Course, Enrollment, Grade and Assistantship and their realated Card file which parse jason files to this.state and get specific data. These data is fetched to a big table in every main compentents. For multilple url api, a specific method is used to concatenate them together to get server data. By 'PATCH', the 'grade' and 'assistantship' can be updated and send to back end. So PAWS and SLATE can access.