--Given university, return a list of ACCEPTED applicants 
--(only those that have not been sent in the past).
SELECT a.fname, a.lname, a.email, a.aid, b.dname 
FROM applicant a 
INNER JOIN application b 
ON a.email = b.email 
WHERE b.university=%s AND b.admissionStatus='ACCEPT' 
AND dataSentToPaws <> 'Yes';

--Given university, term, and year, return university level statistics of applicants 
--(for each department and program, return number of applicants, number of accepts, number of rejects, 
--and number of pending decisions).
SELECT Y.dname, Y.program, Y.accepted, Y.rejected, Y.pending, (Y.accepted + Y.rejected + Y.pending) AS total
FROM(
	select X.dname, X.program, 
		MAX(CASE
			WHEN X.admissionstatus = 'ACCEPT'
				THEN X.applicants
			ELSE 0
		END) AS Accepted,
		MAX(CASE
			WHEN X.admissionstatus = 'REJECT'
				THEN X.applicants
			ELSE 0
		END) AS Rejected,
		MAX(CASE
			WHEN X.admissionstatus = 'PENDING'
				THEN X.applicants
			ELSE 0
		END) AS Pending,
	from (	
			select dname, program, count(email) as applicants, admissionStatus
			from application 
			WHERE university = 'GSU'
			AND yearOfAdmission = 2019
			group by dname, program, admissionStatus ) X
	GROUP BY X.dname, X.program) Y
	
--Given university, department, term, and year, return department level statistics of applicants 
--(for each program, return number of applicants, number of accepts, number of rejects, and number of pending decisions).

SELECT 
	Y.program, 
	Y.accepted, 
	Y.rejected, 
	Y.pending, 
	(Y.accepted + Y.rejected + Y.pending) AS total 
FROM
	(SELECT X.program,
	 	MAX(CASE 
				WHEN X.admissionstatus = 'ACCEPT' 
					THEN X.applicants 
				ELSE 0 END) AS Accepted, 
	 	MAX(CASE 
				WHEN X.admissionstatus = 'REJECT' 
					THEN X.applicants 
				ELSE 0 END) AS Rejected,
	 	MAX(CASE 
				WHEN X.admissionstatus = 'PENDING' 
					THEN X.applicants 
				ELSE 0 END) AS Pending 
	 FROM (select program, count(email) as applicants, admissionStatus 
		   from application 
		   WHERE university = %s AND dname = %s AND termofadmission = %s AND yearOfAdmission = %s 
		   GROUP BY program, admissionStatus ) X 
	 GROUP BY X.program) Y
			
--Reset datasenttopaws

update application set datasenttopaws = null
