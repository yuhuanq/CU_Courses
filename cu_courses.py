#cu_courses.py
#Imani Chilongani
#!/usr/bin/env python
"""
cu_courses is a module that checks Cornell University student center
for any open spots in a particular course
"""

from time import sleep
from open_courses import check_course
import smtplib

def cornell_course():
	"""Returns the number of open spots in a paricular
	 course at Cornell University"""
	netid = raw_input("Thanks for trying CU_Courses, please enter your netid: ")
	password = raw_input("Please enter your password: ")
	term = raw_input("Please enter the term: ")
	department = raw_input("What department is the class you're searching " + 
							"for in (use abbreviated form. E.g. "
							+ "'Computer Science'as 'CS': ")
	number = raw_input("Please enter class number: ")
	c_index = raw_input("Please enter an index of a section of the requested" +
						" class (it is the order in which the section appears" +
						" on the search results page, starting with 0 for the" +
						" section at the top of the page), if you leave blank" +
						"then first section will be selected automatically: ")
	spots = check_course(netid,password,term,department,int(number),int(c_index))
	print "Results: \n" +"Open spots: " + str(spots["open_seats"])
	print "\n Waitlist spots: " + str(spots["waitlist_seats"])


cornell_course()